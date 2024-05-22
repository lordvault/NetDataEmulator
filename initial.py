from gpiozero import CPUTemperature
from time import sleep, strftime, time
from flask import Flask
import json
import psutil
import calendar;
import time;

app = Flask(__name__)

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

class Dimension:
    name = ""
    value = 0

    def __init__(self, name, value):
        self.name = name
        self.value = value

@app.route("/")
def netdata_emulator():
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    
    timestamp = ts

    #CPU 
    cpu0 = Dimension("cpu0", psutil.cpu_freq().current)
    cpu = Sensor("cpu.cpufreq", "MHz", timestamp , {cpu0.name: cpu0.__dict__} )

    #network 
    received = Dimension("received", psutil.net_io_counters().bytes_recv/125)
    sent = Dimension("sent", psutil.net_io_counters().bytes_sent/125)
    net = Sensor("net.wlan", "kilobits/s", timestamp, {received.name: received.__dict__, sent.name: sent.__dict__} )

    #memory     
    free = Dimension("free", psutil.virtual_memory().free/1048576)
    used = Dimension("used", psutil.virtual_memory().used/1048576)
    cached = Dimension("cached", psutil.virtual_memory().cached/1048576)
    buffers = Dimension("buffers", psutil.virtual_memory().buffers/1048576)
    ram = Sensor("system.ram", "MiB", timestamp, {free.name: free.__dict__, used.name: used.__dict__, cached.name: cached.__dict__, buffers.name: buffers.__dict__} )

    #mem available
    
    available = Dimension("avail", psutil.virtual_memory().available/1048576)
    mem_avaliable = Sensor("mem.available", "MiB", timestamp, {"MemAvailable":available.__dict__} )

    #temperature
    cpu = CPUTemperature()
    temp = cpu.temperature
    cpu_temp = Dimension("temp1", temp)
    temperature = Sensor("sensors.cpu_thermal-virtual-0_temperature", "Celsius", timestamp, {"cpu_thermal-virtual-0_temp1":available.__dict__} )

    return json.dumps({ cpu.name: cpu.__dict__ , net.name: net.__dict__, ram.name:ram.__dict__, mem_avaliable.name: mem_avaliable.__dict__})

    
if __name__ == "__main__":
    app.run(debug=False, host='localhost', port=19999)

