from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

# modules for database operations
from report_database import save_report, get_report, list_reports
from modelLoad import load_cnn_model            # Mia's modelLoad.py, UNCOMMENT LATER
from prediction import run_prediction           # Mia's prediction.py, UNCOMMENT LATER 

# global model & upload config
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# will get from Mia's file UNCOMMENT LATER
MODEL = load_cnn_model()   # load CNN once at startup
MODEL_PATH = "CNN_model.keras"   # path where model is stored (optional, can take this out)
METADATA = None            # extra model info (optional,can take this out)


# allowed file extensions for image uploads 
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_filename(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# stub used if model fails (for testing only)
def simple_detector_stub(path):
    import random
    return {
        "is_ai": random.random() > 0.5,
        "confidence": random.random(),
        "model": "stub"
    }

# Flask application that creates and configures the Flask app 
def create_app():
    app = Flask(__name__) # creates the web server 
    CORS(app) #allows frontend to call backend API

    # checkpoint used by developers to confirm backend is running, returns: {"status": "ok"}
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"})

    # model status checkpoint checks whether model is loaded into memory
    @app.route("/api/model_status", methods=["GET"])
    def model_status():
        loaded = MODEL is not None
        meta = METADATA or {}
        return jsonify({
            "model_loaded": bool(loaded),
            "model_path": MODEL_PATH if loaded else None,
            "metadata": meta,
        })

    # deepfake detection route (main feature)
    # what the frontend calls to analyze an uploaded image
    @app.route("/api/detect", methods=["POST"])
    def detect():
        # must upload an image named "image"
        if "image" not in request.files:
            return jsonify({"error": "no image provided"}), 400

        # makes sure filename is not empty
        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "empty filename"}), 400

        # makes sure only images of file type png/jpg/jpeg are imported
        if not allowed_filename(file.filename):
            return jsonify({"error": "file type not allowed"}), 400

        # creates a safe and timestamped filename
        filename = secure_filename(
            f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        )
        # saves the uploaded file to the upload directory
        save_path = os.path.join(UPLOAD_DIR, filename)
        file.save(save_path)

        # run prediction 
        try:
            result = run_prediction(MODEL, save_path)
        except Exception as ex:
            print(f"Model inference failed, falling back to stub: {ex}")
            result = simple_detector_stub(save_path)

        # report entry, builds a JSON object with the report details
        # will be stored in MongoDB database 
        report = {
            "filename": filename,
            "is_ai": result["is_ai"],
            "confidence": result["confidence"],
            "model": result.get("model", "cnn"),
            "created_at": datetime.utcnow().isoformat(),
        }
        report_id = save_report(report) # saves the report to the database
        return jsonify({"report_id": report_id, "report": report}), 201 # frontend receives the report ID and report details in JSON format

    # get report by its unique ID
    @app.route("/api/report/<int:report_id>", methods=["GET"])
    def get_report_route(report_id):
        r = get_report(report_id)
        if not r:
            return jsonify({"error": "not found"}), 404 #returns 404 if report not found
        # adds full URL to access the uploaded image
        r["image_url"] = request.host_url.rstrip("/") + f"/uploads/{r['filename']}"
        return jsonify(r)

    # list all reports (with optional limit), each report gets an image URL
    @app.route("/api/reports", methods=["GET"])
    def list_reports_route():
        try:
            limit = int(request.args.get("limit", 20))
        except ValueError:
            limit = 20

        items = list_reports(limit=limit)

        for r in items:
            r["image_url"] = request.host_url.rstrip("/") + f"/uploads/{r['filename']}"

        return jsonify({"reports": items})

    # serve uploaded files
    @app.route("/uploads/<path:filename>")
    def uploads(filename):
        safe = secure_filename(filename) #prevents path attacks 
        full = os.path.join(UPLOAD_DIR, safe)
        if not os.path.exists(full):
            abort(404)
        return send_from_directory(UPLOAD_DIR, safe)

    return app # returns the app instance


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
