import random
import time

import requests

SERVER_URL = "http://127.0.0.1:5000/api/update"
API_KEY = "ganti-dengan-kunci-rahasia"
SLOT_KODE = ["A1", "A2", "A3", "A4", "A5", "A6"]
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