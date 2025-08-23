# KaitBot

Platform untuk Membangun Chatbot Perusahaan Anda.

KaitBot adalah platform *chatbot-as-a-service* untuk membangun dan mengintegrasikan chatbot asisten AI ke situs web anda. Platform ini memungkinkan kustomisasi respons AI menggunakan data dari dokumen atau URL website, dengan integrasi melalui satu baris skrip JavaScript.


## Fitur Utama

- **Integrasi Sederhana**: Sematkan chatbot ke situs web manapun melalui satu baris skrip JavaScript, tanpa memerlukan implementasi kode yang kompleks di sisi klien.
- **Knowledge Base Fleksibel**: Latih AI dengan data spesifik Anda. Unggah dokumen (PDF, TXT) atau sediakan URL website untuk di-crawl dan diekstrak secara otomatis sebagai basis pengetahuan.
- **Dashboard Manajemen Intuitif**: Antarmuka untuk mengelola *bot*, sumber pengetahuan, melihat riwayat percakapan, dan mendapatkan skrip penyematan.
- **Riwayat & Analitik Percakapan**: Simpan setiap interaksi pengunjung berdasarkan sesi untuk analisis dan pemahaman kebutuhan pengguna.

## Tumpukan Teknologi

- **Backend**: FastAPI (Python)
- **Frontend (Dashboard)**: React.js (Vite)
- **Database**: PostgreSQL dengan ekstensi PGVector

## Instalasi & Konfigurasi

Ikuti langkah-langkah berikut untuk menjalankan KaitBot di lingkungan pengembangan lokal.

### Prasyarat

- Python 3.10+
- Node.js v18+ & npm
- Server PostgreSQL yang sedang berjalan
- API Key untuk LLM (contoh: Google Gemini)

### Instalasi PGVector

KaitBot memerlukan ekstensi `pgvector` di PostgreSQL untuk penyimpanan dan pencarian embedding. Cara instalasinya dapat dilihat pada link berikut:

```bash
https://github.com/pgvector/pgvector
```
```bash
https://github.com/pgvector/pgvector-python
```

Pastikan untuk mengaktifkan ekstensi di database Anda dengan perintah SQL:

```sql
CREATE EXTENSION vector;
```

### 1. Backend (FastAPI)

```bash
# Clone repositori
git clone https://github.com/username-anda/KaitBot.git
cd KaitBot/backend

# Buat dan aktifkan virtual environment
python -m venv venv
source venv/bin/activate  # Untuk Windows: venv\Scripts\activate

# Instal dependensi Python
pip install -r requirements.txt

# Konfigurasi Environment
cp .env.example .env
```

Edit file `.env` dan isi variabel berikut:

- `DATABASE_URL`: URL koneksi ke database PostgreSQL Anda.
- `TAVILY_API_KEY`: API key untuk Tavily Search sebagai tool RAG.
- `GEMINI_API_KEY`: API key Anda untuk Google Gemini.
- `GEMINI_EMBEDDING_MODEL`: Model embedding yang digunakan (contoh: `models/embedding-001`).
- `GEMINI_TEXT_MODEL`: Model teks yang digunakan (contoh: `gemini-2.5-flash-lite`).
- `STORAGE_ROOT`: Path direktori lokal untuk menyimpan file unggahan.
- `LANGSMITH_...`: (Opsional) Konfigurasi untuk tracing dan observability menggunakan LangSmith.

```bash
# Jalankan migrasi database dengan Alembic
alembic upgrade head

# Jalankan server backend
uvicorn app.main:app --reload
```

Server backend akan berjalan di `http://localhost:8000`.

### 2. Frontend (React)

```bash
# Buka terminal baru, navigasi ke direktori frontend
cd ../frontend-app

# Instal dependensi Node.js
npm install

# Konfigurasi Environment
cp .env.example .env
```

Pastikan `VITE_API_URL` di dalam file `.env` sudah sesuai (default: `http://localhost:8000/api/v1`).

```bash
# Jalankan server development frontend
npm run dev
```

Dashboard frontend dapat diakses di `http://localhost:5173`.

## Panduan Penggunaan

1. Akses `http://localhost:5173` melalui browser.
2. Lakukan registrasi akun dan login.
3. Buat entitas *Company* baru melalui Dashboard.
4. Pilih company yang relevan untuk masuk ke halaman manajemen.
5. Gunakan tab *Document* atau *Website* untuk melatih chatbot dengan menyediakan sumber data.
6. Setelah proses data selesai, salin *Embed Script* yang tersedia.
7. Tempelkan skrip tersebut di dalam tag `<head>` pada file HTML situs web Anda.
8. Widget chatbot akan aktif dan muncul di situs web tersebut.

## Berkontribusi

Let's have fun !!!


1. Fork repositori ini.
2. Buat branch baru (`git checkout -b fitur/nama-fitur`).
3. Commit perubahan Anda (`git commit -am 'Menambahkan fitur X'`).
4. Push ke branch Anda (`git push origin fitur/nama-fitur`).
5. Buat Pull Request baru.