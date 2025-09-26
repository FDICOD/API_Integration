from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# 1. Updated Pydantic Model
# Added 'gyro_mag' and 'accel_mag', which can be floats or None (null).
# They will hold sensor magnitudes during an accident event.
class SensorData(BaseModel):
    heartRate: int
    spo2: int
    accident_detected: Optional[bool] = None
    gyro_mag: Optional[float] = None
    accel_mag: Optional[float] = None

# In-memory list to store received sensor data.
# For a real project, you'd use a database.
data_storage = []

@app.post("/sensor-data/")
async def receive_sensor_data(sensor_data: SensorData):
    """
    Receives sensor data. If 'accident_detected' is true,
    it prints a special alert including gyroscope and accelerometer magnitude.
    """
    if sensor_data.accident_detected:
        # 2. Handle the accident flag when present
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"!!! ACCIDENT ALERT RECEIVED !!!")
        print(f"Heart Rate: {sensor_data.heartRate} bpm, SpO2: {sensor_data.spo2}%")
        # Also print the gyro magnitude if it was sent
        if sensor_data.gyro_mag is not None:
            print(f"Gyroscope Magnitude: {sensor_data.gyro_mag:.2f} dps")
        # Also print the accel magnitude if it was sent
        if sensor_data.accel_mag is not None:
            print(f"Acceleration Magnitude: {sensor_data.accel_mag:.2f} G")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        # Normal data logging
        print(f"Health Data -> Heart Rate: {sensor_data.heartRate} bpm, SpO2: {sensor_data.spO2}%")

    data_storage.append(sensor_data.dict())
    return {"message": "Data received successfully", "data": sensor_data}

@app.get("/sensor-data/")
async def get_sensor_data():
    """Returns all the sensor data that has been received."""
    return data_storage
