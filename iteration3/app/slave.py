import os 
import socket
import asyncio
import logging
from fastapi import FastAPI
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Item(BaseModel):
    id: int
    text: str


class Sleep(BaseModel):
    time: float


async def heartbeats(beats, hostname):
    while True:
        await asyncio.sleep(beats)
        logger.info(f'My hostname is "{hostname}" = "{messages}"  = "{len(messages)}"')


HOSTNAME = socket.gethostname()
HEARTBEATS = float(os.getenv("HEARTBEATS", 3))


app = FastAPI()

messages = list()
delay = Sleep(time=0)


@app.on_event('startup')
async def heartbeats_startup():
    asyncio.create_task(heartbeats(HEARTBEATS, HOSTNAME))


@app.get("/")
async def get_messages():
    ''' Select messages from the list messages 
    until the first message with 'None' happens.
    '''
    out = messages + [None]
    return out[0: out.index(None)]


@app.post("/")
async def post_message(item: Item):
    ''' Add a new message to the list.
    '''
    global messages
    
    # Fill the list of messages with values ​​'None' up to the end 
    # and make the list length of the messages equal to the 'id.'
    messages += [None] * (item.id - len(messages) + 1)
    messages[item.id] = item.text
    logger.info(f'Add message "{item}"')
    
    # Make a timeout before the response.
    await asyncio.sleep(delay.time)
    
    return {"ask": 1, "item": item}


@app.get("/sleep")
async def get_sleep():
    ''' Return current sleep time.
    '''
    return {"sleep": delay}


@app.post("/sleep")
async def post_sleep(sleep: Sleep):
    ''' Set sleep time to add a new message.
    '''
    global delay
    delay = sleep
    logger.info(f'Set sleep {delay}')
    return {"sleep": delay}
