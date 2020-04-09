#!/usr/bin/env python3

import asyncio
import websockets
import json
import time
from enum import Enum
from eventemitter import EventEmitter
from collections import OrderedDict

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

active_roads = {
  'N': [],
  'E': [],
  'S': [],
  'W': [],
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

  def is_intersect(self, dir1, dir2, card1, card2, card3, card4):
    return ((dir1['origin'] == card1 and dir1['destination'] == card2 and
             dir2['origin'] == card3 and dir2['destination'] == card4) or
            (dir2['origin'] == card1 and dir2['destination'] == card2 and
             dir1['origin'] == card3 and dir1['destination'] == card4))

  def can_cross(self, dir1, dir2):
    if (self.is_intersect(dir1, dir2, 'N', 'E', 'S', 'N') or
        self.is_intersect(dir1, dir2, 'N', 'E', 'E', 'W') or
        self.is_intersect(dir1, dir2, 'N', 'E', 'W', 'N') or
        self.is_intersect(dir1, dir2, 'N', 'E', 'E', 'S') or
        self.is_intersect(dir1, dir2, 'S', 'W', 'N', 'S') or
        self.is_intersect(dir1, dir2, 'S', 'W', 'N', 'E') or
        self.is_intersect(dir1, dir2, 'S', 'W', 'W', 'E') or
        self.is_intersect(dir1, dir2, 'E', 'S', 'S', 'N') or
        self.is_intersect(dir1, dir2, 'E', 'S', 'S', 'W') or
        self.is_intersect(dir1, dir2, 'W', 'E', 'S', 'N') or
        self.is_intersect(dir1, dir2, 'W', 'E', 'N', 'S') or
        self.is_intersect(dir1, dir2, 'W', 'E', 'E', 'S') or
        self.is_intersect(dir1, dir2, 'W', 'N', 'E', 'W') or
        self.is_intersect(dir1, dir2, 'W', 'N', 'S', 'W') or
        self.is_intersect(dir1, dir2, 'W', 'N', 'N', 'S') or
        self.is_intersect(dir1, dir2, 'W', 'N', 'E', 'S') or
        self.is_intersect(dir1, dir2, 'E', 'W', 'N', 'S') or
        self.is_intersect(dir1, dir2, 'E', 'W', 'N', 'W') or
        self.is_intersect(dir1, dir2, 'E', 'W', 'S', 'N') or
        self.is_intersect(dir1, dir2, 'E', 'W', 'S', 'W') or
        self.is_intersect(dir1, dir2, 'E', 'N', 'S', 'N') or
        self.is_intersect(dir1, dir2, 'N', 'E', 'N', 'N') or
        self.is_intersect(dir1, dir2, 'N', 'S', 'N', 'N') or
        self.is_intersect(dir1, dir2, 'N', 'W', 'N', 'N') or
        self.is_intersect(dir1, dir2, 'W', 'E', 'W', 'W') or
        self.is_intersect(dir1, dir2, 'W', 'N', 'W', 'W') or
        self.is_intersect(dir1, dir2, 'W', 'S', 'W', 'W') or
        self.is_intersect(dir1, dir2, 'S', 'E', 'S', 'S') or
        self.is_intersect(dir1, dir2, 'S', 'N', 'S', 'S') or
        self.is_intersect(dir1, dir2, 'S', 'W', 'S', 'S') or
        self.is_intersect(dir1, dir2, 'N', 'S', 'N', 'W') or
        self.is_intersect(dir1, dir2, 'S', 'E', 'S', 'E')):
      return False

    return True

  async def update(self):
    if self.has_traffic and not self.state == Color.GREEN:
      max_green_traffic_lights = 1

      for traffic_light in active_roads[self.cardinal_direction['destination']]:
        origin = traffic_light.cardinal_direction['origin']
        destination = traffic_light.cardinal_direction['destination']

        if (self.cardinal_direction['origin'] != origin or
          self.cardinal_direction['destination'] != destination):
          break

        max_green_traffic_lights = 20

      if len(active_roads[self.cardinal_direction['destination']]) >= max_green_traffic_lights:
        return

      for cardinal_direction in active_roads:
        for traffic_light in active_roads[cardinal_direction]:
          if not self.can_cross(self.cardinal_direction,
                               traffic_light.cardinal_direction):
            return

      if (self.is_bus() and self.cardinal_direction['destination'] == 'N' and
         len(active_roads[self.cardinal_direction['destination']])):
        return

      if (self.is_bus() and self.cardinal_direction['destination'] == 'N' and
         len(active_roads['E']) > 0):
        return

      if (self.is_car()):
        for traffic_light in active_roads[self.cardinal_direction['destination']]:
          if traffic_light.is_bus():
            return

        if self.cardinal_direction['destination'] == 'E':
          for traffic_light in active_roads['N']:
            if traffic_light.is_bus():
              return

      emitter.emit('green-traffic-light', self.id)
      self.change_state(Color.GREEN)
      active_roads[self.cardinal_direction['destination']].append(self)

      await asyncio.sleep(8)

      emitter.emit('orange-traffic-light', self.id)
      self.change_state(Color.ORANGE)

      await asyncio.sleep(3.5)

      emitter.emit('red-traffic-light', self.id)
      self.change_state(Color.RED)
      active_roads[self.cardinal_direction['destination']].remove(self)

  def change_state(self, state):
    self.state = state
    emitter.emit('state-change')

  def get_has_traffic(self, has_traffic):
    return self.has_traffic

  def set_has_traffic(self, has_traffic):
    self.has_traffic = has_traffic

  def is_red(self):
    return self.state == Color.RED

  def is_bus(self):
    return self.id[1] == 'B'

  def is_car(self):
    return len(self.id) == 2

class World:
  """A world containg all traffic lights logic"""

  def __init__(self, websocket, traffic_light_data):
    self.websocket = websocket
    self.traffic_lights = OrderedDict()
    self.generate_traffic_lights(traffic_light_data)

    self.traffic_lights_to_move_to_end = [];

    self.start_time = time.time()
    self.clearance_time = 6
    self.allow_green = True

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
      self.traffic_lights[id.upper()].set_has_traffic(True if int(traffic_count) > 0 else False)

  async def update(self):
    while True:
      elapsed_time = time.time() - self.start_time

      for id, traffic_light in self.traffic_lights.items():
        if elapsed_time > self.clearance_time and self.allow_green:
          asyncio.create_task(traffic_light.update())

      for id in self.traffic_lights_to_move_to_end:
        self.traffic_lights.move_to_end(id)
        self.traffic_lights_to_move_to_end.remove(id)

      await asyncio.sleep(0.016)

  async def send_state(self):
    payload = json.dumps(self.get_state())

    # print(payload)

    await self.websocket.send(payload)

  def red_traffic_light_event(self, id):
    self.start_time = time.time()

    if self.is_all_traffic_lights_red():
      self.allow_green = True

  def orange_traffic_light_event(self, id):
    pass

  def green_traffic_light_event(self, id):
    self.traffic_lights_to_move_to_end.append(id);

    self.allow_green = False

  def is_all_traffic_lights_red(self):
    for id, traffic_light in self.traffic_lights.items():
      if not traffic_light.is_red():
        return False

    return True

  def get_state(self):
    state = { }

    for key, traffic_light in self.traffic_lights.items():
      state[key] = traffic_light.state.value

    return state


async def index(websocket, path):
  world = World(websocket, traffic_light_data)
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


# async def index():
#     uri = "ws://serene-woodland-92641.herokuapp.com/?group=14&type=controller"
#     async with websockets.connect(uri) as websocket:
#         world = World(websocket, traffic_light_data)
#         emitter.on('state-change', world.send_state)
#         emitter.on('red-traffic-light', world.red_traffic_light_event)
#         emitter.on('green-traffic-light', world.green_traffic_light_event)

#         print('Connected')


#         message = await websocket.recv()
#         simulation_state = json.loads(message)

#         # print(simulation_state)

#         world.process_simulation_state(simulation_state)
#         asyncio.ensure_future(world.update())

# asyncio.get_event_loop().run_until_complete(index())

start_server = websockets.serve(index, '127.0.0.1', 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
