import world from './world';

const socket = new WebSocket('ws://localhost:8080');
// const socket = new WebSocket('ws://0.tcp.ngrok.io:15380');

socket.addEventListener('open', (event) => {
  console.log('Connected');
});

socket.addEventListener('message', (event) => {
  world.processState(JSON.parse(event.data));
  console.log('Message from server ', event.data);
});

window.requestAnimationFrame(gameLoop);

function gameLoop() {
  world.update();
  world.draw();

  if (world.isStateChanged()) {
    console.log('sending state');
    const payload = world.getState();
    socket.send(JSON.stringify(payload));
  }

  window.requestAnimationFrame(gameLoop);
}
