class World {
  constructor() {
    this.canvas = document.getElementById('canvas');
    this.ctx = canvas.getContext('2d');

    this.ctx.canvas.width  = 937;
    this.ctx.canvas.height = 829;

    const background = new Image();
    background.src = './img/crossroads.png';
    background.onload = () => {
      this.ctx.drawImage(background, 0, 0);

      this.onload();
    }
  }
  
  onload() {
    this.ctx.beginPath();
    this.ctx.lineWidth = "6";
    this.ctx.strokeStyle = "red";
    this.ctx.rect(5, 5, 290, 140);
    this.ctx.stroke();
  }

  update() {

  }

  draw() {
    
  }
}

const world = new World;

export { world as default };