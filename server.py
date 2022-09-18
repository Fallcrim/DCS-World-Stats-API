import socket
import json

from utils import save_user_data, get_user_data

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 12000))


def run():
    app_running = True
    while app_running:
        msg, addr = sock.recvfrom(1024)
        data = json.loads(msg.decode())
        if data("eventName") == "kill":
            killerName = data.get("killerPlayerName")
            killerUnit = data.get("killerUnitType")
            killerSide = data.get("killerSide")
            victimName = data.get("victimPlayerName")
            victimUnit = data.get("victimUnitType")
            victimSide = data.get("victimSide")
            weapon = data.get("killerWeapon")
