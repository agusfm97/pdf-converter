# Membuat PDF contoh untuk menguji converter
from fpdf import FPDF, XPos, YPos

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 10, "Laporan Penjualan Bulanan", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
pdf.ln(5)
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 6, "Berikut adalah ringkasan penjualan produk Q4 tahun lalu. "
                     "Data diambil dari sistem kasir dan telah diverifikasi oleh tim keuangan.")
pdf.ln(3)

# Tabel
rows = [
    ["Produk", "Qty", "Harga", "Total"],
    ["Laptop", "12", "8500000", "102000000"],
    ["Mouse", "150", "75000", "11250000"],
    ["Keyboard", "80", "220000", "17600000"],
    ["Monitor", "35", "1900000", "66500000"],
]
col_w = [50, 25, 40, 45]
pdf.set_font("Helvetica", "B", 11)
for i, row in enumerate(rows):
    if i == 1:
        pdf.set_font("Helvetica", "", 11)
    for j, cell in enumerate(row):
        pdf.cell(col_w[j], 8, cell, border=1)
    pdf.ln()

pdf.ln(10)
pdf.multi_cell(0, 6, "Catatan: semua angka dalam Rupiah. Stok tersisa akan diaudit "
                     "pada akhir bulan ini oleh bagian gudang.")

pdf.output("contoh_laporan.pdf")
print("contoh_laporan.pdf dibuat")
