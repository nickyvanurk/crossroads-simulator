class Unit {
  constructor(size = { w: 20, h: 10 }, roadId, animTime) {
    this.position = { x: -100, y: -100 };
    this.size = size;
    this.angle = 0;
    this.color = "hsl(" + 360 * Math.random() + ',' +
                          (95 + 70 * Math.random()) + '%,' +
                          (60 + 10 * Math.random()) + '%)';
    this.moving = true;
    this.collisionRadius = this.size.w * 1.5;
    this.collision = false;

    this.readyForDespawn = false;

    const road = document.getElementById(roadId).getElementsByTagName('path')[0].getAttribute('d');;
    const roadLength = Snap.path.getTotalLength(road);

    this.anim = Snap.animate(0, roadLength, async (step) => {
      const moveToPoint = Snap.path.getPointAtLength(road, step);

      this.position.x = moveToPoint.x;
      this.position.y = moveToPoint.y;
      this.angle = moveToPoint.alpha;
    }, animTime);
  }

  stop() {
    this.moving = false;
    this.anim.pause();
  }

  start() {
    this.moving = true;
    this.anim.resume();
  }

  draw(ctx) {
    ctx.translate(this.position.x, this.position.y);
    ctx.rotate(this.angle * Math.PI / 180);
    ctx.fillStyle = this.color;
    ctx.fillRect(-this.size.w / 2, -this.size.h / 2, this.size.w, this.size.h);
    ctx.stroke();
    ctx.rotate(-(this.angle * Math.PI / 180));
    ctx.translate(-(this.position.x), -(this.position.y));
  }

  isTrafficLightInQueue(id) {
    return this.trafficLightQueues.indexOf(id) > -1;
  }

  isPassedTrafficLight(id) {
    return this.passedTrafficLights.indexOf(id) > -1;
  }

  getPosition() {
    return this.position;
  }

  isMoving() {
    return this.moving;
  }

  isCollidingOther(car) {
    const pos1 = car.getPosition();
    const pos2 = this.position;

    const distance = Math.sqrt(Math.pow(Math.abs(pos1.x - pos2.x), 2) +
                               Math.pow(Math.abs(pos1.y - pos2.y), 2));

    return distance <= this.collisionRadius;
  }

  setCollision(flag) {
    this.collision = flag;
  }

  isColliding() {
    return this.collision;
  }
}

export default Unit;
