---
icon: Lucide/house
---

# Painel Inicial

_Resumo do Projeto: O AFSESAB Middleware é uma aplicação robusta desenvolvida em Python que atua como um nó logístico e interface gráfica desktop para unidades de saúde. Seu objetivo é realizar a interoperabilidade segura com a API do AFSESAB, otimizando a operação de ponta._

## Estrutura do Projeto

Aqui está a estrutura de diretórios ideal (no padrão src layout) para dividirmos o código do seu projeto:

```
src
├── init.py
├── main.py        # Responsável apenas pelo Login, Menu e Roteamento
├── api_client.py  # Gerencia a comunicação HTTP e o Token JWT
├── database.py    # Configura a conexão e a sessão (Engine) do PostgreSQL
├── models.py      # Contém as tabelas do SQLAlchemy (UnidadeLocal, paciente, etc.)
└── telas/         # Módulo dedicado aos componentes visuais
  ├── init.py
  ├── tela_estoque.py
  ├── tela_pacientes.py
  └── tela_recebimento.py
```

## 🎯 Implementações/Features

Abaixo está o mapeamento do nosso roadmap de engenharia e o status de cada módulo da nossa interface e API:

- [x] Arquitetura Base e Estilização: Configuração do projeto desktop em tela cheia com sistema de roteamento de telas (sem janelas pop-up desnecessárias).

- [x] Autenticação e Segurança: Gateway de login integrado ao endpoint oficial (/logistica/login), com validação Fail-Fast e injeção automática de tokens JWT nas requisições.

- [x] Banco de Dados Local (Cache): Mapeamento ORM para persistência local de dados (Unidades, Pacientes e Atendimentos) e sincronização offline-first.
- [x] Módulo "Meu Estoque": Integração via requisição GET com o AFSESAB, processamento rápido de JSON e exibição tabular filtrada.
- [x] Módulo "Lista de Pacientes": Leitura relacional do banco de dados filtrada automaticamente pela unidade de operação ativa (CNES).
- [ ] Módulo "Recebimento de Pedidos": Implementação do interceptador de eventos de teclado para leitura de QR Code/EAN físicos e validação de pacotes.
- [ ] Módulo "Dispensação": Fluxo de atendimento ao paciente e baixa transacional de estoque.
- [ ] Módulo "Transferência de Estoque": Validação de regras de negócio para remanejamento de lotes.

## 📕 Referências e Stack Tecnológico

A arquitetura do nosso sistema foi construída se apoiando no topo de frameworks de alto desempenho que representam o estado da arte no ecossistema Python. Caso precise dar manutenção, consulte as documentações oficiais:

### Interface Gráfica e Visual (Frontend Desktop)

- Tkinter: É a interface padrão do Python para kits de ferramentas GUI Tcl/Tk. Usamos seus fundamentos de empacotadores (geometry managers como pack e grid) e o widget nativo de tabelas (Treeview).
- ttkbootstrap: Utilizado como wrapper do Tkinter para modernizar a aparência da aplicação, adicionando temas profissionais (como o tema superhero) e simplificando componentes visuais com padrões do Bootstrap.

### Persistência de Dados (ORM e Banco)

- SQLAlchemy 2.0: O kit de ferramentas de banco de dados e mapeador objeto-relacional (ORM) para Python que utilizamos. Adotamos o padrão da versão 2.0 (com strings postgresql+psycopg) e configurações avançadas de Pool de conexões (como pool_pre_ping=True e pool_recycle=300) para mitigar quedas inesperadas de conexão com serviços de nuvem como o Neon Tech.
  PostgreSQL: Sistema gerenciador de banco de dados relacional (SGBD) utilizado para nossa persistência local e validações estruturais.

### Camada de Rede (API e Performance)

- HTTPX: Biblioteca utilizada na nossa classe ClienteAFSESAB para sustentar pools de conexão HTTP altamente eficientes.
- FastAPI / Pydantic: (Opcional no nó) O FastAPI é um framework web moderno e rápido (de alta performance), compatível com NodeJS e Go. Validamos a inclusão dele caso o nosso sistema precise atuar ativamente abrindo portas web locais (via servidor Uvicorn) para escutar outras integrações logísticas.
- UV: Um gerenciador de projetos e pacotes Python extremamente rápido escrito em Rust, que substitui o pip e o virtualenv tradicional, sendo de 10 a 100 vezes mais rápido na instalação das dependências do nosso projeto.
