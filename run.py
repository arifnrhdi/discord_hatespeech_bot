import os
import threading
import asyncio
from flask import Flask
import sys

# Menambahkan path src agar bisa mengimpor dari bot.main
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

# Impor fungsi untuk menjalankan bot dari file main.py
from src.bot.main import main_start

# 1. Inisialisasi Aplikasi Flask
#    Aplikasi ini hanya untuk merespons health check dari Railway.
app = Flask(__name__)

@app.route('/')
def home():
    """Endpoint sederhana untuk health check dari Railway."""
    # Anda bisa mengembangkannya untuk memberikan status bot jika perlu
    return "Web server is running, bot thread is active."

# 2. Definisikan fungsi untuk menjalankan bot
#    Fungsi ini akan dijalankan di thread terpisah.
def run_discord_bot():
    """Wrapper untuk menjalankan bot Discord dalam event loop asyncio baru."""
    print("Starting Discord bot in a background thread...")
    try:
        # Setiap thread butuh event loop asyncio sendiri
        asyncio.run(main_start())
    except Exception as e:
        print(f"FATAL ERROR in bot thread: {e}")

# 3. Mulai thread bot di level atas (INI PERUBAHAN UTAMA)
#    Kode ini akan dieksekusi saat Gunicorn mengimpor file ini.
print("Creating and starting bot thread at module level...")
bot_thread = threading.Thread(target=run_discord_bot)
bot_thread.daemon = True  # Memastikan thread bot berhenti saat main app berhenti
bot_thread.start()
print("Bot thread has been started.")

# 4. Blok untuk testing lokal (Opsional)
#    Gunicorn tidak akan menjalankan blok ini.
if __name__ == '__main__':
    print("Running Flask app for local testing via 'python run.py'...")
    # Port untuk testing lokal, Gunicorn akan menggunakan portnya sendiri
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)