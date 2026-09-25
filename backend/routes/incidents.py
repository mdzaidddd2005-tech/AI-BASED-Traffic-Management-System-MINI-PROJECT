from flask import Blueprint,jsonify,request
from database import get_db
incidents_bp=Blueprint("incidents",__name__)

@incidents_bp.get("")
def get():
    return jsonify([dict(r) for r in get_db().execute("SELECT * FROM incidents ORDER BY timestamp DESC").fetchall()])

@incidents_bp.post("")
def create():
    x=request.get_json(force=True); db=get_db()
    cur=db.execute("""INSERT INTO incidents(location,type,severity,confidence,status,description)
      VALUES(?,?,?,?,?,?)""",(x.get("location","Unknown"),x.get("type","Unknown"),x.get("severity","MEDIUM"),
      float(x.get("confidence",0)), "OPEN",x.get("description","")))
    db.commit(); return jsonify({"id":cur.lastrowid,"status":"OPEN"}),201

@incidents_bp.patch("/<int:iid>")
def update(iid):
    status=(request.get_json(force=True)).get("status")
    if status not in ["OPEN","CONFIRMED","RESOLVED","DISMISSED"]:return jsonify({"error":"Invalid status"}),400
    db=get_db(); cur=db.execute("UPDATE incidents SET status=? WHERE id=?",(status,iid)); db.commit()
    return (jsonify({"message":"Incident updated"}) if cur.rowcount else (jsonify({"error":"Not found"}),404))
