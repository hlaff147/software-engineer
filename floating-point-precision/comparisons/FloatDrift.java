package comparisons;

import java.math.BigDecimal;

/**
 * FloatDrift.java
 * ---------------
 * Demonstração em Java da diferença entre `double` (IEEE 754 de hardware)
 * e `BigDecimal` (precisão arbitrária de software).
 */
public class FloatDrift {

    public static void main(String[] args) {
        System.out.println("======================================================================");
        System.out.println(" ☕ JAVA - DEMONSTRAÇÃO DE IEEE 754 (double) VS BigDecimal");
        System.out.println("======================================================================\n");

        int passos = 1_000_000;

        // --- Experimento 1: double nativo ---
        double incrementoDouble = 0.0001;
        double somaDouble = 0.0;

        long startDouble = System.nanoTime();
        for (int i = 0; i < passos; i++) {
            somaDouble += incrementoDouble;
        }
        long endDouble = System.nanoTime();

        double esperadoDouble = incrementoDouble * passos;
        double erroDouble = Math.abs(somaDouble - esperadoDouble);

        System.out.printf("• [double Nativo] Resultado acumulado: %.17f%n", somaDouble);
        System.out.printf("• [double Nativo] Esperado:            %.17f%n", esperadoDouble);
        System.out.printf("• [double Nativo] Erro acumulado:       %.17e%n", erroDouble);
        System.out.printf("• Tempo (double):                       %.2f ms%n%n", (endDouble - startDouble) / 1e6);

        // --- Experimento 2: java.math.BigDecimal ---
        BigDecimal incrementoBD = new BigDecimal("0.0001");
        BigDecimal somaBD = BigDecimal.ZERO;

        long startBD = System.nanoTime();
        for (int i = 0; i < passos; i++) {
            somaBD = somaBD.add(incrementoBD);
        }
        long endBD = System.nanoTime();

        BigDecimal esperadoBD = incrementoBD.multiply(new BigDecimal(passos));
        BigDecimal erroBD = somaBD.subtract(esperadoBD).abs();

        System.out.printf("• [BigDecimal] Resultado acumulado:    %s%n", somaBD.toPlainString());
        System.out.printf("• [BigDecimal] Esperado:               %s%n", esperadoBD.toPlainString());
        System.out.printf("• [BigDecimal] Erro acumulado:          %s%n", erroBD.toPlainString());
        System.out.printf("• Tempo (BigDecimal):                  %.2f ms%n%n", (endBD - startBD) / 1e6);

        // --- Experimento 3: 0.1 + 0.2 ---
        System.out.println("• Teste de igualdade direct: 0.1 + 0.2 == 0.3");
        System.out.printf("  0.1 + 0.2 em double: %.17f%n", (0.1 + 0.2));
        System.out.println("  0.1 + 0.2 == 0.3 ? " + ((0.1 + 0.2) == 0.3));
        System.out.println("======================================================================\n");
    }
}
