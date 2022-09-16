import os

from fastapi import FastAPI
import configparser

config = configparser.ConfigParser()
if not os.path.isfile("config.ini"):
    config["DEFAULT"] = {
        "name": "DCS Server",
        "server_path": "C:/"
    }
else:
    config.read("config.ini")

app = FastAPI(title=f"DCS Server {config['DEFAULT']['name']}")


@app.get("/")
async def root():
    return {"message": "This is the DCS World Stats API!"}


@app.get("/players/{player_name}")
async def return_player_data(player_name: str):
    return {}
