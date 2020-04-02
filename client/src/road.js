import Car from './car';

class Road {
  constructor(id, traffic_light_ids) {
    this.id = id;
    this.traffic_light_ids = traffic_light_ids;
    this.cars = [];
  }

  spawnCar() {
    this.cars.push(new Car({ x: 20, y: 20 }, { w: 20, h: 10}, this.id));
  }

  getCars() {
    return this.cars;
  }

  getTrafficLightIds() {
    return this.traffic_light_ids;
  }
}

export default Road;
