import TrafficLight from './traffic_light';

class World {
  constructor() {
    this.canvas = document.getElementById('canvas');
    this.ctx = canvas.getContext('2d');

    this.ctx.canvas.width  = 937;
    this.ctx.canvas.height = 829;

    window.addEventListener('mousemove', this.onmousemove);

    const background = new Image();
    background.src = './img/crossroads.png';
    background.onload = () => {
      this.ctx.drawImage(background, 0, 0);

      this.onload();
    }
  }
  
  onload() {
    this.traffic_lights = [];
    this.traffic_lights.push(new TrafficLight({ x: 342, y: 398}));
    this.traffic_lights.push(new TrafficLight({ x: 342, y: 419}));
    this.traffic_lights.push(new TrafficLight({ x: 342, y: 442}));
  }

  onmousemove(event) {
    const rect = this.canvas.getBoundingClientRect();
    const pos = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };

    console.log(pos);

  }

  update() {

  }

  draw() {
    for (const index in this.traffic_lights) {
      this.traffic_lights[index].draw(this.ctx);
    }
  }
}

const world = new World;

export { world as default };