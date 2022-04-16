var readline = require("readline");
var RL = readline.createInterface(process.stdin, process.stdout);
const util = require("util");
const question = util.promisify(RL.question).bind(RL);

async function teste() {
  const amperetotal = await question("quantos de corrente total?\n");
  const voltagem = await question("Qual tensão?\n");
  const bateriaA = await question("quantos de corrente tem a bateria?\n");
  const BateriaV = await question("quantos de tensão há bateria?\n");
  const hora = await question("quantas horas serão usadas? (1 = 1hr)\n");

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
