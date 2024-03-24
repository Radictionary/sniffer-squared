from functools import partial
from notifypy import Notify

RUN_FILE_PATH = "../../packet_pool/run.txt"

def write_to_runfile(data):
    with open(RUN_FILE_PATH, "w") as f:
        f.write(data)

def run_file_status():
    with open(RUN_FILE_PATH, "r") as f:
        return f.read().strip().startswith("true")

def start():
    send_notification("Start", "The system is starting.", "normal")
    write_to_runfile("true")

def shutdown():
    send_notification("Shutdown", "The system is shutting down.", "normal")
    write_to_runfile("false")

def send_notification(title, message, urgency="normal"):
    Notify(
        title, 
        message, 
        "S² | Network Sniffer Detection Platform", 
        urgency,
        "./sniffersquaredui/static/sniffersquaredui/favicon.ico"
    ).send()