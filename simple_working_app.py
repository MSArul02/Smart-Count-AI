
# simple_working_app.py - Simple but Effective Factory Counter
import os
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from simple_working_detector import analyze_image_simple, simple_detector

app = Flask(__name__)

# Configuration
RESULTS_DIR = os.path.join("static", "results")
EXPORTS_DIR = "exports"

# Ensure directories exist
for directory in [RESULTS_DIR, EXPORTS_DIR]:
    os.makedirs(directory, exist_ok=True)

@app.route("/")
def index():
    """Main interface"""
    return render_template("simple_factory_index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    """Simple image analysis"""
    if "image" not in request.files:
        return jsonify({"ok": False, "error": "No image file provided"}), 400

    img_file = request.files["image"]
    if img_file.filename == '':
        return jsonify({"ok": False, "error": "No image selected"}), 400

    # Get confidence threshold
    try:
        min_confidence = float(request.form.get("min_confidence", 0.3))
        min_confidence = max(0.1, min(0.9, min_confidence))
    except:
        min_confidence = 0.3

    # Generate unique filenames
    timestamp = int(time.time() * 1000)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    input_path = os.path.join(RESULTS_DIR, f"input_{date_str}_{timestamp}.jpg")
    output_path = os.path.join(RESULTS_DIR, f"analyzed_{date_str}_{timestamp}.jpg")

    try:
        # Save uploaded image
        img_file.save(input_path)

        # Analyze image
        count, objects, classifications, session_stats, vibration_results = analyze_image_simple(
            input_path, output_path, min_confidence
        )

        # Calculate confidence
        if objects:
            avg_confidence = sum(obj['confidence'] for obj in objects) / len(objects)
        else:
            avg_confidence = 0

        # Prepare response
        result_data = {
            "ok": True,
            "timestamp": datetime.now().isoformat(),

            # Detection results
            "count": count,
            "confidence": round(avg_confidence, 3),
            "result_path": output_path.replace("\\", "/"),

            # Object classification
            "classifications": classifications,
            "total_classified": sum(classifications.values()),

            # Vibration analysis
            "vibration_analysis": vibration_results,

            # Session stats
            "session_stats": session_stats
        }

        return jsonify(result_data)

    except Exception as e:
        app.logger.error(f"Analysis failed: {str(e)}")
        return jsonify({
            "ok": False,
            "error": f"Analysis failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route("/api/session-stats")
def get_session_stats():
    """Get current session statistics"""
    try:
        stats = simple_detector.get_session_stats()
        return jsonify({
            "ok": True,
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/reset-session", methods=["POST"])
def reset_session():
    """Reset session data"""
    try:
        simple_detector.reset_session()
        return jsonify({
            "ok": True,
            "message": "Session reset successfully",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/export-data", methods=["POST"])
def export_session_data():
    """Export session data"""
    try:
        import json

        stats = simple_detector.get_session_stats()
        timestamp = int(time.time())
        filename = f"session_export_{timestamp}.json"
        filepath = os.path.join(EXPORTS_DIR, filename)

        export_data = {
            "export_info": {
                "timestamp": datetime.now().isoformat(),
                "system": "Simple Factory Object Counter",
                "version": "1.0"
            },
            "session_data": stats,
            "count_history": list(simple_detector.count_history),
            "confidence_history": list(simple_detector.confidence_history)
        }

        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)

        return jsonify({
            "ok": True,
            "filename": filename,
            "download_url": f"/download/{filename}",
            "file_size": os.path.getsize(filepath)
        })

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/download/<filename>")
def download_file(filename):
    """Download exported file"""
    try:
        filepath = os.path.join(EXPORTS_DIR, filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, 
                           download_name=filename, mimetype='application/json')
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/system-health")
def system_health():
    """System health check"""
    try:
        stats = simple_detector.get_session_stats()
        return jsonify({
            "status": "optimal",
            "system": "Simple Factory Object Counter",
            "version": "1.0.0",
            "uptime_minutes": stats["session_duration_minutes"],
            "total_images": stats["total_images"],
            "last_check": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    print("=" * 60)
    print("🏭 SIMPLE FACTORY OBJECT COUNTER")
    print("=" * 60)
    print("FEATURES:")
    print("✅ Reliable Object Detection")
    print("✅ Your Physical Vibration Method")
    print("✅ Object Classification (Nuts/Bolts/Screws/Washers)")
    print("✅ Session Statistics & Analytics")
    print("✅ Clean, User-Friendly Interface")
    print("✅ Data Export & Session Management")
    print("=" * 60)
    print("🎯 DESIGNED FOR SIMPLICITY & RELIABILITY")
    print("Access at: http://localhost:5000")
    print("=" * 60)

    app.run(host="0.0.0.0", port=5000, debug=False)
