import sqlite3
from flask import current_app, g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception=None):
    db = g.pop("db", None)
    if db: db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        db.executescript("""
        CREATE TABLE IF NOT EXISTS cameras(
          id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,location TEXT NOT NULL,
          latitude REAL,longitude REAL,status TEXT DEFAULT 'ONLINE');

        CREATE TABLE IF NOT EXISTS traffic_data(
          id INTEGER PRIMARY KEY AUTOINCREMENT,camera_id INTEGER,timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
          cars INTEGER DEFAULT 0,bikes INTEGER DEFAULT 0,buses INTEGER DEFAULT 0,trucks INTEGER DEFAULT 0,
          total INTEGER DEFAULT 0,average_speed REAL DEFAULT 0,density REAL DEFAULT 0,congestion TEXT DEFAULT 'LOW');

        CREATE TABLE IF NOT EXISTS signals(
          id INTEGER PRIMARY KEY AUTOINCREMENT,junction TEXT,direction TEXT,
          green_time INTEGER DEFAULT 30,yellow_time INTEGER DEFAULT 5,red_time INTEGER DEFAULT 35,status TEXT DEFAULT 'ACTIVE');

        CREATE TABLE IF NOT EXISTS incidents(
          id INTEGER PRIMARY KEY AUTOINCREMENT,location TEXT,type TEXT,severity TEXT DEFAULT 'MEDIUM',
          confidence REAL DEFAULT 0,status TEXT DEFAULT 'OPEN',description TEXT,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);

        CREATE TABLE IF NOT EXISTS predictions(
          id INTEGER PRIMARY KEY AUTOINCREMENT,location TEXT,prediction_time DATETIME DEFAULT CURRENT_TIMESTAMP,
          predicted_vehicles INTEGER,predicted_congestion TEXT,model TEXT);
        """)
        if db.execute("SELECT COUNT(*) FROM cameras").fetchone()[0] == 0:
            db.executemany("INSERT INTO cameras(name,location,latitude,longitude,status) VALUES(?,?,?,?,?)",[
              ("CAM-01","Junction 1",12.9716,77.5946,"ONLINE"),
              ("CAM-02","Junction 2",12.9784,77.6408,"ONLINE"),
              ("CAM-03","Junction 3",12.9352,77.6245,"ONLINE"),
              ("CAM-04","Junction 4",12.9569,77.7011,"OFFLINE")])
        if db.execute("SELECT COUNT(*) FROM signals").fetchone()[0] == 0:
            db.executemany("INSERT INTO signals(junction,direction,green_time,yellow_time,red_time) VALUES(?,?,?,?,?)",[
              ("Junction 1","North",40,5,35),("Junction 1","South",35,5,40),
              ("Junction 1","East",25,5,50),("Junction 1","West",20,5,55)])
        if db.execute("SELECT COUNT(*) FROM traffic_data").fetchone()[0] == 0:
            db.executemany("""INSERT INTO traffic_data
              (camera_id,cars,bikes,buses,trucks,total,average_speed,density,congestion)
              VALUES(?,?,?,?,?,?,?,?,?)""",[
              (1,55,34,5,3,97,31,48.5,"MEDIUM"),
              (2,82,45,8,7,142,22,71,"HIGH"),
              (3,35,22,3,2,62,39,31,"LOW")])
        db.commit()
    app.teardown_appcontext(close_db)
