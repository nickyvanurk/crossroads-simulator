import Game from './game';

const socket = new WebSocket('ws://localhost:8080');
const game = new Game(socket);

socket.addEventListener('open', game.onOpen.bind(game));
socket.addEventListener('message', game.onMessage.bind(game));
