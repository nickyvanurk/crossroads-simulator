const TrafficStates = {
  Red: 0,
  Orange: 1,
  Green: 2
}

const filterObjectByKeys = (obj, keys) => {
  let arr = [];

  Object.keys(obj)
        .filter(key => keys.includes(key))
        .forEach(key => arr.push(obj[key]));

  return arr;
}

export {
  TrafficStates,
  filterObjectByKeys
};
