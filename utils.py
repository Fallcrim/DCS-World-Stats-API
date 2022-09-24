import configparser
import pickle
import os

DATABASEFILE = "db.pkl"


class Player:
    def __init__(self, username: str, kills: int, deaths: int, ejections: int, used_weapons: list, used_units: list,
                 sides_as_killer: list):
        self.name = username
        self.kills = kills
        self.deaths = deaths
        self.used_weapons = used_weapons
        self.used_units = used_units
        self.sides_as_killer = sides_as_killer
        self.ejections = ejections
        self._score = 0
        self.kd = round(self.kills / self.deaths, 2) if self.deaths != 0 else self.kills
        self.takeoffs = 0
        self.landings = 0

    @property
    def score(self):
        return self._score

    def update_score(self):
        self._score = self.kills * 2 - self.deaths
        self.kd = round(self.kills / self.deaths, 2) if self.deaths != 0 else self.kills


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
    sorted_lb_dict = {username: deathCount for username, deathCount in sorted_lb}
    return sorted_lb_dict


def get_leaderboard_ejections(limit: int = 10):
    data = _load_data(DATABASEFILE)
    unsorted = [(user.name, user.ejections) for user in list(data.values())[:limit]]
    sorted_lb = sorted(unsorted, key=lambda tup: tup[1], reverse=True)
    sorted_lb_dict = {username: ejectCount for username, ejectCount in sorted_lb}
    return sorted_lb_dict


def get_leaderboard_weapons(limit: int = 10):
    data = _load_data(DATABASEFILE)
    weapon_scores = {}
    for entry in data.values():
        for weapon in entry.used_weapons:
            if weapon not in weapon_scores:
                weapon_scores[weapon] = 1
            else:
                weapon_scores[weapon] += 1
    unsorted = [(wpn_name, wpn_kills) for wpn_name, wpn_kills in list(weapon_scores.items())[:limit]]
    sorted_lb = sorted(unsorted, key=lambda tup: tup[1], reverse=True)
    leaderboard = dict(sorted_lb)
    return leaderboard


def get_leaderboard_kd(limit: int = 10):
    data = _load_data(DATABASEFILE)
    unsorted = [(user.name, user.kd) for user in list(data.values())[:limit]]
    sorted_lb = sorted(unsorted, key=lambda tup: tup[1], reverse=True)
    sorted_lb_dict = {username: kd for username, kd in sorted_lb}
    return sorted_lb_dict


def get_leaderboard_score(limit: int = 10):
    data = _load_data(DATABASEFILE)
    unsorted = [(user.name, user.kd) for user in list(data.values())[:limit]]
    sorted_lb = sorted(unsorted, key=lambda tup: tup[1], reverse=True)
    sorted_lb_dict = {username: score for username, score in sorted_lb}
    return sorted_lb_dict


def get_leaderboard_both_sides():
    data = _load_data(DATABASEFILE)
    side_scores = {}
    for entry in data.values():
        for side in entry.sides_as_killer:
            if side not in side_scores:
                side_scores[side] = 1
            else:
                side_scores[side] += 1
    unsorted = [(wpn_name, wpn_kills) for wpn_name, wpn_kills in list(side_scores.items())]
    sorted_lb = sorted(unsorted, key=lambda tup: tup[1], reverse=True)
    leaderboard = dict(sorted_lb)
    return leaderboard


def get_leaderboard_per_side(side: str, limit: int):
    data = _load_data(DATABASEFILE)
    kill_scores = {}
    for entry in data.values():
        for entry_side in entry.sides_as_killer:
            if entry_side.upper() == side.upper():
                if entry.name not in kill_scores:
                    kill_scores[entry.name] = 0
                kill_scores[entry.name] += 1
    unsorted = [(user[0], user[1]) for user in list(kill_scores.items())[:limit]]
    sorted_leaderboard = sorted(unsorted, key=lambda tup: tup[1], reverse=True)
    return dict(sorted_leaderboard)


def get_leaderboard_planes(limit: int = 10):
    data = _load_data(DATABASEFILE)
    plane_scores = {}
    for entry in data.values():
        for plane in entry.used_units:
            if plane not in plane_scores:
                plane_scores[plane] = 1
            else:
                plane_scores[plane] += 1
    unsorted = [(wpn_name, wpn_kills) for wpn_name, wpn_kills in list(plane_scores.items())[:limit]]
    sorted_lb = sorted(unsorted, key=lambda tup: tup[1], reverse=True)
    leaderboard = dict(sorted_lb)
    return leaderboard
