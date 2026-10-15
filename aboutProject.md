# Network Log Analysis

## About the Project

In this project, I have worked on understanding network logs and identifying problems in a network using log messages.

Network devices like routers, switches, and optical devices generate logs to record their activities. These logs help us understand whether a device is working properly or facing any problem.

For example, if a router loses its connection, a switch experiences packet loss, or an optical device receives a weak signal, these problems can be identified by reading the logs.

My main goal is to understand these logs in a simple way and identify which device needs attention.

## What is a Network Log?

A network log is a record of activities happening on a network device.

It contains information such as the date, time, device name, message type, and details about an event.

For example:

```text
2026-10-05 09:08:23 router-delhi-01 ERR LINK-DOWN interface=Gi0/1 reason=carrier-loss
```

This log tells us that the Delhi router lost its connection on the `Gi0/1` interface at 09:08:23.

## Types of Log Messages

I have studied three common types of log messages:

- **INFO:** Shows normal activities or status updates.
- **WARN:** Shows a warning that may need attention.
- **ERR:** Shows an error or a problem that needs investigation.

For example:

```text
INFO HEARTBEAT status=ok
WARN HIGH-LATENCY latency=246ms
ERR PACKET-LOSS loss=8.4% interface=Eth1/4
```

## Important Events in Network Logs

### 1. HEARTBEAT

A heartbeat message helps us check whether a device is responding normally.

Example:

```text
INFO HEARTBEAT status=ok
```

It indicates that the device is reporting its status as okay. However, it does not guarantee that every connection on the device is working properly.

### 2. CONFIG-SAVED

This message indicates that a device's configuration has been saved.

Example:

```text
INFO CONFIG-SAVED user=admin
```

It can help us track configuration-related activities on a device.

### 3. LINK-DOWN and LINK-UP

These messages show when a network connection goes down and comes back up.

Example:

```text
ERR LINK-DOWN interface=Gi0/1 reason=carrier-loss
INFO LINK-UP interface=Gi0/1
```

If the same connection repeatedly goes down and comes back up, it is called link flapping.

Possible reasons include a loose cable, a faulty port, or a problem with the connected device.

### 4. OPTICAL-LOW-POWER

This warning is related to the signal received through a fiber-optic connection.

Example:

```text
WARN OPTICAL-LOW-POWER port=1/1 rx_power=-27.0dBm threshold=-25dBm
```

It indicates that the received signal power is below the configured warning threshold.

A weak signal can be caused by a damaged fiber, a dirty connector, or a problem with the optical device.

### 5. HIGH-LATENCY

Latency means the time taken for data to travel between two points in a network.

Example:

```text
WARN HIGH-LATENCY latency=246ms
```

High latency can make activities like online gaming, video calls, and other real-time applications slow or unresponsive.

### 6. PACKET-LOSS

Packet loss occurs when some of the data packets sent through a network do not reach their destination.

Example:

```text
ERR PACKET-LOSS loss=8.4% interface=Eth1/4
```

If 1,000 packets are sent and 84 packets are lost, the packet loss is 8.4%.

Packet loss can affect network performance and may cause interruptions in communication.

## Analysis of the Given Logs

After studying the provided logs, I identified the following problems:

### 1. Delhi Router

The `router-delhi-01` device repeatedly reported LINK-DOWN and LINK-UP events on interface `Gi0/1`.

This shows that the connection was repeatedly going down and coming back up. The cable, port, and connected device may need to be checked.

### 2. Pune Switch

The `switch-pune-03` device reported high latency and packet loss on interface `Eth1/4`.

This indicates possible network performance issues that need further investigation.

### 3. Mumbai Optical Device

The `optical-mumbai-02` device reported low optical signal power multiple times.

The received signal power changed from `-27 dBm` to `-33 dBm`, showing that the reported signal was becoming weaker.

The fiber connection and optical device should be checked.

### 4. Chennai Router

The `router-chennai-04` device mainly reported heartbeat and configuration-save messages in the provided logs.

No explicit error is shown for this device in the given data.

## What I Learned

While studying these logs, I learned:

- How to read and understand network log messages.
- How to identify normal activities, warnings, and errors.
- How to understand LINK-DOWN and LINK-UP events.
- How to identify high latency and packet loss.
- How to understand low signal power in fiber-optic connections.
- How repeated log messages can help identify possible network problems.
- Why we need to investigate the cause before deciding that a particular component is faulty.

## Conclusion

This analysis helped me understand how network logs can be used to identify problems in routers, switches, and optical devices.

By checking the device name, time, and event details, we can identify which devices need attention and what should be investigated.

Network log analysis is useful for troubleshooting problems, understanding network performance, and maintaining a reliable network.

The exact cause of a problem cannot always be confirmed from a single log message, so further checks may be required.