'''

Description: This SDK application will uses Ookla Speedtest python library and
will perform a speed test every 15 mins, and generate an NCM Custom Alert
with the test results as well as logging to the System Log.

'''

from csclient import EventingCSClient
from speedtest import Speedtest
from time import sleep
from datetime import datetime, time, timezone, timedelta

MINUTES_BETWEEN_TESTS = 15
UTC_OFFSET = -5
START_TIME = time(00, 00)
END_TIME = time(23, 59)

cp = EventingCSClient('Recurring_Speedtest')
model = cp.get('/status/product_info/product_name')
serial_number = cp.get('/status/product_info/manufacturing/serial_num')
system_id = cp.get('/config/system/system_id')

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.now(timezone(timedelta(hours=UTC_OFFSET))).time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def get_modem_data():
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
                        diag = cp.get('/status/wan/devices/{}/diagnostics'.format(wan))
                        modem_data = {"APN": diag['APN1'],
                                      "CARRID": diag['CARRID'],
                                      "CELL_ID": diag['CELL_ID'],
                                      "DBM": diag['DBM'],
                                      "ICCID": diag['ICCID'],
                                      "LTEBANDWIDTH": diag['LTEBANDWIDTH'],
                                      "PRD": diag['PRD'],
                                      "RFBAND": diag['RFBAND'],
                                      "RSRP": diag['RSRP'],
                                      "SIM_NUM": diag['SIM_NUM'],
                                      "SINR": diag['SINR']
                                      }
                        return modem_data

def speedtest():

    servers = []
    s = Speedtest()

    #Find the best ookla speedtest server based from latency and ping
    cp.log("Finding the Best Ookla Speedtest.net Server...")
    server = s.get_best_server()
    cp.log('Found Best Ookla Speedtest.net Server: {}'.format(server['sponsor']))

    p = s.results.ping

    #Perform Download ookla download speedtest
    cp.log("Performing Ookla Speedtest.net Download Test...")
    d = s.download()

    #Perform Upload ookla upload speedtest. Option pre_allocate false prevents memory error
    cp.log("Performing Ookla Speedtest.net Upload Test...")
    u = s.upload(pre_allocate=False)

    #Access speedtest result dictionary
    res = s.results.dict()

    #share link for ookla test result page
    share = s.results.share()

    t = res['timestamp']
    i = res["client"]["isp"]
    s = server['sponsor']


    cp.log('')
    cp.log('Test Result')
    cp.log('Timestamp GMT: {}'.format(t))
    cp.log('Client ISP: {}'.format(i))
    cp.log('Ookla Speedtest.net Server: {}'.format(s))
    cp.log('Ping: {}ms'.format(p))
    cp.log('Download Speed: {:.2f} Mb/s'.format(d / 1000 / 1000))
    cp.log('Upload Speed: {:.2f} Mb/s'.format(u / 1000 / 1000))
    cp.log('Ookla Speedtest.net URL Result: {}'.format(share))

    cp.log(f'Speedtest Complete!')

    test_result = {"timestamp": t,
                   "isp": i,
                   "server": s,
                   "download": "{:.2f}Mbps".format(d / 1000 / 1000),
                   "upload": "{:.2f}Mbps".format(u / 1000 / 1000),
                   "ping": "{}ms".format(p),
                   "result": share}
    modem_data = get_modem_data()
    alert_msg = {"alertName": "Recurring_Speedtest",
             "executionStatus": "SUCCEED",
             "errorMessage": "NONE",
             "deviceName": system_id,
             "serialNumber": serial_number,
             "product": model,
             "testResult": test_result,
             "modemData": modem_data}
    cp.alert(alert_msg)
    cp.log(alert_msg)
    cp.log("ALERT SENT")


while 1:
    if is_time_between(START_TIME, END_TIME):
        try:
            cp.log('Running Speed Test')
            speedtest()

        except Exception as e:
            cp.log(e)
        cp.log("Sleeping before next Speed Test...")
    sleep(MINUTES_BETWEEN_TESTS * 60)

