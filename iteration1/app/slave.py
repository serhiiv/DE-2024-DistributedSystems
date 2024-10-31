import logging
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    text: str

app = FastAPI()
logger = logging.getLogger(__name__)
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
    messages += [None] * (item.id - len(messages) + 1)
    messages[item.id] = item.text
    logger.info(f'add [post] message {item}')
    return {"ask": 1, "item": item}
