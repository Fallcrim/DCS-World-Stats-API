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
        self._score = 0
        self.kd = kills / deaths
        self.takeoffs = 0
        self.landings = 0

    @property
    def score(self):
        return self._score

    def update_score(self):
        self._score = self.kills * 2 - self.deaths
        self.kd = round(self.kills / self.deaths, 2)


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
        return Player(username, 0, 0, 0, list(), list(), list())


def save_user_data(player_data: Player):
    if player_data.name == "null":
        return
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


def get_leaderboard_kills(limit: int = 10):
    data = _load_data(DATABASEFILE)
    unsorted = [(user.name, user.kills) for user in list(data.values())[:limit]]
    sorted_lb = sorted(unsorted, key=lambda tup: tup[1], reverse=True)
    sorted_lb_dict = {username: killCount for username, killCount in sorted_lb}
    return sorted_lb_dict


def get_leaderboard_deaths(limit: int = 10):
    data = _load_data(DATABASEFILE)
    unsorted = [(user.name, user.deaths) for user in list(data.values())[:limit]]
    sorted_lb = sorted(unsorted, key=lambda tup: tup[1], reverse=True)
    sorted_lb_dict = {username: killCount for username, killCount in sorted_lb}
    return sorted_lb_dict


def get_leaderboard_ejections(limit: int = 10):
    data = _load_data(DATABASEFILE)
    unsorted = [(user.name, user.ejections) for user in list(data.values())[:limit]]
    sorted_lb = sorted(unsorted, key=lambda tup: tup[1], reverse=True)
    sorted_lb_dict = {username: killCount for username, killCount in sorted_lb}
    return sorted_lb_dict

