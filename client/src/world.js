import trafficLightsData from './data/traffic_lights.json';
import TrafficLight from './traffic_light';
import roadsData from './data/roads';
import Road from './road';
import { filterObjectByKeys } from './utils';

class World {
  constructor(size) {
    this.size = size;

    this.trafficLights = {};
    this.roads = [];
    this.ready = false;
    this.stateUpdate = false;
  }

  init() {
    this.generateTrafficLights(trafficLightsData);
    this.generateRoads(roadsData);

    for (const road of this.roads) {
      setInterval(() => {
        this.spawnTraffic(road);
      }, road.spawnTimer);
    }

    this.ready = true;
  }

  update() {
    this.stateUpdate = false;

    for (const road of this.roads) {
      road.update(this.size);

      const keys = road.getTrafficLightIds();
      const traffic_lights = filterObjectByKeys(this.trafficLights, keys);

      for (const car of road.getCars()) {
        for (const [key, traffic_light] of Object.entries(traffic_lights)) {
          if (traffic_light.isUnitWithinQueueRadius(car) &&
              !car.isTrafficLightInQueue(key) &&
              !car.isPassedTrafficLight(key)) {
            traffic_light.incrementQueue();
            car.addTrafficLightToQueue(key);
            this.stateUpdate = true;
          }

          if (traffic_light.isUnitWithinStopRadius(car) &&
              car.isTrafficLightInQueue(key) &&
              !car.isPassedTrafficLight(key)) {
            if (car.isMoving() && traffic_light.isRed()) {
              car.stop();
            }

            if (car.isMoving() && traffic_light.isGreen()) {
              car.deleteTrafficLightFromQueue(key);
              traffic_light.decrementQueue();
              this.stateUpdate = true;
            }

            if (!car.isMoving() && traffic_light.isGreen()) {
              car.start();
              car.deleteTrafficLightFromQueue(key);
              traffic_light.decrementQueue();
              this.stateUpdate = true;
            }
          }
        }
      }
    }
  }

  draw(ctx) {
    ctx.clearRect(0, 0, this.size.w, this.size.h);

    for (const road of this.roads) {
      for (const car of road.getCars()) {
        car.draw(ctx);
      }
    }

    for (const key in this.trafficLights) {
      this.trafficLights[key].draw(ctx);
    }
  }

  generateTrafficLights(data) {
    for (const [key, values] of Object.entries(data)) {
      this.trafficLights[key] = new TrafficLight(values.position,
                                                 values.queueRadius,
                                                 values.stopRadius);
    }
  }

  generateRoads(data) {
    for (const [key, values] of Object.entries(data)) {
      this.roads.push(new Road(key, values.type, values.trafficLightIds, values.spawnTimer));
    }
  }

  processState(state) {
    for (const [key, traffic_light_state] of Object.entries(state)) {
      this.trafficLights[key].changeState(parseInt(traffic_light_state));
    }
  }

  isWithinRadius(unit, traffic_light) {
    const pos1 = unit.getPosition();
    const pos2 = traffic_light.getPosition();

    const distance = Math.sqrt(Math.pow(Math.abs(pos1.x - pos2.x), 2) +
                               Math.pow(Math.abs(pos1.y - pos2.y), 2));

    return distance <= traffic_light.getStopRadius();
  }

  getState() {
    let data = {};

    for (const [traffic_light_id, traffic_light] of Object.entries(this.trafficLights)) {
      data[traffic_light_id] = traffic_light.getQueuedUnits();
    }

    return data;
  }

  spawnTraffic(road) {
    if (road.hasTraffic()) {
      const lastCar = road.getLastCar();

      if (lastCar) {
        if (this.isInBounds(lastCar.getPosition())) {
          road.spawnCar();
        }
      }
    } else {
      road.spawnCar();
    }
  }

  isInBounds(pos) {
    return pos.x >= 0 && pos.y >= 0 &&
           pos.x < this.size.w &&
           pos.y < this.size.h;
  }

  isReady() {
    return this.ready;
  }

  isStateUpdate() {
    return this.stateUpdate;
  }
}

export default World;
