# Desafio Técnico - API de Criação de Conta Bancária

## Visão Geral
Este desafio consiste em uma API de criação de contas bancárias parcialmente desenvolvida por uma IA. A aplicação contém bugs, problemas estruturais e más práticas que precisam ser identificados e corrigidos.

Seu objetivo é analisar, corrigir e melhorar o código existente, garantindo que todos os requisitos funcionais sejam atendidos e que a base de código esteja pronta para futuras implementações.

## Requisitos Funcionais

### Criação de Conta
- Implementar um endpoint que permita a criação de contas de usuário
- Toda conta criada deve estar no estado **ativo** por padrão
- Se um código de indicação válido for fornecido, a conta deve ser iniciada com saldo de **R$10,00**

### Especificação da API

#### Endpoint para Criação de Conta
- **Método**: POST
- **URL**: http://localhost:8080/corabank
- **Conteúdo** (JSON):
```json
{
    "name": "Nome do Usuário",
    "cpf": "12345678901",
    "referralCode": "CORA10"
}
```

#### Resposta Esperada
- **Conteúdo** (JSON):
```json
{
    "id": 1,
    "name": "Nome do Usuário",
    "cpf": "12345678901",
    "balance": 10.00,  // 0.00 se nenhum código de indicação válido for informado
    "active": true
}
```

## Objetivos do Desafio
1. **Correção de Bugs**: Identificar e corrigir os erros presentes na implementação atual
2. **Refatoração**: Eliminar code smells e aplicar boas práticas de desenvolvimento
3. **Implementação**: Completar funcionalidades ausentes ou incorretas
4. **Testes**: Implementar testes automatizados para validar o comportamento da API é um plus

### Banco de Dados
- A aplicação utiliza um banco de dados H2 em memória
- Console de administração: http://localhost:8080/h2-console
- Credenciais:
  - **JDBC URL**: `jdbc:h2:mem:testdb`
  - **Username**: `sa`
  - **Password**: (deixe em branco)
