import Car from './car';
import Pedestrian from './pedestrian';

class Road {
  constructor(id, type, trafficLightIds) {
    this.id = id;
    this.type = type;
    this.trafficLightIds = trafficLightIds;
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

      if (!car2) continue;

      if (car2.isCollidingOther(car1) && !car2.isColliding()) {
        car2.setCollision(true);
        car2.stop();
      }

      if (!car2.isCollidingOther(car1) && car2.isColliding()) {
        car2.setCollision(false);
        car2.start();
      }
    }
  }

  spawnCar() {
    switch (this.type) {
      case "car":
        this.cars.push(new Car(this.id));
        break;
      case "pedestrian":
        this.cars.push(new Pedestrian(this.id));
        break;
    }
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
    return this.trafficLightIds;
  }

  getAllStoppedUnits() {
    return this.cars.filter((car) => !car.moving);
  }

  getLastCar() {
    return this.cars[this.cars.length - 1];
  }
}

export default Road;
