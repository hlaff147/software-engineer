package com.portfolio.java25.java21;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.SequencedCollection;
import java.util.SequencedMap;

/**
 * SequencedCollectionsDemo.java
 * -----------------------------
 * Demonstração das Sequenced Collections (Java 21 LTS - JEP 431).
 * 
 * Unifica a API de coleções ordenadas com métodos padronizados:
 * `getFirst()`, `getLast()`, `addFirst()`, `addLast()`, `reversed()`.
 */
public class SequencedCollectionsDemo {

    public static void runDemo() {
        System.out.println("======================================================================");
        System.out.println(" 📚 JAVA 21 LTS: SEQUENCED COLLECTIONS (JEP 431)");
        System.out.println("======================================================================\n");

        // SequencedCollection (List)
        SequencedCollection<String> lista = new ArrayList<>(List.of("Segunda", "Terça", "Quarta"));
        lista.addFirst("Domingo");
        lista.addLast("Quinta");

        System.out.println("• Lista Ordenada: " + lista);
        System.out.println("  Primeiro Elemento (getFirst): " + lista.getFirst());
        System.out.println("  Último Elemento (getLast):   " + lista.getLast());
        System.out.println("  Lista Invertida (reversed):  " + lista.reversed());

        // SequencedMap (Map)
        SequencedMap<String, String> mapa = new LinkedHashMap<>();
        mapa.putFirst("1", "Primeiro");
        mapa.putLast("2", "Segundo");
        mapa.putLast("3", "Terceiro");

        System.out.println("\n• SequencedMap:");
        System.out.println("  Primeiro Entry: " + mapa.firstEntry());
        System.out.println("  Último Entry:   " + mapa.lastEntry());
        System.out.println("  Mapa Invertido: " + mapa.reversed());

        System.out.println("======================================================================\n");
    }
}
