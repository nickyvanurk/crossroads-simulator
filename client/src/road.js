import Car from './car';
import Pedestrian from './pedestrian';
import Bicycle from './bicycle';

class Road {
  constructor(id, type, trafficLightIds, spawnTimer) {
    this.id = id;
    this.type = type;
    this.trafficLightIds = trafficLightIds;
    this.spawnTimer = spawnTimer;
    this.cars = [];
  }

  init() {
    setInterval(this.spawnCar().bind(this), this.spawnTimer);
  }

  update(worldSize) {
    if (!this.hasTraffic()) return;

    for (const car of this.cars) {
      if (car.passedTrafficLights.length > 0 &&
          (car.position.x + car.size.w < 0 ||
           car.position.y + car.size.h < 0 ||
           car.position.x - car.size.w > worldSize.w ||
           car.position.y - car.size.h > worldSize.h)) {
        this.despawnCar(car);
      }
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
      case "bicycle":
        this.cars.push(new Bicycle(this.id));
        break;
      default:
        console.log(`Can't spawn "${this.type}": not found`);
        break;
    }
  }

  despawnCar(car) {
    this.cars.splice(this.cars.indexOf(car), 1);
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
