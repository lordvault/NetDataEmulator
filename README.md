# NetData Emulator

This proyect was created as solution to report from my RPI Zero W 2, the necessary data to be monitored on Home Assistant. The idea its emulate the published data from netdata to reuse the actual netdata integration in home assistant. To achieve this i require a flask server and use a couple of libraries.

## Exposed sensors: 
 - CPU Usage
 - CPU Temperature
 - RAM Total
 - RAM in Use
 - System Uptime

For the code solution, already exist a part implmented by raspberry team:
- [temperature-log](https://projects.raspberrypi.org/en/projects/temperature-log/4)

## Development Tasks: 

- [x] Create the flask service and publish hello world on port 19999 path /api/v1/allmetrics?format=json
- [x] adjust the data to allign the netdata format
- [x] Create an script to install the required python version and libraries.
- [x] Documentate the process on the readme.md file.

## Installation and run

Install the dependencies
```sh
/bin/bash install.sh
```

Run python program:
```sh
python initial.py
```
to run deatached mode:
```sh
nohup python initial.py > output.log 2>&1 &
```


## Home Assistant integration

Use the following configuration on your hass server:
```yml
- platform: netdata
  name: 'zero' # give a name to the sensor.
  host: 192.168.0.XXX #Your zero ip
  scan_interval: 30
  resources:
    core0_freq:
        data_group: 'cpu.cpufreq'
        element: 'cpu0'
        icon: mdi:chip
    sys_network_in:
        data_group: 'net.wlan0'
        element: 'received'
    sys_network_out:
        data_group: 'net.wlan0'
        element: 'sent'
    sys_ram_free:
        data_group: 'system.ram'
        element: 'free'
    sys_ram_used:
        data_group: 'system.ram'
        element: 'used'
    sys_ram_cached:
        data_group: 'system.ram'
        element: 'cached'
    sys_ram_buffers:
        data_group: 'system.ram'
        element: 'buffers'
    sys_cpu_idle_perc:
        data_group: 'system.cpu'
        element: 'idle'
    sys_ram_avail:
        data_group: 'mem.available'
        element: 'MemAvailable'
    sys_temperature:
        data_group: 'sensors.cpu_thermal-virtual-0_temperature'
        element: 'cpu_thermal-virtual-0_temp1'
    sys_uptime:
        data_group: 'system.uptime'
        element: 'uptime'
```