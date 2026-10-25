# 嵌入式设备离线分析

用历史日志比较故障设备和正常设备，生成健康报告。300 行规模用 Pandas 分析。实时告警仍由边缘到云端监测项目单独处理，这里只读本目录的 CSV。

## 运行

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
MPLBACKEND=Agg .venv/bin/python scripts/generate_logs.py
MPLBACKEND=Agg .venv/bin/python scripts/analyze_logs.py
```

报告在 `reports/health_report.md`。温度图上的 80°C 虚线用来和实时监测对照，不直接当作故障。

## 目录

```text
scripts/generate_logs.py    按隐藏健康状态生成 30 天日志
scripts/analyze_logs.py     对比故障特征并写报告
data/device_logs.csv        生成的日志
reports/                    健康报告和箱型图
```
