import asyncio
import logging
import itertools
from fastapi import FastAPI
from pydantic import BaseModel
from aiohttp import ClientSession


class Item(BaseModel):
    wc: int
    text: str


app = FastAPI()
logger = logging.getLogger(__name__)
messages = list()
urls = ['rl-slave-1', 'rl-slave-2']
HEARTBEATS = 3


# Helper Functions 
async def replicate(url, data):
    """replicate data to the specified URL using the aiohttp"""
    async with ClientSession() as session:
        logger.info(f'Send to "{url}" data "{data}"')
        response = await session.post('http://' + url + ':8000', json=data)
        logger.info(f'Got from "{url}" status {response.status}')
    return response.status == 200


@app.get("/")
async def get_messages():
    return messages


@app.post("/")
async def post_message(item: Item):
    global messages
    data = {"id": len(messages), "text": item.text}
    messages.append(item.text)

    # after each POST request, the message should be replicated on every Secondary server
    logger.info(f'replicate to slaves the "{data}"')
    tasks = [asyncio.create_task(replicate(url, data)) for url in urls]
    await asyncio.sleep(0)

    for task in itertools.islice(asyncio.as_completed(tasks), item.wc-1):
        await task

    return {"id": len(messages) - 1, "text": item.text}


@app.get("/health")
async def get_health():
    return messages
