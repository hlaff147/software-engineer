package com.portfolio.java25.java21;

import java.util.concurrent.Executors;
import java.util.stream.IntStream;

/**
 * VirtualThreadsDemo.java
 * -----------------------
 * Demonstração das Virtual Threads (Java 21 LTS - JEP 444).
 * 
 * Permite criar milhões de threads leves gerenciadas pela JVM (não pelo SO),
 * ideal para I/O concorrente maciço.
 */
public class VirtualThreadsDemo {

    public static void runDemo() {
        System.out.println("======================================================================");
        System.out.println(" 🧵 JAVA 21 LTS: VIRTUAL THREADS (JEP 444)");
        System.out.println("======================================================================\n");

        int totalTarefas = 10_000;
        System.out.println("• Disparando " + totalTarefas + " Virtual Threads simultâneas...");

        long inicio = System.currentTimeMillis();

        // Executor de Virtual Threads (um thread leve por tarefa)
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            IntStream.range(0, totalTarefas).forEach(i -> {
                executor.submit(() -> {
                    // Simula I/O bloqueante leve
                    Thread.sleep(10);
                    return i;
                });
            });
        } // O try-with-resources aguarda o término de todas as Virtual Threads automaticamente!

        long fim = System.currentTimeMillis();

        System.out.println("• " + totalTarefas + " Virtual Threads concluídas com sucesso!");
        System.out.println("• Tempo total de execução: " + (fim - inicio) + " ms");
        System.out.println("======================================================================\n");
    }
}
