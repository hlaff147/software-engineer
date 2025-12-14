# MongoDB ObjectId DateTime Proof

Este projeto demonstra que o ObjectId do MongoDB contém um timestamp embutido, provando que documentos inseridos posteriormente têm ObjectIds com timestamps mais recentes.

## 🎯 Objetivo

Provar que:
1. Cada `_id` (ObjectId) possui um datetime diferente
2. O último ObjectId inserido tem uma data mais recente que o primeiro

## 🛠️ Tecnologias

- **FastAPI** - API REST
- **MongoDB** - Banco de dados
- **PyMongo/BSON** - Driver MongoDB e extração do timestamp
- **Docker** - Container para MongoDB
- **Jupyter Notebook** - Visualização e análise

## 🚀 Como Executar

### 1. Iniciar MongoDB com Docker

```bash
cd mongodb-objectid-proof
docker-compose up -d
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Iniciar a API

```bash
uvicorn app.main:app --reload --port 8000
```

Acesse: http://localhost:8000/docs

### 4. Executar o Jupyter Notebook

```bash
jupyter notebook notebooks/objectid_analysis.ipynb
```

## 📡 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/documents` | Insere um documento |
| POST | `/documents/batch` | Insere múltiplos documentos com delay opcional |
| GET | `/documents` | Lista todos com timestamps do ObjectId |
| DELETE | `/documents` | Remove todos os documentos |
| GET | `/documents/compare-first-last` | Compara primeiro e último ObjectId |

## 📊 Conceito do ObjectId

```
|----- 4 bytes -----|--- 3 bytes ---|-- 2 bytes --|-- 3 bytes --|
|    Timestamp      |  Machine ID   | Process ID  |   Counter   |
```

Use `ObjectId.generation_time` do módulo `bson` para extrair o timestamp.

## 📝 Licença

MIT
