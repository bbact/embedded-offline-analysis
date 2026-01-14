import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# 读取日志
df = pd.read_csv("data/device_logs.csv")

# 将故障和非故障设备分开
faulty = df[df["fault"] == True]
normal = df[df["fault"] == False]

# 按设备类型统计温度和电压均值
summary = faulty.groupby("device_type")[["temperature", "voltage"]].mean().reset_index()
print("Faulty devices summary:")
print(summary)

# 可视化
os.makedirs("reports", exist_ok=True)
plt.figure(figsize=(8,6))
sns.boxplot(x="device_type", y="temperature", data=df)
plt.title("Temperature Distribution by Device Type")
plt.savefig("reports/temperature_boxplot.png")
plt.close()

plt.figure(figsize=(8,6))
sns.boxplot(x="device_type", y="voltage", data=df)
plt.title("Voltage Distribution by Device Type")
plt.savefig("reports/voltage_boxplot.png")
plt.close()

print("Analysis complete. Boxplots saved in reports/")
