from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# --- Pydantic Models for Data Validation ---
class SensorData(BaseModel):
    heartRate: int
    spo2: int

class AlertData(BaseModel):
    status: str
    message: str

# --- FastAPI App ---
app = FastAPI()

# --- API Endpoints ---
@app.post("/sensor-data/")
async def receive_sensor_data(data: SensorData):
    """Handles periodic health data from the ESP32."""
    print(f"HEALTH DATA -> Heart Rate: {data.heartRate} bpm, SpO2: {data.spo2}%")
    return {"status": "success", "data_received": data}

# NEW ENDPOINT for accident alerts
@app.post("/accident-alert/")
async def receive_accident_alert(data: AlertData):
    """Handles immediate accident alerts from the ESP32."""
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"ALERT RECEIVED -> Status: {data.status}, Message: {data.message}")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # Add logic here to send an email, SMS, or trigger another action
    return {"status": "alert_acknowledged", "alert_received": data}

@app.get("/")
def root():
    return {"message": "Server is running."}

# --- Run the Server ---
if _name_ == "_main_":
    uvicorn.run(app, host="0.0.0.0", port=8000)
