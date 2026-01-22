# Implantação Canary com Istio Service Mesh

![Istio Canary Deployment](./images/istio-canary-deployment.png)

Este diagrama ilustra como utilizar um Service Mesh para realizar implantações seguras do tipo Canary, minimizando riscos ao lançar novas versões de um serviço.

## Padrões e Técnicas Utilizadas

- **Canary Deployment:** Estratégia de lançamento onde uma nova versão (V2) é exposta a uma pequena fração do tráfego real antes de ser lançada para todos.
- **Service Mesh (Istio):** Uma camada de infraestrutura dedicada para gerenciar a comunicação entre serviços (L7 traffic management).
- **Sidecar Pattern:** O **Envoy Proxy** roda como um container adjacente a cada Pod, interceptando e gerenciando todo o tráfego de entrada e saída.
- **Traffic Splitting:** Divisão programática do tráfego baseada em regras definidas no Virtual Service.

## Componentes e Suas Funções

### 1. Camada de Ingress
- **Cloud Load Balancer:** Ponto de entrada externo (AWS ELB/GCP LB).
- **Istio Gateway:** Gerencia o tráfego de borda do cluster, definindo quais portas e protocolos estão expostos.

### 2. Controle de Tráfego (Service Mesh)
- **Istio Virtual Service:** O componente chave onde a lógica de roteamento reside. Aqui é definido que 95% do tráfego vá para a V1 e 5% para a V2.
- **Service V1 vs Service V2:** Abstrações do Kubernetes que agrupam os Pods de cada versão.

### 3. Camada de Execução (Pods)
- **Payment V1 (Stable):** Versão atual e estável do serviço.
- **Payment V2 (Canary):** Nova versão em teste.
- **Envoy Proxy Sidecar:** Realiza o roteamento real, coleta métricas e aplica políticas de segurança (mTLS) dentro do mesh.

## Benefícios Desta Abordagem
- **Rollback Instantâneo:** Se a versão V2 (5%) apresentar erros, basta alterar a regra no Virtual Service para 0%.
- **Observabilidade:** O Istio permite monitorar o sucesso da V2 em comparação à V1 sem alterar o código da aplicação.
- **Segurança:** O tráfego entre os proxies pode ser criptografado automaticamente via mTLS.
