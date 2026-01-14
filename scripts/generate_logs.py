import random
import csv
import os
from datetime import datetime, timedelta

# 输出目录
os.makedirs("data", exist_ok=True)
output_file = "data/device_logs.csv"

# 模拟设备
device_types = ["sensorA", "sensorB", "sensorC"]
num_devices = 10
num_days = 30  # 最近30天的日志

start_date = datetime.now() - timedelta(days=num_days)

with open(output_file, mode="w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "device_id", "device_type", "timestamp", "temperature", "voltage", "fault"
    ])
    writer.writeheader()

    for device_num in range(1, num_devices + 1):
        device_id = f"dev-{device_num:03d}"
        device_type = random.choice(device_types)
        for day in range(num_days):
            timestamp = (start_date + timedelta(days=day)).strftime("%Y-%m-%d")
            temperature = round(random.uniform(60, 95), 2)
            voltage = round(random.uniform(3.0, 4.2), 2)
            fault = temperature > 85 or voltage < 3.2  # 简单故障规则
            writer.writerow({
                "device_id": device_id,
                "device_type": device_type,
                "timestamp": timestamp,
                "temperature": temperature,
                "voltage": voltage,
                "fault": fault
            })

print(f"Generated logs at {output_file}")
