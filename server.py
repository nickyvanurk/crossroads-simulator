#!/usr/bin/env python3

import asyncio
import websockets
import json
from enum import Enum

# traffic_light_ids = ['A1','A2','A3','A4','AB1','AB2','B1','B2','B3','B4','B5','BB1','C1','C2','C3','D1','D2','D3','E1','E2','EV1','EV2','EV3','EV4','FV1','FV2','FV3','FV4','FF1','FF2','GV1','GV2','GV3','GV4','GF1','GF2']
# traffic_light_groups = ['A2','A3','A4','B2','B3','B4',   'C2','C3','D2','D3',   'A1','E1','E2','EV1','EV2','EV3','EV4',    'B1','FV1','FV2','FV3','FV4','FF1','FF2','GV1','GV2','GV3','GV4','GF1','GF2',    'C1','E1','E2','EV1','EV2','EV3','EV4','FV1','FV2','FV3','FV4','FF1','FF2',    'D1','GV1','GV2','GV3','GV4','GF1','GF2']

traffic_light_data = {
  'A1': {
    'origin': 'S',
    'destination': 'W'
  },
  'A2': {
    'origin': 'S',
    'destination': 'N'
  },
  'A3': {
    'origin': 'S',
    'destination': 'N'
  },
  'A4': {
    'origin': 'S',
    'destination': 'E'
  },
  'AB1': {
    'origin': 'S',
    'destination': 'N'
  },
  'AB2': {
    'origin': 'S',
    'destination': 'E'
  },
  'B1': {
    'origin': 'N',
    'destination': 'E'
  },
  'B2': {
    'origin': 'N',
    'destination': 'S'
  },
  'B3': {
    'origin': 'N',
    'destination': 'S'
  },
  'B4': {
    'origin': 'N',
    'destination': 'W'
  },
  'B5': {
    'origin': 'W',
    'destination': 'W'
  },
  'BB1': {
    'origin': 'N',
    'destination': 'S'
  },
  'C1': {
    'origin': 'E',
    'destination': 'S'
  },
  'C2': {
    'origin': 'E',
    'destination': 'W'
  },
  'D3': {
    'origin': 'W',
    'destination': 'S'
  },
  'E1': {
    'origin': 'N',
    'destination': 'N'
  },
  'E2': {
    'origin': 'N',
    'destination': 'N'
  },
  'EV1': {
    'origin': 'N',
    'destination': 'N'
  },
  'EV2': {
    'origin': 'N',
    'destination': 'N'
  },
  'EV3': {
    'origin': 'N',
    'destination': 'N'
  },
  'EV4': {
    'origin': 'N',
    'destination': 'N'
  },
  'FV1': {
    'origin': 'W',
    'destination': 'W'
  },
  'FV2': {
    'origin': 'W',
    'destination': 'W'
  },
  'FV3': {
    'origin': 'W',
    'destination': 'W'
  },
  'FV4': {
    'origin': 'W',
    'destination': 'W'
  },
  'FF1': {
    'origin': 'W',
    'destination': 'W'
  },
  'FF2': {
    'origin': 'W',
    'destination': 'W'
  },
  'GV1': {
    'origin': 'S',
    'destination': 'S'
  },
  'GV2': {
    'origin': 'S',
    'destination': 'S'
  },
  'GV3': {
    'origin': 'S',
    'destination': 'S'
  },
  'GV4': {
    'origin': 'S',
    'destination': 'S'
  },
  'GF1': {
    'origin': 'S',
    'destination': 'S'
  },
  'GF2': {
    'origin': 'S',
    'destination': 'S'
  }
}


class Color(Enum):
  RED = 0
  ORANGE = 1
  GREEN = 2


class CarTrafficLight:
  """A car traffic light"""

  def __init__(self, id):
    self.id = id
    self.state = Color.RED

  def change_state(self, state):
    self.state = state


class BusTrafficLight:
  """A bus traffic light"""

  def __init__(self, id):
    self.id = id
    self.state = Color.RED

  def change_state(self, state):
    self.state = state


class PedestrianTrafficLight:
  """A pedestrian traffic light"""

  def __init__(self, id):
    self.id = id
    self.state = Color.RED

  def change_state(self, state):
    self.state = state


class CycleTrafficLight:
  """A cycle traffic light"""

  def __init__(self, id):
    self.id = id
    self.state = Color.RED

  def change_state(self, state):
    self.state = state


class World:
  """A world containg all traffic lights logic"""

  def __init__(self, traffic_light_data):
    self.traffic_lights = { }
    self.generate_traffic_lights(traffic_light_data)

  def generate_traffic_lights(self, traffic_light_data):
    for id, cardinal_directions in traffic_light_data.items():
      traffic_light_type = id[1]    

      if traffic_light_type == 'B':
        self.traffic_lights[id] = BusTrafficLight(id)
      elif traffic_light_type == 'V':
        self.traffic_lights[id] = PedestrianTrafficLight(id)
      elif traffic_light_type == 'F':
        self.traffic_lights[id] = CycleTrafficLight(id)
      else:
        self.traffic_lights[id] = CarTrafficLight(id)

  def get_state(self):
    state = { }

    for key, traffic_light in self.traffic_lights.items():
      state[key] = traffic_light.state.value
    
    return state
    
  
async def index(websocket, path):
  world = World(traffic_light_data)

  async for message in websocket:
    data = json.loads(message)

    print(f"< {data}")

    payload = json.dumps(world.get_state())
    await websocket.send(payload)


start_server = websockets.serve(index, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()