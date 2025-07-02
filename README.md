# Discord Hate Speech Detection Bot

Bot Discord berbasis AI yang dirancang untuk mendeteksi dan memoderasi ujaran kebencian (*hate speech*) dan kata-kata kasar (*abusive words*) dalam bahasa Indonesia secara otomatis. Proyek ini menggunakan model *Machine Learning* untuk menganalisis pesan dan mengambil tindakan moderasi, bertujuan untuk menciptakan lingkungan komunitas yang lebih aman dan positif.

## Fitur Utama

  - **Deteksi Otomatis**: Mendeteksi pesan yang mengandung ujaran kebencian atau kata-kata kasar menggunakan model klasifikasi teks Naive Bayes.
  - **Pra-pemrosesan Teks Indonesia**: Dilengkapi dengan fitur pembersihan teks, normalisasi kata "alay" menggunakan kamus, penghapusan *stopword*, dan *stemming* (mengubah kata ke bentuk dasarnya).
  - **Tindakan Moderasi Otomatis**: Secara otomatis menghapus pesan yang terdeteksi dan mengirimkan notifikasi ke channel khusus moderator.
  - **Logging**: Semua pesan yang dihapus dicatat dalam file log (`logs/deleted_messages.log`) untuk peninjauan lebih lanjut.
  - **Notifikasi Moderator**: Mengirimkan notifikasi *embed* yang detail ke channel moderator setiap kali ada pesan yang dihapus, lengkap dengan informasi pengguna, isi pesan, dan probabilitas deteksi.
  - **Ambang Batas (Threshold) Fleksibel**: Tingkat kepercayaan deteksi dapat diatur melalui file konfigurasi untuk menyesuaikan sensitivitas bot.
  - **Perintah Status**: Dilengkapi perintah `!cekstatus` untuk memverifikasi apakah model deteksi sudah aktif dan berjalan.

## Cara Kerja

Bot bekerja melalui beberapa tahapan utama:

1.  **Pra-pemrosesan Data**: Teks dari dataset mentah dibersihkan. Proses ini meliputi:

      - Mengubah teks menjadi huruf kecil.
      - Menghapus URL, mention (`@user`), dan tagar (`#`).
      - Mengganti kata-kata tidak baku (alay) dengan kata baku dari `new_kamusalay.csv`.
      - Menghapus kata-kata umum yang tidak memiliki makna signifikan (*stopwords*).
      - Mengubah setiap kata ke bentuk dasarnya (*stemming*) menggunakan library Sastrawi.
      - Dataset yang sudah bersih disimpan di `data/cleaned_dataset.csv`.

2.  **Pelatihan Model**:

      - Dataset bersih digunakan untuk melatih model. Teks diubah menjadi representasi numerik menggunakan **TF-IDF Vectorizer**.
      - Model **Multinomial Naive Bayes** dilatih untuk mengklasifikasikan teks sebagai ujaran kebencian atau bukan.
      - Model yang telah dilatih (`hate_speech_model.pkl`) dan vectorizer (`tfidf_vectorizer.pkl`) disimpan di direktori `models/`.

3.  **Deteksi Real-time di Discord**:

      - Bot memonitor setiap pesan baru di server.
      - Setiap pesan melewati proses pra-pemrosesan yang sama seperti saat pelatihan.
      - Model yang sudah dimuat akan memprediksi apakah pesan tersebut mengandung sentimen negatif.
      - Jika probabilitas deteksi melebihi ambang batas yang ditentukan di konfigurasi, bot akan menghapus pesan tersebut dan mengirim laporan ke channel moderator.

## Struktur Proyek

```
discord-hatespeech-bot/
│
├── data/
│   ├── dataset.csv            
│   ├── new_kamusalay.csv      
│   ├── abusive.csv            
│   ├── stopwordbahasa.csv     
│   └── cleaned_dataset.csv    
│
├── models/
│   ├── hate_speech_model.pkl  
│   └── tfidf_vectorizer.pkl   
│
├── src/
│   ├── bot/
│   │   ├── cogs/
│   │   │   └── detection.py  
│   │   ├── config.py          
│   │   └── main.py           
│   │
│   └── utils/
│   │   ├── data_loader.py      
│   │   └── text_preprocessor.py 
│   │
│   └── ml/
│       ├── clean_dataset.py     
│       ├── train.py             
│       ├── evaluate.py          
│       └── predictor.py         
│
├── logs/
│   └── deleted_messages.log   
│
├── .env                       
├── requirements.txt           
└── README.md                  
```

## Cara Penggunaan
### Langkah 1: Proses Machine Learning (Hanya perlu dijalankan sekali)

Langkah ini hanya perlu dilakukan saat pertama kali mengatur bot, atau jika Anda ingin melatih ulang model dengan data yang telah diperbarui.

**a. Bersihkan Dataset**

Buka terminal Anda, arahkan ke direktori utama proyek, dan jalankan skrip berikut untuk memproses dataset mentah menjadi dataset yang bersih.

```bash
python -m src.ml.clean_dataset
```

Perintah ini akan membaca `data/dataset.csv` dan menghasilkan file baru `data/cleaned_dataset.csv`.

**b. Latih Model**

Setelah dataset bersih, jalankan skrip pelatihan untuk membuat model machine learning. Model dan vectorizer akan disimpan di dalam direktori `models/`.

```bash
python -m src.ml.train
```

**Opsional**: Untuk mengevaluasi seberapa baik performa model yang baru saja Anda latih, jalankan perintah berikut:

```bash
python -m src.ml.evaluate
```

### Langkah 2: Menjalankan Bot

Setelah model berhasil dilatih, Anda dapat mengaktifkan bot di server Discord Anda.

a. Pastikan file `.env` Anda sudah berisi `DISCORD_TOKEN` dan `MODERATOR_CHANNEL_ID` yang benar.

b. Jalankan bot dengan perintah berikut:

```bash
python -m src.bot.main
```

c. Jika berhasil, Anda akan melihat pesan konfirmasi di terminal bahwa bot telah login. Bot sekarang aktif dan akan memantau pesan di server Discord tempat ia diundang. Pastikan bot memiliki izin "Read Messages" dan "Manage Messages".

### Langkah 3: Perintah di Discord

Anda dapat berinteraksi dengan bot di Discord menggunakan perintah yang tersedia.

  * **`!cekstatus`**
    Gunakan perintah ini di server Discord untuk memastikan model deteksi telah dimuat dengan benar dan bot siap bekerja. Perintah ini hanya dapat digunakan oleh anggota yang memiliki izin "Manage Messages".