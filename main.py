import threading

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from utils import load_config, get_user_data, get_leaderboard_kills, get_leaderboard_ejections, get_leaderboard_deaths
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
    if leaderboard_name == "kills":
        return get_leaderboard_kills(limit)

    if leaderboard_name == "ejections":
        return get_leaderboard_ejections(limit)

    if leaderboard_name == "deaths":
        return get_leaderboard_deaths(limit)
