import time
from flask import Flask, request
from logging.config import dictConfig

# config for loggining
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s | %(module)s]  %(message)s",
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

time_out = 0

# for save incoming messages
messages = list()


@app.route('/', methods=['POST', 'GET'])
def root():
    global time_out
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
        time.sleep(time_out) # time_out in seconds
        
        id = message.get("id", None)
        text = message.get("text", None)
        while id >= len(messages):
            messages.append(None)
        messages[id] = text

        app.logger.info(f'Add message #{id} "{text}"')
        return {"ask": 1, "id": id, "text":text, "sleep": time_out}


@app.route('/sleep', methods=['POST', 'GET'])
def route_sleep():
    global time_out

    # return sleep time
    if request.method == 'GET':
        app.logger.info(f"Returned sleep time:  {time_out}")
        return {"sleep": time_out}

    # set sleep time
    elif request.method == 'POST':
        message = request.json
        app.logger.info(f'Post message #{message}')
        time_out = int(message.get("sleep", 0))
        app.logger.info(f"Set sleep time:  {time_out} seconds")
        return {"ask": 1, "sleep": time_out}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=False)
