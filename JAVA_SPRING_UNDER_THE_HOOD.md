# ☕ Java & Spring: Perguntas de Entrevista "Under the Hood" (Por Baixo dos Panos)

> **Documento de Estudo Baseado na Análise do Blog Saurska**  
> Idioma: Português do Brasil (pt-BR)  
> Foco: Funcionamento interno da JVM, APIs do Core Java (Collections, Concorrência, Exceptions) e mecanismos internos do ecossistema Spring (Proxies, Lifecycle, DI, JPA).

---

## 📑 Sumário das Perguntas

1. [🧠 Como o ConcurrentHashMap funciona internamente no Java 8?](#1-como-o-concurrenthashmap-funciona-internamente-no-java-8)
2. [⚖️ HashMap vs ConcurrentHashMap vs SynchronizedMap: Quando e por que usar?](#2-hashmap-vs-concurrenthashmap-vs-synchronizedmap-quando-e-por-que-usar)
3. [🔄 Iteradores Fail-Fast vs Fail-Safe: Como o Java detecta modificações concorrentes?](#3-iteradores-fail-fast-vs-fail-safe-como-o-java-detecta-modificacoes-concorrentes)
4. [🧩 Uma Interface Funcional pode conter métodos default e static?](#4-uma-interface-funcional-pode-conter-metodos-default-e-static)
5. [⚠️ Try-With-Resources: O que acontece quando o bloco try e o método close() lançam exceções simultaneamente?](#5-try-with-resources-o-que-acontece-quando-o-bloco-try-e-o-metodo-close-lancam-excecoes-simultaneamente)
6. [💡 Quais são as principais novidades do Java 8 e como elas mudaram o design de código?](#6-quais-sao-as-principais-novidades-do-java-8-e-como-elas-mudaram-o-design-de-codigo)
7. [🌱 O que acontece por baixo dos panos ao inicializar uma aplicação com `@SpringBootApplication`?](#7-o-que-acontece-por-baixo-dos-panos-ao-inicializar-uma-aplicacao-com-springbootapplication)
8. [🔌 Como a Injeção de Dependências (DI) do Spring funciona internamente?](#8-como-a-injecao-de-dependencias-di-do-spring-funciona-internamente)
9. [🛡️ Como o `@Transactional` funciona e qual o impacto do problema de self-invocation?](#9-como-o-transactional-funciona-e-qual-o-impacto-do-problema-de-self-invocation)
10. [🔄 Qual é o ciclo de vida completo de um Bean no Spring?](#10-qual-e-o-ciclo-de-vida-completo-de-um-bean-no-spring)
11. [🎭 Quais são os Escopos de Bean no Spring e qual a diferença para o Singleton Pattern (GoF)?](#11-quais-sao-os-escopos-de-bean-no-spring-e-qual-a-diferenca-para-o-singleton-pattern-gof)
12. [🗃️ O que é o problema de consulta N+1 no JPA/Hibernate e como resolvê-lo?](#12-o-que-e-o-problema-de-consulta-n1-no-jpahibernate-e-como-resolvelo)

---

## 1. Como o `ConcurrentHashMap` funciona internamente no Java 8?

### ❓ Pergunta de Entrevista
*Como o `ConcurrentHashMap` do Java 8 difere de um `HashMap` convencional e da implementação legada do Java 7? O que é feito para evitar locks globais em operações de escrita?*

### 💡 Resposta Detalhada (Under the Hood)
Diferente de um `HashMap` comum (que não é thread-safe e pode sofrer corrupção de estado ou loops infinitos sob concorrência), e do `ConcurrentHashMap` do Java 7 (que dividia o mapa rigidamente em **16 segmentos** com locks fixos), o **Java 8** redesenhou a estrutura completamente.

1. **Locks a Nível de Bucket (Bin-Level Locking):**  
   Em vez de bloquear segmentos inteiros, o Java 8 usa o primeiro nó de cada balde (bucket/bin) como o próprio monitor de lock. Ou seja, se duas threads tentarem atualizar chaves que caem em buckets diferentes (ex: Bucket 3 e Bucket 7), **ambas prosseguem em paralelo** sem nenhum bloqueio mútuo.
2. **Uso Intensivo de CAS (Compare-And-Swap):**  
   Ao inserir um valor em um bucket vazio, a JVM não adquire um lock pesado synchronized. Em vez disso, ela faz uma operação CAS atômica no nível da CPU:
   ```java
   // Pseudo-código do que acontece internamente:
   if (tab[i] == null) {
       if (casTabAt(tab, i, null, new Node<K,V>(hash, key, value, null)))
           break; // Inserido com sucesso sem bloquear!
   }
   ```
   Se o CAS falhar (porque outra thread inseriu um nó no mesmo milissegundo), a thread atual entra em um loop de retry ou adquire o lock `synchronized` do nó raiz daquele bucket específico caso ele já possua elementos.
3. **Leituras Não-Bloqueantes:**  
   As operações de leitura (`get`) usam referências de memória marcadas como `volatile` (como a referência ao array de nós e o campo `next` de cada nó). Isso garante a visibilidade de escrita imediata entre as memórias de cache dos núcleos de CPU (CPU caches) sem a necessidade de locks na leitura.
4. **Proibição de Chaves e Valores Nulos:**  
   Não são permitidos `null`s porque, em ambiente concorrente, um retorno `null` do método `get(key)` criaria ambiguidade (não é possível distinguir de forma determinística se a chave não existe ou se o valor mapeado é literalmente `null` sem causar condições de corrida entre chamadas de `containsKey` e `get`).

---

## 2. `HashMap` vs `ConcurrentHashMap` vs `SynchronizedMap`: Quando e por que usar?

### ❓ Pergunta de Entrevista
*Qual a diferença entre usar um `HashMap` comum, um mapa retornado por `Collections.synchronizedMap()` e um `ConcurrentHashMap`?*

### 💡 Resposta Detalhada (Under the Hood)

#### 📊 Tabela Comparativa de Comportamento Interno

| Característica | `HashMap` | `Collections.synchronizedMap()` | `ConcurrentHashMap` |
| :--- | :--- | :--- | :--- |
| **Mecanismo de Lock** | Nenhum (unsafe) | **Lock Global Único** (bloqueia o mapa inteiro) | **Lock por Bucket** + CAS (Compare-And-Swap) |
| **Escrita Concorrente** | Lança `ConcurrentModificationException` ou corrompe dados | Lenta (threads de escrita esperam umas pelas outras) | Altamente escalável (paralelismo real por bucket) |
| **Leitura Concorrente** | Rápida, mas perigosa (pode retornar dados inconsistentes) | Lenta (leitores disputam lock global com escritores) | **Rápida e segura** (não bloqueante para a maioria dos `get`s) |
| **Chaves/Valores Null**| Permite | Depende do mapa de origem (geralmente sim) | **Não permite** (lança `NullPointerException`) |

- **`Collections.synchronizedMap`:** Retorna um wrapper onde cada método é encapsulado por um bloco `synchronized(mutex)`. Isso introduz gargalo de concorrência massivo porque mesmo leitores sofrem bloqueio mútuo.
- **Recomendação:** Use `ConcurrentHashMap` em qualquer cenário onde o mapa é compartilhado globalmente entre threads. Use `HashMap` apenas para variáveis locais ou escopos estritamente de thread única.

---

## 3. Iteradores Fail-Fast vs Fail-Safe: Como o Java detecta modificações concorrentes?

### ❓ Pergunta de Entrevista
*Como um iterador do tipo "Fail-Fast" detecta que a coleção foi modificada? O que é o mecanismo do "Fail-Safe"?*

### 💡 Resposta Detalhada (Under the Hood)

#### 🚀 Mecanismo do Fail-Fast (ex: `ArrayList`)
Internamente, a classe `ArrayList` possui um campo inteiro chamado `modCount` (contador de modificações estruturais, como adições, inserções e remoções). 

Quando você chama `list.iterator()`, o iterador criado copia esse valor em uma variável interna chamada `expectedModCount`:

```
ArrayList (modCount = 5)  ───> Cria Iterator (expectedModCount = 5)
```

Se a lista for modificada fora do iterador (ex: `list.add(value)`), o `modCount` da lista sobe para 6. Na próxima chamada de `iterator.next()` ou `iterator.hasNext()`, a verificação é realizada:

```java
if (modCount != expectedModCount) {
    throw new ConcurrentModificationException();
}
```

> **Atenção:** Fail-fast é um mecanismo de "melhor esforço" (*best-effort*). Ele serve apenas para depuração de bugs de concorrência no mesmo fluxo de execução e **não deve** ser usado como garantia de concorrência.

#### 🛡️ Mecanismo do Fail-Safe (ex: `CopyOnWriteArrayList`)
Embora o termo "Fail-Safe" não esteja formalmente escrito na especificação do Java, ele se refere a iteradores que não lançam exceção quando a estrutura muda:
- No caso do `CopyOnWriteArrayList`, ao iniciar uma iteração, o iterador obtém uma referência direta para o array atual (um *snapshot* estático em memória).
- Se outra thread adicionar um elemento, um novo array de dados é instanciado e a referência principal da lista é atualizada. O iterador antigo continua percorrendo a cópia anterior imutável intacta.

---

## 4. Uma Interface Funcional pode conter métodos default e static?

### ❓ Pergunta de Entrevista
*Quais são as regras para que uma interface seja considerada "Funcional" (SAM)? Ela pode ter métodos concretos?*

### 💡 Resposta Detalhada (Under the Hood)
Sim, ela pode conter múltiplos métodos concretos, desde que contenha **exatamente um método abstrato** (SAM - *Single Abstract Method*).

#### 📜 Estrutura Interna de Compilação
A anotação `@FunctionalInterface` é meramente informativa para o compilador (evita que outros desenvolvedores acidentalmente adicionem novos métodos abstratos àquela interface no futuro).
- **Métodos `default`:** Possuem corpo de implementação e não contam como abstratos. Eles existem para permitir a evolução de interfaces sem quebrar códigos legados.
- **Métodos `static`:** Também possuem código e pertencem ao escopo da própria interface, não da instância.
- **Métodos da classe `Object`:** Métodos públicos declarados na classe `java.lang.Object` (como `public boolean equals(Object obj)` ou `public int hashCode()`) quando explícitos na interface **não contam** como o único método abstrato.

```java
@FunctionalInterface
public interface Validator<T> {
    
    // O único método abstrato (SAM)
    boolean isValid(T target);

    // Métodos default são aceitos
    default Validator<T> and(Validator<T> other) {
        return target -> isValid(target) && other.isValid(target);
    }

    // Métodos static são aceitos
    static <T> Validator<T> alwaysTrue() {
        return target -> true;
    }
}
```

---

## 5. Try-With-Resources: O que acontece quando o bloco try e o método close() lançam exceções simultaneamente?

### ❓ Pergunta de Entrevista
*Se o código dentro de um bloco try-with-resources falhar e, ao tentar fechar o recurso no close(), outra exceção for lançada, qual exceção será propagada para quem chamou o método? E onde fica a outra exceção?*

### 💡 Resposta Detalhada (Under the Hood)
A **exceção disparada dentro do bloco try** (a falha principal de negócio) é a que será capturada e propagada. A exceção lançada pelo método `close()` não é perdida: ela é marcada como uma **exceção suprimida** (*suppressed exception*).

```
[Exceção no Bloco Try (Principal)]
          │
          └───► [Exceções Suprimidas (Anexadas)]
                     └───► Exceção vinda do close()
```

#### ☕ Recuperando Exceções Suprimidas em Código:
```java
try (MyResource res = new MyResource()) {
    throw new RuntimeException("Falha no processamento principal"); // Exceção Primária
} catch (RuntimeException ex) {
    System.out.println("Capturada: " + ex.getMessage());
    
    // Obtendo as exceções que ocorreram durante o fechamento do recurso:
    Throwable[] suppressed = ex.getSuppressed();
    for (Throwable s : suppressed) {
        System.out.println("Suprimida: " + s.getMessage());
    }
}
```

#### 🛡️ Requisitos do Recurso:
Para ser utilizado na sintaxe do try-with-resources, o objeto deve implementar a interface `java.lang.AutoCloseable` ou `java.io.Closeable`. Se múltiplos recursos forem abertos na mesma instrução, o fechamento ocorre na **ordem inversa** à que foram declarados.

---

## 6. Quais são as principais novidades do Java 8 e como elas mudaram o design de código?

### ❓ Pergunta de Entrevista
*Quais foram as grandes novidades introduzidas no Java 8 que alteraram o estilo de programação imperativa para declarativa/funcional?*

### 💡 Resposta Detalhada (Under the Hood)

1. **Expressões Lambda:** 
   Substituem classes anônimas verbosas por representações de comportamento de linha única, reduzindo o overhead sintático.
2. **Stream API (`java.util.stream`):**
   Permite o processamento declarativo de coleções de dados utilizando pipelines (filtros, mapeamentos, reduções). O foco muda de "*como fazer*" (loops `for` manuais) para "*o que deve ser feito*".
3. **Optional (`java.util.Optional`):**
   Um wrapper de referência tipada para encapsular a presença ou ausência de um valor, forçando assinaturas de métodos a exporem de forma transparente quando podem retornar vazios, atenuando a proliferação de `NullPointerException`.
4. **Métodos Default e Static em Interfaces:**
   Permitiu à equipe de desenvolvimento do JDK estender as interfaces do framework de Collections (ex: adicionar o método `stream()` ou `forEach()`) sem quebrar bilhões de linhas de código de implementações customizadas ao redor do mundo.
5. **Nova API de Date & Time (`java.time`):**
   Substituiu as classes inseguras para concorrência (non-thread-safe) e confusas `java.util.Date` e `Calendar` por classes imutáveis e legíveis baseadas no padrão ISO-8601 (como `LocalDate`, `LocalTime`, `Instant`).

---

## 7. O que acontece por baixo dos panos ao inicializar uma aplicação com `@SpringBootApplication`?

### ❓ Pergunta de Entrevista
*Quando executamos `SpringApplication.run(Application.class, args)` em uma classe com `@SpringBootApplication`, qual é o fluxo interno de inicialização do Spring Boot?*

### 💡 Resposta Detalhada (Under the Hood)

```
[SpringApplication.run()] ──> Instancia ApplicationContext
                                     │
                                     ▼
                      [Varre @SpringBootApplication]
                      ├── @Configuration (Classe fonte)
                      ├── @ComponentScan (Varre pacotes por @Component, @Service...)
                      └── @EnableAutoConfiguration
                                     │
                                     ▼
          [Lê arquivos .imports do Autoconfigure / META-INF]
                                     │
                                     ▼
        [Instancia e injeta beans se as Condições forem atendidas]
        (ex: @ConditionalOnClass, @ConditionalOnMissingBean)
                                     │
                                     ▼
              [Inicializa o Servidor Embutido (ex: Tomcat)]
```

1. **Combinação de Três Anotações Base:**
   A anotação `@SpringBootApplication` é um atalho para:
   - `@Configuration`: Identifica a classe como fonte de definições de beans do Spring.
   - `@ComponentScan`: Instrui o Spring a varrer o pacote atual e subpacotes em busca de componentes estocados (`@Component`, `@Service`, `@Repository`, `@RestController`).
   - `@EnableAutoConfiguration`: Habilita o mecanismo de configuração automática do Spring Boot.
2. **Carregamento das Configurações Automáticas:**
   O Spring Boot busca no classpath por arquivos de definição:
   - *Spring Boot 3.x:* `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`.
   - *Spring Boot 2.x:* `META-INF/spring.factories` sob a chave `EnableAutoConfiguration`.
3. **Validação das Condições (`@Conditional`):**
   Para cada classe de configuração automática importada, o Spring verifica se os requisitos foram atendidos (ex: se o driver do PostgreSQL está no classpath, ele configura automaticamente um bean de `DataSource`).
4. **Subida do Servidor Embutido:**
   Se for detectado que a aplicação é do tipo Web, o Spring cria um servidor HTTP embarcado (como o Tomcat ou Jetty) e o inicializa de forma programática como parte do ciclo do `ApplicationContext`.

---

## 8. Como a Injeção de Dependências (DI) do Spring funciona internamente?

### ❓ Pergunta de Entrevista
*Como o Spring sabe quais classes instanciar e como ele resolve dependências dinamicamente sem o uso de `new` explícito?*

### 💡 Resposta Detalhada (Under the Hood)

1. **Varredura (Scanning) e Registro:**
   O Spring lê as classes marcadas com anotações de componente. Ele não cria instâncias de imediato; primeiro ele cria objetos do tipo `BeanDefinition` (metadados com tipo, escopo e dependências do bean).
2. **Resolução do Grafo de Dependências:**
   O container cria um Grafo Direcionado Acíclico (DAG) das dependências para descobrir a ordem topológica correta de criação (ex: se A precisa de B, B deve ser criado primeiro).
3. **Instanciação por Reflexão (Reflection):**
   Utilizando a Reflection API (`Constructor.newInstance`), o Spring cria a instância no heap do Java. A injeção por construtor é a recomendada porque garante que o objeto nunca seja instanciado em estado inconsistente/incompleto.
4. **Post-Processors (BeanPostProcessor):**
   Após a criação básica, o objeto passa por pós-processadores de beans (`BeanPostProcessor`). É aqui que o Spring analisa e adiciona interceptadores AOP para transações, segurança ou validação de beans.

---

## 9. Como o `@Transactional` funciona e qual o impacto do problema de self-invocation?

### ❓ Pergunta de Entrevista
*Como o Spring gerencia transações com `@Transactional` sem alteração direta de bytecode? O que é o problema da autofocalização/self-invocation?*

### 💡 Resposta Detalhada (Under the Hood)

#### 🛡️ O Mecanismo do Proxy Dinâmico
Quando você anota um método ou classe com `@Transactional`, o Spring não entrega a referência direta do seu objeto para os outros beans. Ele gera e injeta uma **classe Proxy dinâmica** (gerada em runtime via JDK Dynamic Proxy ou CGLIB).

```
Chamador ──> [Spring Proxy (Transaction Interceptor)] ──> [Objeto Real (Seu Serviço)]
                   │                                             ▲
                   ├── 1. Abre Transação                         │
                   ├── 2. Invoca Método ─────────────────────────┤
                   └── 3. Commit / Rollback se houver Exception  │
```

O proxy atua como um wrapper: ele intercepta a chamada, inicia a conexão transacional com o banco de dados (abrindo a transação), executa o método real e, caso não ocorram exceções não verificadas (`RuntimeException`), faz o commit. Se uma exceção não verificada for lançada, ele sinaliza o rollback no banco.

#### 🚨 O Problema da Auto-Invocação (Self-Invocation)
Se uma classe chamar internamente um método seu que possui `@Transactional`, a chamada **ignora o proxy** e a transação **não é iniciada**.

```java
@Service
public class PaymentService {

    public void processPayment() {
        // Chamada interna direta
        // Equivalente a 'this.saveToDatabase()'
        saveToDatabase(); 
    }

    @Transactional
    public void saveToDatabase() {
        // O proxy não intercepta esta chamada! 
        // Não haverá início de transação aqui.
    }
}
```

- **Por que acontece:** Como a chamada a `saveToDatabase()` foi iniciada a partir de um método da própria classe (`processPayment`), a JVM executa a chamada sobre a referência `this` real, contornando o objeto proxy que o Spring gerou.
- **Como corrigir:** Mover o método transacional para uma classe dedicada diferente, injetar o próprio serviço de forma preguiçosa (`@Lazy`) ou usar transações programáticas (`TransactionTemplate`).

---

## 10. Qual é o ciclo de vida completo de um Bean no Spring?

### ❓ Pergunta de Entrevista
*Qual a sequência exata de eventos de ciclo de vida que ocorre quando o Spring cria e destrói um Bean?*

### 💡 Resposta Detalhada (Under the Hood)

#### 🔄 Fases do Ciclo de Vida:
```
1. Instanciação (Criação física do objeto via Construtor)
   ↓
2. População de Propriedades (Injeção de dependências via campos/@Autowired/Setters)
   ↓
3. Callbacks de Aware (Injeta informações de infra, ex: BeanNameAware, ApplicationContextAware)
   ↓
4. BeanPostProcessor (Método: postProcessBeforeInitialization)
   ↓
5. Inicialização:
   ├── Executa método com anotação @PostConstruct
   ├── Executa InitializingBean.afterPropertiesSet()
   └── Executa método configurado como 'init-method' customizado
   ↓
6. BeanPostProcessor (Método: postProcessAfterInitialization - onde são tecidos Proxies AOP)
   ↓
7. Bean Pronto (Ativo e utilizável pela aplicação)
   ↓
8. Destruição (Inicia ao fechar o container):
   ├── Executa método anotado com @PreDestroy
   ├── Executa DisposableBean.destroy()
   └── Executa método 'destroy-method' customizado
```

---

## 11. Quais são os Escopos de Bean no Spring e qual a diferença para o Singleton Pattern (GoF)?

### ❓ Pergunta de Entrevista
*Quais são os escopos de beans suportados pelo Spring e qual a diferença crucial entre o escopo Singleton do Spring e o padrão de projeto Singleton clássico do livro da Gang of Four (GoF)?*

### 💡 Resposta Detalhada (Under the Hood)

#### 1. Diferença de Escopo de Singleton
- **Singleton GoF (Clássico):** Garante a existência de exatamente uma instância de uma determinada classe por **Classloader** da JVM. O construtor é privado e o controle é codificado de forma estática.
- **Singleton do Spring:** Garante a existência de exatamente uma instância **por Container do Spring (ApplicationContext)**. Se houver mais de um container na mesma JVM (ou definições de bean distintas apontando para a mesma classe), poderão existir múltiplas instâncias daquela classe.

#### 🎭 Outros Escopos Comuns:
- **`prototype`:** Uma nova instância é criada sempre que o bean for solicitado (`context.getBean()` ou injeção). O Spring não gerencia a fase de destruição para beans prototype.
- **`request`:** Uma instância é vinculada ao ciclo de vida de uma única requisição HTTP (web-aware).
- **`session`:** Instância atrelada ao tempo de vida da sessão HTTP do usuário.
- **`application`:** Instância compartilhada por todo o escopo do `ServletContext`.
- **`websocket`:** Instância associada ao ciclo de vida de uma conexão WebSocket.

---

## 12. O que é o problema de consulta N+1 no JPA/Hibernate e como resolvê-lo?

### ❓ Pergunta de Entrevista
*O que é a anomalia N+1 no JPA/Hibernate e como ela pode degradar drasticamente a performance do banco de dados sem que ocorram erros de compilação ou log de exceções?*

### 💡 Resposta Detalhada (Under the Hood)

#### ⚠️ A Origem do Problema
Ocorre quando realizamos uma busca inicial para carregar registros da entidade pai (1 query) e, em seguida, o Hibernate executa subconsultas individuais em cascata para carregar as coleções filhas associadas de cada registro pai (N queries adicionais), gerando latência de rede massiva.

Se você tem 100 registros de `Department` e quer buscar todos eles para imprimir seus `Employee`s:
```java
// Dispara 1 consulta para obter os 100 departamentos:
List<Department> depts = repository.findAll();

// Para cada departamento, ao acessar a lista de funcionários (Lazy Loading):
for (Department d : depts) {
    // Dispara 1 consulta separada no banco para carregar a coleção de funcionários daquele departamento:
    d.getEmployees().size(); 
}
```
**Total de chamadas ao banco:** $1 \text{ (dos pais)} + 100 \text{ (dos filhos)} = 101 \text{ queries}$.

#### 🛠️ Estratégias de Resolução

1. **Uso de `JOIN FETCH` (Recomendado para queries JPQL específicas):**
   Instrui o Hibernate a realizar um JOIN relacional comum e carregar imediatamente as associações na mesma query SQL:
   ```java
   @Query("SELECT d FROM Department d JOIN FETCH d.employees")
   List<Department> findAllWithEmployees();
   ```
2. **Definição de `@EntityGraph`:**
   Mecanismo declarativo do JPA para indicar quais atributos do relacionamento devem ser carregados eager de forma dinâmica:
   ```java
   @EntityGraph(attributePaths = {"employees"})
   List<Department> findAll();
   ```
3. **Batch Fetching (`@BatchSize`):**
   Configura o Hibernate para agrupar as cargas de entidades filhas em lotes menores usando cláusulas SQL `IN (...)`:
   ```java
   @OneToMany
   @BatchSize(size = 25)
   private List<Employee> employees;
   ```
   Em vez de 100 queries secundárias, o Hibernate agrupa em lotes de 25, reduzindo para apenas 4 queries secundárias.
4. **Projeções DTO (Data Transfer Object):**
   Se a tela ou API precisa apenas de dados pontuais (ex: nome do departamento e a contagem de funcionários), é melhor consultar os dados diretamente via projeção SQL simples, evitando carregar e gerenciar todo o grafo de entidades em memória.

---
*Fim do roteiro complementar de análise técnica.*
