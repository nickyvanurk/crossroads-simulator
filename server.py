#!/usr/bin/env python3

import asyncio
import websockets
import json
from enum import Enum
from eventemitter import EventEmitter

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
  'C3': {
    'origin': 'E',
    'destination': 'N'
  },
  'D1': {
    'origin': 'W',
    'destination': 'N'
  },
  'D2': {
    'origin': 'W',
    'destination': 'E'
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
  'FF1': {
    'origin': 'W',
    'destination': 'W'
  },
  'FF2': {
    'origin': 'W',
    'destination': 'W'
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
  'GF1': {
    'origin': 'S',
    'destination': 'S'
  },
  'GF2': {
    'origin': 'S',
    'destination': 'S'
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
  }
}

emitter = EventEmitter()

road_exceptions = [
  {
    'origin': 'S',
    'destination': 'N',
    'max_green_traffic_lights': 2
  },
  {
    'origin': 'N',
    'destination': 'S',
    'max_green_traffic_lights': 2
  }
]

active_roads = {
  'N': 0,
  'E': 0,
  'S': 0,
  'W': 0,
}

class Color(Enum):
  RED = 0
  ORANGE = 1
  GREEN = 2


class TrafficLight:
  """A traffic light"""

  def __init__(self, id, cardinal_direction):
    self.id = id
    self.state = Color.RED
    self.cardinal_direction = cardinal_direction
    self.has_traffic = False

  async def update(self):
    if self.has_traffic and not self.state == Color.GREEN:
      max_green_traffic_lights = 1

      for road_exception in road_exceptions:
        origin = road_exception['origin']
        destination = road_exception['destination']
        max_green_lights = road_exception['max_green_traffic_lights']

        if (self.cardinal_direction['origin'] == origin and
           self.cardinal_direction['destination'] == destination and
           active_roads[self.cardinal_direction['destination']] < max_green_lights):
          max_green_traffic_lights = max_green_lights

      if active_roads[self.cardinal_direction['destination']] >= max_green_traffic_lights:
        return

      self.change_state(Color.GREEN)
      active_roads[self.cardinal_direction['destination']] += 1
      print(active_roads)

      await asyncio.sleep(6)

      self.change_state(Color.RED)
      active_roads[self.cardinal_direction['destination']] -= 1
      print(active_roads)


  def change_state(self, state):
    self.state = state
    emitter.emit('state-change')

  def get_has_traffic(self, has_traffic):
    return self.has_traffic

  def set_has_traffic(self, has_traffic):
    self.has_traffic = has_traffic


class World:
  """A world containg all traffic lights logic"""

  def __init__(self, websocket, traffic_light_data):
    self.websocket = websocket
    self.traffic_lights = { }
    self.generate_traffic_lights(traffic_light_data)

  def generate_traffic_lights(self, traffic_light_data):
    for id, cardinal_direction in traffic_light_data.items():
      traffic_light_type = id[1]    

      if traffic_light_type == 'B':
        self.traffic_lights[id] = TrafficLight(id, cardinal_direction)
      elif traffic_light_type == 'V':
        self.traffic_lights[id] = TrafficLight(id, cardinal_direction)
      elif traffic_light_type == 'F':
        self.traffic_lights[id] = TrafficLight(id, cardinal_direction)
      else:
        self.traffic_lights[id] = TrafficLight(id, cardinal_direction)

  def process_simulation_state(self, simulation_state):
    for id, traffic_count in simulation_state.items():
      self.traffic_lights[id].set_has_traffic(True if traffic_count > 0 else False)

  async def update(self):
    while True:
      for id, traffic_light in self.traffic_lights.items():
        asyncio.ensure_future(traffic_light.update())

      await asyncio.sleep(1)

  async def send_state(self):
    payload = json.dumps(self.get_state())
    await self.websocket.send(payload)

  def get_state(self):
    state = { }

    for key, traffic_light in self.traffic_lights.items():
      state[key] = traffic_light.state.value
    
    return state

  
async def index(websocket, path):
  world = World(websocket, traffic_light_data)
  emitter.on('state-change', world.send_state)

  async for message in websocket:
    simulation_state = json.loads(message)

    world.process_simulation_state(simulation_state)

    asyncio.ensure_future(world.update())


start_server = websockets.serve(index, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()