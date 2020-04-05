import { TrafficStates } from './utils';

export default class TrafficLight {
  constructor(position, queueRadius, stopRadius) {
    this.position = position;
    this.queueRadius = queueRadius;
    this.stopRadius = stopRadius;

    this.state = TrafficStates.Red;
    this.queuedUnits = 0;
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

  setNumQueuedUnits(num) {
    this.queuedUnits = num;
  }

  incrementQueue() {
    this.queuedUnits++;
  }

  decrementQueue() {
    this.queuedUnits--;
  }

  getQueuedUnits() {
    return this.queuedUnits;
  }

  isUnitWithinStopRadius(unit) {
    const pos1 = unit.getPosition();
    const pos2 = this.position;

    const distance = Math.sqrt(Math.pow(Math.abs(pos1.x - pos2.x), 2) +
                               Math.pow(Math.abs(pos1.y - pos2.y), 2));

    return distance <= this.stopRadius;
  }

  isUnitWithinQueueRadius(unit) {
    const pos1 = unit.getPosition();
    const pos2 = this.position;

    const distance = Math.sqrt(Math.pow(Math.abs(pos1.x - pos2.x), 2) +
                               Math.pow(Math.abs(pos1.y - pos2.y), 2));

    return distance <= this.queueRadius;
  }
}
