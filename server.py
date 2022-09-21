import socket
import json
import logging

from utils import save_user_data, get_user_data

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 12000))


def run():
    app_running = True
    while app_running:
        msg, addr = sock.recvfrom(1024)
        data = json.loads(msg.decode())
        if data.get("eventName") == "kill":
            killerName = data.get("killerPlayerName")
            killerUnit = data.get("killerUnitType")
            killerSide = data.get("killerSide")
            victimName = data.get("victimPlayerName")
            weapon = data.get("killerWeapon")

            killer = get_user_data(killerName)
            killer.kills += 1
            killer.used_units.append(killerUnit)
            if weapon != "":
                killer.used_weapons.append(weapon)
            killer.sides_as_killer.append(killerSide)

            victim = get_user_data(victimName)
            victim.deaths += 1

            killer.update_score()
            victim.update_score()
            save_user_data(killer)
            save_user_data(victim)

        if data.get("eventName") == "eject":
            player = get_user_data(data.get("playerName"))
            player.ejections += 1
            save_user_data(player)

        if data.get("eventName") == "simulationEnded":
            app_running = False

        if data.get("eventName") == "pilot_death":
            player = get_user_data(data.get("playerName"))
            player.deaths += 1
            player.update_score()
            save_user_data(player)
