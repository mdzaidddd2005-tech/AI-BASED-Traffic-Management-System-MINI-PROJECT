from flask import Blueprint,jsonify,request
from werkzeug.utils import secure_filename
from pathlib import Path
from ai.vehicle_detection import detect_vehicles
detection_bp=Blueprint("detection",__name__)
UPLOAD=Path("uploads"); UPLOAD.mkdir(exist_ok=True)

@detection_bp.post("/image")
def image():
    if "image" not in request.files:return jsonify({"error":"Use multipart field 'image'"}),400
    f=request.files["image"]
    if not f.filename:return jsonify({"error":"No file selected"}),400
    name=secure_filename(f.filename); path=UPLOAD/name; f.save(path)
    result=detect_vehicles(str(path)); result["filename"]=name
    return jsonify(result)
