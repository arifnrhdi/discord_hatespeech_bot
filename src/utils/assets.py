import os
import requests
import zipfile
import io

# URL aset dari GitHub Releases Anda
ASSETS = {
    "models": "https://github.com/arifnrhdi/discord_hatespeech_bot/releases/download/v1.0/models.zip",
    "data": "https://github.com/arifnrhdi/discord_hatespeech_bot/releases/download/v1.0/data.zip"
}

# Path absolut ke root direktori proyek
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def download_and_unzip(asset_name, url, destination_folder):
    """
    Mengunduh, mengekstrak file zip dengan logging yang detail, dan menangani error.
    """
    print(f"-> Memulai proses untuk aset: '{asset_name}'")
    
    # Validasi URL dasar
    if not url or "USERNAME" in url or "REPO" in url:
        print(f"❌ Peringatan: URL untuk '{asset_name}' tampaknya belum diatur. Melewatkan...")
        return

    try:
        # 1. Mengunduh file
        print(f"   Downloading dari: {url}")
        response = requests.get(url, stream=True, timeout=60) # Tambahkan timeout
        response.raise_for_status()  # Ini akan memunculkan error jika status bukan 200 (OK)
        print(f"   Download '{asset_name}' berhasil (status: {response.status_code}).")

        # 2. Mengekstrak file dari memori
        print(f"   Mengekstrak '{asset_name}' ke direktori: {destination_folder}")
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(destination_folder)
        print(f"✅ Ekstraksi '{asset_name}' selesai.")

    except requests.exceptions.RequestException as e:
        print(f"❌ FATAL: Gagal mengunduh '{asset_name}'. Error: {e}")
    except zipfile.BadZipFile:
        print(f"❌ FATAL: File yang diunduh untuk '{asset_name}' bukan file zip yang valid.")
    except Exception as e:
        print(f"❌ FATAL: Terjadi error tak terduga saat memproses '{asset_name}': {e}")

if __name__ == "__main__":
    print("--- Memulai Proses Build: Pengunduhan Aset ---")
    
    models_dest = os.path.join(PROJECT_ROOT, 'models')
    data_dest = os.path.join(PROJECT_ROOT, 'data')

    os.makedirs(models_dest, exist_ok=True)
    os.makedirs(data_dest, exist_ok=True)
    print(f"Direktori 'models' dan 'data' dipastikan ada.")

    # Jalankan fungsi untuk setiap aset
    download_and_unzip("models", ASSETS["models"], models_dest)
    download_and_unzip("data", ASSETS["data"], data_dest)
    
    print("--- Proses Build: Pengunduhan Aset Selesai ---")