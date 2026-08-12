package com.portfolio.java25.java21;

/**
 * PatternMatchingSwitchDemo.java
 * ------------------------------
 * Demonstração do Pattern Matching para switch e Record Patterns (Java 21 LTS - JEP 440/441).
 */
public class PatternMatchingSwitchDemo {

    sealed interface Operacao permits Deposito, Saque, Transferencia {}
    record Deposito(double valor) implements Operacao {}
    record Saque(double valor) implements Operacao {}
    record Transferencia(double valor, String destino) implements Operacao {}

    public static void runDemo() {
        System.out.println("======================================================================");
        System.out.println(" 🔀 JAVA 21 LTS: PATTERN MATCHING PARA SWITCH & RECORD PATTERNS");
        System.out.println("======================================================================\n");

        Operacao op1 = new Deposito(250.0);
        Operacao op2 = new Saque(100.0);
        Operacao op3 = new Transferencia(500.0, "PIX-1234");

        processarOperacao(op1);
        processarOperacao(op2);
        processarOperacao(op3);

        System.out.println("======================================================================\n");
    }

    private static void processarOperacao(Operacao op) {
        // Pattern Matching com desestruturação direta de Record no switch!
        String resultado = switch (op) {
            case Deposito(double valor) when valor > 1000 -> "Depósito alto valor: R$ " + valor;
            case Deposito(double valor) -> "Depósito normal: R$ " + valor;
            case Saque(double valor) -> "Saque realizado: R$ " + valor;
            case Transferencia(double valor, String destino) -> "Transferência de R$ " + valor + " para " + destino;
        };

        System.out.println("• " + resultado);
    }
}
