var readline = require("readline");
var RL = readline.createInterface(process.stdin, process.stdout);
const util = require("util");
const question = util.promisify(RL.question).bind(RL);

async function teste() {
  const amperetotal = await question("quantos de ampere total?\n");
  const voltagem = await question("quantos de voltagem usara?\n");
  const bateriaA = await question("quantos de ampere na bateria?\n");
  const BateriaV = await question("quantos de voltagem na bateria?\n");
  const hora = await question("quantas horas será usado?\n");

  // let amperetotal = 4900;
  // let voltagem = 7.4;
  // let bateriaA = 2000;
  // let bateriaV = 3.8;
  console.log(
    "ampere = " +
      (amperetotal / bateriaA) * hora +
      " em paralelo" +
      "\nvoltagem = " +
      voltagem / BateriaV +
      " em serie"
  );
}
teste();
