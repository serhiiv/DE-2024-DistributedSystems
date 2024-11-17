import os
import time
import asyncio
import logging
import itertools
from fastapi import FastAPI
from pydantic import BaseModel
from aiohttp import ClientSession


class Item(BaseModel):
    wc: int
    text: str

class Health(BaseModel):
    hostname: str
    delivered: int


app = FastAPI()
logger = logging.getLogger(__name__)
messages = list()
slaves = dict()

urls = ['rl-slave-1', 'rl-slave-2']

HEARTBEATS = float(os.getenv("HEARTBEATS", 3))


def get_host_status(key):
    ''' implement a heartbeat mechanism to check 
    slaves’ health (status): Healthy -> Suspected -> Unhealthy. 
    '''
    delta = time.time() - slaves[key]['uptime']
    if delta > HEARTBEATS * 1.25:
        return 'Unhealthy'
    elif delta < HEARTBEATS * 0.75:
        return 'Healthy'
    else:
        return 'Suspected'

def not_quorum(quorum):
    ''' Check quorum for slaves and master ( +1 )
    '''
    return quorum > (sum([get_host_status(key) != 'Unhealthy' for key in slaves.keys()]) + 1)
        



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
    '''
    '''
    return messages


@app.post("/")
async def post_message(item: Item):
    '''
    '''
    if not_quorum(item.wc):
        # If there is no quorum the master should be switched into read-only mode 
        # and shouldn’t accept messages append requests and should return the appropriate message
        return {'ask': 0, 'text': 'does not have a quorum'}


    global messages
    data = {"id": len(messages), "text": item.text}
    messages.append(item.text)

    # # after each POST request, the message should be replicated on every Secondary server
    # logger.info(f'replicate to slaves the "{data}"')
    # tasks = [asyncio.create_task(replicate(url, data)) for url in urls]
    # await asyncio.sleep(0)

    # for task in itertools.islice(asyncio.as_completed(tasks), item.wc-1):
    #     await task

    return {'ask': 1, "text": item.text, "id": len(messages) - 1}


@app.get("/health")
async def get_health():
    ''' You should have an API on the master to check the slaves’ status: GET /health
    '''
    out = list()
    for key in sorted(slaves.keys()):
        out.append({'hostname': key, 'status': get_host_status(key)})

    return out


@app.post("/health")
async def post_message(health: Health):
    '''
    '''
    global slaves
    slaves[health.hostname] = {'delivered': health.delivered, 'uptime': time.time()}

    # All messages that secondaries have missed due to unavailability should be replicated after (re)joining the master
    for id in range(health.delivered, len(messages)):
        data = {"id": id, "text": messages[id]}
        #  sent to health.hostname

    return {'ask': 1, 'hostname': health.hostname}

