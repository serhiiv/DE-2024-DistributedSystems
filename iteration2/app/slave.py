import asyncio
import logging
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    text: str


class Sleep(BaseModel):
    time: int


app = FastAPI()
logger = logging.getLogger(__name__)
delay = Sleep(time=0)
messages = list()


@app.get("/")
async def get_messages():
    global messages
    # select messages until first 'None'
    out = messages + [None]
    return out[0: out.index(None)]


@app.post("/")
async def post_message(item: Item):
    global messages
    global delay
    await asyncio.sleep(delay.time)
    messages += [None] * (item.id - len(messages) + 1)
    messages[item.id] = item.text
    logger.info(f'Add message "{item}"')
    return {"ask": 1, "item": item}


@app.get("/sleep")
async def get_sleep():
    global delay
    return {"ask": 1, "sleep": delay}


@app.post("/sleep")
async def post_sleep(sleep: Sleep):
    global delay
    delay = sleep
    logger.info(f'Set sleep {delay}')
    return {"ask": 1, "sleep": delay}
