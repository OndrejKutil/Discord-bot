from fastapi import FastAPI
import os
import datetime
import signal
import json
from timeit import default_timer as timer
import multiprocessing

app = FastAPI()

def bot_turn_on():
    os.system("cd /home/pi/Desktop/DC_BOT ; ./run.sh")


def generate_message(text: str, time_el: float):
    date = datetime.datetime.now().strftime("%H:%M:%S")
    data = {
        "Status": f"{text}",
        "Time": f"{date}",
        "Time to finnish": f"{time_el}"
    }
    return data


@app.get("/dcbot/on")
def start():
    start = timer()
    p = multiprocessing.Process(target=bot_turn_on)
    p.daemon = True
    p.start()
    end = timer()
    elapsed = end - start
    return generate_message("Started discord bot", elapsed)


@app.get("/dcbot/off")
def shutdown():
    start = timer()
    with open("/home/pi/Desktop/pidjson.json", "r") as f:
        data = json.load(f)
        pid = data["pid"]
    os.kill(pid, signal.SIGKILL)
    end = timer()
    elapsed = end - start
    return generate_message("Succuesfully stopped bot thread", elapsed)


@app.get("/")
def root():
    return {"Root": "hello"}
           