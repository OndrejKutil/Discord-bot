from fastapi import FastAPI
import multiprocessing
import typing
import os
import psutil
import time
import signal
import json

app = FastAPI()

def bot_turn_on():
    try:
        os.system("cd /home/pi/Desktop/DC_BOT ; ./run.sh")
    except OSError as e:
        print("Execution failed")


@app.get("/dcbot/on")
def start():
    bot_turn_on()
    return {"Status": "sucess"}


@app.get("/dcbot/off")
def shutdown():
    with open("/home/pi/Desktop/pidjson.json", "r") as f:
        data = json.load(f)
        pid = data["pid"]
    os.kill(pid, signal.SIGKILL)
    return {"Status":"stopped thread"}


@app.get("/")
def root():
    return {"Root": "hello",
            "pid": f"{pid}"}