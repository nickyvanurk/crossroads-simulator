import TrafficLight from './traffic_light';
import { TrafficStates } from './utils';

class World {
  constructor() {
    this.canvas = document.getElementById('canvas');
    this.ctx = canvas.getContext('2d');

    this.ctx.canvas.width  = 937;
    this.ctx.canvas.height = 829;

    this.isReady = false;

    // window.addEventListener('mousemove', this.onmousemove);

    const background = new Image();
    background.src = './img/crossroads.png';
    background.onload = () => {
      this.ctx.drawImage(background, 0, 0);

      this.onload();
      this.isReady = true;
    }
  }
  
  onload() {
    this.traffic_lights = {};

    this.traffic_lights['A1'] = new TrafficLight({ x: 489, y: 497 });
    this.traffic_lights['A2'] = new TrafficLight({ x: 514, y: 497 });
    this.traffic_lights['A3'] = new TrafficLight({ x: 536, y: 497 });
    this.traffic_lights['A4'] = new TrafficLight({ x: 560, y: 497 });

    this.traffic_lights['AB1'] = new TrafficLight({ x: 598, y: 632 });
    this.traffic_lights['AB2'] = new TrafficLight({ x: 598, y: 652 });

    this.traffic_lights['B1'] = new TrafficLight({ x: 459, y: 283 });
    this.traffic_lights['B2'] = new TrafficLight({ x: 439, y: 283 });
    this.traffic_lights['B3'] = new TrafficLight({ x: 419, y: 283 });
    this.traffic_lights['B4'] = new TrafficLight({ x: 390, y: 283 });
    this.traffic_lights['B5'] = new TrafficLight({ x: 195, y: 316 });

    this.traffic_lights['BB1'] = new TrafficLight({ x: 358, y: 283 });

    this.traffic_lights['C1'] = new TrafficLight({ x: 598, y: 369 });
    this.traffic_lights['C2'] = new TrafficLight({ x: 598, y: 346 });
    this.traffic_lights['C3'] = new TrafficLight({ x: 598, y: 322 });

    this.traffic_lights['D1'] = new TrafficLight({ x: 342, y: 398 });
    this.traffic_lights['D2'] = new TrafficLight({ x: 342, y: 419 });
    this.traffic_lights['D3'] = new TrafficLight({ x: 342, y: 442 });

    this.traffic_lights['E1'] = new TrafficLight({ x: 555, y: 211 });

    this.traffic_lights['EV1'] = new TrafficLight({ x: 346, y: 211 });
    this.traffic_lights['EV2'] = new TrafficLight({ x: 476, y: 211 });
    this.traffic_lights['EV3'] = new TrafficLight({ x: 497, y: 211 });
    this.traffic_lights['EV4'] = new TrafficLight({ x: 555, y: 191 });

    this.traffic_lights['FF1'] = new TrafficLight({ x: 337, y: 463 });
    this.traffic_lights['FF2'] = new TrafficLight({ x: 310, y: 323 });

    this.traffic_lights['FV1'] = new TrafficLight({ x: 290, y: 463 });
    this.traffic_lights['FV2'] = new TrafficLight({ x: 290, y: 384 });
    this.traffic_lights['FV3'] = new TrafficLight({ x: 290, y: 364 });
    this.traffic_lights['FV4'] = new TrafficLight({ x: 290, y: 323 });

    this.traffic_lights['GF1'] = new TrafficLight({ x: 588, y: 535 });
    this.traffic_lights['GF2'] = new TrafficLight({ x: 371, y: 545 });

    this.traffic_lights['GV1'] = new TrafficLight({ x: 290, y: 463 });
    this.traffic_lights['GV2'] = new TrafficLight({ x: 456, y: 565 });
    this.traffic_lights['GV3'] = new TrafficLight({ x: 476, y: 565 });
    this.traffic_lights['GV4'] = new TrafficLight({ x: 371, y: 565 });
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
    if (!this.isReady) return;
  }

  draw() {
    if (!this.isReady) return;

    for (const index in this.traffic_lights) {
      this.traffic_lights[index].draw(this.ctx);
    }
  }

  processState(state) {
    if (!this.isReady) return;

    for (const [key, traffic_light_state] of Object.entries(state)) {
      this.traffic_lights[key].changeState(parseInt(traffic_light_state));
    }

    this.draw();
  }
}

const world = new World;

export { world as default };