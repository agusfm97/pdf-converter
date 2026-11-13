#!/usr/bin/env python3
"""
PDF Converter - Konversi PDF ke TXT dan CSV

Cara pakai:
    python pdf_converter.py <file-atau-folder> [--format txt|csv|both] [--output FOLDER]

Contoh:
    # Konversi satu file (default: txt + csv)
    python pdf_converter.py laporan.pdf

    # Hanya TXT
    python pdf_converter.py laporan.pdf --format txt

    # Batch: semua PDF dalam folder (dan subfolder)
    python pdf_converter.py C:\\folder\\pdf --format both --output hasil
"""

import argparse
import csv
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("Library 'pdfplumber' belum terpasang. Install dengan:")
    print("    pip install pdfplumber")
    sys.exit(1)


def pdf_to_txt(pdf_path: Path, out_path: Path) -> int:
    """Ekstrak seluruh teks PDF menjadi satu file TXT. Return jumlah halaman."""
    parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            parts.append(f"--- Halaman {i} ---\n{text}")
        n_pages = len(pdf.pages)
    out_path.write_text("\n\n".join(parts), encoding="utf-8")
    return n_pages


def pdf_to_csv(pdf_path: Path, out_path: Path) -> int:
    """Ekstrak semua tabel di PDF menjadi CSV. Return jumlah tabel yang ditemukan."""
    tables_found = 0
    with pdfplumber.open(pdf_path) as pdf:
        with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            for page in pdf.pages:
                for table in page.extract_tables():
                    if not table:
                        continue
                    tables_found += 1
                    for row in table:
                        writer.writerow(["" if c is None else str(c).strip() for c in row])
    return tables_found


def convert_pdf(pdf_path: Path, output_dir: Path, fmt: str) -> bool:
    """Konversi satu PDF sesuai format. Return True jika berhasil."""
    print(f"\n[PDF] {pdf_path.name}")
    ok = True

    if fmt in ("txt", "both"):
        out = output_dir / f"{pdf_path.stem}.txt"
        try:
            n = pdf_to_txt(pdf_path, out)
            print(f"  TXT  -> {out.name}  ({n} halaman)")
        except Exception as e:
            ok = False
            print(f"  TXT  GAGAL: {e}")

    if fmt in ("csv", "both"):
        out = output_dir / f"{pdf_path.stem}.csv"
        try:
            n = pdf_to_csv(pdf_path, out)
            if n == 0:
                print("  CSV  -> tidak ada tabel terdeteksi (file CSV kosong)")
            else:
                print(f"  CSV  -> {out.name}  ({n} tabel)")
        except Exception as e:
            ok = False
            print(f"  CSV  GAGAL: {e}")

    return ok


def collect_pdfs(target: Path, recursive: bool = True) -> list[Path]:
    """Kumpulkan daftar PDF dari file atau folder."""
    if target.is_file():
        return [target]
    pattern = "**/*.pdf" if recursive else "*.pdf"
    return sorted(target.glob(pattern))


def main():
    parser = argparse.ArgumentParser(
        description="Konversi PDF ke TXT dan/atau CSV (mendukung batch folder)"
    )
    parser.add_argument("input", help="File PDF atau folder berisi PDF")
    parser.add_argument("--format", choices=["txt", "csv", "both"], default="both",
                        help="Format output (default: both)")
    parser.add_argument("--output", default="hasil",
                        help="Folder output (default: ./hasil)")
    parser.add_argument("--no-recursive", action="store_true",
                        help="Jangan scan subfolder jika input berupa folder")
    args = parser.parse_args()

    target = Path(args.input)
    if not target.exists():
        print(f"Error: '{target}' tidak ditemukan.")
        sys.exit(1)

    pdfs = collect_pdfs(target, recursive=not args.no_recursive)
    if not pdfs:
        print(f"Tidak ada file PDF ditemukan di '{target}'.")
        sys.exit(1)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Menemukan {len(pdfs)} file PDF. Output ke: {output_dir.resolve()}")

    success = 0
    for pdf in pdfs:
        if convert_pdf(pdf, output_dir, args.format):
            success += 1

    print(f"\nSelesai: {success}/{len(pdfs)} file berhasil dikonversi.")
    if success < len(pdfs):
        sys.exit(1)


if __name__ == "__main__":
    main()
