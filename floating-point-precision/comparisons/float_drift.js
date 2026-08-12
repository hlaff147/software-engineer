/**
 * float_drift.js
 * --------------
 * Demonstração do fenômeno de perda de precisão em ponto flutuante em JavaScript (Node.js).
 * Em JS, todos os números nativos são do tipo Number (64-bit IEEE 754 double precision).
 */

console.log("======================================================================");
console.log(" 🟨 JAVASCRIPT / NODE.JS - DEMONSTRAÇÃO DE IEEE 754");
console.log("======================================================================\n");

// Experimento 1: Soma acumulada
const incremento = 0.0001;
const passos = 1_000_000;
let soma = 0.0;

const inicio = performance.now();
for (let i = 0; i < passos; i++) {
  soma += incremento;
}
const fim = performance.now();

const esperado = incremento * passos;
const erroAbsoluto = Math.abs(soma - esperado);

console.log(`• Somando ${incremento} um milhão de vezes em JS:`);
console.log(`  Resultado Real:    ${soma.toFixed(17)}`);
console.log(`  Resultado Esperado: ${esperado.toFixed(17)}`);
console.log(`  Erro Acumulado:    ${erroAbsoluto.toExponential(10)}`);
console.log(`  Tempo:             ${(fim - inicio).toFixed(2)} ms\n`);

// Experimento 2: 0.1 + 0.2
console.log("• Teste de igualdade direct: 0.1 + 0.2 === 0.3");
console.log(`  0.1 + 0.2 = ${(0.1 + 0.2).toFixed(17)}`);
console.log(`  0.1 + 0.2 === 0.3 ? ${0.1 + 0.2 === 0.3}`);
console.log("======================================================================\n");
