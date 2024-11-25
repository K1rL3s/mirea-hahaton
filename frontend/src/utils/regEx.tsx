export const ipPattern =
  "^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])((-(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9]))|(/(3[0-2]|2[7-9])))?$";

export const multipleIpPattern =
  "^(((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\\.(25[0-5]|2[3-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])((-(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9]))|(/(3[0-2]|2[7-9])))?)+\\s?)+$";

const ipPatternRe =
  /^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])((-(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][1-9]|[0-9]))|(\/(3[0-2]|2[7-9])))?$/;
export const chechIpPattern = (str: string) => {
  return ipPatternRe.test(str);
};
