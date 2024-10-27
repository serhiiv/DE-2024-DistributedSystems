import sys
import requests
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


messages = list()
slaves = set()
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def route_root():
    global messages
    global slaves

    # return the json of messages from memory
    if request.method == 'GET':
        app.logger.info(f'/ answered [get] {messages}')
        return messages

    # add new message
    elif request.method == 'POST':
        # load POST to json
        message = request.json
        app.logger.info(f'/ received [post] {message}')

        text = message['text']
        id = len(messages)

        counter = 0
        # send to slave services
        for slave in slaves:
            app.logger.info(f'Send to "{slave}" the json: #{id} "{text}"')
            answer = requests.post('http://' + str(slave) + ':80', json={"id": id, "text": text}).json()
            app.logger.info(f'The "{slave}" answered json: {answer}')
            if answer.get("ask", None) == 1:
                counter += 1

        
        # control counter of sends
        if counter == len(slaves):
            messages.append(text)
            app.logger.info(f'Added to memory the message:  #{id}  "{text}"')
            return {"ask": 1, "id": id, "text":text}
        else:
            app.logger.error(f'The message "{text}" did not add to the memory')
            return {"ask": 0, "error": f'The message "{text}" did not add to the memory'}


@app.route('/hosts', methods=['POST', 'GET'])
def route_hosts():
    global slaves

    if request.method == 'GET':
        answer = list(slaves)
        app.logger.info(f'/hosts answered [get] {answer}')
        return answer

    elif request.method == 'POST':
        message = request.json
        app.logger.info(f'/hosts received [post] {message}')
        
        slave = message['host']
        slaves.add(slave)
        app.logger.info(f'My slaves {list(slaves)}')

        answer = {"ask": 1, "info": f'The host "{slave}" add to the set'}
        app.logger.info(f'/hosts answered [post] {answer}')
        return answer


if __name__ == '__main__':

    # debug mode
    if len(sys.argv) > 1:
        if sys.argv[1] == '--debug':
            app.run(host="0.0.0.0", port=80, debug=True)

    # deploy mode
    serve(app, host="0.0.0.0", port=80)