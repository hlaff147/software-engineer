package com.portfolio.java25.scopedvalue;

/**
 * ThreadLocalLegacyComparison.java
 * --------------------------------
 * Demonstração dos problemas do ThreadLocal legado vs a modernidade do ScopedValue.
 * 
 * Problemas do ThreadLocal:
 * 1. Mutabilidade: Qualquer código pode chamar ThreadLocal.set() e alterar o estado global da thread.
 * 2. Vazamento de Memória (Memory Leak): Se a thread vier de um ThreadPool (ExecutorService),
 *    o valor permanece preso na thread se você esquecer de chamar ThreadLocal.remove().
 * 3. Ineficiência em Virtual Threads: Herança de mapa de threads locais gera overhead severo.
 */
public class ThreadLocalLegacyComparison {

    public static final ThreadLocal<String> CONTEXTO_THREAD = new ThreadLocal<>();

    public static void runDemo() {
        System.out.println("======================================================================");
        System.out.println(" ⚠️ LEGADO: PROBLEMAS DO ThreadLocal");
        System.out.println("======================================================================\n");

        System.out.println("• 1. Definindo valor no ThreadLocal: 'user_bob'");
        CONTEXTO_THREAD.set("user_bob");

        processarLegado();

        System.out.println("\n• 2. APÓS a execução do método:");
        System.out.println("  Valor ainda presente na Thread? " + CONTEXTO_THREAD.get());
        
        // Se a thread for reaproveitada por um Thread Pool, 'user_bob' vazará para a próxima requisição!
        System.out.println("  ⚠️ ALERTA: Se não chamarmos .remove(), ocorrerá MEMORY LEAK!");

        // Limpeza manual obrigatória (vulnerável a esquecimento se ocorrer exceção sem try-finally)
        CONTEXTO_THREAD.remove();
        System.out.println("  Valor após .remove() manual: " + CONTEXTO_THREAD.get());
        System.out.println("======================================================================\n");
    }

    private static void processarLegado() {
        System.out.println("  [ThreadLocal] Lendo contexto: " + CONTEXTO_THREAD.get());
        
        // Mutabilidade indesejada: qualquer método interno pode alterar o valor global da thread!
        CONTEXTO_THREAD.set("user_bob_MUTATED");
        System.out.println("  [ThreadLocal] Estado alterado acidentalmente para: " + CONTEXTO_THREAD.get());
    }
}
