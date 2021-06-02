#!/usr/bin/env python

import os
import json
import random
from sanic import Sanic, response

tag = 'mylobot-mark-i'
app = Sanic(name=tag)

class Game:
    def __init__(self):
        self.turn = int()
        self.height = int()
        self.width = int()
        self.opponents = list()
        self.food = list()
        self.health = int()
        self.body = list()
        self.head = dict()
        self.length = int()

    def process_incoming(self, request):
        self.turn = request.json['turn']
        self.height = request.json['board']['height']
        self.width = request.json['board']['width']
        self.opponents = [s for s in request.json['board']['snakes'] if s['name'] != tag]
        self.food = request.json['board']['food']
        self.health = request.json['you']['health']
        self.body = request.json['you']['body']
        self.head = request.json['you']['head']
        self.length = request.json['you']['length']

game = Game()

@app.route('/', methods=['GET',])
async def index(request):
    return response.json({
        'apiversion': '1',
        'author': 'vesche',
        'color': '#FF69FF',
        'head': 'fang',
        'tail': 'curled',
        'version': tag,
    })

@app.route('/start', methods=['POST',])
async def start(request):
    process_incoming(request)
    print('****** START', game.__dict__)
    return response.json({}, status=200)

@app.route('/move', methods=['POST',])
async def move(request):
    process_incoming(request)
    print('****** MOVE', game.__dict__)
    direction = random.choice(['up', 'down', 'left', 'right'])
    shout = f'I am moving {direction}!'
    return response.json({'move': direction, 'shout': shout}, status=200)

@app.route('/end', methods=['POST',])
async def end(request):
    print('****** END', request.json)
    return response.json({}, status=200)

def run():
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))

if __name__ == '__main__':
    run()
