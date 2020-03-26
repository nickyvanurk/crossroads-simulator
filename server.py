#!/usr/bin/env python3

import asyncio
import websockets
import json
from enum import Enum

traffic_light_ids = ['A1','A2','A3','A4','AB1','AB2','B1','B2','B3','B4','B5','BB1','C1','C2','C3','D1','D2','D3','E1','E2','EV1','EV2','EV3','EV4','FV1','FV2','FV3','FV4','FF1','FF2','GV1','GV2','GV3','GV4','GF1','GF2']

class Color(Enum):
  RED = 0
  ORANGE = 1
  GREEN = 2


class CarTrafficLight:
  """A car traffic light"""

  def __init__(self, name):
    self.name = name
    self.state = Color.RED

  def change_state(self, state):
    self.state = state


class World:
  """A world containg all traffic lights logic"""

  def __init__(self, traffic_light_ids):
    self.traffic_lights = { }
    self.generate_traffic_lights(traffic_light_ids)

  def generate_traffic_lights(self, traffic_light_ids):
    for id in traffic_light_ids:
      traffic_light_type = id[1]    

      if traffic_light_type == 'B':
        # Bus
        pass
      elif traffic_light_type == 'V':
        # Walk
        pass
      elif traffic_light_type == 'F':
        # Bike
        pass
      else:
        # Car
        self.traffic_lights[id] = CarTrafficLight(id)

  def get_state(self):
    state = { }

    for key, traffic_light in self.traffic_lights.items():
      state[key] = traffic_light.state.value
    
    return state
    

  
async def index(websocket, path):
  world = World(traffic_light_ids)

  async for message in websocket:
    data = json.loads(message)

    print(f"< {data}")

    payload = json.dumps(world.get_state())
    await websocket.send(payload)

start_server = websockets.serve(index, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()