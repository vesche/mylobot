#!/usr/bin/env python

import os
import json
import random
from sanic import Sanic, response

tag = 'mylobot-mark-i'
app = Sanic(name=tag)

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collision = False
    def __str__(self):
        return f'Coord(x={self.x}, y={self.y})'
    def __repr__(self):
        return f'Coord(x={self.x}, y={self.y})'

class Game:
    def __init__(self):
        self.stack = list()

    def process_incoming(self, request):
        self.turn = request.json['turn']
        self.height = request.json['board']['height']
        self.width = request.json['board']['width']
        self.opponents = [s for s in request.json['board']['snakes'] if s['name'] != tag]
        self.opponents_coords = [Coord(c['x'], c['y']) for c in sum([opponent['body'] for opponent in self.opponents], [])]
        self.food = request.json['board']['food']
        self.health = request.json['you']['health']
        self.body = request.json['you']['body']
        self.body_coords = [Coord(c['x'], c['y']) for c in self.body]
        self.head_x = request.json['you']['head']['x']
        self.head_y = request.json['you']['head']['y']
        self.length = request.json['you']['length']

    def runner(self):
        if self.stack:
            return self.stack.pop(0)
        awc = self.anti_wall_collision()
        if awc:
            return awc
        return self.moving

    def anti_wall_collision(self):
        coordinates = dict(
            up = Coord(self.head_x, self.head_y+1),
            down = Coord(self.head_x, self.head_y-1),
            left = Coord(self.head_x-1, self.head_y),
            right = Coord(self.head_x+1, self.head_y),
        )
        # evaluate collisions
        for direction, coord in coordinates.items():
            if (coord.x >= self.width) or (coord.x == 0) or (coord.y >= self.height) or (coord.y == 0):
                coord.collision = True
            if (coord.x, coord.y) in [(c.x, c.y) for c in self.body_coords]:
                coord.collision = True
            if (coord.x, coord.y) in [(c.x, c.y) for c in self.opponents_coords]:
                coord.collision = True
        # leggo
        # return random.choice([direction for direction, coord in coordinates.items() if not coord.collision])

        foo = list()
        for direction, coord in coordinates.items():
            if not coord.collision:
                foo.append(direction)
        return random.choice(foo)

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
    game.process_incoming(request)
    print('****** START', game.__dict__)
    return response.json({}, status=200)

@app.route('/move', methods=['POST',])
async def move(request):
    game.process_incoming(request)
    print('****** MOVE', game.__dict__)
    direction = game.runner()
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
