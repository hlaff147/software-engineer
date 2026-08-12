package com.portfolio.java25.scopedvalue;

import java.lang.ScopedValue;

/**
 * ScopedValueDemo.java
 * -------------------
 * Demonstração do ScopedValue (Java 25 / Preview Java 21+).
 * 
 * Filosofia:
 * 1. Imutabilidade: Um ScopedValue é vinculado a um escopo e não pode ser alterado durante a execução daquele bloco.
 * 2. Limpeza Automática: Ao sair do bloco `run(...)` ou `call(...)`, o vínculo é desfeito automaticamente. Zero risco de Memory Leaks.
 * 3. Rebind Seguro (Shadowing): Um sub-escopo pode definir um novo valor para a mesma chave sem afetar o escopo pai.
 */
public class ScopedValueDemo {

    // Declaração de chaves de escopo imutáveis
    public static final ScopedValue<String> CURRENT_USER = ScopedValue.newInstance();
    public static final ScopedValue<String> REQUEST_ID = ScopedValue.newInstance();

    public static void runDemo() {
        System.out.println("======================================================================");
        System.out.println(" ⚡ JAVA 25: DEMONSTRAÇÃO DO ScopedValue");
        System.out.println("======================================================================\n");

        System.out.println("• 1. Verificando estado antes de definir o escopo:");
        System.out.println("  CURRENT_USER isBound? " + CURRENT_USER.isBound()); // false

        System.out.println("\n• 2. Definindo o contexto do escopo com ScopedValue.where(...):");

        // Associa valores ao escopo e executa o lambda
        ScopedValue.where(CURRENT_USER, "user_alice")
                   .where(REQUEST_ID, "req-98765")
                   .run(() -> {
                       processRequest();
                   });

        System.out.println("\n• 3. Verificando estado APÓS sair do escopo:");
        System.out.println("  CURRENT_USER isBound? " + CURRENT_USER.isBound()); // false (Limpeza automática!)
        System.out.println("  -> Nenhum risco de vazamento de memória em Thread Pools!");
        System.out.println("======================================================================\n");
    }

    private static void processRequest() {
        System.out.println("  [Escopo Principal] Usuário Atual: " + CURRENT_USER.get() + " | Request ID: " + REQUEST_ID.get());

        // Chamada de método intermediário transmitindo o contexto implicitamente sem passar parâmetros no método
        validarPermissoes();

        // Sub-escopo (Rebind / Shadowing): Sobregravação temporária para uma sub-tarefa interna
        System.out.println("  [Sub-Escopo] Criando escopo de sobreelevação (Admin Override)...");
        ScopedValue.where(CURRENT_USER, "user_admin_system").run(() -> {
            System.out.println("    [Dentro do Sub-Escopo] Usuário Atual: " + CURRENT_USER.get());
        });

        // Ao sair do sub-escopo, o valor original do escopo pai permanece intacto e inalterado!
        System.out.println("  [Escopo Principal] Retornando ao escopo pai. Usuário Atual: " + CURRENT_USER.get());
    }

    private static void validarPermissoes() {
        System.out.println("  [Camada de Serviço] Validando permissão para: " + CURRENT_USER.get());
    }
}
