from os import path
import time
import datetime
from csclient import EventingCSClient

cp = EventingCSClient('RSSI_to_disk')

time.sleep(30)

def dms2dd(degrees, minutes, seconds):
    if degrees >= 0:
        dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    else:
        dd = float(degrees) - (float(minutes) / 60 + float(seconds) / (60 * 60))
    return dd

while True:
    today = datetime.date.today().strftime("%Y-%m-%d")
    csv_header = 'TIME,MODEM,RSSI,RSRP,RSRQ,SINR,CELL ID,LATITUDE,LONGITUDE,HEADING,GROUND SPEED,ALTITUDE (METERS)\n'

    usb_file = '/var/media/rssi_{}.csv'.format(today)
    if not path.exists(usb_file):
        try:
            with open(usb_file, 'w') as f:
                f.write(csv_header)
        except:
            pass

    local_file = '/var/mnt/sdk/rssi_{}.csv'.format(today)
    if not path.exists(local_file):
        with open(local_file, 'w') as f:
            f.write(csv_header)


    rssi = ''
    rsrp = ''
    rsrq = ''
    sinr = ''
    cell_id = ''
    mdm = ''

    try:
        wans = cp.get('status/wan/devices')
        for wan in (wan for wan in wans if 'mdm' in wan):
            """Filter to only track modems. Will show green if at least one modem is active"""
            if 'mdm' in wan:

                """Get modem status for each modem"""
                summary = cp.get('status/wan/devices/{}/status/summary'.format(wan))
                diagnostics = cp.get('status/wan/devices/{}/diagnostics'.format(wan))

                if 'connected' in summary:
                    cp.log(wan + " RSSI: " + diagnostics['DBM'])
                    rssi = diagnostics['DBM']
                    cp.log(wan + " RSRP: " + diagnostics['RSRP'])
                    rsrp = diagnostics['RSRP']
                    cp.log(wan + " RSRQ: " + diagnostics['RSRQ'])
                    rsrq = diagnostics['RSRQ']
                    cp.log(wan + " SINR: " + diagnostics['SINR'])
                    sinr = diagnostics['SINR']
                    cp.log(wan + " CELL ID: " + diagnostics['CELL_ID'])
                    cell_id = diagnostics['CELL_ID']
                    mdm = wan
                    break
    except Exception as e:
        cp.log("UNABLE TO GET MODEM STATUS")

    if rssi is '':
        cp.log("NO ACTIVE MODEM FOUND")

    data = str(datetime.datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S")) + ',' + mdm + ',' + \
           rssi + ',' + rsrp + ',' + rsrq + ',' + \
           sinr + ',' + cell_id

    lat = 0
    long = 0
    gpsfix = {}
    try:
        gpsfix = cp.get('status/gps/fix')
        if gpsfix['lock']:
            lat = dms2dd(gpsfix['latitude']['degree'],
                         gpsfix['latitude']['minute'],
                         gpsfix['latitude']['second'])
            long = dms2dd(gpsfix['longitude']['degree'],
                         gpsfix['longitude']['minute'],
                         gpsfix['longitude']['second'])
            cp.log("LOCATION: {}, {}".format(lat, long))
        else:
            cp.log("NO GPS FIX.")
    except Exception as e:
        cp.log("ERROR GETTING GPS STATUS")


    if gpsfix:
        data = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + ',' + mdm + ',' + \
           rssi + ',' + rsrp + ',' + rsrq + ',' + \
           sinr + ',' + cell_id + ',' + str(lat) + ',' + \
           str(long) + ',' + str(gpsfix['heading'])  + ',' + str(gpsfix['ground_speed_knots'])  + ',' + str(gpsfix['altitude_meters']) + '\n'

    try:
        with open(usb_file, 'a+', newline='') as f:
            f.write(data)
    except:
        pass

    with open(local_file, 'a+', newline='') as f:
        f.write(data)

    cp.log("SLEEPING 1 SECOND...")
    time.sleep(1)
