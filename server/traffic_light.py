import asyncio
from utils import Color


class TrafficLight:
    """A traffic light"""

    def __init__(self, id, cardinal_direction, emitter, active_roads):
        self.id = id
        self.state = Color.RED
        self.cardinal_direction = cardinal_direction
        self.has_traffic = False
        self.emitter = emitter
        self.active_roads = active_roads

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

            for traffic_light in self.active_roads[self.cardinal_direction['destination']]:
                origin = traffic_light.cardinal_direction['origin']
                destination = traffic_light.cardinal_direction['destination']

                if (self.cardinal_direction['origin'] != origin or
                    self.cardinal_direction['destination'] != destination):
                    break

                max_green_traffic_lights = 20

            if len(self.active_roads[self.cardinal_direction['destination']]) >= max_green_traffic_lights:
                return

            for cardinal_direction in self.active_roads:
                for traffic_light in self.active_roads[cardinal_direction]:
                    if not self.can_cross(self.cardinal_direction,
                                                             traffic_light.cardinal_direction):
                        return

            if (self.is_bus() and self.cardinal_direction['destination'] == 'N' and
                 len(self.active_roads[self.cardinal_direction['destination']])):
                return

            if (self.is_bus() and self.cardinal_direction['destination'] == 'N' and
                 len(self.active_roads['E']) > 0):
                return

            if (self.is_car()):
                for traffic_light in self.active_roads[self.cardinal_direction['destination']]:
                    if traffic_light.is_bus():
                        return

                if self.cardinal_direction['destination'] == 'E':
                    for traffic_light in self.active_roads['N']:
                        if traffic_light.is_bus():
                            return

            self.emitter.emit('green-traffic-light', self.id)
            self.change_state(Color.GREEN)
            self.active_roads[self.cardinal_direction['destination']].append(self)

            await asyncio.sleep(8)

            self.emitter.emit('orange-traffic-light', self.id)
            self.change_state(Color.ORANGE)

            await asyncio.sleep(3.5)

            self.emitter.emit('red-traffic-light', self.id)
            self.change_state(Color.RED)
            self.active_roads[self.cardinal_direction['destination']].remove(self)

    def change_state(self, state):
        self.state = state
        self.emitter.emit('state-change')

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
