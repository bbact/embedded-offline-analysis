from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "device_logs.csv"
REPORTS = ROOT / "reports"
TEMP_CHART = REPORTS / "temperature_boxplot.png"
VOLT_CHART = REPORTS / "voltage_boxplot.png"
REPORT = REPORTS / "health_report.md"
TEMPERATURE_LINE = 80


def longest_fault_streak(flags):
    best = current = 0
    for flag in flags:
        if flag:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def load_logs():
    frame = pd.read_csv(DATA)
    frame["fault"] = frame["fault"].astype(str).str.lower().isin(["true", "1"])
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    return frame.sort_values(["device_id", "timestamp"])


def comparison(frame):
    grouped = frame.groupby("fault")[["temperature", "voltage"]].mean()
    faulty = grouped.loc[True]
    normal = grouped.loc[False]
    return {
        "fault_temperature": faulty["temperature"],
        "normal_temperature": normal["temperature"],
        "temperature_gap": faulty["temperature"] - normal["temperature"],
        "fault_voltage": faulty["voltage"],
        "normal_voltage": normal["voltage"],
        "voltage_gap": faulty["voltage"] - normal["voltage"],
    }


def fault_rates(frame):
    rates = (
        frame.groupby("device_type")["fault"]
        .mean()
        .sort_values(ascending=False)
    )
    return rates


def device_streaks(frame):
    rows = []
    for device_id, group in frame.groupby("device_id"):
        ordered = group.sort_values("timestamp")
        rows.append({
            "device_id": device_id,
            "device_type": ordered["device_type"].iloc[0],
            "streak": longest_fault_streak(ordered["fault"].tolist()),
            "offline_hours": ordered["offline_hours"].sum(),
        })
    return pd.DataFrame(rows).sort_values(
        ["streak", "offline_hours"], ascending=False
    )


def save_charts(frame):
    REPORTS.mkdir(parents=True, exist_ok=True)
    plt.rcParams["font.sans-serif"] = ["PingFang SC", "Arial Unicode MS", "Heiti SC"]
    plt.rcParams["axes.unicode_minus"] = False
    labeled = frame.assign(状态=frame["fault"].map({True: "故障", False: "正常"}))

    plt.figure(figsize=(8, 6))
    sns.boxplot(x="状态", y="temperature", data=labeled, order=["正常", "故障"])
    plt.axhline(TEMPERATURE_LINE, color="#c4554d", linestyle="--", label="80°C")
    plt.legend()
    plt.ylabel("温度 (°C)", rotation=0, labelpad=36, ha="right")
    plt.xlabel("")
    plt.title("故障与正常设备的温度分布")
    plt.tight_layout()
    plt.savefig(TEMP_CHART)
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.boxplot(x="状态", y="voltage", data=labeled, order=["正常", "故障"])
    plt.ylabel("电压 (V)", rotation=0, labelpad=32, ha="right")
    plt.xlabel("")
    plt.title("故障与正常设备的电压分布")
    plt.tight_layout()
    plt.savefig(VOLT_CHART)
    plt.close()


def write_report(frame, stats, rates, streaks):
    top_type = rates.index[0]
    leader = streaks.iloc[0]
    lines = [
        "# 设备健康报告",
        "",
        f"共 {len(frame)} 条日志，覆盖 {frame['device_id'].nunique()} 台设备、{frame['timestamp'].nunique()} 天。温度超过 80°C 只作为和实时监测对照的观察线，不直接记为故障。",
        "",
        "## 故障和正常设备差多少",
        "",
        f"- 故障设备平均温度 {stats['fault_temperature']:.1f}°C，正常设备 {stats['normal_temperature']:.1f}°C，相差 {stats['temperature_gap']:.1f}°C。",
        f"- 故障设备平均电压 {stats['fault_voltage']:.2f}V，正常设备 {stats['normal_voltage']:.2f}V，相差 {stats['voltage_gap']:.2f}V。",
        "",
        "## 哪类设备故障率更高",
        "",
    ]
    for device_type, rate in rates.items():
        lines.append(f"- {device_type}：{rate:.1%}")
    lines.extend([
        "",
        f"{top_type} 的故障率最高。",
        "",
        "## 连续故障和离线",
        "",
        f"{leader['device_id']}（{leader['device_type']}）连续故障 {int(leader['streak'])} 天，累计离线 {leader['offline_hours']:.1f} 小时，是连续故障最长的设备。",
        "",
        "| 设备 | 类型 | 最长连续故障天数 | 累计离线小时 |",
        "| --- | --- | --- | --- |",
    ])
    for row in streaks.itertuples(index=False):
        lines.append(
            f"| {row.device_id} | {row.device_type} | {int(row.streak)} | {row.offline_hours:.1f} |"
        )
    lines.extend([
        "",
        "## 图表",
        "",
        "![温度分布](temperature_boxplot.png)",
        "",
        "![电压分布](voltage_boxplot.png)",
        "",
    ])
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main():
    frame = load_logs()
    stats = comparison(frame)
    rates = fault_rates(frame)
    streaks = device_streaks(frame)
    save_charts(frame)
    write_report(frame, stats, rates, streaks)
    print(f"Report written to {REPORT}")


if __name__ == "__main__":
    main()
