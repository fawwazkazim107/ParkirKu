
# ParkirKu - Smart Parking Monitoring

## 1. Deskripsi Proyek

ParkirKu merupakan sistem monitoring tempat parkir berbasis IoT yang bertujuan untuk membantu pengguna mengetahui ketersediaan slot parkir secara lebih mudah.

Sistem ini memungkinkan pengguna melihat jumlah slot parkir, jumlah slot kosong, jumlah slot terisi, serta kondisi setiap slot melalui website dashboard.

## 2. Tujuan Proyek

- Memudahkan pengguna mengetahui ketersediaan tempat parkir.
- Menampilkan informasi kondisi setiap slot secara langsung dari data sistem.
- Menyimpan status dan riwayat perubahan kondisi parkir.
- Mengurangi kesulitan pengguna dalam mencari tempat parkir kosong.

## 3. Fitur Utama

- Menampilkan jumlah seluruh slot parkir.
- Menampilkan jumlah slot kosong dan terisi.
- Menampilkan status masing-masing slot.
- Menyimpan riwayat perubahan status parkir.
- Menampilkan informasi parkir melalui dashboard website.

## 4. Teknologi yang Digunakan

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- ESP32 dan HC-SR04 (integrasi IoT, jika sudah diimplementasikan)
- Wokwi (simulasi IoT, jika digunakan)

## 5. Alur Kerja Sistem

1. Sensor atau simulator mendeteksi kondisi slot parkir.
2. Data dikirimkan ke backend melalui HTTP API.
3. Backend Flask menerima dan memvalidasi data.
4. Data status disimpan ke database SQLite.
5. Website dashboard mengambil data melalui API.
6. Pengguna dapat melihat kondisi tempat parkir melalui dashboard.

## 6. Struktur Proyek

Bagian ini akan disesuaikan dengan struktur folder dan file yang benar-benar digunakan dalam repository.

## 7. Instalasi

Petunjuk instalasi akan dilengkapi sesuai konfigurasi dan dependensi proyek.

## 8. Cara Menjalankan Aplikasi

Petunjuk menjalankan backend dan dashboard akan dilengkapi setelah implementasi selesai.

## 9. Pengujian

Bagian ini berisi skenario dan hasil pengujian API, database, dashboard, simulator, dan integrasi sistem.

## 10. Tim Pengembang

- Fawwaz - Database
- Alif - Backend
- Ardhy - Frontend
- Ucup - IoT dan Wokwi
- Anis - Dokumentasi dan Presentasi
