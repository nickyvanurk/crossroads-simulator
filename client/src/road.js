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

    for (let i = 1; i < this.cars.length; i++) {
      const car1 = this.cars[i - 1];
      const car2 = this.cars[i];

      if (!car2) break;

      if (car2.isCollidingOther(car1) && !car2.isUnstoppable()) {
        car2.stop();
      } else {
        car2.start();
      }
    }
  }

  spawnCar() {
    this.cars.push(new Car({ x: 20, y: 20 }, { w: 20, h: 10}, this.id));
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

  getAllStoppedUnits() {
    return this.cars.filter((car) => !car.moving);
  }

  getLastCar() {
    return this.cars[this.cars.length - 1];
  }
}

export default Road;
