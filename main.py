import threading

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from utils import *
from server import run

config = load_config()

app = FastAPI(title=f"DCS Server {config['DEFAULT']['name']}")
threading.Thread(target=run).start()


@app.get("/", response_class=HTMLResponse)
async def root():
    return open("html/index.html").read()


@app.get("/players/{player_name}")
async def return_player_data(player_name: str):
    return get_user_data(player_name).__dict__


@app.get("/leaderboards/{leaderboard_name}/{limit}")
async def return_leaderboard_data(leaderboard_name: str, limit: int):
    try:
        if leaderboard_name == "kills":
            return get_leaderboard_kills(limit)

        if leaderboard_name == "ejections":
            return get_leaderboard_ejections(limit)

        if leaderboard_name == "deaths":
            return get_leaderboard_deaths(limit)

        if leaderboard_name == "weapons":
            return get_leaderboard_weapons(limit)

        if leaderboard_name == "kd":
            return get_leaderboard_kd(limit)

        if leaderboard_name == "score":
            return get_leaderboard_score(limit)
    except Exception as e:
        return {"ERROR": e}


@app.get("/sides/{side}/{limit}")
async def return_side_kills(side: str, limit: int):
    if side.lower() == "both":
        return get_leaderboard_both_sides()
    else:
        return get_leaderboard_per_side(side, limit)
