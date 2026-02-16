---

# 📌 User API – CRUD com Kotlin, Spring Boot e MongoDB

Uma API REST simples para gerenciamento de usuários, desenvolvida em **Kotlin**, usando **Spring Boot** e **MongoDB**, sem Lombok e com uso de **DTOs** para requests e responses.

## 🚀 Tecnologias
- [Kotlin](https://kotlinlang.org/)  
- [Spring Boot](https://spring.io/projects/spring-boot)  
- [Spring Data MongoDB](https://spring.io/projects/spring-data-mongodb)  
- [Bean Validation – Jakarta](https://jakarta.ee/specifications/bean-validation/)  
- [BCrypt](https://spring.io/projects/spring-security) para hash de senhas  
- MongoDB como banco de dados NoSQL  

---

## 📂 Estrutura de Pastas
```

src/main/kotlin/user/userApi/
├── UserApiApplication.kt        # Classe principal
├── domain/                      # Entidades do domínio
├── dto/                         # DTOs de request/response
├── repository/                  # Repositórios (MongoRepository)
├── service/                      # Regras de negócio
├── controller/                  # Endpoints REST
└── config/                       # Configurações extras (ex: MongoConfig)

````

---

## ⚙️ Pré-requisitos
- **Java 17**
- **Maven 3.9+**
- **Docker** (opcional, para subir o MongoDB localmente)

---

## 🛠️ Configuração do Banco de Dados

### Opção 1 — Usando Docker
```bash
docker run -d --name mongo \
  -p 27017:27017 \
  -v mongo-data:/data/db \
  mongo:7
````

### Opção 2 — Mongo local

Instale e inicie o MongoDB na porta padrão (`27017`).

---

## 📄 Configuração da aplicação

No `application.yml`:

```yaml
spring:
  data:
    mongodb:
      uri: mongodb://localhost:27017/users_db
```

---

## ▶️ Executando a aplicação

```bash
mvn spring-boot:run
```

A API estará disponível em:

```
http://localhost:8080
```

---

## 📚 Endpoints

| Método | Endpoint          | Descrição                     |
| ------ | ----------------- | ----------------------------- |
| POST   | `/api/users`      | Criar novo usuário            |
| GET    | `/api/users`      | Listar usuários com paginação |
| GET    | `/api/users/{id}` | Buscar usuário por ID         |
| PATCH  | `/api/users/{id}` | Atualizar dados do usuário    |
| DELETE | `/api/users/{id}` | Deletar usuário               |

---

## 🧪 Testando com `curl`

### Criar usuário

```bash
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  --data-raw '{"name":"Ana","email":"ana@example.com","password":"segredo123"}'
```

### Listar usuários

```bash
curl "http://localhost:8080/api/users?page=0&size=5"
```

### Buscar por ID

```bash
curl http://localhost:8080/api/users/ID_AQUI
```

### Atualizar parcialmente

```bash
curl -X PATCH http://localhost:8080/api/users/ID_AQUI \
  -H "Content-Type: application/json" \
  --data-raw '{"name":"Ana Silva","active":false}'
```

### Alterar senha

```bash
curl -X PATCH http://localhost:8080/api/users/ID_AQUI \
  -H "Content-Type: application/json" \
  --data-raw '{"newPassword":"novaSenhaSegura123"}'
```

### Deletar usuário

```bash
curl -X DELETE http://localhost:8080/api/users/ID_AQUI
```

---

## 🛡️ Validações

* **Nome**: mínimo 2 e máximo 120 caracteres
* **Email**: formato válido e único
* **Senha**: mínimo 6 caracteres
* **Senha armazenada**: sempre como hash BCrypt

---

## 📜 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar e modificar.

---