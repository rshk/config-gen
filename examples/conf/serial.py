## Generate serial numbers

import datetime

def dns_serial():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")
