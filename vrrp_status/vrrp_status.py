"""
VRRP_STATUS
Created by: Nathan Wiens (nathan.wiens@cradlepoint.com)

This application will set the device asset ID to visually show
the VRRP status of all VRRP-enabled LANs.

"""
import time
from csclient import EventingCSClient
cp = EventingCSClient('vrrp-status')

APP_NAME = 'VRRP_STATUS'

while True:
    try:
        vrrp_status = ""
        vrrp_string = "VRRP: "
        vrrp = cp.get('/status/vrrp')

        """Only take action if grabbing VRRP state was successful"""
        if vrrp:
            for net in vrrp:
                vrrp_state = cp.get(f"/status/vrrp/{net}/state")
                vrrp_string += f"{str(net)}: {str(vrrp_state)}, "

            vrrp_string = vrrp_string[:-1]
            """Write string to description field"""
            cp.logger.debug(f"WRITING ASSET ID: {vrrp_string}")
            cp.put('config/system/asset_id', vrrp_string)

    except Exception as err:
        cp.logger.error("Failed with exception={} err={}".format(type(err), str(err)))

    """Wait 5 seconds before checking again"""
    time.sleep(5)
