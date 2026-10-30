from flask import Flask, jsonify, render_template, request

from models import ParkingManager, init_db

app = Flask(__name__)
manager = ParkingManager()

API_KEY = "ganti-dengan-kunci-rahasia"

init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/update", methods=["POST"])
def api_update():
    """Dipanggil node sensor. Body JSON: {"kode": "A1", "status": "Terisi"}"""
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


@app.route("/api/riwayat")
def api_riwayat():
    return jsonify(manager.riwayat_per_jam())


if __name__ == "__main__":
    app.run(debug=True)