import discord
from discord.ext import commands
from datetime import datetime
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

from bot.config import DETECTION_THRESHOLD, DELETED_MESSAGES_LOG_PATH, MODERATOR_CHANNEL_ID
from ml.predictor import HateSpeechPredictor

class DetectionCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.predictor = HateSpeechPredictor()

    def _log_deleted_message(self, original_message, reason):
        os.makedirs(os.path.dirname(DELETED_MESSAGES_LOG_PATH), exist_ok=True)
        with open(DELETED_MESSAGES_LOG_PATH, 'a', encoding='utf-8') as f:
            log_entry = (
                f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Author: {original_message.author} (ID: {original_message.author.id})\n"
                f"Content: {original_message.content}\n"
                f"Reason: {reason}\n"
                f"{'-'*20}\n"
            )
            f.write(log_entry)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or not self.predictor.is_ready:
            return

        is_toxic, probability = self.predictor.predict(message.content)

        if is_toxic == 1 and probability >= DETECTION_THRESHOLD:
            try:
                original_content = message.content
                await message.delete()

                bot_response_content = (
                    f"Pesan dari {message.author.mention} telah dihapus karena terdeteksi mengandung konten toxic/kasar ❌.\n"
                    f"Probabilitas Deteksi: {probability*100:.2f}%"
                )
                await message.channel.send(bot_response_content)

                reason = f"Konten toxic terdeteksi (Prob: {probability:.2f})"
                self._log_deleted_message(message, reason)
                print(f"Pesan dari {message.author} dihapus. Alasan: {reason}")
                
                if MODERATOR_CHANNEL_ID:
                    mod_channel = self.bot.get_channel(MODERATOR_CHANNEL_ID)
                    if mod_channel:
                        embed = discord.Embed(title="Moderasi Konten Toxic", color=discord.Color.red(), timestamp=datetime.now())
                        embed.add_field(name="Pengguna", value=f"{message.author.mention}", inline=False)
                        embed.add_field(name="Pesan Asli", value=f"```{original_content}```", inline=False)
                        embed.add_field(name="Probabilitas", value=f"{probability*100:.2f}%", inline=True)
                        embed.add_field(name="Channel", value=message.channel.mention, inline=True)
                        await mod_channel.send(embed=embed)

            except discord.Forbidden:
                print(f"Tidak memiliki izin untuk menghapus pesan di channel #{message.channel.name}.")
            except Exception as e:
                print(f"Error saat memproses pesan: {e}")

    @commands.command(name='cekstatus')
    @commands.has_permissions(manage_messages=True)
    async def check_status(self, ctx: commands.Context):
        if self.predictor.is_ready:
            await ctx.send("✅ Predictor berhasil dimuat dan siap mendeteksi.")
        else:
            await ctx.send("❌ Peringatan: Predictor GAGAL dimuat. Fitur deteksi tidak aktif.")

async def setup(bot: commands.Bot):
    await bot.add_cog(DetectionCog(bot))