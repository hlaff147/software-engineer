package com.portfolio.java25;

import com.portfolio.java25.java21.PatternMatchingSwitchDemo;
import com.portfolio.java25.java21.SequencedCollectionsDemo;
import com.portfolio.java25.java21.VirtualThreadsDemo;
import com.portfolio.java25.java25.FlexibleConstructorsDemo;
import com.portfolio.java25.scopedvalue.ScopedValueDemo;
import com.portfolio.java25.scopedvalue.ThreadLocalLegacyComparison;

/**
 * Main.java
 * ---------
 * Classe principal que executa a bateria de testes e demonstrações do Java 25 e Java 21 LTS.
 */
public class Main {

    public static void main(String[] args) {
        System.out.println("\n" + "🚀".repeat(35));
        System.out.println("   PORTFÓLIO: DEMONSTRAÇÃO DAS NOVIDADES DO JAVA 25 & JAVA 21 LTS");
        System.out.println("🚀".repeat(35) + "\n");

        // 1. Java 25 Highlight: ScopedValue vs ThreadLocal
        ScopedValueDemo.runDemo();
        ThreadLocalLegacyComparison.runDemo();

        // 2. Java 25 Highlight: Flexible Constructor Bodies
        FlexibleConstructorsDemo.runDemo();

        // 3. Java 21 LTS Highlights
        VirtualThreadsDemo.runDemo();
        PatternMatchingSwitchDemo.runDemo();
        SequencedCollectionsDemo.runDemo();

        System.out.println("✨ TODAS AS DEMONSTRAÇÕES FORAM EXECUTADAS COM SUCESSO! ✨\n");
    }
}
