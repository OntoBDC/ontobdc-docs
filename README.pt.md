# 🚀 OntoBDC (Ontology-Based Data Capabilities)

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/OntoBDC/ontobdc-core/blob/main/LICENSE) [![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/) [![RO-Crate](https://img.shields.io/badge/RO--Crate-1.1-green)](https://www.researchobject.org/ro-crate/) [![Status](https://img.shields.io/badge/status-active-success)](https://github.com/OntoBDC)

**OntoBDC** (Ontology-Based Data Capabilities) é uma arquitetura orientada a domínio e um runtime de capacidades para executar operações de dados com consciência ontológica sobre conjuntos de dados portáteis.

Quando os dados são descritos por **RO-Crate**, eles se tornam auto-descritivos. O OntoBDC aproveita essa metadata para descobrir e executar automaticamente operações relevantes ao contexto.

Use o OntoBDC para gerenciar o ciclo de vida de projetos de dados de engenharia. O runtime orquestra **L1 Queries** (Descoberta), **L2 Actions** (Transformação) e **L3 Use Cases** (Transições de estado) para prover fluxos reprodutíveis e auditáveis.

**Sumário**

- [Foco do projeto](#foco-do-projeto)
- [Princípios](#princípios)
- [Arquitetura](#arquitetura)
- [Capacidades](#capacidades)
- [Como começar](#como-começar)
- [Entity Framework](#entity-framework)
- [Links úteis](#links-úteis)
- [Código aberto](#código-aberto)
- [Contribuindo](#contribuindo)
- [Quem usa OntoBDC?](#quem-usa-ontobdc)

## Foco do projeto

OntoBDC funciona melhor com **projetos de dados portáteis e descentralizados**. Em vez de prender os dados em bancos monolíticos, o OntoBDC assume que os dados vivem em pacotes portáteis (Zip/Pasta/Armazenamento local) que podem circular entre ambientes sem perder significado semântico nem capacidade operacional.

## Princípios

- **Semântico**: Dados não são apenas bytes; têm significado definido por ontologias e metadata (RO-Crate).
- **Modular**: Queries/Actions são plugins isolados. Você pode adicionar novas operações sem mudar o core.
- **Portátil**: Rode em laptop, servidor ou container.

## Arquitetura

OntoBDC é construído sobre uma camada semântica central:

1. **Context Layer**: [RO-Crate](https://www.researchobject.org/ro-crate/) para metadata e relacionamentos.

O **Capability Runtime** conecta essas camadas e resolve dinamicamente quais estratégias de CLI se aplicam ao estado atual.

## Capacidades

| Nível | Nome | Escopo e Poder | Efeitos colaterais? | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| **L1** | **Query** | **Somente leitura / Descoberta.** Interface pura para consultar o ambiente. | **NÃO.** Deve ser idempotente e segura para retry infinito. | `list_documents`, `get_file_content`, `check_syntax`. |
| **L2** | **Action** | **Transformação / Criação.** Produz novos dados/arquivos sem mudar lógica de estado. | **Somente local.** Pode criar/escrever arquivos sem avançar estado. | `unzip_file`, `convert_pdf_to_png`, `generate_ro_crate_json`. |
| **L3** | **Use Case** | **Transição de estado.** Orquestra L1 e L2 para avançar processo. | **SIM.** Altera a “verdade” do sistema. | `process_chat_folder`, `publish_dataset`. |

## Como começar

Requer Python 3.11+ e pip:

```bash
pip install ontobdc
```

Inicialize o contexto do projeto:

```bash
ontobdc init
```

Execute queries/capacidades interativamente:

```bash
ontobdc run
```

Valide dados e aplique correções automatizadas quando possível:

```bash
ontobdc check --repair
```

## Entity Framework

O Entity Framework é uma estrutura local para gerenciar **Entities** (ELOFs) e seus arquivos de fachada ontológica em `.__ontobdc__/ontology/entity/`, indexados por `.__ontobdc__/entity.rdf`.

Habilitar:

```bash
ontobdc entity --enable true
```

Criar e listar:

```bash
ontobdc entity --create org.example.my_entity
ontobdc entity --list
```

Desabilitar e limpar tudo:

```bash
ontobdc entity --enable false
ontobdc entity --purge
```

## Links úteis

| Recurso | Link |
|----------|------|
| 📘 Documentação | <a href="https://docs.ontobdc.org" target="_blank">docs.ontobdc.org</a> |
| 🐙 GitHub | <a href="https://github.com/OntoBDC" target="_blank">github.com/OntoBDC</a> |
| 📦 PyPI | <a href="https://pypi.org/project/ontobdc" target="_blank">pypi.org/project/ontobdc</a> |

## Código aberto

OntoBDC é open-source sob a licença **Apache 2.0**.

## Contribuindo

Contribuições são bem-vindas via PRs e issues no GitHub.

## Quem usa OntoBDC?

OntoBDC é o core do **InfoBIM**, suportando interoperabilidade semântica para projetos complexos de engenharia.

---
<p align="center">Proudly developed in Brazil 🇧🇷</p>
