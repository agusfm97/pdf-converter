@echo off
REM Runner cepat: double-click untuk melihat cara pakai, atau pakai argumen
REM Contoh: pdf_converter.bat C:\folder\pdf --format csv
python "%~dp0pdf_converter.py" %*
pause
