from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# --- Pydantic Model ---
# heartRate, spo2, accel_mag, and gyro_mag are now required fields.
# accident_detected remains optional, only present during an alert.
class SensorData(BaseModel):
    heartRate: int
    spo2: int
    accel_mag: float
    gyro_mag: float
    accident_detected: Optional[bool] = None

# In-memory list for data storage.
data_storage = []

@app.post("/sensor-data/")
async def receive_sensor_data(sensor_data: SensorData):
    """
    Receives sensor data. Always logs the four primary metrics.
    If 'accident_detected' is true, it prints a special, high-visibility alert.
    """
    # The accident flag triggers the special alert format.
    if sensor_data.accident_detected:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"!!! ACCIDENT ALERT RECEIVED !!!")
        print(f"-> Heart Rate: {sensor_data.heartRate} bpm, SpO2: {sensor_data.spo2}%")
        print(f"-> Impact Accel: {sensor_data.accel_mag:.2f} G")
        print(f"-> Impact Gyro: {sensor_data.gyro_mag:.2f} dps")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        # Standard logging for continuous data stream.
        print(f"Health & IMU Data -> HR: {sensor_data.heartRate}, SpO2: {sensor_data.spo2}, "
              f"Accel: {sensor_data.accel_mag:.2f} G, Gyro: {sensor_data.gyro_mag:.2f} dps")

    # Store the data, excluding 'null' values from the optional fields.
    output_data = sensor_data.dict(exclude_none=True)
    data_storage.append(output_data)
    
    return {"message": "Data received successfully", "data": output_data}

@app.get("/sensor-data/")
async def get_sensor_data():
    """Returns all the sensor data that has been received."""
    return data_storage
