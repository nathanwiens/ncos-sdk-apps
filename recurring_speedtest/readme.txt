Application Name
================
recurring_speedtest


Application Version
===================
0.1


NCOS Devices Supported
======================
ALL


External Requirements
=====================


Application Purpose
===================
This SDK application will uses Ookla Speedtest python library and
will perform a speed test every 15 mins, and generate an NCM Custom Alert
with the test results as well as logging to the System Log.


Expected Output
===============
System Log will output speed test results
NCM Custom Alert will be generated with speed test results
Note: NCM Custom Alerts must be enabled in NCM to trigger email alerts.

Example output:
09:03:44 AM INFO Recurring_Speedtest Checking time.
09:03:45 AM INFO Recurring_Speedtest Running Speed Test
09:04:11 AM INFO Recurring_Speedtest
09:04:11 AM INFO Recurring_Speedtest Test Result
09:04:11 AM INFO Recurring_Speedtest Timestamp GMT: 2022-02-25T16:03:46.624957Z
09:04:11 AM INFO Recurring_Speedtest Client ISP: Rogers Cable
09:04:11 AM INFO Recurring_Speedtest Ookla Speedtest.net Server: TELUS
09:04:11 AM INFO Recurring_Speedtest Ping: 79.259ms
09:04:11 AM INFO Recurring_Speedtest Download Speed: 37.04 Mb/s
09:04:11 AM INFO Recurring_Speedtest Upload Speed: 4.62 Mb/s
09:04:11 AM INFO Recurring_Speedtest Ookla Speedtest.net URL Result: http://www.speedtest.net/result/12815471468.png
09:04:11 AM INFO Recurring_Speedtest Sleeping before next Speed Test...
