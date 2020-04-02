import traffic_lights_data from './data/traffic_lights.json';
import TrafficLight from './traffic_light';
import Car from './car';

class World {
  constructor() {
    this.canvas = document.getElementById('canvas');
    this.ctx = canvas.getContext('2d');

    this.ctx.canvas.width  = 937;
    this.ctx.canvas.height = 829;

    this.traffic_lights = {};
    this.isReady = false;

    this.init();

    // window.addEventListener('mousemove', this.onmousemove);
  }

  init() {
    this.generateTrafficLights(traffic_lights_data);

    this.car = new Car({ x: 20, y: 20 }, { w: 20, h: 10}, 'road-w-n');

    this.isReady = true;
  }

  update() {
    if (!this.isReady) return;
  }

  draw() {
    if (!this.isReady) return;

    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    this.car.draw(this.ctx);

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
  generateTrafficLights(json) {
    for (const [key, coordinates] of Object.entries(traffic_lights_data)) {
      this.traffic_lights[key] = new TrafficLight(coordinates);
    }
  }

  processState(state) {
    if (!this.isReady) return;


    for (const [key, traffic_light_state] of Object.entries(state)) {
      this.traffic_lights[key].changeState(parseInt(traffic_light_state));

      if (key === 'D1') {
        if (this.traffic_lights[key].state == 2) {
          this.car.resume();
        }
      }
    }

    this.draw();
  }
}

const world = new World;

export { world as default };
