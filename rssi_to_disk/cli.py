import os
import time
import datetime
from csclient import EventingCSClient

cp = EventingCSClient('RSSI_to_disk')

print(os.popen('ls /var/').read())
