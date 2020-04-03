class Car {
  constructor(position, size = { w: 20, h: 10 }, roadId) {
    this.size = size;
    this.position = position;
    this.angle = 0;
    this.moving = true;
    this.trafficLightChecks = 0;
    this.isFinishedAnim = false;
    this.inQueue = false;
    this.unstoppable = false;

    const road = document.getElementById(roadId).getElementsByTagName('path')[0].getAttribute('d');;
    const roadLength = Snap.path.getTotalLength(road);

    this.numPaused = 0;

    this.anim = Snap.animate(0, roadLength, async (step) => {
      const moveToPoint = Snap.path.getPointAtLength(road, step);

      this.position.x = moveToPoint.x;
      this.position.y = moveToPoint.y;
      this.angle = moveToPoint.alpha;

      // if (step > 350 && step < 360 && this.numPaused == 0) {
      //   this.numPaused += 1;

      //   this.anim.pause();
      // }
    }, 5000, () => {
      this.isFinishedAnim = true;
    });
  }

  stop() {
    this.moving = false;
    this.inQueue = true;
    this.anim.pause();
  }

  start() {
    this.moving = true;
    this.inQueue = false;
    this.anim.resume();
  }

  draw(ctx) {
    ctx.translate(this.position.x, this.position.y);
    ctx.rotate(this.angle * Math.PI / 180);
    ctx.fillStyle = "#0B9ADA";
    ctx.fillRect(-this.size.w / 2, -this.size.h / 2, this.size.w, this.size.h);
    ctx.stroke();
    ctx.rotate(-(this.angle * Math.PI / 180));
    ctx.translate(-(this.position.x), -(this.position.y));
  }

  getPosition() {
    return this.position;
  }

  isMoving() {
    return this.moving;
  }

  isFlaggedForDespawn() {
    return this.isFinishedAnim;
  }

  isInQueue() {
    return this.inQueue;
  }

  setInQueue(flag) {
    this.inQueue = flag;
  }

  isUnstoppable() {
    return this.unstoppable;
  }

  setUnstoppable(flag) {
    this.unstoppable = flag;
  }
}

export default Car;
