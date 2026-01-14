# Embedded Device Offline Analysis System

## 1. 项目背景
嵌入式设备长期运行会生成大量日志。
本项目通过离线分析这些日志，提取故障设备的共性特征，并生成健康报告。

## 2. 技术栈
- Python / Pandas：日志生成与分析
- Spark：分布式统计计算
- Hive / Parquet：日志存储
- Matplotlib / Seaborn：可视化报告

## 3. 功能说明
- 生成设备历史运行日志
- 统计故障设备的温度、电压等特征
- 可视化分析结果并生成报告

## 4. 项目结构
embedded-offline-analysis/
├── data/ # 模拟日志
├── scripts/ # 日志生成与分析脚本
├── reports/ # 图表与报告
└── README.md

## 5. 可扩展方向
- 增加更多设备类型
- 使用 Spark SQL / Hive 做更复杂分析
- 结合第一项目实现实时 + 离线综合分析
## 6. 离线分析功能
- 使用 Pandas / Spark 对历史设备日志进行统计分析
- 分析故障设备温度、电压特征
- 生成箱型图可视化结果，输出在 `reports/`
