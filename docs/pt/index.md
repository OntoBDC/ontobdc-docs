# 🚀 OntoBDC (Ontology-Based Data Capabilities)

| Categoria  | Badges |
|------------|--------|
| Licença    | [![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE) |
| Python     | [![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/) |
| Padrões    | [![Frictionless](https://img.shields.io/badge/frictionless-data-black)](https://frictionlessdata.io/) [![RO-Crate](https://img.shields.io/badge/RO--Crate-1.1-green)](https://www.researchobject.org/ro-crate/) |
| Estado     | [![Sismic](https://img.shields.io/badge/statecharts-sismic-blue)](https://sismic.readthedocs.io/) |
| Status     | [![Status](https://img.shields.io/badge/status-active-success)]() |

**OntoBDC** (Ontology-Based Data Capabilities) é um runtime orientado a capabilities para a execução de operações de dados conscientes de ontologia em datasets portáteis. Ele preenche a lacuna entre o armazenamento de dados estático e a execução semântica dinâmica.

Quando os dados são descritos por **RO-Crate** e **Frictionless Data Packages**, eles se tornam autodescritivos. O OntoBDC aproveita esses metadados para descobrir e executar automaticamente **Capabilities** (operações) disponíveis e relevantes para o contexto dos dados.

Use o OntoBDC para gerenciar o ciclo de vida de seus projetos de dados. O runtime orquestra **L1 Capabilities** (Descoberta), **L2 Actions** (Transformação) e **L3 Use Cases** (Transições de Estado), mantendo uma espinha dorsal rigorosa de **Event Sourcing** (System Crate).

**Índice**

- [Foco do Projeto](#foco-do-projeto)
- [Princípios](#principios)
- [Arquitetura](#arquitetura)
- [Começando](#comecando)
- [Instalação](#instalacao)
- [Links Úteis](#links-uteis)
- [Open Source](#open-source)
- [Contribuindo](#contribuindo)
- [Quem usa o OntoBDC?](#quem-usa-o-ontobdc)

## 🎯 Foco do Projeto

O OntoBDC funciona melhor com **projetos de dados descentralizados e portáteis**. Diferente de sistemas monolíticos que bloqueiam dados em bancos de dados específicos, o OntoBDC assume que os dados vivem em pacotes portáteis (Zip/Pasta/WEB/API/FTP) que podem ser movidos entre armazenamento local, nuvem e dispositivos de borda sem perder significado semântico ou capacidade operacional.

O OntoBDC é comumente usado para:

- **Padronizar** a troca de dados entre diversas disciplinas de engenharia (BIM, GIS, Documentos).
- **Executar** operações conscientes do contexto (ex: "Extrair Entidades de PDF", "Validar Modelo IFC") sem pipelines hardcoded.
- **Rastrear** cada modificação no histórico de um projeto via um log de eventos imutável (System Crate).

## 💡 Princípios

- **Semântico**: Dados não são apenas bytes; eles têm significado definido por ontologias e metadados (RO-Crate).
- **Modular**: Capabilities são plugins isolados. Você pode adicionar novas operações sem alterar o runtime principal.
- **Portátil**: Todo o runtime e o pacote de dados são independentes. Execute em um laptop, servidor ou dentro de um contêiner.
- **Event-Sourced**: O estado é derivado de uma sequência de eventos, garantindo auditabilidade e depuração "time-travel".

## 🏗️ Arquitetura

O OntoBDC é construído sobre três pilares:

1.  **Camada Física**: [Frictionless Data Package](https://frictionlessdata.io/) para organização de arquivos.
2.  **Camada de Contexto**: [RO-Crate](https://www.researchobject.org/ro-crate/) para metadados semânticos e relacionamentos.
3.  **Camada de Sistema**: **System Crate** para event sourcing e memória operacional, implementando uma **Máquina de Estados Finitos (FSM)** robusta.

O **Capability Runtime** une essas camadas, resolvendo dinamicamente quais ferramentas (estratégias CLI) se aplicam ao estado atual dos dados.

## ⚡ Capabilities

Capabilities são as unidades centrais de execução no OntoBDC. Elas são categorizadas em três níveis de poder e responsabilidade, garantindo segurança e clareza para agentes autônomos:

| Nível | Nome | Escopo & Poder | Efeitos Colaterais? | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| **L1** | **Capability** | **Somente Leitura / Descoberta.** Interface pura para consultar o ambiente. | **NÃO.** Deve ser idempotente e segura para tentar infinitas vezes. | `list_documents`, `get_file_content`, `check_syntax`. |
| **L2** | **Action** | **Transformação / Criação.** Recebe dados de entrada e produz novos dados/arquivos sem alterar a lógica de estado do negócio. | **Apenas Local.** Pode criar/escrever arquivos, mas não avança o estado do fluxo de trabalho. | `unzip_file`, `convert_pdf_to_png`, `generate_ro_crate_json`. |
| **L3** | **Use Case** | **Transição de Estado.** Orquestra L1 e L2 para mover o processo de negócios adiante. | **SIM.** Altera a "verdade" do sistema. | `process_chat_folder` (Bruto -> Processado), `publish_dataset`. |

Essa estrutura permite controle granular sobre o que um agente pode fazer, separando "sentir" (L1) de "fazer" (L2) e "decidir" (L3).

## 📦 Instalação

O OntoBDC é tipicamente implantado via pip. Instale-o para começar a usar a CLI:

```bash
pip install ontobdc

# Após a instalação, você pode executar a CLI assim:
ontobdc --help
```

## 🔗 Links Úteis

| Recurso | Link |
|----------|------|
| 📘 Documentação | <a href="https://docs.ontobdc.org" target="_blank">docs.ontobdc.org</a> |
| 🐙 GitHub | <a href="https://github.com/OntoBDC" target="_blank">github.com/OntoBDC</a> |
| 📦 PyPI | <a href="https://pypi.org/project/ontobdc" target="_blank">pypi.org/project/ontobdc</a> |

## ❤️ Open Source

O OntoBDC é uma iniciativa livre e de código aberto, licenciada sob a **Licença Apache 2.0**.
Acreditamos no poder do desenvolvimento impulsionado pela comunidade para resolver desafios complexos de interoperabilidade de dados.

## 🤝 Contribuindo

O OntoBDC é uma iniciativa aberta. Contribuições são bem-vindas!

## 🏢 Quem usa o OntoBDC?

O OntoBDC é o motor central por trás do **InfoBIM**, impulsionando a interoperabilidade de dados semânticos para projetos de engenharia complexos.

---
<p align="center">Orgulhosamente desenvolvido no Brasil 🇧🇷</p>
