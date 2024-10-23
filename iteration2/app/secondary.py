import os
import time
import requests
from flask import Flask, request
from logging.config import dictConfig

# config for loggining
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(levelname)s]  %(message)s",
                # "format": "[%(asctime)s] [%(levelname)s | %(module)s]  %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console"]},
     }
)

app = Flask(__name__)

# for save incoming messages
messages = list()

@app.route('/', methods=['POST', 'GET'])
def root():
    global messages

    # return the json of messages from memory
    if request.method == 'GET':
        out = list()
        # select messages until first 'None'
        for m in messages:
            if m is None:
                break
            out.append(m)
        app.logger.info(f"Returned json:  {out}")
        return out

    # add new message
    elif request.method == 'POST':
        message = request.json
        app.logger.info(f'Received json:  {message}')
        
        id = message.get("id", None)
        text = message.get("text", None)
        while id >= len(messages):
            messages.append(None)
        messages[id] = text

        app.logger.info(f'Add message #{id} "{text}"')
        return {"ask": 1, "id": id, "text":text}


if __name__ == '__main__':
    hostname = os.environ["HOSTNAME"]
    app.logger.info(f'Send hostname "{hostname}" to the master')
    answer = False
    while not answer:
        try:
            answer = requests.post("http://master/secondaries", json={"hostname": hostname}).json()
            if answer.get("ask", None) == 1:
                app.logger.info(f'The master answered json: {answer}')
        except:
            answer = False
            time.sleep(1)

    app.run(host="0.0.0.0", port=80, debug=True)
