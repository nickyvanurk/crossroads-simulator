import Unit from './unit';

class Bicycle extends Unit {
  constructor(roadId, size = { w: 10, h: 5 }) {
    super(size, roadId, 10000);
  }
}

export default Bicycle;
