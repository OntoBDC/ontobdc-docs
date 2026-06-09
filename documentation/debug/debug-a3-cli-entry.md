# Debug Session: a3-cli-entry

Status: OPEN

Question:
- Quando o usuario digita `ontobdc a3 --etl --source <local-path>`, qual e a primeira coisa que acontece na arquitetura/codigo?

Hypotheses:
- H1: O primeiro ponto de entrada e `ontobdc.cli:main` definido em `wip/pyproject.toml`.
- H2: O fluxo atual resolve `a3` via `CliCommandRunAdapter.make(...)` como caminho principal de execucao.
- H3: Nao ha mais fallback ativo de execucao para `a3` em `cli/__init__.py`.
- H4: A primeira acao de dominio do ETL e `_IncomingResourceFactory.create(source)` dentro de `A3EtlStarterAdapter.start(...)`.

Evidence Collected:
- `wip/pyproject.toml` expoe `ontobdc = "ontobdc.cli:main"`.
- `wip/src/ontobdc/cli/__init__.py` chama `CliCommandRunAdapter.make(incoming_args)` como primeira tentativa de resolucao do comando.
- `wip/src/ontobdc/a3/plugin/command/etl.py` reconhece `--etl --source <value>` e delega para `A3EtlStarterAdapter.start(...)`.
- `wip/src/ontobdc/a3/adapter/etl.py` inicia o dominio com `_IncomingResourceFactory(root_path).create(source)`.
- `wip/src/ontobdc/cli/__init__.py` nao possui mais ramo ativo de execucao para `cmd == "a3"`; restam apenas comentarios antigos.

Current Conclusion:
- O primeiro evento arquitetural e a entrada em `ontobdc.cli:main`.
- O primeiro evento especifico do modulo `a3` e a resolucao do comando `a3` por `CliCommandRunAdapter` com `CommandLoader('a3')`.
- A primeira acao de ETL no dominio e transformar o `source` em um recurso de arquivo com `_IncomingResourceFactory.create(...)`.
