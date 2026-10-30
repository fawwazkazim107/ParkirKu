import random
import time

import requests

SERVER_URL = "http://127.0.0.1:5000/api/update"  # ganti ke alamat PythonAnywhere saat deploy
API_KEY = "ganti-dengan-kunci-rahasia"
SLOT_KODE = [f"{z}{i}" for z in "AB" for i in range(1, 6)]
INTERVAL_DETIK = 5

while True:
    kode = random.choice(SLOT_KODE)
    status = random.choice(["Kosong", "Terisi"])
    try:
        r = requests.post(
            SERVER_URL,
            json={"kode": kode, "status": status},
            headers={"X-API-Key": API_KEY},
            timeout=5,
        )
        print(f"{kode} -> {status} | {r.status_code}")
    except requests.RequestException as e:
        print("Gagal kirim:", e)
    time.sleep(INTERVAL_DETIK)