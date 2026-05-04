🚀 Lead Capture & WhatsApp Automation System
Este projeto é um ecossistema completo de automação para captura de leads e notificações em tempo real. Ele integra um formulário frontend, uma API de persistência em Python e um fluxo de orquestração via n8n para disparos automáticos no WhatsApp via Evolution API.

🛠️ Tecnologias e Arquitetura
O projeto foi construído utilizando uma stack moderna e containerizada, garantindo escalabilidade e facilidade de deploy:

Frontend: HTML5, CSS3 e JavaScript (Fetch API) para captura de dados.

Backend: FastAPI (Python 3.10+) pela sua alta performance e suporte nativo a operações assíncronas.

Banco de Dados: SQLite para persistência leve e rápida de dados locais.

Orquestração de Workflow: n8n (self-hosted via Docker) para gerenciar a lógica de negócios e webhooks.

Integração WhatsApp: Evolution API (Docker) para comunicação estável com o protocolo do WhatsApp.

Infraestrutura: Docker & Docker Compose para padronização dos ambientes de serviços.

📝 Como o projeto foi construído (Passo a Passo)
Containerização: O primeiro passo foi configurar o docker-compose.yml para subir instâncias separadas do n8n e da Evolution API, permitindo que os serviços se comuniquem em uma rede isolada.

API de Recebimento: Desenvolvi uma API em FastAPI que expõe o endpoint /api/enviar. Esta rota valida os dados recebidos do frontend, grava as informações no clientes.db usando SQLAlchemy/SQLite e, em seguida, dispara um Webhook para o n8n.

Configuração de Rede Docker: Um desafio técnico superado foi a comunicação entre o host (Python rodando localmente) e o container (n8n). Isso foi resolvido utilizando host.docker.internal para garantir que o n8n alcançasse a API local.

Automação no n8n: O workflow foi desenhado para receber o JSON do Python, tratar os dados e realizar uma requisição HTTP POST para a Evolution API, enviando a mensagem personalizada para o número do lead.

⚙️ Como Rodar o Projeto Localmente
1. Pré-requisitos
Docker e Docker Desktop instalados.

Python 3.10 ou superior.

2. Configurando os Containers
Na raiz do projeto, suba os serviços de automação:

Bash
docker-compose up -d
3. Configurando o Backend Python
Entre na pasta da API e ative seu ambiente virtual:

Bash
cd api
..\venv\Scripts\activate
Instale as dependências:

Bash
pip install -r requirements.txt
Inicie o servidor:

Bash
uvicorn index:app --reload
4. Configurando o n8n
Acesse http://localhost:5678.

Importe o arquivo JSON do workflow (localizado na pasta /automation).

Certifique-se de que o nó de Webhook está configurado para a URL: http://localhost:5678/webhook/registro-cliente.

Ative o fluxo (Active).

5. Testando
Abra o arquivo frontend/cadastro.html no seu navegador, preencha os dados e clique em Cadastrar. O log do terminal mostrará a gravação no banco e o n8n processará o envio da mensagem.

🛡️ Boas Práticas Implementadas
Segurança: Uso de .gitignore para não expor bancos de dados (.db) ou ambientes virtuais no GitHub.

CORS: Configuração de middlewares no FastAPI para permitir requisições seguras do frontend.

Documentação: README detalhado focado em Developer Experience (DX).

Desenvolvido por Marco Antonio - Focado em soluções Web3 e Automação de Processos.
