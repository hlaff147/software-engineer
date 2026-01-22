# Design Patterns — perguntas objetivas (Factory, Strategy, Template Method)

## Como responder “o que é Design Pattern?”

**Resposta curta:** soluções recorrentes para problemas recorrentes de design, com nomes compartilhados para comunicação e redução de acoplamento.

**Gatilhos:** intenção > implementação, trade-offs, composição.

---

## Factory (Factory Method / Simple Factory)

**Pergunta:** Quando usar Factory?

**Resposta curta:** quando a criação de objetos varia por regras (tipo, config, contexto) e você quer esconder `new` + reduzir acoplamento.

**Gatilhos:** centralizar criação, variar implementação sem mudar cliente, map tipo→classe.

**Exemplo simples (ideia):**
```java
interface Notificador { void enviar(String msg); }

class EmailNotificador implements Notificador {
  public void enviar(String msg) { /* ... */ }
}

class SmsNotificador implements Notificador {
  public void enviar(String msg) { /* ... */ }
}

class NotificadorFactory {
  static Notificador criar(String canal) {
    return switch (canal) {
      case "email" -> new EmailNotificador();
      case "sms" -> new SmsNotificador();
      default -> throw new IllegalArgumentException("Canal inválido");
    };
  }
}
```

**Trade-offs:** fábrica pode virar “Deus” se crescer; às vezes DI/IoC resolve melhor.

---

## Strategy

**Pergunta:** Quando usar Strategy?

**Resposta curta:** quando você tem **variações de algoritmo/regra** e quer trocar em runtime sem `if/else` gigante.

**Gatilhos:** OCP, composição, regra por país/canal/status, testes por estratégia.

**Exemplo (desconto):**
```java
interface RegraDesconto { long aplicar(long valor); }

class DescontoVip implements RegraDesconto {
  public long aplicar(long valor) { return Math.round(valor * 0.9); }
}

class DescontoPadrao implements RegraDesconto {
  public long aplicar(long valor) { return valor; }
}

class CheckoutService {
  private final RegraDesconto regra;
  CheckoutService(RegraDesconto regra) { this.regra = regra; }
  long total(long valor) { return regra.aplicar(valor); }
}
```

**Como falar em Spring:** injeção de lista/map de strategies, escolher por chave.

---

## Template Method

**Pergunta:** O que é Template Method e quando faz sentido?

**Resposta curta:** define um “esqueleto” de algoritmo em uma classe base e permite customizar passos via métodos abstratos/gancho.

**Gatilhos:** fluxo padrão com variações, pipeline fixo, herança controlada.

**Exemplo (pipeline):**
```java
abstract class ImportadorBase {
  public final void importar(String arquivo) {
    validar(arquivo);
    var dados = ler(arquivo);
    transformar(dados);
    salvar(dados);
  }

  protected void validar(String arquivo) {}
  protected abstract Object ler(String arquivo);
  protected abstract void transformar(Object dados);
  protected abstract void salvar(Object dados);
}
```

**Trade-offs:** usa herança (pode limitar); às vezes composição (Strategy) é melhor.

---

## Pergunta comum: “Strategy vs Template Method?”

**Resposta curta:** Strategy troca comportamento por composição (mais flexível); Template Method fixa o fluxo por herança e deixa ganchos.
