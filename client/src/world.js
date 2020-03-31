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

    this.traffic_lights.push(new TrafficLight('A1', { x: 489, y: 497}));
    this.traffic_lights.push(new TrafficLight('A2', { x: 514, y: 497}));
    this.traffic_lights.push(new TrafficLight('A3', { x: 536, y: 497}));
    this.traffic_lights.push(new TrafficLight('A4', { x: 560, y: 497}));

    this.traffic_lights.push(new TrafficLight('AB1', { x: 598, y: 632}));
    this.traffic_lights.push(new TrafficLight('AB2', { x: 598, y: 652}));

    this.traffic_lights.push(new TrafficLight('B1', { x: 459, y: 283}));
    this.traffic_lights.push(new TrafficLight('B2', { x: 439, y: 283}));
    this.traffic_lights.push(new TrafficLight('B3', { x: 419, y: 283}));
    this.traffic_lights.push(new TrafficLight('B4', { x: 390, y: 283}));
    this.traffic_lights.push(new TrafficLight('B5', { x: 195, y: 316}));

    this.traffic_lights.push(new TrafficLight('BB1', { x: 358, y: 283}));

    this.traffic_lights.push(new TrafficLight('C1', { x: 598, y: 369}));
    this.traffic_lights.push(new TrafficLight('C2', { x: 598, y: 346}));
    this.traffic_lights.push(new TrafficLight('C3', { x: 598, y: 322}));

    this.traffic_lights.push(new TrafficLight('D1', { x: 342, y: 398}));
    this.traffic_lights.push(new TrafficLight('D2', { x: 342, y: 419}));
    this.traffic_lights.push(new TrafficLight('D3', { x: 342, y: 442}));

    // this.traffic_lights.push(new TrafficLight('E1', { x: 364, y: 242}));
    this.traffic_lights.push(new TrafficLight('E2', { x: 555, y: 211}));

    this.traffic_lights.push(new TrafficLight('EV1', { x: 346, y: 211}));
    this.traffic_lights.push(new TrafficLight('EV2', { x: 476, y: 211}));
    this.traffic_lights.push(new TrafficLight('EV3', { x: 497, y: 211}));
    this.traffic_lights.push(new TrafficLight('EV4', { x: 555, y: 191}));

    this.traffic_lights.push(new TrafficLight('FF1', { x: 337, y: 463}));
    this.traffic_lights.push(new TrafficLight('FF2', { x: 310, y: 323}));

    this.traffic_lights.push(new TrafficLight('FV1', { x: 290, y: 463}));
    this.traffic_lights.push(new TrafficLight('FV2', { x: 290, y: 384}));
    this.traffic_lights.push(new TrafficLight('FV3', { x: 290, y: 364}));
    this.traffic_lights.push(new TrafficLight('FV4', { x: 290, y: 323}));

    this.traffic_lights.push(new TrafficLight('GF1', { x: 588, y: 535}));
    this.traffic_lights.push(new TrafficLight('GF2', { x: 371, y: 545}));

    this.traffic_lights.push(new TrafficLight('GV1', { x: 290, y: 463}));
    this.traffic_lights.push(new TrafficLight('GV2', { x: 456, y: 565}));
    this.traffic_lights.push(new TrafficLight('GV3', { x: 476, y: 565}));
    this.traffic_lights.push(new TrafficLight('GV4', { x: 371, y: 565}));
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