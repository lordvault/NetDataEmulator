NetData Emulator

This proyect was created as solution to report from my RPI Zero W 2, the necessary data to be monitored on Home Assistant. The idea its emulate the published data from netdata to reuse the actual netdata integration in home assistant. To achieve this i require a flask server and use a couple of libraries.

Exposed sensors: 
 - CPU Usage
 - CPU Temperature
 - RAM Total
 - RAM in Use
 - System Uptime

For the code solution, already exist a part implmented by raspberry team:
- https://projects.raspberrypi.org/en/projects/temperature-log/4


Development Tasks: 

[x] - Create the flask service and publish hello world on port 19999 path /api/v1/allmetrics?format=json
[x] - adjust the data to allign the netdata format
[x] - Create an script to install the required python version and libraries.
[] - Documentate the process on the read.me file.