import os
import configparser

from fastapi import FastAPI

from utils import load_config

config = load_config()

app = FastAPI(title=f"DCS Server {config['DEFAULT']['name']}")


@app.get("/")
async def root():
    return {"message": "This is the DCS World Stats API!"}


@app.get("/players/{player_name}")
async def return_player_data(player_name: str):
    return {}
