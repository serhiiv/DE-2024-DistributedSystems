import os
import requests
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


# for save incoming messages
messages = list()

# make list with secondary services
number_secondaries = int(os.environ.get("NUMBER_SECONDARIES", default=0))
secondaries = ['http://secondary'+str(i+1)+':80' for i in range(number_secondaries)]


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def root():
    global messages
    global secondaries

    # return the json of messages from memory
    if request.method == 'GET':
        app.logger.info(f"Returned json:  {messages}")
        return messages

    # add new message
    elif request.method == 'POST':
        # load POST to json
        message = request.json
        app.logger.info(f'Received json:  {message}')

        text = message.get("text", None)
        id = len(messages)

        counter=0
        # send to secondary services
        for secondary in secondaries:
            app.logger.info(f'Send to "{secondary}" the json: #{id} "{text}"')
            answer = requests.post(secondary, json={"id": id, "text": text}).json()
            app.logger.info(f'The "{secondary}" answered json: {answer}')
            if answer.get("ask", None) == 1:
                counter += 1

        
        # control counter of sends
        if counter == number_secondaries:
            messages.append(text)
            app.logger.info(f'Added to memory the message:  #{id}  "{text}"')
            return {"ask": 1, "id": id, "text":text}
        else:
            app.logger.error(f'The message "{text}" did not add to the memory')
            return {"ask": 0, "error": f'The message "{text}" did not add to the memory'}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=False)
