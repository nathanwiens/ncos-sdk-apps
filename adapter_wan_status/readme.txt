Application Name
================
adapter_wan_status


Application Version
===================
0.8.0


NCOS Devices Supported
======================
ALL


External Requirements
=====================
None

Application Purpose
===================
This application detects whether a branch adapter is "active" based on
a throughput threshold and updates the Asset ID field in NCM with the
current status
Default threshold is 1024 KB within a 60 second window.


Expected Output
===============
Asset ID updated when 1000KB or more is transmitted within 60 seconds
Example:
WAN ACTIVITY: 🟢 - IN: xKB, OUT: yKB
