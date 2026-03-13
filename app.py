# app.py

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import datetime
import qrcode
import io
import base64
from pathlib import Path

# -------------------- APP CONFIG --------------------
app = Flask(__name__)
CORS(app)

# -------------------- DATABASE SETUP --------------------
DB_PATH = Path("maintenance_db.json")

def get_db():
    if not DB_PATH.exists():
        DB_PATH.write_text(json.dumps({"reports": []}))
    return json.loads(DB_PATH.read_text())

def save_db(data):
    DB_PATH.write_text(json.dumps(data, indent=4))

# -------------------- QR CODE --------------------
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
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return base64.b64encode(img_io.getvalue()).decode()

# -------------------- ROUTES --------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# -------------------- API: SUBMIT REPORT --------------------
@app.route('/api/maintenance', methods=['POST'])
def handle_submission():
    try:
        data = request.get_json(silent=True)

        required_fields = [
            'name', 'email', 'phone', 'block', 'floor',
            'room_no', 'category', 'priority',
            'issue_date', 'description'
        ]

        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "status": "error",
                    "message": f"Missing field: {field}"
                }), 400

        ticket_id = 'CL' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        qr_code_base64 = generate_qr_code(ticket_id)

        new_report = {
            "ticket_id": ticket_id,
            "name": data['name'],
            "email": data['email'],
            "phone": data['phone'],
            "block": data['block'],
            "floor": data['floor'],
            "room_no": data['room_no'],
            "category": data['category'],
            "other_detail": data.get('other_detail', ''),
            "priority": data['priority'],
            "issue_date": data['issue_date'],
            "description": data['description'],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Pending",
            "qr_code": qr_code_base64
        }

        db = get_db()
        db["reports"].append(new_report)
        save_db(db)

        return jsonify({
            "status": "success",
            "message": "Report submitted successfully!",
            "ticket_id": ticket_id,
            "qr_code": qr_code_base64
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# -------------------- API: GET ALL REPORTS --------------------
@app.route('/api/reports', methods=['GET'])
def get_reports():
    try:
        db = get_db()
        reports = db.get("reports", [])

        for report in reports:
            report.pop("qr_code", None)

        return jsonify({
            "status": "success",
            "reports": reports
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# -------------------- API: GET SINGLE REPORT --------------------
@app.route('/api/reports/<ticket_id>', methods=['GET'])
def get_report(ticket_id):
    try:
        db = get_db()
        for report in db.get("reports", []):
            if report["ticket_id"] == ticket_id:
                return jsonify({
                    "status": "success",
                    "report": report
                }), 200

        return jsonify({
            "status": "error",
            "message": "Report not found"
        }), 404

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# -------------------- API: UPDATE STATUS --------------------
@app.route('/api/reports/<ticket_id>', methods=['PUT'])
def update_report(ticket_id):
    try:
        data = request.get_json(silent=True)
        db = get_db()

        for report in db.get("reports", []):
            if report["ticket_id"] == ticket_id:
                if "status" in data:
                    report["status"] = data["status"]
                save_db(db)
                return jsonify({
                    "status": "success",
                    "message": "Report updated"
                }), 200

        return jsonify({
            "status": "error",
            "message": "Report not found"
        }), 404

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# -------------------- HEALTH CHECK --------------------
@app.route('/health')
def health():
    return {"status": "ok"}

# -------------------- ENTRY POINT --------------------
if __name__ == "__main__":
    app.run()
