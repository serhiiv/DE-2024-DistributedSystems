import sys
import time
from flask import Flask, request
from waitress import serve
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

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def root():
    global messages

    # GET method - returns all replicated messages from the in-memory list
    if request.method == 'GET':
        # select messages until first 'None'
        answer = list()
        for m in messages:
            if m is None:
                break
            answer.append(m)
        return answer

    # add new message
    elif request.method == 'POST':
        message = request.json

        id = message['id']
        text = message['text']
        while id >= len(messages):
            messages.append(None)
        messages[id] = text

        app.logger.info(f'Add message #{id} "{text}"')
        return {"ask": 1, "id": id, "text":text}


if __name__ == '__main__':

    # debug mode
    if len(sys.argv) > 1:
        if sys.argv[1] == '--debug':
            app.run(host="0.0.0.0", port=80, debug=True)

    # deploy mode
    serve(app, host="0.0.0.0", port=80)
