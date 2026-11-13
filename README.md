# PDF Converter

Program Python untuk mengkonversi file PDF menjadi **TXT** (teks per halaman) dan **CSV** (tabel). Mendukung konversi satu file maupun batch seluruh PDF dalam folder.

## Instalasi

```bash
pip install -r requirements.txt
```

## Cara Pakai

```bash
# Konversi satu file (TXT + CSV)
python pdf_converter.py laporan.pdf

# Hanya TXT
python pdf_converter.py laporan.pdf --format txt

# Hanya CSV (ekstrak tabel)
python pdf_converter.py laporan.pdf --format csv

# Batch: semua PDF dalam folder + subfolder
python pdf_converter.py C:\folder\pdf --output hasil

# Batch tanpa subfolder
python pdf_converter.py C:\folder\pdf --no-recursive
```

Pengguna Windows bisa juga double-click `run.bat`.

## Opsi

| Opsi | Keterangan |
|------|-----------|
| `input` | File PDF atau folder berisi PDF |
| `--format txt\|csv\|both` | Format output (default: `both`) |
| `--output FOLDER` | Folder hasil (default: `./hasil`) |
| `--no-recursive` | Jangan scan subfolder |

## Catatan

- **CSV** mengekstrak tabel yang terdeteksi di PDF (hasilnya kosong jika PDF tidak berisi tabel).
- **TXT** menyimpan teks per halaman dengan penanda `--- Halaman N ---`.
- PDF hasil scan (gambar) tidak bisa diekstrak — membutuhkan OCR (tambahan seperti `pytesseract`).
- CSV di-encode `utf-8-sig` agar tampil benar saat dibuka di Excel.

## Isi Folder

- `pdf_converter.py` — program utama
- `buat_contoh.py` — generator PDF contoh untuk testing
- `contoh_laporan.pdf` — PDF contoh
- `hasil/` — folder output
