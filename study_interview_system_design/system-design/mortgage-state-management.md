# Orquestração de Fluxos Longos (Empréstimo Imobiliário)

![Mortgage System Design](./images/emprestimo_imovel_system_des.png)

Processos de empréstimo imobiliário são complexos, duram dias ou semanas e envolvem múltiplas etapas humanas e automáticas. Este diagrama mostra como gerenciar esse estado.

## Padrões e Técnicas Utilizadas

- **Workflow Orchestration:** Uso de uma engine de BPMN (Camunda/Zeebe) para coordenar a ordem de execução das tarefas e gerenciar retentativas.
- **Saga Orchestration:** A engine central coordena as transações entre diferentes domínios (Documentos, Análise, Avaliação).
- **State Machine:** O processo é tratado como uma máquina de estados finitos persistida em banco de dados.
- **OCR (Optical Character Recognition):** Processamento automático de documentos para extração de dados.

## Componentes e Suas Funções

### 1. State Management (Orquestração)
- **Mortgage Service:** Serviço de entrada que inicia o processo de empréstimo.
- **BPMN Engine (Camunda/Zeebe):** O orquestrador central. Ele sabe que o "Passo 2" só ocorre após o sucesso do "Passo 1". Se um passo falhar, ele pode executar uma lógica de compensação.
- **Postgres (State):** Armazena o estado atual de cada processo de empréstimo (ex: "Aguardando Análise Humana").

### 2. Domain Services (Executores)
- **Document Service:** Gerencia o upload e a extração de dados de documentos via OCR, salvando os originais no **AWS S3**.
- **Underwriting Service:** Integração com o painel do analista para decisão humana (análise de risco).
- **Property Valuation:** Serviço que consulta APIs externas (Prefeitura/Cartórios) para avaliar o imóvel.

## Fluxo de Execução
1. O usuário faz o upload de documentos via App.
2. O **Mortgage Service** sinaliza a **BPMN Engine** para iniciar um novo processo.
3. **Passo 1:** A engine chama o **Document Service** para processar os arquivos.
4. **Passo 2:** A engine solicita a análise ao **Underwriting Service**. O estado fica pausado no Postgres até que um humano aprove no painel.
5. **Passo 3:** Após aprovação, a engine chama a **Property Valuation** para validar o imóvel via API externa.
6. O estado final é persistido e o usuário é notificado.
