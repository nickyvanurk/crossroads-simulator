const TrafficStates = {
  Red: 0,
  Orange: 1,
  Green: 2
}

const filterObjectByKeys = (obj, keys) => {
  let newObj = {};

  Object.keys(obj)
        .filter(key => keys.includes(key))
        .forEach(key => newObj[key] = obj[key]);

  return newObj;
}

export {
  TrafficStates,
  filterObjectByKeys
};
