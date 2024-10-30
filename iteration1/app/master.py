import os
import sys
import asyncio

from aiohttp import ClientSession
from waitress import serve

from flask import Flask, request
from logging.config import dictConfig

# config for loggining
dictConfig({
    "version": 1,
    "formatters": {"default": {"format": "%(asctime)s.%(msecs)03d  %(message)s", "datefmt": "%H:%M:%S"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "default"}},
    "root": {"level": "INFO", "handlers": ["console"]}
    })


# for save incoming messages
messages = list()
urls = ['rl-slave-1', 'rl-slave-2']

app = Flask(__name__)

# Helper Functions 
async def replicate(session, url, data):
    """replicate data to the specified URL using the aiohttp session specified."""
    response = await session.post('http://'+ url, json=data)
    return response.status == 200


@app.route('/', methods=['POST', 'GET'])
async def root():
    global messages

    # - GET method - returns all messages from the in-memory list
    if request.method == 'GET':
        return messages

    # - POST method - appends a message into the in-memory list
    elif request.method == 'POST':
        message = request.json
        app.logger.info(f'received {message}')
        data = {"id": len(messages), "text": message['text']}

        # after each POST request, the message should be replicated on every Secondary server
        app.logger.info(f'replicate to slaves the "{data}"')
        async with ClientSession() as session:
            tasks = []
            for url in urls:
                task = asyncio.create_task(replicate(session, url, data))
                tasks.append(task)
            answers = await asyncio.gather(*tasks)
       
        # Master should ensure that Secondaries have received a message via ACK
        # Master’s POST request should be finished only after receiving ACKs from all Secondaries (blocking replication approach)
        if sum(answers) == len(urls):
            messages.append(message['text'])
            app.logger.info(f'Add message "{data}"')
            return {"ask": 1, "id": len(messages), "text":message['text']}
        else:
            app.logger.info(f'error add message')
            return {"ask": 0}


if __name__ == '__main__':
    # debug mode
    if len(sys.argv) > 1:
        if sys.argv[1] == '--debug':
            app.run(host="0.0.0.0", port=80, debug=True)

    # deploy mode
    serve(app, host="0.0.0.0", port=80)
