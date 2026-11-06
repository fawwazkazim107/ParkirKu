from flask import Flask, jsonify, render_template, request
import paho.mqtt.client as mqtt
import json
import threading

from models import ParkingManager, init_db

app = Flask(__name__)
manager = ParkingManager()

API_KEY = "ganti-dengan-kunci-rahasia"

# Inisialisasi Database
init_db()

# ==========================================
# KONFIGURASI SUBSCRIBER MQTT (DARI WOKWI)
# ==========================================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "parkirku/kelompok3/sensor"

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"📩 [MQTT] Data masuk: {payload}")
    
    try:
        data = json.loads(payload)
        kode_slot = data.get("kode")
        status_baru = data.get("status")
        
        # Panggil fungsi database (models.py)
        if manager.update_status(kode_slot, status_baru):
            print(f"✅ Database terupdate: {kode_slot} -> {status_baru}")
        else:
            print(f"❌ Gagal update database untuk {kode_slot}")
            
    except Exception as e:
        print(f"Error parsing data MQTT: {e}")

def start_mqtt():
    print("Memulai Subscriber MQTT...")
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_message = on_message
    
    try:
        # Konek ke HiveMQ (Tanpa SSL/Password)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.subscribe(MQTT_TOPIC)
        print("✅ MQTT Subscriber Berjalan di Background!")
        
        # Jalankan loop di background
        client.loop_start() 
    except Exception as e:
        print(f"❌ Gagal konek ke MQTT: {e}")

# Jalankan MQTT di thread terpisah agar tidak memblokir web
mqtt_thread = threading.Thread(target=start_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()

# ==========================================
# ROUTES WEB FLASK
# ==========================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/update", methods=["POST"])
def api_update():
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify({"error": "API key salah"}), 401

    data = request.get_json(silent=True) or {}
    if manager.update_status(data.get("kode"), data.get("status")):
        return jsonify({"pesan": "berhasil"})
    return jsonify({"error": "kode slot atau status tidak valid"}), 400

@app.route("/api/slots")
def api_slots():
    return jsonify({
        "ringkasan": manager.ringkasan(),
        "slots": [s.to_dict() for s in manager.daftar_slot()], 
    })

@app.route("/api/riwayat-area")
def api_riwayat_area():
    return jsonify(manager.riwayat_per_area())

@app.route("/api/riwayat-slot")
def api_riwayat_slot():
    return jsonify(manager.riwayat_per_slot())

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)