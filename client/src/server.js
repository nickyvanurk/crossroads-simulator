const path = require('path');
const express = require('express');
const http = require('http');

const port = process.env.PORT || 3000;

const app = express();

app.use(express.static(path.join(__dirname, '../public')));

const httpServer = http.createServer(app);

httpServer.listen(port, () => {
  console.log('listening on %d', port);
});