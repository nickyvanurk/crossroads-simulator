export default class TrafficLight {
  constructor(position) {
    this.position = position;
  }
  
  draw(ctx) {
    ctx.beginPath();
    ctx.arc(this.position.x, this.position.y, 8, 0, 2 * Math.PI, false);
    ctx.fillStyle = 'green';
    ctx.fill();
    ctx.lineWidth = 1;
    ctx.strokeStyle = '#003300';
    ctx.stroke();
  }
}