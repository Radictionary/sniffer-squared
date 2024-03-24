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

from pickledsocks import picklesocks

async def get_history():
    try:
        return dict(history=await picklesocks.send("", 3952), error=None)
    except Exception as e:
        return dict(history=None, error=str(e))

async def add_to_whitelist(ip):
    data = {"list":"whitelist", "mode":"add", "ip": ip}
    await picklesocks.send(data, 3958)

async def remove_from_whitelist(ip):
    data = {"list":"whitelist", "mode":"remove", "ip": ip}
    await picklesocks.send(data, 3958)

async def add_to_blacklist(ip):
    data = {"list":"blacklist", "mode":"add", "ip": ip}
    await picklesocks.send(data, 3958)

async def remove_from_blacklist(ip):
    data = {"list":"blacklist", "mode":"remove", "ip": ip}
    await picklesocks.send(data, 3958)