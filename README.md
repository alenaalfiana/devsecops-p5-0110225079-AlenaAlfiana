# Perpustakaan Mini (devsecops-p5-NIM)

## 1. Nama Aplikasi & Fungsi
**Perpustakaan Mini** adalah aplikasi manajemen perpustakaan berbasis command line (CLI).
Fungsi utama: menambah buku, mencari buku berdasarkan judul/penulis, meminjam buku,
mengembalikan buku, dan melihat daftar peminjaman aktif. Data disimpan dalam berkas JSON.

## 2. Bahasa / Framework
- Python 3.12 (hanya pustaka standar untuk aplikasi)
- pytest + pytest-cov (unit test & coverage)
- Bandit (SAST)

## 3. Cara Menjalankan
```bash
git clone https://github.com/<username>/devsecops-p5-NIM.git
cd devsecops-p5-NIM
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Contoh penggunaan
python main.py add 9780132350884 "Clean Code" "Robert Martin" 2008
python main.py search clean
python main.py borrow 9780132350884 Budi
python main.py loans
python main.py return 9780132350884

# Menjalankan unit test
python -m pytest tests/ -v --cov=library
```

## 4. Overview Pipeline CI/CD
Workflow: `.github/workflows/devsecops.yml`
Trigger: `push` dan `pull_request` ke branch `main`. Runner: `ubuntu-latest`.

| Job | Fungsi | Quality Gate |
|-----|--------|--------------|
| `build` | Install dependencies, jalankan unit test + coverage | Gagal jika coverage < 70% atau ada test gagal |
| `sast-scan` (`needs: build`) | Scan kode dengan Bandit, unggah laporan JSON sebagai artifact | Gagal jika ada temuan severity MEDIUM/HIGH |

Alur: `push/PR` -> `build` -> `sast-scan` -> hasil (pass/fail) di tab Actions.

## Struktur Proyek
```
library/        models.py, validators.py, storage.py, services.py, cli.py
tests/          test_validators.py, test_services.py, test_cli.py
main.py         titik masuk aplikasi
.github/workflows/devsecops.yml
```
