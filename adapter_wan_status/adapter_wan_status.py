import time
from csclient import EventingCSClient
cp = EventingCSClient('adapter-wan-status')

APP_NAME = 'ADAPTER_WAN_STATUS'
DEBUG = False
KB_PER_60_SECS_THRESHOLD = 1024
BYTES_PER_60_SECS_THRESHOLD = KB_PER_60_SECS_THRESHOLD * 1024


MODELS_WITHOUT_WAN = ['CBA', 'W200', 'W400', 'L950', 'IBR200', '4250']

cp.logger.debug("Getting Model")

"""Get model number, since some models don't have ethernet WAN"""
model = ''
model = cp.get('/status/product_info/product_name')
cp.logger.debug(model)

ipackets = 0
opackets = 0
ibytes = 0
obytes = 0
wan_active = False

while True:
    try:
        is_available_modem = 0
        is_available_wan = 0
        is_available_wwan = 0
        is_configured_wwan = 0

        wans = cp.get('/status/wan/devices')

        if wans:

            """Get status of all modems"""
            for wan in (wan for wan in wans if 'mdm' in wan):

                """Filter to only track modems. Will show green if at least one modem is active"""
                if 'mdm' in wan:

                    """Get modem status for each modem"""
                    summary = cp.get('/status/wan/devices/{}/status/summary'.format(wan))

                    if summary:
                        if 'connected' in summary:
                            cp.logger.debug("MODEM {} ACTIVE".format(wan))
                            is_available_modem = 1

                            stats = cp.get('/status/wan/devices/{}/stats'.format(wan))
                            cp.logger.debug(stats)
                            """
                            old_ipackets = ipackets
                            old_opackets = opackets
                            ipackets = stats['ipackets']
                            opackets = stats['opackets']
                            """

                            old_ibytes = ibytes
                            old_obytes = obytes
                            ibytes = stats['in']
                            obytes = stats['out']

                            old_wan_active = wan_active
                            if (ibytes - old_ibytes >= BYTES_PER_60_SECS_THRESHOLD) or (obytes - old_obytes >= BYTES_PER_60_SECS_THRESHOLD):
                                wan_active = True
                                wan_string = "WAN ACTIVITY: 🟢 - IN: {:.2f}KB, OUT: {:.2f}KB".format((ibytes - old_ibytes)/1024, (obytes - old_obytes)/1024)
                            else:
                                wan_active = False
                                wan_string = "WAN ACTIVITY: ⚫ - IN: {:.2f}KB, OUT: {:.2f}KB".format((ibytes - old_ibytes)/1024, (obytes - old_obytes)/1024)
                            if old_wan_active is not wan_active:
                                cp.logger.info("WAN ACTIVE STATUS CHANGED FROM {} TO {}".format(old_wan_active, wan_active))

                        elif 'error' in summary:
                            continue

            """If no active/standby modems are found, show offline"""
            if is_available_modem == 0:
                cp.logger.info("NO ACTIVE MODEM FOUND")

        """Write string to description field"""
        cp.logger.debug(f"WRITING ASSET ID: {wan_string}")
        cp.put('config/system/asset_id', wan_string)

    except Exception as err:
        cp.logger.error("Failed with exception={} err={}".format(type(err), str(err)))

    """Wait 60 seconds before checking again"""
    time.sleep(60)
