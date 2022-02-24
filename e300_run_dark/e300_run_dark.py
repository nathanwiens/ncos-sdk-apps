import cs
from time import sleep

APP_NAME = 'E300_RUN_DARK'

while 1:
    for i in range(0, 18):
        cs.CSClient().put('/control/gpio/LED_BAR_{}'.format(i), 0)
    sleep(1)
