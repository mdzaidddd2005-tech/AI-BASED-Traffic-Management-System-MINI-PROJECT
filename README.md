# AI-Powered Urban Traffic Management and Mobility Optimization System

## Complete academic project

### Modules
1. Interactive traffic dashboard
2. Live traffic data
3. AI vehicle detection using YOLO
4. Traffic-density calculation
5. Congestion classification
6. 15-minute traffic prediction
7. AI-assisted traffic signal optimization
8. Incident reporting and resolution
9. Traffic analytics
10. Map visualization
11. Route optimization simulation
12. REST backend and SQLite database

## Setup

### 1. Backend
Open terminal in `backend`:

Windows:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend:
`http://127.0.0.1:5000`

### 2. Frontend
Open another terminal in `frontend`:

```
python -m http.server 5500
```

Open:
`http://127.0.0.1:5500`

### 3. YOLO
For actual detection, place a compatible Ultralytics YOLO model such as `yolov8n.pt` inside `backend/`.
If the model is absent, the API uses clearly marked demo mode so the rest of the system can be tested.

## Architecture

Camera/Image -> YOLO -> Vehicle Count -> Density -> Congestion -> Prediction -> Signal Recommendation -> Dashboard

## Important academic note
Signal control and route optimization are simulations for the project. The system does not directly control real-world traffic infrastructure.
