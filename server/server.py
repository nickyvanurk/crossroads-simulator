#!/usr/bin/env python3

import asyncio
import websockets
import json
from world import World


async def index(websocket, path):
    with open('./data/traffic_lights.json', 'r') as file:
        traffic_light_data = json.load(file)

    world = World(websocket, traffic_light_data)

    print('Connected')

    async for message in websocket:
        simulation_state = json.loads(message)
        world.process_simulation_state(simulation_state)
        asyncio.ensure_future(world.update())


start_server = websockets.serve(index, '127.0.0.1', 8080, ping_interval=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
