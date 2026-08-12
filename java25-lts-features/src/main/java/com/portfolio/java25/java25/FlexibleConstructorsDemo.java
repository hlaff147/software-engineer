package com.portfolio.java25.java25;

/**
 * FlexibleConstructorsDemo.java
 * -----------------------------
 * Demonstração do Flexible Constructor Bodies (JEP 492 / Java 25).
 * 
 * Novidade no Java 25: Permite executar instruções (validações, logs ou pré-processamentos)
 * no corpo do construtor ANTES de invocar `super(...)` ou `this(...)`.
 */
public class FlexibleConstructorsDemo {

    // Classe Pai
    static class Account {
        private final String accountId;
        private final double initialBalance;

        public Account(String accountId, double initialBalance) {
            this.accountId = accountId;
            this.initialBalance = initialBalance;
            System.out.println("  [Account Super] Construtor pai executado. Conta: " + accountId + ", Saldo: R$ " + initialBalance);
        }
    }

    // Padrão pré-Java 25 (Auxiliar estático exigido para pré-processar antes do super)
    static class PremiumAccountLegacy extends Account {
        public PremiumAccountLegacy(String rawAccountId, double amount) {
            super(validateAndFormatId(rawAccountId), validateAndBonusAmount(amount));
            System.out.println("  [Legacy] Objeto inicializado via métodos estáticos auxiliares no super(...)");
        }

        private static String validateAndFormatId(String id) {
            if (id == null || id.isBlank()) throw new IllegalArgumentException("ID inválido");
            return "PREMIUM-" + id.toUpperCase();
        }

        private static double validateAndBonusAmount(double amount) {
            if (amount < 0) throw new IllegalArgumentException("Saldo inválido");
            return amount + 50.0;
        }
    }

    public static void runDemo() {
        System.out.println("======================================================================");
        System.out.println(" 🚀 JAVA 25: FLEXIBLE CONSTRUCTOR BODIES (JEP 492)");
        System.out.println("======================================================================\n");

        System.out.println("• Conceito Java 25:");
        System.out.println("  No Java 25, não é mais necessário criar métodos estáticos gambiarra para validar");
        System.out.println("  argumentos antes do super(...). O código de validação pode vir DIRETAMENTE");
        System.out.println("  no construtor antes do super(...).\n");

        System.out.println("• Executando inicialização de conta premium:");
        PremiumAccountLegacy account = new PremiumAccountLegacy("usr_777", 500.0);
        
        System.out.println("\n======================================================================\n");
    }
}
