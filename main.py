import network
import urequests
import time
from machine import Pin

# Inisialisasi LED indikator pada GPIO 2 (Sesuai diagram.json)
led = Pin(2, Pin.OUT)

# Konfigurasi WiFi Wokwi
SSID = "Wokwi-GUEST"
PASSWORD = ""

# URL Server Flask Anda via Ngrok
# Pastikan ganti bagian "xxxx-xx.ngrok-free.app" dengan URL aktif dari terminal ngrok Anda
SERVER_URL = "https://xxxx-xx.ngrok-free.app/api/update" 
API_KEY = "ganti-dengan-kunci-rahasia"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Menghubungkan WiFi...", end="")
    while not wlan.isconnected():
        led.value(not led.value()) # LED berkedip saat proses koneksi
        time.sleep(0.3)
        print(".", end="")
        
    led.value(1) # LED menyala penuh jika berhasil terhubung
    print("\nWiFi Terhubung! IP Address:", wlan.ifconfig()[0])

def send_data():
    headers = {
        "Content-Type": "application/json", 
        "X-API-Key": API_KEY
    }
    
    # Data status slot parkir yang dikirim ke backend Flask
    post_data = '{"kode": "A4", "status": "Terisi"}'
    
    try:
        print("Mengirim data ke server...")
        res = urequests.post(SERVER_URL, data=post_data, headers=headers)
        print("Response Server:", res.text)
        res.close()
    except Exception as e:
        print("Gagal mengirim data:", e)

# Jalankan koneksi WiFi saat ESP32 pertama kali menyala
connect_wifi()

# Loop utama pengiriman data setiap 5 detik
while True:
    send_data()
    time.sleep(5)