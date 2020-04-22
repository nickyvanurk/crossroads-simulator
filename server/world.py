import asyncio
import json
import time
from eventemitter import EventEmitter
from collections import OrderedDict
from traffic_light import TrafficLight


class World:
    """A world containg all traffic lights logic"""

    def __init__(self, websocket, traffic_light_data):
        self.websocket = websocket
        self.traffic_lights = OrderedDict()
        self.emitter = EventEmitter()
        self.active_roads = {'N': [], 'E': [], 'S': [], 'W': []}

        self.traffic_lights_to_move_to_end = []

        self.start_time = time.time()
        self.clearance_time = 6
        self.allow_green = True

        self.generate_traffic_lights(traffic_light_data)

        self.emitter.on('state-change', self.send_state)
        self.emitter.on('red-traffic-light', self.red_traffic_light_event)
        self.emitter.on('orange-traffic-light', self.orange_traffic_light_event)
        self.emitter.on('green-traffic-light', self.green_traffic_light_event)

    def generate_traffic_lights(self, traffic_light_data):
        for id, cardinal_direction in traffic_light_data.items():
            traffic_light_type = id[1]

            if traffic_light_type == 'B':
                self.traffic_lights[id] = TrafficLight(id, cardinal_direction, self.emitter, self.active_roads)
            elif traffic_light_type == 'V':
                self.traffic_lights[id] = TrafficLight(id, cardinal_direction, self.emitter, self.active_roads)
            elif traffic_light_type == 'F':
                self.traffic_lights[id] = TrafficLight(id, cardinal_direction, self.emitter, self.active_roads)
            else:
                self.traffic_lights[id] = TrafficLight(id, cardinal_direction, self.emitter, self.active_roads)

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
        state = {}

        for key, traffic_light in self.traffic_lights.items():
            state[key] = traffic_light.state.value

        return state
