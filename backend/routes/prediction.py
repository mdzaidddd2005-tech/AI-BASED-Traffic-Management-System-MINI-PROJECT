from flask import Blueprint,jsonify,request
from database import get_db
prediction_bp=Blueprint("prediction",__name__)

@prediction_bp.get("/forecast")
def forecast():
    x=request.args.get("location","Junction 1")
    db=get_db()
    rows=db.execute("SELECT total FROM traffic_data ORDER BY timestamp DESC LIMIT 10").fetchall()
    vals=[r["total"] for r in rows]
    current=int(sum(vals)/len(vals)) if vals else 0
    # Academic baseline: recent moving average with a rush-hour factor.
    predicted=round(current*1.12)
    congestion="HIGH" if predicted>=120 else "MEDIUM" if predicted>=70 else "LOW"
    db.execute("INSERT INTO predictions(location,predicted_vehicles,predicted_congestion,model) VALUES(?,?,?,?)",
               (x,predicted,congestion,"Moving Average Baseline"))
    db.commit()
    return jsonify({"location":x,"current_average":current,"predicted_vehicles":predicted,
                    "predicted_congestion":congestion,"horizon":"15 minutes","model":"Moving Average Baseline"})
