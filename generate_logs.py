"""Sample network logs banata hai (3 planted problems ke saath)."""
import random
from datetime import datetime, timedelta

random.seed(7)
t = datetime(2026, 10, 5, 9, 0, 0)
devices = ["router-delhi-01", "optical-mumbai-02", "switch-pune-03", "router-chennai-04"]
lines = []

def add(dev, sev, ev, msg):
    global t
    t += timedelta(seconds=random.randint(5, 40))
    lines.append(f"{t:%Y-%m-%d %H:%M:%S} {dev} {sev} {ev} {msg}")

for i in range(120):
    r = random.random()
    d = random.choice(devices)
    if r < 0.6:
        add(d, "INFO", "HEARTBEAT", "status=ok")
    elif r < 0.75:
        add(d, "INFO", "CONFIG-SAVED", "user=admin")
    # Problem 1: link flapping on router-delhi-01
    if i in (20, 24, 28, 33, 40):
        add("router-delhi-01", "ERR", "LINK-DOWN", "interface=Gi0/1 reason=carrier-loss")
        add("router-delhi-01", "INFO", "LINK-UP", "interface=Gi0/1")
    # Problem 2: optical power dropping on optical-mumbai-02
    if i in (30, 50, 70, 90):
        add("optical-mumbai-02", "WARN", "OPTICAL-LOW-POWER",
            f"port=1/1 rx_power={-24 - i/10:.1f}dBm threshold=-25dBm")
    # Problem 3: latency + packet loss on switch-pune-03
    if i in (60, 75, 100):
        add("switch-pune-03", "WARN", "HIGH-LATENCY", f"latency={random.randint(180, 300)}ms")
        add("switch-pune-03", "ERR", "PACKET-LOSS", f"loss={random.uniform(3, 9):.1f}% interface=Eth1/4")

open("sample_logs/network.log", "w").write("\n".join(lines) + "\n")
print(f"{len(lines)} log lines likhe -> sample_logs/network.log")
