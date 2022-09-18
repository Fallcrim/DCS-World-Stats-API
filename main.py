import threading

from fastapi import FastAPI

from utils import load_config
from server import run

config = load_config()

app = FastAPI(title=f"DCS Server {config['DEFAULT']['name']}")
threading.Thread(target=run).start()


@app.get("/")
async def root():
    return {"message": "This is the DCS World Stats API!"}


@app.get("/players/{player_name}")
async def return_player_data(player_name: str):
    return {}
