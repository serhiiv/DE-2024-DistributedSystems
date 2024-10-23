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


# for save incoming messages
messages = list()
secondaries = set()

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
            answer = requests.post('http://' + str(secondary) + ':80', json={"id": id, "text": text}).json()
            app.logger.info(f'The "{secondary}" answered json: {answer}')
            if answer.get("ask", None) == 1:
                counter += 1

        
        # control counter of sends
        if counter == len(secondaries):
            messages.append(text)
            app.logger.info(f'Added to memory the message:  #{id}  "{text}"')
            return {"ask": 1, "id": id, "text":text}
        else:
            app.logger.error(f'The message "{text}" did not add to the memory')
            return {"ask": 0, "error": f'The message "{text}" did not add to the memory'}


@app.route('/secondaries', methods=['POST', 'GET'])
def second():
    global secondaries

    # return the list of connected secondaries
    if request.method == 'GET':
        app.logger.info(f'Returned from "/secondary" json:  {secondaries}')
        return list(secondaries)

    # add new seconddary to list
    elif request.method == 'POST':
        # load POST to json
        message = request.json
        app.logger.info(f'Received for "/secondary" json:  {message}')

        secondary = message.get("hostname", None)
        secondaries.add(secondary)
        app.logger.info(f'The secondary "{secondary}" add to the list')
        return {"ask": 1, "text": f'The secondary "{secondary}" add to the list'}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
