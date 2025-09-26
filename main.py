from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SensorData(BaseModel):
    heartRate: int
    spo2: int
    accel_mag: float
    gyro_mag: float

# In-memory list for data storage
data_storage = []

@app.post("/sensor-data/")
async def receive_sensor_data(sensor_data: SensorData):
    data_storage.append(sensor_data.dict())
    return sensor_data

@app.get("/sensor-data/")
async def get_sensor_data():
    return data_storage
