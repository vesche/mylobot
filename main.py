#!/usr/bin/env python

import json
import random
from sanic import Sanic, response

tag = 'mylobot-mark-i'
app = Sanic(name=tag)

@app.route('/', methods=['GET',])
async def index(request):
    return response.json({
        'apiversion': '1',
        'author': 'vesche',
        'color': '#FAEBD7',
        'head': 'fang',
        'tail': 'curled',
        'version': tag,
    })

@app.route('/start', methods=['POST',])
async def start(request):
    print(request.json)
    return response.json({}, status=200)

@app.route('/move', methods=['POST',])
async def move(request):
    print(request.json)
    direction = random.choice(['up', 'down', 'left', 'right'])
    shout = f'I am moving {direction}!'
    return response.json({'move': direction, 'shout': shout}, status=200)

@app.route('/end', methods=['POST',])
async def end(request):
    print(request.json)
    # tear down here?
    return response.json({}, status=200)

def run():
    app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    run()
