DAVIA CRM --- Sistema Genérico de Gestão de Vendas
O DAVIA CRM é um sistema de gerenciamento de relacionamento com
clientes (CRM), desenvolvido em Python, com o objetivo de ajudar
pequenos negócios e equipes comerciais a organizar contatos, acompanhar
oportunidades e visualizar o desempenho das vendas em um único ambiente.

A aplicação foi criada como um projeto inicial, com interface web
simples e intuitiva, utilizando Streamlit para a interface e
SQLite para armazenar os dados localmente.
✨ Funcionalidades
- Painel inicial: visão geral dos indicadores comerciais.
- Cadastro de contatos e leads: registro e atualização de clientes
  e potenciais clientes.
- Funil de vendas: acompanhamento das oportunidades por etapa.
- Etapas comerciais: Novo, Contato feito, Qualificado, Proposta
  enviada, Negociação, Ganho e Perdido.
- Tarefas e atividades: organização de acompanhamentos e próximos
  contatos.
- Filtros e pesquisa: localização de registros por critérios
  disponíveis na interface.
- Relatórios: visualização resumida dos dados comerciais.
- Exportação CSV: possibilidade de exportar dados para análise em
  planilhas.
🧰 Tecnologias utilizadas
- Python --- linguagem principal.
- Streamlit --- construção da interface web.
- SQLite --- banco de dados local.
- Pandas --- apoio à organização e exportação de dados.
📁 Estrutura do projeto
davia_crm_generico/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── crm.db   # criado automaticamente durante a execução, quando aplicável
A pasta e o arquivo do banco de dados podem ser criados
automaticamente pela aplicação. O banco local não precisa ser enviado
ao GitHub.

⚙️ Requisitos
- Python 3.10 ou superior (recomendado).
- pip instalado.
- Windows, Linux ou macOS.
🚀 Como executar
1. Baixe ou clone o repositório
git clone URL_DO_SEU_REPOSITORIO
cd davia_crm_generico
Substitua URL_DO_SEU_REPOSITORIO pelo endereço real do repositório no
GitHub.
2. Crie um ambiente virtual
No Windows:
python -m venv .venv
.venv\Scripts\activate
No Linux ou macOS:
python3 -m venv .venv
source .venv/bin/activate
3. Instale as dependências
pip install -r requirements.txt
4. Inicie o sistema
streamlit run app.py
O Streamlit exibirá um endereço local no terminal e, normalmente, abrirá
o sistema no navegador automaticamente.
💾 Armazenamento dos dados
Nesta versão, os dados são armazenados em um banco SQLite local. Isso
facilita a instalação e os testes em um computador, mas significa que os
dados não são sincronizados automaticamente entre diferentes
dispositivos.

Faça cópias de segurança do banco de dados regularmente. Antes de
substituir ou atualizar arquivos do projeto, preserve a pasta de dados
caso queira manter os registros cadastrados.
🔐 Limitações e segurança
Esta versão é um protótipo funcional para uso local e evolução do
projeto. Ela ainda não deve ser considerada uma plataforma SaaS pronta
para uso comercial em larga escala.

Antes de disponibilizar o sistema para várias empresas ou pela internet,
será necessário implementar e testar, entre outros pontos:
- autenticação segura de usuários;
- perfis e permissões de acesso;
- separação dos dados de cada empresa;
- banco de dados adequado para ambiente de produção;
- backups automatizados e recuperação de dados;
- proteção de dados pessoais e adequação à LGPD;
- validação de entradas, logs e monitoramento;
- testes automatizados e processo seguro de implantação.
Não utilize esta versão para armazenar informações pessoais ou
comerciais sensíveis sem avaliar e implementar as medidas de segurança
necessárias.
🛣️ Possíveis evoluções
O DAVIA CRM poderá evoluir com recursos como:
- login e gerenciamento de equipes;
- múltiplas empresas e usuários;
- metas, comissões e indicadores por vendedor;
- integração com WhatsApp e e-mail;
- agenda de compromissos e lembretes;
- histórico detalhado de interações;
- API para integrações externas;
- versão em nuvem e acesso por dispositivos móveis;
- recursos de inteligência artificial da família davIA.
Esses itens representam possibilidades de desenvolvimento e não
necessariamente estão disponíveis nesta versão.
🤝 Contribuições
Sugestões, relatos de problemas e melhorias são bem-vindos. Para
contribuir:
1. Faça um fork do repositório.
2. Crie uma branch para sua alteração.
3. Faça as modificações e teste localmente.
4. Envie um pull request descrevendo o que foi alterado.
📄 Licença
Defina uma licença antes de permitir reutilização, modificação ou
distribuição do projeto. Se optar por uma licença de código aberto,
adicione o arquivo LICENSE ao repositório e atualize esta seção com o
nome da licença escolhida.
DAVIA CRM --- organização e acompanhamento de vendas em um só lugar.

Projeto em desenvolvimento.
