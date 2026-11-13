# -*- coding: utf-8 -*-
"""
PDF Converter Web - Konversi PDF ke TXT dan CSV via browser
Deploy gratis di Streamlit Community Cloud (https://share.streamlit.io)
"""

import io
import csv
import streamlit as st
import pdfplumber

st.set_page_config(page_title="PDF Converter", page_icon="📄", layout="centered")

# Batas ukuran file agar layanan tidak disalahgunakan (byte)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


# ------------------------- Logika konversi -------------------------

def pdf_to_txt(file) -> str:
    """Ekstrak seluruh teks PDF menjadi string (per halaman)."""
    parts = []
    with pdfplumber.open(file) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            parts.append(f"--- Halaman {i} ---\n{text}")
    return "\n\n".join(parts)


def pdf_to_csv(file) -> bytes:
    """Ekstrak semua tabel di PDF menjadi CSV (utf-8-sig agar rapi di Excel)."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    found = 0
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                if not table:
                    continue
                found += 1
                for row in table:
                    writer.writerow(["" if c is None else str(c).strip() for c in row])
    return buf.getvalue().encode("utf-8-sig"), found


# ------------------------- UI -------------------------

st.title("📄 PDF Converter")
st.markdown("Ubah file PDF menjadi **TXT** atau **CSV** — gratis, langsung di browser.")

with st.sidebar:
    st.header("⚙️ Opsi")
    fmt = st.radio("Format output", ["TXT + CSV", "Hanya TXT", "Hanya CSV"])
    st.markdown("---")
    st.markdown(
        "**Cara pakai:**\n"
        "1. Upload file PDF\n"
        "2. Tunggu proses selesai\n"
        "3. Klik tombol download\n\n"
        f"Maks. ukuran file: **{MAX_FILE_SIZE // (1024 * 1024)} MB**"
    )

uploaded_files = st.file_uploader(
    "Upload file PDF (bisa lebih dari satu)",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploaded_files:
    # Validasi ukuran
    too_big = [f.name for f in uploaded_files if f.size > MAX_FILE_SIZE]
    files = [f for f in uploaded_files if f.size <= MAX_FILE_SIZE]
    if too_big:
        st.warning(f"Melebihi batas {MAX_FILE_SIZE // (1024 * 1024)} MB: {', '.join(too_big)}")
    if not files:
        st.stop()

    do_txt = fmt in ("TXT + CSV", "Hanya TXT")
    do_csv = fmt in ("TXT + CSV", "Hanya CSV")

    progress = st.progress(0, text="Memproses...")
    results = []
    errors = []

    for idx, file in enumerate(files):
        try:
            pdf_file = io.BytesIO(file.getvalue())
            txt_bytes = csv_bytes = None
            n_tables = 0

            if do_txt:
                text = pdf_to_txt(pdf_file)
                txt_bytes = text.encode("utf-8")

            if do_csv:
                pdf_file.seek(0)
                csv_bytes, n_tables = pdf_to_csv(pdf_file)

            results.append((file.name, txt_bytes, csv_bytes, n_tables))
        except Exception as e:
            errors.append((file.name, str(e)))

        progress.progress((idx + 1) / len(files), text=f"Memproses {idx + 1}/{len(files)}...")

    progress.empty()

    if errors:
        with st.expander(f"⚠️ {len(errors)} file gagal diproses"):
            for name, err in errors:
                st.error(f"**{name}**: {err}")

    for name, txt_bytes, csv_bytes, n_tables in results:
        stem = name.rsplit(".", 1)[0]
        with st.container(border=True):
            st.subheader(f"✅ {name}")
            if do_txt and txt_bytes is not None:
                st.download_button(
                    "⬇️ Download TXT",
                    data=txt_bytes,
                    file_name=f"{stem}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key=f"txt-{name}",
                )
            if do_csv and csv_bytes is not None:
                label = f"⬇️ Download CSV ({n_tables} tabel)" if n_tables else "⬇️ Download CSV (tidak ada tabel terdeteksi)"
                st.download_button(
                    label,
                    data=csv_bytes,
                    file_name=f"{stem}.csv",
                    mime="text/csv",
                    disabled=(n_tables == 0),
                    use_container_width=True,
                    key=f"csv-{name}",
                )
                if n_tables == 0:
                    st.caption("PDF ini tidak berisi tabel yang bisa dideteksi.")
else:
    st.info("👆 Silakan upload file PDF untuk memulai.")

st.markdown("---")
st.caption("Dibuat dengan Streamlit + pdfplumber • File diproses langsung di memori dan tidak disimpan.")
