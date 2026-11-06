import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "parkirku.db")
STATUS_VALID = ("Kosong", "Terisi")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(zona=("A", "B"), per_zona=4):
    """Buat 2 tabel dan isi data awal slot jika masih kosong."""
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS parking_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode TEXT UNIQUE NOT NULL,
            lokasi TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Kosong'
        );
        CREATE TABLE IF NOT EXISTS parking_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            waktu TEXT NOT NULL,
            FOREIGN KEY (slot_id) REFERENCES parking_slots(id)
        );
    """)
    ada = conn.execute("SELECT COUNT(*) FROM parking_slots").fetchone()[0]
    if ada == 0:
        for z in zona:
            for i in range(1, per_zona + 1):
                conn.execute(
                    "INSERT INTO parking_slots (kode, lokasi) VALUES (?, ?)",
                    (f"{z}{i}", f"Area {z}"),
                )
    conn.commit()
    conn.close()


class ParkingSlot:
    def __init__(self, id, kode, lokasi, status):
        self.id = id
        self.kode = kode
        self.lokasi = lokasi
        self.status = status

    def to_dict(self):
        return {"kode": self.kode, "lokasi": self.lokasi, "status": self.status}


class ParkingLog:
    def __init__(self, slot_id, status, waktu):
        self.slot_id = slot_id
        self.status = status
        self.waktu = waktu


class ParkingManager:
    def daftar_slot(self):
        conn = get_conn()
        rows = conn.execute("SELECT * FROM parking_slots ORDER BY kode").fetchall()
        conn.close()
        return [ParkingSlot(r["id"], r["kode"], r["lokasi"], r["status"]) for r in rows]

    def hitung_kosong(self):
        conn = get_conn()
        n = conn.execute(
            "SELECT COUNT(*) FROM parking_slots WHERE status = 'Kosong'"
        ).fetchone()[0]
        conn.close()
        return n

    def update_status(self, kode, status):
        """Update status slot dan catat ke log. Return True jika berhasil."""
        if status not in STATUS_VALID:
            return False
        conn = get_conn()
        slot = conn.execute(
            "SELECT id FROM parking_slots WHERE kode = ?", (kode,)
        ).fetchone()
        if slot is None:
            conn.close()
            return False
        conn.execute(
            "UPDATE parking_slots SET status = ? WHERE id = ?", (status, slot["id"])
        )
        log = ParkingLog(
            slot["id"], status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        conn.execute(
            "INSERT INTO parking_logs (slot_id, status, waktu) VALUES (?, ?, ?)",
            (log.slot_id, log.status, log.waktu),
        )
        conn.commit()
        conn.close()
        return True

    def ringkasan(self):
        slots = self.daftar_slot()
        kosong = sum(1 for s in slots if s.status == "Kosong")
        return {"total": len(slots), "kosong": kosong, "terisi": len(slots) - kosong}

    def riwayat_per_area(self):
        """Persentase keterisian tiap area dari data log."""
        conn = get_conn()
        rows = conn.execute("""
            SELECT s.lokasi,
                   COUNT(l.id) AS total,
                   SUM(CASE WHEN l.status = 'Terisi' THEN 1 ELSE 0 END) AS terisi
            FROM parking_slots s
            LEFT JOIN parking_logs l ON l.slot_id = s.id
            GROUP BY s.lokasi ORDER BY s.lokasi
        """).fetchall()
        conn.close()
        return [
            {
                "lokasi": r["lokasi"],
                "persen_terisi": round((r["terisi"] or 0) * 100 / r["total"]) if r["total"] else 0,
            }
            for r in rows
        ]

    def riwayat_per_slot(self):
        """Persentase keterisian tiap slot dari data log."""
        conn = get_conn()
        rows = conn.execute("""
            SELECT s.kode,
                   COUNT(l.id) AS total,
                   SUM(CASE WHEN l.status = 'Terisi' THEN 1 ELSE 0 END) AS terisi
            FROM parking_slots s
            LEFT JOIN parking_logs l ON l.slot_id = s.id
            GROUP BY s.id ORDER BY s.kode
        """).fetchall()
        conn.close()
        return [
            {
                "kode": r["kode"],
                "persen_terisi": round((r["terisi"] or 0) * 100 / r["total"]) if r["total"] else 0,
            }
            for r in rows
        ]