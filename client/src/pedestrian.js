import Unit from './unit';

class Pedestrian extends Unit {
  constructor(roadId, size = { w: 5, h: 5 }) {
    super(size, roadId, 20000);
  }
}

export default Pedestrian;
