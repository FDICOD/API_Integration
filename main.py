from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SensorData(BaseModel):
    heartRate: int
    spo2: int

data_storage = []  # List to store received sensor data

@app.post("/sensor-data/")
async def receive_sensor_data(sensor_data: SensorData):
    print(f"Heart Rate: {sensor_data.heartRate} bpm, SpO2: {sensor_data.spo2}%")
    data_storage.append(sensor_data)
    return {"message": "Data received", "data": sensor_data}

@app.get("/sensor-data/")
async def get_sensor_data():
    return data_storage
