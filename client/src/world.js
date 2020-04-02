import trafficLightsData from './data/traffic_lights.json';
import TrafficLight from './traffic_light';
import roadsData from './data/roads';
import Road from './road';

class World {
  constructor() {
    this.canvas = document.getElementById('canvas');
    this.ctx = canvas.getContext('2d');

    this.ctx.canvas.width  = 937;
    this.ctx.canvas.height = 829;

    this.traffic_lights = {};
    this.roads = [];
    this.isReady = false;

    this.init();

    // window.addEventListener('mousemove', this.onmousemove);
  }

  init() {
    this.generateTrafficLights(trafficLightsData);
    this.generateRoads(roadsData);

    this.roads[0].spawnCar();

    this.isReady = true;
  }

  update() {
    if (!this.isReady) return;

    for (const road of this.roads) {
      const traffic_lights = [];

      Object.keys(this.traffic_lights)
        .filter(key => road.getTrafficLightIds().includes(key))
        .forEach(key => traffic_lights.push(this.traffic_lights[key]));

      for (const car of road.getCars()) {
        for (const traffic_light of traffic_lights) {
          if (this.isWithinRadius(car, traffic_light)) {
            if (car.isMoving() && traffic_light.isRed()) {
              car.stop();
            }

            if (!car.isMoving() && traffic_light.isGreen()) {
              car.start();
            }
          }
        }
      }
    }
  }

  draw() {
    if (!this.isReady) return;

    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    for (const road of this.roads) {
      for (const car of road.getCars()) {
        car.draw(this.ctx);
      }
    }

    for (const index in this.traffic_lights) {
      this.traffic_lights[index].draw(this.ctx);
    }
  }

  onmousemove(event) {
    const rect = this.canvas.getBoundingClientRect();
    const pos = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };

    console.log(pos);
  }

  generateTrafficLights(data) {
    for (const [traffic_light_id, coordinates] of Object.entries(data)) {
      this.traffic_lights[traffic_light_id] = new TrafficLight(coordinates);
    }
  }

  generateRoads(data) {
    for (const [roadId, traffic_light_ids] of Object.entries(data)) {
      this.roads.push(new Road(roadId, traffic_light_ids));
    }
  }

  processState(state) {
    if (!this.isReady) return;


    for (const [key, traffic_light_state] of Object.entries(state)) {
      this.traffic_lights[key].changeState(parseInt(traffic_light_state));
    }

    this.draw();
  }

  isWithinRadius(unit, traffic_light) {
    const pos1 = unit.getPosition();
    const pos2 = traffic_light.getPosition();

    const distance = Math.sqrt(Math.pow(Math.abs(pos1.x - pos2.x), 2) +
                               Math.pow(Math.abs(pos1.y - pos2.y), 2));

    return distance <= traffic_light.getStopRadius();
  }
}

const world = new World;

export { world as default };
