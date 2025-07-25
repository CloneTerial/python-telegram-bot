# Base telegram bot e-commerce

Ini adalah proyek base bot telegram sederhana yang dibangun dengan Python, dirancang dengan arsitektur plugin yang dapat diperluas, sistem kontrol akses berbasis peran yang kuat, dan platform e-commerce yang bisa di sesuaikan pada kebutuhan.

## Fitur Utama

- **Arsitektur Plugin Dinamis**: Tambahkan fungsionalitas dan perintah baru dengan mudah hanya dengan membuat file Python baru di direktori `plugins`. Sistem berbasis _decorator_ secara otomatis akan mendaftarkan perintah baru saat bot dimulai.
- **Platform E-commerce**: Pengguna dapat membuat toko virtual mereka sendiri, menambahkan produk, dan menjualnya ke pengguna lain. Proses pembelian ditangani melalui _inline keyboard_ yang interaktif.
- **Manajemen Peran & Hak Akses**: Sistem peran yang aman (`owner`, `store`, `premium`, `free`) melindungi perintah-perintah penting. Peran dapat diberikan dengan durasi waktu tertentu dan akan otomatis nonaktif saat kedaluwarsa.
- **Database JSON**: Menggunakan file JSON sederhana untuk menyimpan dan mengelola data pengguna dan transaksi, membuatnya mudah untuk dilihat dan dicadangkan[cite: 1].
- **Konfigurasi Aman**: Memisahkan kunci API dan konfigurasi sensitif dari kode sumber menggunakan file `.env`.

## Arsitektur

Proyek ini dirancang dengan pemisahan tugas yang jelas untuk kemudahan pemeliharaan dan skalabilitas:

- **`main.py`**: Titik masuk utama yang menginisialisasi bot dan memuat semua plugin.
- **`/plugins`**: Setiap file di direktori ini mewakili sebuah fitur atau kumpulan perintah bot. Ini adalah tempat sebagian besar logika fungsional berada.
- **`/core`**: Berisi logika bisnis inti, termasuk manajemen pengguna (`User_Manager.py`), keamanan (`security.py`), dan fungsi utilitas lainnya.
- **`/data`**: Direktori tempat file database JSON (`users.json`, `transaction.json`) disimpan.

## Instalasi dan Pengaturan

Ikuti langkah-langkah ini untuk menjalankan bot di lingkungan lokal Anda.

1.  **Clone Repositori**

    ```bash
    git clone [https://github.com/CloneTerial/python-telegram-bot.git](https://github.com/CloneTerial/python-telegram-bot.git)
    cd python-telegram-bot
    ```

2.  **Buat Lingkungan Virtual (Direkomendasikan)**

    ```bash
    python -m venv venv
    ```

    - Pada Windows: `venv\Scripts\activate`
    - Pada macOS/Linux: `source venv/bin/activate`

3.  **Instal Dependensi**
    Instal semua pustaka yang diperlukan dari file `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Atur File Konfigurasi**
    Buat file bernama `.env` di direktori utama dan isi dengan format berikut.

    ```env
    token=MASUKKAN_TOKEN_BOT_TELEGRAM_ANDA
    OWNER_ID=MASUKKAN_ID_TELEGRAM_ANDA
    ```

    - `token`: Diperoleh dari BotFather di Telegram.
    - `OWNER_ID`: ID pengguna Telegram Anda, yang bisa didapatkan dengan menggunakan perintah `/id` pada bot setelah berjalan.

5.  **Jalankan Bot**
    ```bash
    python main.py
    ```
    Jika semua pengaturan benar, Anda akan melihat pesan "Bot is running..." di terminal.

## Daftar Perintah

Berikut adalah daftar perintah yang tersedia di dalam bot, dikategorikan berdasarkan fungsi.

#### Perintah Umum

- `/start` - Memulai interaksi dengan bot.
- `/register` - Mendaftarkan diri Anda sebagai pengguna di database bot.
- `/list` - Menampilkan semua daftar perintah yang tersedia.
- `/id` - Mendapatkan ID pengguna Telegram Anda.

#### Perintah E-Commerce

- `/create_store <nama> <deskripsi>` - Membuat toko virtual Anda sendiri.
- `/create_produck <nama> <harga> <deskripsi>` - Menambahkan produk baru ke toko Anda.
- `/produck` - Melihat daftar produk yang Anda jual di toko Anda.
- `/buy <nama_toko>` - Melihat dan membeli produk dari toko pengguna lain.
- `/my_orders` - Melihat riwayat transaksi pembelian Anda.

#### Perintah Admin (Khusus Pemilik)

- `/promote <user_id> <role> <duration> <unit>` - Mempromosikan pengguna ke peran tertentu (misal: `/promote 12345 store 30 d`).
- `/demote <user_id>` - Menurunkan peran pengguna kembali menjadi "free".

## Teknologi yang Digunakan

- **Python 3**
- **python-telegram-bot**: Pustaka utama untuk berinteraksi dengan Telegram Bot API.
- **python-dotenv**: Untuk mengelola variabel lingkungan.
