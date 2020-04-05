import world from './world';
import World from './world';

class Game {
  constructor(socket) {
    this.socket = socket;

    this.canvas = document.getElementById('canvas');
    this.ctx = canvas.getContext('2d');

    this.ctx.canvas.width  = 937;
    this.ctx.canvas.height = 829;

    this.world = new World({ w: this.canvas.width, h: this.canvas.height });
  }

  run() {
    this.world.init();

    window.requestAnimationFrame(this.loop.bind(this));
  }

  loop() {
    if (!this.world.isReady()) return;

    this.world.update();
    this.world.draw(this.ctx);

    if (this.world.isStateUpdate()) {
      this.sendMessage(this.world.getState());
    }

    window.requestAnimationFrame(this.loop.bind(this));
  }

  onOpen(event) {
    console.log(`Connected to "${event.target.url}"`);

    this.run();
  }

  onMessage(event) {
    this.world.processState(JSON.parse(event.data));
  }

  sendMessage(payload) {
    this.socket.send(JSON.stringify(payload));
  }
}

export default Game;
