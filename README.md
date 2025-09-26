# Projeto AI Arch Review

Projeto de análise de imagens de arquitetura de sistemas usando o modelo STRIDE, com backend em **Python (Azure Functions)** e frontend em **Angular**.  
O sistema permite enviar imagens, gerar anotações automáticas e uma análise detalhada em Markdown.

---

## Estrutura do repositório

```
repo-root/
│
├─ backend/ # Python + Azure Functions
│ ├─ requirements.txt
│ ├─ local.settings.json (não versionado)
│ ├─ function_app.py
│ └─ services/
│
├─ frontend/ # Angular
│ ├─ package.json
│ ├─ angular.json
│ └─ src/
│
└─ README.md
```

> Cada pasta pode ser versionada separadamente, com CI/CD próprio.

---

## Backend (Python + Azure Functions)

### Pré-requisitos
- Python 3.9+
- [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- Variáveis de ambiente:
  - `OPENAI_API_KEY` → chave de API da OpenAI

### Instalando dependências
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Rodando localmente
```bash
func start
```

## Frontend (Angular)

### Pré-requisitos
 - Node.js 18+
 - Angular CLI

### Instalando dependências

```bash
cd frontend
npm install
```

### Rodando localmente

```bash
ng serve
```

O frontend será servido em `http://localhost:4200`.

---

## Funcionamento

1. Acesse o frontend.
2. Faça upload de uma imagem.
3. O backend envia a imagem para o modelo STRIDE e gera:
    * Overlay com anotações da imagem
    * Markdown detalhado de análise STRIDE
4. O frontend exibe a imagem anotada e o Markdown renderizado.

## Boas práticas

* Separar repositórios se o projeto crescer: backend e frontend.
* Não versionar arquivos de configuração sensíveis (local.settings.json, .env).
* Utilizar CI/CD separado:
    * Backend → testes Python, deploy Azure Functions
    * Frontend → build Angular, deploy em static hosting

## Tecnologias utilizadas

* Backend: Python 3, Azure Functions, OpenAI API
* Frontend: Angular, Angular Material, ngx-markdown