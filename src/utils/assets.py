import os
import requests
import zipfile
import io

# GANTI DENGAN LINK YANG ANDA DAPATKAN DARI GITHUB RELEASES
ASSETS = {
    "models": "https://github.com/arifnrhdi/discord_hatespeech_bot/releases/download/v1.0/models.zip",
    "data": "https://github.com/arifnrhdi/discord_hatespeech_bot/releases/download/v1.0/data.zip"
}

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def unzip(asset_name, url, destination_folder):
    if not url or "USERNAME" in url:
        return

    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(destination_folder)

if __name__ == "__main__":
    models_dest = os.path.join(PROJECT_ROOT, 'models')
    data_dest = os.path.join(PROJECT_ROOT, 'data')

    os.makedirs(models_dest, exist_ok=True)
    os.makedirs(data_dest, exist_ok=True)

    unzip("models", ASSETS["models"], models_dest)
    
    unzip("data", ASSETS["data"], data_dest)
    
    print("unduh aset selesai")