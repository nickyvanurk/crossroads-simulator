import Car from './car';

class Road {
  constructor(id, traffic_light_ids) {
    this.id = id;
    this.traffic_light_ids = traffic_light_ids;
    this.cars = [];
  }

  update() {
    if (!this.hasTraffic()) return;

    if (this.firstCar().isFlaggedForDespawn()) {
      this.despawnCar();
    }
  }

  spawnCar() {
    this.cars.push(new Car({ x: 20, y: 20 }, { w: 20, h: 10}, this.id, this.despawnCar));
  }

  despawnCar() {
    if (this.hasTraffic()) {
      this.cars.shift();
    }
  }

  hasTraffic() {
    return this.cars.length !== 0;
  }

  firstCar() {
    if (this.hasTraffic()) {
      return this.cars[0];
    }
  }

  getCars() {
    return this.cars;
  }

  getTrafficLightIds() {
    return this.traffic_light_ids;
  }
}

export default Road;
