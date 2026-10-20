# praktikum-simple-app

Aplikasi Flask yang terhubung ke database MySQL, dibangun dan dideploy
menggunakan pipeline Jenkins dengan Docker (Praktikum Komputasi Awan).

## Endpoint
- GET  /        : pesan sambutan
- GET  /health  : cek koneksi database
- GET  /notes   : daftar catatan dari MySQL
- POST /notes   : tambah catatan, body JSON: {"content": "isi catatan"}

## Pipeline
Checkout, Build, Build Docker Image, Push Docker Image, Deploy (App + MySQL), Verify.