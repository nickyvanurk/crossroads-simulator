import { TrafficStates } from './utils';

export default class TrafficLight {
  constructor(position, facing, queueRadius, stopRadius) {
    this.position = position;
    this.facing = facing;

    this.queueRadius = queueRadius;
    this.stopRadius = stopRadius;

    this.state = TrafficStates.Red;

    this.queue = [];
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

  isOrange() {
    return this.state === TrafficStates.Orange;
  }

  isGreen() {
    return this.state === TrafficStates.Green;
  }

  getQueueCount() {
    return this.queue.length;
  }

  isWithinStopRadius(unit) {
    const pos1 = unit.getPosition();
    const pos2 = this.position;

    const distance = Math.sqrt(Math.pow(Math.abs(pos1.x - pos2.x), 2) +
                               Math.pow(Math.abs(pos1.y - pos2.y), 2));

    const distanceVec = { x: pos1.x - pos2.x, y: pos1.y - pos2.y };
    const dot = this.getDotProduct(this.facing, distanceVec);

    return distance <= this.stopRadius &&
           dot > 0; // Half-circle detection
  }

  isWithinQueueRadius(unit) {
    const pos1 = unit.getPosition();
    const pos2 = this.position;

    const distance = Math.sqrt(Math.pow(Math.abs(pos1.x - pos2.x), 2) +
                               Math.pow(Math.abs(pos1.y - pos2.y), 2));

    const distanceVec = { x: pos1.x - pos2.x, y: pos1.y - pos2.y };
    const dot = this.getDotProduct(this.facing, distanceVec);

    return distance > this.stopRadius &&
           distance <= this.queueRadius &&
           dot > 0; // Half-circle detection
  }

  addToQueue(unit) {
    this.queue.push(unit);
  }

  removeFromQueue(unit) {
    const index = this.queue.indexOf(unit);

    if (index > -1) {
      this.queue.splice(index, 1);
    }
  }

  isInQueue(unit) {
    return this.queue.indexOf(unit) > -1;
  }

  getDotProduct(vec1, vec2) {
    return vec1.x*vec2.x + vec1.y*vec2.y;
  }
}
