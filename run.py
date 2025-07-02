import os
import threading
import asyncio
from flask import Flask

# Menambahkan path src agar bisa mengimpor dari bot.main
import sys
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

# Impor fungsi untuk menjalankan bot dari file main.py
# Kita akan memodifikasi file ini di langkah berikutnya
from src.bot.main import main

# 1. Inisialisasi Aplikasi Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot running.."

def run_flask_app():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def run_discord_bot():
    asyncio.run(main())

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_discord_bot)
    bot_thread.daemon = True 
    bot_thread.start()
    run_flask_app()