def shutdown():
    # assume run from folder adjacent to
    # python manage.py
    with open("../../packet_pool/run.txt") as f:
        f.write("false")

def start():
    with open("../../packet_pool/run.txt") as f:
        f.write("true")