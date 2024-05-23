from gpiozero import CPUTemperature
from time import sleep, strftime, time
from flask import Flask
import json
import psutil
import calendar;
import time;

app = Flask(__name__)
last_time = 0
last_upload = 0
last_download = 0

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

@app.route("/api/v1/allmetrics")
@app.route("/api/v1/allmetrics?format=json&help=no&types=no&timestamps=yes&names=yes&data=average")
def netdata_emulator():
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    
    timestamp = ts

    #CPU 
    cpu0 = Dimension("cpu0", psutil.cpu_freq().current)
    cpu = Sensor("cpu.cpufreq", "MHz", timestamp , {cpu0.name: cpu0.__dict__} )

    #network 
    data_to_upload = 0
    data_to_download = 0
    global last_time, last_download, last_upload
    if(last_time > 0):
        amount_time = timestamp - last_time
        up = psutil.net_io_counters().bytes_sent
        dow = psutil.net_io_counters().bytes_recv
        some_download = psutil.net_io_counters().bytes_recv - last_download
        some_upload = last_upload - psutil.net_io_counters().bytes_sent
        if amount_time > 0 : 
            data_to_download = some_download / amount_time
            data_to_upload = some_upload / amount_time
        else: 
            data_to_download = 0
            data_to_upload = 0
        last_time = timestamp
        last_upload = up
        last_download = dow

    last_time = timestamp

    received = Dimension("received", data_to_download/125)
    sent = Dimension("sent", data_to_upload/125)
    net = Sensor("net.wlan0", "kilobits/s", timestamp, {received.name: received.__dict__, sent.name: sent.__dict__} )

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
    temp = CPUTemperature().temperature
    #temp = 12
    cpu_temp = Dimension("temp1", temp)
    temperature = Sensor("sensors.cpu_thermal-virtual-0_temperature", "Celsius", timestamp, {"cpu_thermal-virtual-0_temp1":cpu_temp.__dict__} )

    #cpu idle:
    idle_dimension = Dimension("idle", 100 - psutil.cpu_percent(2))
    idle = Sensor("system.cpu", "percentage", timestamp, {idle_dimension.name:idle_dimension.__dict__} )

    #uptime

    time_dimension = Dimension("uptime", time.time() - psutil.boot_time())
    uptime = Sensor("system.uptime", "seconds", timestamp, {time_dimension.name:time_dimension.__dict__} )

    return json.dumps({ cpu.name: cpu.__dict__ , net.name: net.__dict__, ram.name:ram.__dict__, mem_avaliable.name: mem_avaliable.__dict__, 
                       temperature.name: temperature.__dict__, uptime.name: uptime.__dict__, idle.name: idle.__dict__})

    
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=19999)

