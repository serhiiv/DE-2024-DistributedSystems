import asyncio
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from aiohttp import ClientSession

class Item(BaseModel):
    text: str

app = FastAPI()
logger = logging.getLogger(__name__)
messages = list()
urls = ['rl-slave-1', 'rl-slave-2']

# Helper Functions 
async def replicate(session, url, data):
    """replicate data to the specified URL using the aiohttp session specified."""
    logger.info(f'send to "{url}" data "{data}"')
    response = await session.post('http://' + url + ':8000', json=data)
    logger.info(f'receved from "{url}" status {response.status}')
    return response.status == 200

@app.get("/")
async def get_messages():
    global messages
    return messages

@app.post("/")
async def post_message(item: Item):
    global messages
    data = {"id": len(messages), "text": item.text}

    # after each POST request, the message should be replicated on every Secondary server
    logger.info(f'replicate to slaves the "{data}"')
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(replicate(session, url, data))
            tasks.append(task)
        answers = await asyncio.gather(*tasks)
       
    # Master should ensure that Secondaries have received a message via ACK
    # Master’s POST request should be finished only after receiving ACKs from all Secondaries (blocking replication approach)
    if sum(answers) == len(urls):
        messages.append(item.text)
        logger.info(f'Add message "{item}"')
        return {"ask": 1, "item": item}
    else:
        logger.info(f'error add message')
        return {"ask": 0}
