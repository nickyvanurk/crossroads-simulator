const path = require('path');

module.exports = {
  entry: './src/main.js',
  output: {
    path: path.join(__dirname, './public/js'),
    filename: 'bundle.js',
    publicPath: '/js/',
  },
  mode: 'development',
  devServer: {
    stats: "errors-only",
    host: process.env.HOST, // Defaults to `localhost`
    port: process.env.PORT, // Defaults to 8080
    open: true,
    contentBase: path.join(__dirname, 'public')
  },
};