Application Name
================
rssi_to_disk


Application Version
===================
0.1.0


NCOS Devices Supported
======================
ALL


External Requirements
=====================
None

Application Purpose
===================
This application logs GPS coordinates and cell signal info
to a USB drive (if present) and locally to /var/mnt/sdk/rssi.csv every second.
This can be used for later plotting in a GIS visualization tool


Expected Output
===============
Example resulting CSV file:

TIME,MODEM,RSSI,RSRP,RSRQ,SINR,CELL ID,LATITUDE,LONGITUDE,HEADING,GROUND SPEED,ALTITUDE (METERS)
18/11/2021 13:58:17,mdm-2af77ad5,-78,-111,-17,-2.0,28311234 (0x1af1234),49.1234,-119.1234,0.0,0.1,123.87
18/11/2021 13:58:18,mdm-2af77ad5,-78,-111,-17,-2.0,28311234 (0x1af1234),49.1234,-119.1234,0.0,0.1,123.87
