# NetData Emulator

The project was updated and now works for all hardwarde running linux (debian based). The idea its emulate the published data from netdata to reuse the actual netdata integration in home assistant. To achieve this i require a flask server and use a couple of libraries. 

Why? Because netdata consumes lot of resources and cpu, obviously netdata generates a lot of data, and create a database with the historic data, but i dont require it, i just need pure data to monitor on HomeAssistant, without generate a big impact over my hardware devices.

## Exposed sensors: 
 - CPU Usage
 - CPU Temperature (/sys/class/thermal/thermal_zone0/temp) (validate it, sometimes thermal_zone0 doesnt exists but 1 or 2 exist)
 - RAM Total
 - RAM in Use
 - System Uptime
 - Network speed (calculated)

For the code solution, already exist a part implmented by raspberry team:
- [temperature-log](https://projects.raspberrypi.org/en/projects/temperature-log/4)

## Development Tasks: 

- [x] Create the flask service and publish hello world on port 19999 path /api/v1/allmetrics?format=json
- [x] adjust the data to allign the netdata format
- [x] Create an script to install the required python version and libraries.
- [x] Documentate the process on the readme.md file.

## Requirements:

- Python 3.13
- Python pip

## Installation and run
New versions of python require venv as mandatory, so here the steps to create and activate it.
Install venv complement
```sh
apt install python3.XX-venv
```

Creates the venv, named myenv.
```sh
python3 -m venv myenv
```

Activates the venv to be able to install dependencies.
```sh
source myenv/bin/activate
```

Install the dependencies
```sh
pip install -r requirements.txt
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