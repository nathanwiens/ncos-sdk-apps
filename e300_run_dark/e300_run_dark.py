from csclient import EventingCSClient
cp = EventingCSClient('ports-status')
from time import sleep

APP_NAME = 'E-SERIES_RUN_DARK'

cp.log('STARTED E300 RUN DARK APP')
cp.put('config/system/disable_leds', True)

"""
while 1:
    for i in range(0, 18):
        cs.CSClient().put('/control/gpio/LED_BAR_{}'.format(i), 0)
    sleep(1)
"""
