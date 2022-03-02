Application Name
================
one-to-one-nat


Application Version
===================
0.1


NCOS Devices Supported
======================
ALL


External Requirements
=====================
Connected modem with IP in the 10.0.0.0/8 range.

Application Purpose
===================
This application will check for the IP of a connected modem at boot and
add/update the 1:1 NAT configuration to match


Expected Output
===============
MODEM FOUND: mdm-36633f12 WITH IP: 10.193.82.173
ONE TO ONE NAT CONFIG COMPLETE
{'nat_to_network': '10.92.198.5', 'original_network': '10.193.82.173', 'priority': 10, 'proxy_arp_routes': True}