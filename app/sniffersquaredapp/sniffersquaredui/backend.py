from functools import partial
from notifypy import Notify

RUN_FILE_PATH = "../../packet_pool/run.txt"

def write_to_runfile(data):
    with open(RUN_FILE_PATH) as f:
        f.write(data)

shutdown = partial(write_to_runfile, "false")
start    = partial(write_to_runfile, "true")

def send_notification(title, notification):
    notification = Notify()
    notification.title = title
    notification.message = notification
    notification.send()