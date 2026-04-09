import time
from flask import Flask
import json
import psutil
import calendar

app = Flask(__name__)
net_state = {}

class Sensor:    
    name = ''
    units = ''
    last_updated = 0
    dimensions = {}

    def __init__(self, name, units, last_updated, dimensions):
        self.name = name
        self.units = units
        self.last_updated = last_updated
        self.dimensions = dimensions

@app.route("/api/v1/allmetrics")
@app.route("/api/v1/allmetrics?format=json&help=no&types=no&timestamps=yes&names=yes&data=average")
def netdata_emulator():
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    
    timestamp = ts
    sensors = []

    sensors.extend(cpu_sensors(timestamp))
    sensors.append(net_sensor(timestamp))
    sensors.extend(system_ram_sensor(timestamp))
    sensors.append(get_cpu_temp(timestamp))
    sensors.append(get_uptime(timestamp))

    return json.dumps({sensor.name: sensor.__dict__ for sensor in sensors})

def cpu_sensors(timestamp):
    cpu0_freq = psutil.cpu_freq().current
    cpu = Sensor("cpu.cpufreq", "MHz", timestamp, {"cpu0": {"name": "cpu0", "value": cpu0_freq}})
    idle = Sensor("system.cpu", "percentage", timestamp, {"idle": {"name": "idle", "value": 100 - psutil.cpu_percent(2)}})
    return cpu, idle

def net_sensor(timestamp, interface="default"):
    global net_state

    net_io_per_nic = psutil.net_io_counters(pernic=True)

    if interface == "default":
        interface = next((nic for nic in ["eth0", "wlan0"] if nic in net_io_per_nic), None)
        if interface is None and net_io_per_nic:
            interface = next(iter(net_io_per_nic))

    if interface is None or interface not in net_io_per_nic:
        return Sensor("net.unknown", "Mbps/s", timestamp, {})

    current_up = net_io_per_nic[interface].bytes_sent
    current_dow = net_io_per_nic[interface].bytes_recv

    state = net_state.get(interface, {"last_time": 0, "last_upload": 0, "last_download": 0})

    data_to_download = 0
    data_to_upload = 0

    if state["last_time"] > 0:
        amount_time = timestamp - state["last_time"]
        if amount_time > 0:
            data_to_download = (current_dow - state["last_download"]) / amount_time
            data_to_upload = (current_up - state["last_upload"]) / amount_time
        state["last_upload"] = current_up
        state["last_download"] = current_dow
    state["last_time"] = timestamp

    net_state[interface] = state
    
    return Sensor(f"net.{interface}", "Mbps/s", timestamp, {
        "received": {"name": "received", "value": data_to_download / 125000},
        "sent": {"name": "sent", "value": data_to_upload / 125000}
    })

def system_ram_sensor(timestamp):
    vm = psutil.virtual_memory()
    ram = Sensor("system.ram", "MiB", timestamp, {
        "free": {"name": "free", "value": vm.free / 1048576},
        "used": {"name": "used", "value": vm.used / 1048576},
        "cached": {"name": "cached", "value": vm.cached / 1048576},
        "buffers": {"name": "buffers", "value": vm.buffers / 1048576}
    })

    mem_available = Sensor("mem.available", "MiB", timestamp, {"MemAvailable": {"name": "avail", "value": vm.available / 1048576}})

    return ram, mem_available

def get_cpu_temp(timestamp):
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = float(f.read()) / 1000
    return Sensor("sensors.cpu_thermal-virtual-0_temperature", "Celsius", timestamp, {"cpu_thermal-virtual-0_temp1": {"name": "temp1", "value": temp}})

def get_uptime(timestamp):
    uptime = time.time() - psutil.boot_time()
    return Sensor("system.uptime", "seconds", timestamp, {"uptime": {"name": "uptime", "value": uptime}})
    
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=19999)
