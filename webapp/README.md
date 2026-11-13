# PDF Converter Web

Web app untuk mengkonversi PDF menjadi **TXT** dan **CSV** langsung di browser.
Dibangun dengan [Streamlit](https://streamlit.io) dan [pdfplumber](https://github.com/jsvine/pdfplumber).

Fitur:
- ✅ Upload beberapa PDF sekaligus
- ✅ Pilih format output: TXT, CSV, atau keduanya
- ✅ Deteksi tabel otomatis untuk CSV
- ✅ Tombol download langsung
- ✅ Batas ukuran file 50 MB
- ✅ File diproses di memori, tidak disimpan di server

---

## 🚀 Cara Deploy Publik (Gratis) — Streamlit Community Cloud

### Langkah 1: Simpan kode ke GitHub

```bash
cd pdf-converter
git init
git add webapp/
git commit -m "PDF converter web app"
```

Lalu buat repo baru di https://github.com/new (misal: `pdf-converter`), dan push:

```bash
git remote add origin https://github.com/USERNAME/pdf-converter.git
git push -u origin main
```

> **Penting:** pastikan struktur repo seperti ini:
> ```
> pdf-converter/
> ├── webapp/
> │   ├── app.py              ← entrypoint
> │   └── requirements.txt    ← dependency untuk web app
> ```

### Langkah 2: Deploy ke Streamlit Cloud

1. Buka https://share.streamlit.io
2. Login dengan akun GitHub
3. Klik **"Create app"** → **"Paste repo URL"**
4. Isi:
   - **Repository:** `USERNAME/pdf-converter`
   - **Branch:** `main`
   - **Main file path:** `webapp/app.py`
5. Klik **Deploy** ✅

Setelah 2–3 menit, app kamu aktif di URL seperti:
`https://username-pdf-converter.streamlit.app`

Bagikan URL itu ke siapa saja! 🎉

### Langkah 3 (opsional): Custom domain

Bagian **Settings → Custom domain** di dashboard Streamlit Cloud jika kamu punya domain sendiri.

---

## 💻 Menjalankan di Komputer Sendiri

```bash
pip install -r requirements.txt
streamlit run app.py
```

Buka http://localhost:8501 di browser.

---

## ❓ FAQ / Catatan

**Apakah ada batas penggunaan?**
Streamlit Community Cloud gratis tanpa login pengguna, tapi resource bersifat shared — batas 50 MB per file sudah cukup aman. Jika traffic tinggi, pertimbangkan Streamlit Teams atau hosting lain (Hugging Face Spaces, Render, Railway).

**PDF hasil scan (gambar) tidak bisa dikonversi?**
Ya, karena butuh OCR. Bisa ditambahkan nanti dengan `pytesseract` + `pdf2image`.

**Apakah file pengguna disimpan?**
Tidak. File dibaca ke memori, dikonversi, lalu dibuang.
