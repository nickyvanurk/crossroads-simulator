const TrafficStates = {
  Red: 0,
  Orange: 1,
  Green: 2
}

const getObjectValuesByKeys = (obj, keys) => {
  let values = [];

  Object.keys(obj)
        .filter(key => keys.includes(key))
        .forEach(key => values.push(obj[key]));

  return values;
}

export {
  TrafficStates,
  getObjectValuesByKeys
};
