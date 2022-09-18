import configparser
import pickle
import os


DATABASEFILE = "db.pkl"


class Player:
    def __init__(self, username: str, kills: int, deaths: int, ejections: int, used_weapons: list, used_units: list, sides_as_killer: list):
        self.name = username
        self.kills = kills
        self.deaths = deaths
        self.used_weapons = used_weapons
        self.used_units = used_units
        self.sides_as_killer = sides_as_killer
        self.ejections = ejections


def _load_data(filename):
    if not os.path.exists(filename):
        return {}
    else:
        with open(filename, "rb") as f:
            return pickle.load(f)


def get_user_data(username: str):
    data = _load_data(DATABASEFILE)
    user_data = data.get(username)
    if user_data is not None:
        return user_data
    else:
        return Player(username, 0, 0, list(), list(), list())


def save_user_data(player_data: Player):
    data = _load_data(DATABASEFILE)
    data[player_data.name] = player_data
    with open(DATABASEFILE, "wb") as f:
        pickle.dump(data, f)


def load_config():
    config = configparser.ConfigParser()
    if not os.path.isfile("config.ini"):
        config["DEFAULT"] = {
            "name": "DCS Server"
        }
    else:
        config.read("config.ini")
    return config
