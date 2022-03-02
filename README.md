# Cradlepoint NCOS SDK Applications.
----------

This directory contains the NCOS SDK tools and sample applications. Below is a description of each. 
Refer to the Cradlepoint NetCloud OS Application Developers Guide for more information on building SDK apps: https://customer.cradlepoint.com/s/article/NCOS-SDK-v3-1

This is not an official Cradlepoint repository and should not be treated as such. Cradlepoint maintains an SDK app respository along with the tools required to build apps here: https://github.com/cradlepoint/sdk-samples

## Application Directories

- **adapter_wan_status**
    - Detects whether a branch adapter is "active" based on a throughput threshold and updates the Asset ID field in NCM with the current status
- **e300_run_dark**
    - Disables the LED light bar on E300 (and E3000)
- **one-to-one-nat**
    - Checks for the IP of a connected modem at boot and adds/updates the 1:1 NAT configuration to match
- **ports_status**
    - Sets the device description to visually show the LAN/WAN/WWAN/Modem/IP Verify status
- **recurring_speedtest**
    - Runs an Ookla speed test every 15 mins during a specified time window and generates an NCM alert with the results
- **rssi_to_disk**
    - Logs GPS and cellular signal strength data to a csv file once per second
- **vrrp_status**
    - Sets the asset ID field to visually show the VRRP status of all VRRP-enabled LANs.