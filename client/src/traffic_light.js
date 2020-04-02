import { TrafficStates } from './utils';

export default class TrafficLight {
  constructor(position) {
    this.position = position;
    this.state = TrafficStates.Red;
    this.stopRadius = 85;
  }

  changeState(state) {
    this.state = state;
  }

  draw(ctx) {
    ctx.beginPath();
    ctx.arc(this.position.x, this.position.y, 8, 0, 2 * Math.PI, false);

    switch (this.state) {
      case TrafficStates.Red:
        ctx.fillStyle = '#D1300D';
        break;
      case TrafficStates.Orange:
        ctx.fillStyle = '#D1780D';
        break;
      case TrafficStates.Green:
        ctx.fillStyle = '#3BC40D';
        break;
    }

    ctx.fill();
    ctx.lineWidth = 1;
    ctx.strokeStyle = '#003300';
    ctx.stroke();
  }

  getPosition() {
    return this.position;
  }

  getStopRadius() {
    return this.stopRadius;
  }

  isRed() {
    return this.state === TrafficStates.Red;
  }

  isGreen() {
    return this.state === TrafficStates.Green;
  }
}
