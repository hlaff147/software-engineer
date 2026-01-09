# Vuln Analyzer Agent

Agente Python para análise de vulnerabilidades em projetos Java Spring (Maven).

## Instalação

```bash
cd vuln-analyzer-agent
pip install -e .

# Com suporte a Mend.io
pip install -e ".[mend]"
```

## Uso

### Análise de Vulnerabilidades

```bash
# Scan básico (OWASP + NVD)
vuln-analyzer scan /path/to/java/project

# Com integração Mend (requer config)
vuln-analyzer scan /path/to/java/project --mend

# Gerar relatório HTML
vuln-analyzer scan /path/to/java/project --format html --output report.html

# Gerar relatório JSON
vuln-analyzer scan /path/to/java/project --format json --output report.json
```

### Correção Automática

```bash
# Preview de correções (dry-run)
vuln-analyzer fix /path/to/java/project --dry-run

# Aplicar correções
vuln-analyzer fix /path/to/java/project --apply
```

## Configuração

Crie um arquivo `config.yaml` (opcional):

```yaml
# Mend.io credentials (optional)
mend:
  api_key: "your-api-key"
  user_key: "your-user-key"
  org_token: "your-org-token"
  url: "https://saas.mend.io"  # ou URL on-premise

# NVD API Key (para evitar rate limiting)
nvd:
  api_key: "your-nvd-api-key"

# OWASP Dependency-Check
owasp:
  path: "/path/to/dependency-check"  # opcional, usa PATH por padrão
  
# Thresholds
thresholds:
  fail_on_cvss: 7.0  # Falha se CVSS >= 7.0
  
# Ignorar vulnerabilidades específicas
suppressions:
  - CVE-2023-12345
  - CVE-2024-67890
```

## Fontes de Dados

1. **OWASP Dependency-Check**: Análise offline usando NVD
2. **NVD Direct**: Consulta direta ao National Vulnerability Database
3. **Mend.io** (opcional): Inclui vulnerabilidades proprietárias "WS-"

## Requisitos

- Python 3.11+
- Java 11+ (para OWASP Dependency-Check)
- OWASP Dependency-Check CLI (opcional, baixado automaticamente)
