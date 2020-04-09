import Unit from './unit';

class Car extends Unit {
  constructor(roadId, size = { w: 20, h: 10 }) {
    super(size, roadId, 12000);
  }
}

export default Car;
