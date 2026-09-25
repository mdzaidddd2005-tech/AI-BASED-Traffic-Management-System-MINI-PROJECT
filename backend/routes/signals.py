from flask import Blueprint,jsonify,request
from database import get_db
signals_bp=Blueprint("signals",__name__)

@signals_bp.get("")
def get():
    return jsonify([dict(r) for r in get_db().execute("SELECT * FROM signals ORDER BY junction,id").fetchall()])

@signals_bp.post("/optimize")
def optimize():
    x=request.get_json(silent=True) or {}; junction=x.get("junction","Junction 1")
    db=get_db(); rows=db.execute("SELECT * FROM signals WHERE junction=?",(junction,)).fetchall()
    if not rows:return jsonify({"error":"Junction not found"}),404
    density=float(db.execute("SELECT COALESCE(AVG(density),0) d FROM traffic_data").fetchone()["d"])
    mult=1.5 if density>=70 else 1.2 if density>=40 else .9
    rec=[{"id":r["id"],"direction":r["direction"],"old_green_time":r["green_time"],
          "recommended_green_time":max(15,min(90,round(r["green_time"]*mult)))} for r in rows]
    return jsonify({"junction":junction,"traffic_density":round(density,2),
                    "method":"AI-assisted density-based simulation","recommendations":rec})

@signals_bp.post("/apply")
def apply():
    x=request.get_json(force=True); sid=int(x["signal_id"]); green=max(10,min(120,int(x["green_time"])))
    db=get_db(); cur=db.execute("UPDATE signals SET green_time=? WHERE id=?",(green,sid)); db.commit()
    if not cur.rowcount:return jsonify({"error":"Signal not found"}),404
    return jsonify({"message":"Simulation timing updated","signal_id":sid,"green_time":green})
