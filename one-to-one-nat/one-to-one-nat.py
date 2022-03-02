"""
ONE-TO-ONE-NAT
Created by: Nathan Wiens (nathan.wiens@cradlepoint.com)

This application will check for the IP of a connected modem at boot and
add/update the 1:1 NAT configuration to match. It will only match the
first detected modem interface with a 10.x.x.x address.

Change the inside_ip variable to match the inside translated address.

Example output:
MODEM FOUND: mdm-36633f12 WITH IP: 10.193.82.173
ONE TO ONE NAT CONFIG COMPLETE
{'nat_to_network': '192.168.0.10', 'original_network': '10.193.82.173',
'priority': 10, 'proxy_arp_routes': True}

"""

import time
from csclient import EventingCSClient
cp = EventingCSClient('one-to-one-nat')

APP_NAME = 'ONE-TO-ONE-NAT'

"""CHANGE THIS TO MATCH THE DESTINATION (INSIDE) IP"""
inside_ip = "192.168.0.10"

payload = ''
success = False

"""GET LIST OF WANS"""
wans = cp.get('status/wan/devices')

old_nat_config = cp.get('config/security/dynamic_nat/0/original_network')
if old_nat_config:
    cp.log(f"NAT CONFIG: {old_nat_config}")

"""DON'T RUN IF WANS ARE NOT RETURNED"""
if wans:

    try:
        """KEEP TRYING UNTIL VALID MODEM IP FOUND"""
        while not success:
            cp.log("CHECKING ONE-TO-ONE NAT SETTINGS")

            """ONLY LOOK AT MODEM INTERFACES"""
            for wan in (wan for wan in wans if 'mdm' in wan):
                """GET THE IP ADDRESS OF THE MODEM"""
                ip = cp.get(f'status/wan/devices/{wan}/status/ipinfo/ip_address')
                if ip:

                    """MAKE SURE THE IP ADDRESS IS VALID"""
                    if '10' in ip:

                        cp.log(f"MODEM FOUND: {wan} WITH IP: {ip}")

                        """IF THE IP HASN'T CHANGED, DON'T MAKE CONFIG CHANGES"""
                        if old_nat_config:
                            if ip == old_nat_config:
                                cp.log("MODEM IP HASN'T CHANGED. NO NAT CHANGES MADE.")
                                success = True
                                break

                        """GENERATE ONE TO ONE NAT CONFIG"""
                        payload = {"0": {
                            "nat_to_network": inside_ip,
                            "original_network": ip,
                            "priority": 10,
                            "proxy_arp_routes": True
                            }
                        }

                        """APPLY CONFIG TO THE ROUTER"""
                        cp.put('config/security/dynamic_nat', payload)

                        cp.log("ONE TO ONE NAT CONFIG COMPLETE")
                        cp.log(cp.get('config/security/dynamic_nat/0'))

                        """PREVENT FURTHER IP CHECKS"""
                        success = True
                        break
            """WAIT 10 SECONDS BETWEEN IP CHECKS"""
            time.sleep(10)

    except Exception as err:
        cp.log("Failed with exception={} err={}".format(type(err), str(err)))
