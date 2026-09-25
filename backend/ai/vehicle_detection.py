from pathlib import Path

def detect_vehicles(image_path):
    try:
        from ultralytics import YOLO
        model_path=Path("yolov8n.pt")
        if not model_path.exists(): raise FileNotFoundError("yolov8n.pt not found; using demo mode")
        model=YOLO(str(model_path)); results=model(image_path,verbose=False)
        names=results[0].names
        mapping={"car":"cars","motorcycle":"bikes","bus":"buses","truck":"trucks"}
        c={"cars":0,"bikes":0,"buses":0,"trucks":0}; conf=0; n=0
        for b in results[0].boxes:
            label=names[int(b.cls[0])].lower()
            if label in mapping:
                c[mapping[label]]+=1; conf+=float(b.conf[0]); n+=1
        total=sum(c.values()); density=min(100,round(total/2,2))
        level="HIGH" if density>=70 else "MEDIUM" if density>=40 else "LOW"
        return {**c,"total":total,"density":density,"congestion":level,
                "average_confidence":round(conf/n,3) if n else 0,"mode":"YOLO"}
    except Exception as e:
        return {"cars":52,"bikes":31,"buses":4,"trucks":6,"total":93,"density":46.5,
                "congestion":"MEDIUM","average_confidence":0,"mode":"DEMO","note":str(e)}
