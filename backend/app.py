from flask import Flask, jsonify
from flask_cors import CORS
from database import init_db
from routes.traffic import traffic_bp
from routes.signals import signals_bp
from routes.incidents import incidents_bp
from routes.analytics import analytics_bp
from routes.detection import detection_bp
from routes.prediction import prediction_bp

app = Flask(__name__)
CORS(app)
app.config["DATABASE"] = "traffic.db"
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

init_db(app)

app.register_blueprint(traffic_bp, url_prefix="/api/traffic")
app.register_blueprint(signals_bp, url_prefix="/api/signals")
app.register_blueprint(incidents_bp, url_prefix="/api/incidents")
app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
app.register_blueprint(detection_bp, url_prefix="/api/detection")
app.register_blueprint(prediction_bp, url_prefix="/api/prediction")

@app.get("/")
def home():
    return jsonify({"project":"AI-Powered Urban Traffic Management and Mobility Optimization System","status":"running"})

@app.get("/api/health")
def health():
    return jsonify({"status":"healthy","database":"connected"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
