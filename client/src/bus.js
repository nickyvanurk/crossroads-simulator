import Unit from './unit';

class Bus extends Unit {
  constructor(roadId, size = { w: 40, h: 10 }) {
    super(size, roadId, 7000);
  }
}

export default Bus;
