# app.py

from flask import Flask, request, jsonify, render_template, redirect, session
from flask_cors import CORS
import json
import datetime
import qrcode
import io
import os
import base64
from pathlib import Path
from email_utils import send_ticket_email

app = Flask(__name__)
app.secret_key = "campuslink_secret_key"
CORS(app)

DB_PATH = Path("maintenance_db.json")

# --------------ADMIN_PASSWORD--------------

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

# ---------------- DATABASE ----------------

def init_db():
    if not DB_PATH.exists():
        DB_PATH.write_text(json.dumps({"reports": []}, indent=4))

def get_db():
    init_db()
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- UTILITIES ----------------

def generate_ticket_id():
    return "CL" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def generate_qr_code(ticket_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(f"Ticket ID: {ticket_id}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    return base64.b64encode(img_io.getvalue()).decode()

def error_response(message, code=400):
    return jsonify({"status": "error", "message": message}), code

def success_response(data={}, code=200):
    return jsonify({"status": "success", **data}), code

# ---------------- ROUTES ----------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin-auth", methods=["POST"])
def admin_auth():
    data = request.get_json()
    password = data.get("password")

    if password == ADMIN_PASSWORD:
        session["admin"] = True
        return jsonify({"status": "success"})

    return jsonify({"status":"error", "message": "Wrong password"}), 401
    
@app.route("/admin")
def admin():
    return render_template("admin.html")

# ---------------- SUBMIT REPORT ----------------

@app.route("/api/maintenance", methods=["POST"])
def submit_report():

    data = request.get_json()

    if not data:
        return error_response("Invalid JSON body")

    required_fields = [
        "name",
        "email",
        "phone",
        "block",
        "floor",
        "room_no",
        "category",
        "priority",
        "issue_date",
        "description",
    ]

    for field in required_fields:
        if not data.get(field):
            return error_response(f"Missing field: {field}")

    ticket_id = generate_ticket_id()
    qr_code = generate_qr_code(ticket_id)

    report = {
        "ticket_id": ticket_id,
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "block": data["block"],
        "floor": data["floor"],
        "room_no": data["room_no"],
        "category": data["category"],
        "other_detail": data.get("other_detail", ""),
        "priority": data["priority"],
        "description": data["description"],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Pending",
        "qr_code": qr_code,
    }

    db = get_db()
    db["reports"].append(report)
    save_db(db)

    try:
        send_ticket_email(ticket_id, report)

    except Exception as e:
        print(f"Email error: {str(e)}")

    return success_response(
        {
            "message": "Report submitted successfully",
            "ticket_id": ticket_id,
            "qr_code": qr_code,
        }
    )

# ---------------- GET ALL REPORTS ----------------

@app.route("/api/reports", methods=["GET"])
def get_reports():

    db = get_db()
    reports = db.get("reports", [])

    # hide qr codes
    clean_reports = []

    for r in reports:
        copy = r.copy()
        copy.pop("qr_code", None)
        clean_reports.append(copy)

    return success_response({"reports": clean_reports})

# ---------------- GET SINGLE REPORT ----------------

@app.route("/api/reports/<ticket_id>", methods=["GET"])
def get_report(ticket_id):

    db = get_db()

    for report in db.get("reports", []):
        if report["ticket_id"] == ticket_id:
            return success_response({"report": report})

    return error_response("Report not found", 404)

# ---------------- UPDATE STATUS ----------------

@app.route("/api/reports/<ticket_id>", methods=["PUT"])
def update_report(ticket_id):

    data = request.get_json()

    if not data:
        return error_response("Invalid JSON body")

    status = data.get("status")

    if not status:
        return error_response("Missing status field")

    db = get_db()

    for report in db["reports"]:

        if report["ticket_id"] == ticket_id:

            report["status"] = status
            save_db(db)

            return success_response({"message": "Report updated"})

    return error_response("Report not found", 404)

# ---------------- HEALTH ----------------

@app.route("/health")
def health():
    return {"status": "ok"}

# ---------------- MAIN ----------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)