#!/usr/bin/env python3

import asyncio
import websockets
import json
from eventemitter import EventEmitter
from world import World


async def index(websocket, path):
    with open('./data/traffic_lights.json', 'r') as file:
        traffic_light_data = json.load(file)

    emitter = EventEmitter()
    active_roads = { 'N': [], 'E': [], 'S': [], 'W': [] }

    world = World(websocket, traffic_light_data, emitter, active_roads)
    emitter.on('state-change', world.send_state)
    emitter.on('red-traffic-light', world.red_traffic_light_event)
    emitter.on('orange-traffic-light', world.orange_traffic_light_event)
    emitter.on('green-traffic-light', world.green_traffic_light_event)

    print('Connected')

    async for message in websocket:
        simulation_state = json.loads(message)

        # print(simulation_state)

        world.process_simulation_state(simulation_state)

        asyncio.ensure_future(world.update())


start_server = websockets.serve(index, '127.0.0.1', 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
