from flask import Blueprint,jsonify,request
from database import get_db
traffic_bp=Blueprint("traffic",__name__)

def level(d):
    return "HIGH" if d>=70 else "MEDIUM" if d>=40 else "LOW"

@traffic_bp.get("/current")
def current():
    rows=get_db().execute("""SELECT t.*,c.name camera_name,c.location FROM traffic_data t
      LEFT JOIN cameras c ON c.id=t.camera_id ORDER BY t.timestamp DESC""").fetchall()
    return jsonify([dict(r) for r in rows])

@traffic_bp.get("/cameras")
def cameras():
    return jsonify([dict(r) for r in get_db().execute("SELECT * FROM cameras").fetchall()])

@traffic_bp.get("/summary")
def summary():
    r=get_db().execute("""SELECT COALESCE(SUM(total),0) total,COALESCE(AVG(average_speed),0) average_speed,
      COALESCE(AVG(density),0) density,COALESCE(SUM(cars),0) cars,COALESCE(SUM(bikes),0) bikes,
      COALESCE(SUM(buses),0) buses,COALESCE(SUM(trucks),0) trucks FROM traffic_data""").fetchone()
    d=dict(r); d["congestion"]=level(d["density"]); return jsonify(d)

@traffic_bp.post("/record")
def record():
    x=request.get_json(force=True)
    cars=int(x.get("cars",0)); bikes=int(x.get("bikes",0)); buses=int(x.get("buses",0)); trucks=int(x.get("trucks",0))
    total=cars+bikes+buses+trucks
    capacity=max(int(x.get("road_capacity",200)),1)
    density=min(100,round(total/capacity*100,2))
    db=get_db(); cur=db.execute("""INSERT INTO traffic_data
      (camera_id,cars,bikes,buses,trucks,total,average_speed,density,congestion)
      VALUES(?,?,?,?,?,?,?,?,?)""",(x.get("camera_id"),cars,bikes,buses,trucks,total,float(x.get("average_speed",0)),density,level(density)))
    db.commit()
    return jsonify({"id":cur.lastrowid,"total":total,"density":density,"congestion":level(density)}),201
