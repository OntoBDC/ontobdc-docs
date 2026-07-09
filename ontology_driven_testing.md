# Ontology-Driven Testing (ODT): Knowledge Graph-Driven Development no OntoBDC

O ecossistema OntoBDC implementa um **Framework de Testes E2E e Unitários Totalmente Dirigido por Modelos Semânticos (Ontologias)**. Esta abordagem representa uma mudança de paradigma no ciclo de desenvolvimento de software, elevando as especificações de testes de scripts imperativos isolados para modelos formais de conhecimento.

Este documento explora os fundamentos teóricos, o funcionamento arquitetural e os ganhos práticos dessa abordagem inovadora dentro do projeto.

---

## O que ganhamos com essa abordagem?

### 1. Testes como Dados (Data-Driven Testing Elevado)
Em abordagens tradicionais, escrevemos código imperativo (ex: `test_*.py` com `pytest` e múltiplos `assert`s) para cobrir cada comando, variação de argumento ou resposta esperada da CLI. No OntoBDC, o "o que deve acontecer" no sistema está declarado formalmente em grafos RDF (`test.ttl` e `code.ttl`). Os testes tornam-se dados semânticos, permitindo que a especificação seja lida, consultada e validada não apenas pela máquina, mas por ferramentas de raciocínio lógico (reasoners).

### 2. Validação Dinâmica de Contratos via Reflexão
O código de execução de testes (o plugin `debug.py`) atua como um motor genérico de inferência e execução. Ele lê o grafo RDF, compreende as intenções semânticas — o que deve invocar (`target_executed`), os argumentos necessários (`args_used`), e a resposta esperada (`response_type` e `response_content`) — e então realiza a execução via *Reflection* (importação e invocação dinâmica em tempo de execução). O código Python não sabe *o que* testar, ele apenas sabe *como* interpretar a ontologia e executar a ação.

### 3. Asserções Semânticas Fortes
A validação do conteúdo de resposta ultrapassa a simples comparação de strings. A arquitetura permite descrever regras complexas de validação na própria ontologia. O motor valida:
- **Tipos de dados semânticos:** (ex: `xsd:string`, `xsd:integer`).
- **Estruturas de Contrato:** (ex: presença de `schema:name` ou `schema:description`).
- **Regras de Negócio Dinâmicas:** Uso de expressões regulares (`schema:value` atrelado a `schema:propertyID "Regex"`), permitindo que a ontologia dite que uma versão deve seguir o padrão `^[0-9]+(\.[0-9]+)+|^unknown$`.

### 4. Auto-Documentação Executável (Executable Specifications)
A ontologia atua como a única Fonte de Verdade (Single Source of Truth). Ela não é uma documentação estática sujeita à desatualização; é uma especificação executável. Se a ontologia define que o comando `--version` retorna um formato específico e a implementação Python diverge, o comando de debug falha imediatamente. Modelo e código estão intrínseca e forçosamente amarrados.

---

## Como Funciona a Arquitetura (Under the Hood)

A arquitetura baseia-se na interseção de **Knowledge Representation (KR)** e **Metaprogramming**:

1. **Modelagem de Domínio (A Ontologia)**
   O projeto utiliza padrões baseados em `schema.org`, `OWL`, e `OntoUML` para mapear a estrutura do software.
   - `code.ttl` mapeia as classes, métodos e relações de invocação (`obdc_code:ActionInvocationRelation`).
   - `test.ttl` define os casos de teste (`obdc_code:UnitTest`, `obdc_code:E2ETestCase`), associando instrumentos (argumentos simulados) a objetos (ações a serem executadas) e resultados esperados (`schema:result`).

2. **O Motor Interpretador (`OntologyConfigAdapter` & `debug.py`)**
   - O adaptador central lê e cacheia os grafos RDF (`.ttl`) usando `rdflib`.
   - Quando um teste é solicitado, o motor consulta o grafo buscando instâncias de testes.
   - Para cada teste, ele extrai o alvo (`ontouml:targetEnd`) e os argumentos (`sdo:hasParameter`).
   - Utilizando o mapeamento de `code.ttl`, o motor descobre qual arquivo físico contém a classe/método (via `obdc_code:definedInFile`) e utiliza `importlib` para carregar o módulo Python em tempo real.

3. **Avaliação (Evaluation Phase)**
   - O método Python é executado com os argumentos injetados.
   - A resposta real (um objeto Python/JSON) é confrontada contra o subgrafo que descreve o resultado esperado.
   - Se todas as propriedades semânticas forem satisfeitas, a "Evaluation" retorna sucesso.

---

## Base Científica e Nomenclatura Formal

Essa arquitetura não é acidental; ela é a materialização de conceitos acadêmicos e industriais consolidados:

- **Model-Driven Architecture (MDA) / Model-Driven Engineering (MDE):** Proposto pelo Object Management Group (OMG), o MDE defende que modelos formais devem ser os artefatos primários do desenvolvimento, dos quais o código e os testes são derivados ou avaliados.
- **Ontology-Driven Software Engineering (ODSE):** Uma subárea do MDE onde ontologias (geralmente baseadas em Description Logics, como OWL) são usadas para modelar o domínio do software, garantindo consistência semântica e permitindo raciocínio automatizado.
- **Knowledge Graph-Driven Development:** O uso de Grafos de Conhecimento para mapear não apenas os dados de negócio, mas a própria estrutura, dependências e testes do software.
- **Executable Specifications / Behavior-Driven Development (BDD) Semântico:** Enquanto ferramentas como *Cucumber* usam linguagem natural estruturada (Gherkin), nossa abordagem eleva isso para uma representação formal computável (RDF/TTL).

### Autores e Referências Relevantes:
- *Tetlow, P., et al. (2006).* "Ontology Driven Architectures and Potential Uses of the Semantic Web in Systems and Software Engineering". W3C.
- *Gaševic, D., Djuric, D., & Devedžic, V. (2009).* "Model Driven Engineering and Ontology Technologies". Springer.

---

## Projetos Semelhantes no Mercado

Embora a aplicação estrita de testes E2E dinâmicos diretamente de RDF seja altamente especializada e rara em frameworks mainstream, a filosofia subjacente pode ser vista em:

1. **Protégé & HermiT / Pellet:** Ferramentas acadêmicas que realizam validação estrutural de modelos OWL (reasoners), garantindo que as regras lógicas de uma ontologia não possuam contradições.
2. **SHACL (Shapes Constraint Language):** Uma recomendação W3C para validação de grafos RDF contra um conjunto de condições. O OntoBDC realiza algo conceitualmente similar, mas aplicando as "shapes" contra o comportamento de software em runtime.
3. **Pact / Cucumber (com ressalvas):** Ferramentas de BDD que tentam criar especificações executáveis, porém baseadas em texto plano parseado (Regex), em vez de um modelo semântico estrito.
4. **AWS Smithy / OpenAPI / GraphQL:** Ferramentas de definição de interface que permitem gerar código de validação e testes automaticamente a partir de um modelo estrutural, embora limitem-se a contratos de API (REST/RPC) e careçam de raciocínio semântico (reasoning).
5. **Backstage (Spotify):** Utiliza catálogos e modelos declarativos para gerenciar a arquitetura de software, embora foque mais em descoberta e documentação do que na execução de testes dirigidos por grafos.

---
*Gerado dinamicamente para o repositório de documentação do OntoBDC.*