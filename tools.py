"""Agent ke tools: logs parse, anomalies detect, device status, ping (simulated)."""
import re
import random
from collections import Counter, defaultdict

LOG_FILE = "sample_logs/network.log"
PATTERN = re.compile(r"^(\S+ \S+) (\S+) (\w+) (\S+) ?(.*)$")


def _load():
    events = []
    with open(LOG_FILE) as f:
        for line in f:
            m = PATTERN.match(line.strip())
            if m:
                ts, dev, sev, ev, msg = m.groups()
                events.append(dict(time=ts, device=dev, severity=sev, event=ev, message=msg))
    return events


def parse_logs(severity: str = "", device: str = "", limit: int = 10):
    events = _load()
    if severity:
        events = [e for e in events if e["severity"] == severity.upper()]
    if device:
        events = [e for e in events if e["device"] == device]
    return {
        "total_matched": len(events),
        "severity_counts": dict(Counter(e["severity"] for e in events)),
        "latest_events": events[-limit:],
    }


def find_anomalies():
    events = _load()
    found = []
    flaps = Counter((e["device"], e["message"].split()[0]) for e in events if e["event"] == "LINK-DOWN")
    for (dev, iface), n in flaps.items():
        if n >= 3:
            found.append({"device": dev, "type": "LINK_FLAPPING", "detail": f"{iface} down {n} times"})
    for e in events:
        if e["event"] == "OPTICAL-LOW-POWER":
            pw = float(re.search(r"rx_power=(-?[\d.]+)", e["message"]).group(1))
            if pw < -25:
                found.append({"device": e["device"], "type": "OPTICAL_POWER_LOW",
                              "detail": f"rx_power {pw} dBm at {e['time']}"})
        if e["event"] == "HIGH-LATENCY":
            found.append({"device": e["device"], "type": "HIGH_LATENCY", "detail": f"{e['message']} at {e['time']}"})
        if e["event"] == "PACKET-LOSS":
            found.append({"device": e["device"], "type": "PACKET_LOSS", "detail": f"{e['message']} at {e['time']}"})
    return {"anomaly_count": len(found), "anomalies": found}


def get_device_status(device: str):
    events = [e for e in _load() if e["device"] == device]
    if not events:
        return {"error": f"device '{device}' logs me nahi mila"}
    bad = [e for e in events if e["severity"] in ("ERR", "WARN", "CRIT")]
    return {
        "device": device,
        "status": "DEGRADED" if bad else "HEALTHY",
        "warn_err_count": len(bad),
        "last_event": events[-1],
    }


def ping_host(host: str):
    """Simulated ping (real network pe depend nahi karta, demo ke liye safe)."""
    rnd = random.Random(host)
    bad = any(k in host for k in ("pune", "delhi"))
    return {"host": host, "avg_latency_ms": rnd.randint(150, 260) if bad else rnd.randint(5, 40),
            "packet_loss_pct": rnd.randint(3, 8) if bad else 0}


FUNCS = {f.__name__: f for f in (parse_logs, find_anomalies, get_device_status, ping_host)}


def _tool(name, desc, props=None, required=None):
    return {"type": "function", "function": {"name": name, "description": desc,
            "parameters": {"type": "object", "properties": props or {}, "required": required or []}}}


TOOL_SCHEMAS = [
    _tool("parse_logs", "Logs filter karke summary + latest events deta hai.",
          {"severity": {"type": "string", "description": "INFO, WARN ya ERR"},
           "device": {"type": "string"}, "limit": {"type": "integer"}}),
    _tool("find_anomalies", "Saare logs scan karke link flapping, low optical power, latency, packet loss detect karta hai."),
    _tool("get_device_status", "Ek device ka health status deta hai.",
          {"device": {"type": "string"}}, ["device"]),
    _tool("ping_host", "Host ko ping karke latency aur packet loss deta hai.",
          {"host": {"type": "string"}}, ["host"]),
]
