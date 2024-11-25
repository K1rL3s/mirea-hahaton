export const ipToNumber = (ip: string) => {
  return ip
    .split(".")
    .map(
      (octet, index, array) =>
        parseInt(octet) * Math.pow(256, array.length - index - 1),
    )
    .reduce((prev, cur) => prev + cur);
};
