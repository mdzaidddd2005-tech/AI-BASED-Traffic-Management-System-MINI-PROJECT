from flask import Blueprint,jsonify
from database import get_db
analytics_bp=Blueprint("analytics",__name__)

@analytics_bp.get("/overview")
def overview():
    rows=get_db().execute("""SELECT timestamp,total,cars,bikes,buses,trucks,average_speed,density,congestion
      FROM traffic_data ORDER BY timestamp DESC LIMIT 50""").fetchall()
    return jsonify([dict(r) for r in reversed(rows)])

@analytics_bp.get("/stats")
def stats():
    r=get_db().execute("""SELECT COUNT(*) records,COALESCE(SUM(total),0) vehicles,
      ROUND(COALESCE(AVG(average_speed),0),2) average_speed,
      ROUND(COALESCE(AVG(density),0),2) average_density FROM traffic_data""").fetchone()
    return jsonify(dict(r))
