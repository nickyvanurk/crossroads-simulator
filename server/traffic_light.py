import asyncio
from utils import Color


class TrafficLight:
    """A traffic light"""

    def __init__(self, id, cardinals, emitter, active_roads):
        self.id = id
        self.state = Color.RED
        self.cardinals = cardinals
        self.emitter = emitter
        self.active_roads = active_roads

        self.has_traffic = False

        self.green_time = 8
        self.orange_time = 3.5

    def is_intersect(self, dir1, dir2, card1, card2, card3, card4):
        return ((dir1['origin'] == card1 and dir1['destination'] == card2 and
                 dir2['origin'] == card3 and dir2['destination'] == card4) or
                (dir2['origin'] == card1 and dir2['destination'] == card2 and
                 dir1['origin'] == card3 and dir1['destination'] == card4))

    def is_intersect_other(self, traffic_light):
        c1 = self.cardinals
        c2 = traffic_light.cardinals

        return (self.is_intersect(c1, c2, 'N', 'E', 'S', 'N') or
                self.is_intersect(c1, c2, 'N', 'E', 'E', 'W') or
                self.is_intersect(c1, c2, 'N', 'E', 'W', 'N') or
                self.is_intersect(c1, c2, 'N', 'E', 'E', 'S') or
                self.is_intersect(c1, c2, 'S', 'W', 'N', 'S') or
                self.is_intersect(c1, c2, 'S', 'W', 'N', 'E') or
                self.is_intersect(c1, c2, 'S', 'W', 'W', 'E') or
                self.is_intersect(c1, c2, 'E', 'S', 'S', 'N') or
                self.is_intersect(c1, c2, 'E', 'S', 'S', 'W') or
                self.is_intersect(c1, c2, 'W', 'E', 'S', 'N') or
                self.is_intersect(c1, c2, 'W', 'E', 'N', 'S') or
                self.is_intersect(c1, c2, 'W', 'E', 'E', 'S') or
                self.is_intersect(c1, c2, 'W', 'N', 'E', 'W') or
                self.is_intersect(c1, c2, 'W', 'N', 'S', 'W') or
                self.is_intersect(c1, c2, 'W', 'N', 'N', 'S') or
                self.is_intersect(c1, c2, 'W', 'N', 'E', 'S') or
                self.is_intersect(c1, c2, 'E', 'W', 'N', 'S') or
                self.is_intersect(c1, c2, 'E', 'W', 'N', 'W') or
                self.is_intersect(c1, c2, 'E', 'W', 'S', 'N') or
                self.is_intersect(c1, c2, 'E', 'W', 'S', 'W') or
                self.is_intersect(c1, c2, 'E', 'N', 'S', 'N') or
                self.is_intersect(c1, c2, 'N', 'E', 'N', 'N') or
                self.is_intersect(c1, c2, 'N', 'S', 'N', 'N') or
                self.is_intersect(c1, c2, 'N', 'W', 'N', 'N') or
                self.is_intersect(c1, c2, 'W', 'E', 'W', 'W') or
                self.is_intersect(c1, c2, 'W', 'N', 'W', 'W') or
                self.is_intersect(c1, c2, 'W', 'S', 'W', 'W') or
                self.is_intersect(c1, c2, 'S', 'E', 'S', 'S') or
                self.is_intersect(c1, c2, 'S', 'N', 'S', 'S') or
                self.is_intersect(c1, c2, 'S', 'W', 'S', 'S') or
                self.is_intersect(c1, c2, 'N', 'S', 'N', 'W') or
                self.is_intersect(c1, c2, 'S', 'E', 'S', 'E'))

    async def update(self):
        if self.has_traffic and not self.is_green():
            for destination, traffic_lights in self.active_roads.items():
                for traffic_light in traffic_lights:
                    if ((destination == self.cardinals['destination'] and
                         not self.sameCardinals(traffic_light)) or
                        self.is_intersect_other(traffic_light)):
                        return

            if self.is_bus() and self.cardinals['destination'] == 'N':
                if (len(self.active_roads['N']) or
                    len(self.active_roads['E'])):
                    return

            if (self.is_car()):
                for traffic_light in self.active_roads[self.cardinals['destination']]:
                    if traffic_light.is_bus():
                        return

                if self.cardinals['destination'] == 'E':
                    for traffic_light in self.active_roads['N']:
                        if traffic_light.is_bus():
                            return

            self.set_green()
            self.active_roads[self.cardinals['destination']].append(self)
            await asyncio.sleep(self.green_time)

            self.set_orange()
            await asyncio.sleep(self.orange_time)

            self.set_red()
            self.active_roads[self.cardinals['destination']].remove(self)

    def change_state(self, state):
        self.state = state
        self.emitter.emit('state-change')

    def get_has_traffic(self, has_traffic):
        return self.has_traffic

    def set_has_traffic(self, has_traffic):
        self.has_traffic = has_traffic

    def is_red(self):
        return self.state == Color.RED

    def is_green(self):
        return self.state == Color.GREEN

    def is_bus(self):
        return self.id[1] == 'B'

    def is_car(self):
        return len(self.id) == 2

    def sameCardinals(self, traffic_light):
        c1 = self.cardinals
        c2 = traffic_light.cardinals

        return (c1['origin'] == c2['origin'] and
                c1['destination'] == c2['destination'])

    def set_green(self):
        self.emitter.emit('green-traffic-light', self.id)
        self.change_state(Color.GREEN)
        self.active_roads[self.cardinals['destination']].append(self)

    def set_orange(self):
        self.emitter.emit('orange-traffic-light', self.id)
        self.change_state(Color.ORANGE)

    def set_red(self):
        self.emitter.emit('red-traffic-light', self.id)
        self.change_state(Color.RED)
