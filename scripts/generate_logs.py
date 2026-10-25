import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "device_logs.csv"
NUM_DAYS = 30
RANDOM_SEED = 20261025

# sensorC 更容易不健康，用来让故障率在类型之间拉开。
DEVICE_PLAN = [
    ("dev-001", "sensorA", False),
    ("dev-002", "sensorA", False),
    ("dev-003", "sensorA", False),
    ("dev-004", "sensorA", True),
    ("dev-005", "sensorB", False),
    ("dev-006", "sensorB", False),
    ("dev-007", "sensorB", True),
    ("dev-008", "sensorC", True),
    ("dev-009", "sensorC", True),
    ("dev-010", "sensorC", False),
]


def clamp(value, low, high):
    return min(max(value, low), high)


def reading(unhealthy, offline_streak):
    if unhealthy:
        temperature = random.gauss(86, 3.5)
        voltage = random.gauss(3.25, 0.1)
        humidity = random.gauss(72, 6)
        offline_hours = 3 + offline_streak * 1.4 + random.random()
    else:
        temperature = random.gauss(68, 3.5)
        voltage = random.gauss(3.9, 0.08)
        humidity = random.gauss(46, 5)
        offline_hours = random.random() * 0.6
    return {
        "temperature": round(clamp(temperature, 40, 110), 2),
        "voltage": round(clamp(voltage, 2.5, 5.0), 2),
        "humidity": round(clamp(humidity, 10, 95), 1),
        "offline_hours": round(clamp(offline_hours, 0, 24), 1),
    }


def fault_label(unhealthy):
    """Follow the hidden health state, then flip a small share of days."""
    fault = unhealthy
    if random.random() < 0.08:
        fault = not fault
    return fault


def main():
    random.seed(RANDOM_SEED)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=NUM_DAYS)
    fieldnames = [
        "device_id",
        "device_type",
        "timestamp",
        "temperature",
        "voltage",
        "humidity",
        "offline_hours",
        "fault",
    ]
    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for device_id, device_type, unhealthy in DEVICE_PLAN:
            offline_streak = 0
            for day in range(NUM_DAYS):
                if unhealthy and random.random() < 0.6:
                    offline_streak += 1
                else:
                    offline_streak = 0
                row = reading(unhealthy, offline_streak)
                row.update({
                    "device_id": device_id,
                    "device_type": device_type,
                    "timestamp": (start + timedelta(days=day)).strftime("%Y-%m-%d"),
                    "fault": fault_label(unhealthy),
                })
                writer.writerow(row)
    print(f"Generated logs at {OUTPUT}")


if __name__ == "__main__":
    main()
