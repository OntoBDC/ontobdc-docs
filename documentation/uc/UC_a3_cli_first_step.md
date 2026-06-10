# Debug do fluxo `ontobdc a3 --etl --source <local-path>`

## Pergunta

Quando o usuario digita `ontobdc a3 --etl --source <local-path>`, qual e a primeira coisa que acontece na arquitetura/codigo?

## Resposta curta

A primeira coisa que acontece e a entrada no CLI principal, em `ontobdc.cli:main`.

No fluxo atual, esse `main()` resolve o comando via `CliCommandRunAdapter.make(incoming_args)`. Como o primeiro token e `a3`, o adaptador trata `a3` como `logical_component`, carrega os comandos do plugin `a3` e tenta casar `--etl`.

Entao, antes de qualquer ETL de fato, o primeiro evento especifico do modulo `a3` e:

1. reconhecer `a3` como componente logico;
2. carregar os comandos do plugin `a3`;
3. instanciar `A3EtlCommand` para os argumentos `--etl --source <valor>`.

## Ordem real do fluxo

1. O executavel `ontobdc` chama `ontobdc.cli:main`.
2. `main()` normaliza os argumentos e chama `CliCommandRunAdapter.make(incoming_args)`.
3. `CliCommandRunAdapter.make(...)` separa o primeiro argumento como componente logico: `a3`.
4. O adaptador cria `CommandLoader("a3")` e percorre os comandos do plugin.
5. Ao encontrar correspondencia com `--etl`, ele instancia `A3EtlCommand`.
6. `main()` chama `cli_command_run.check()`.
7. Se `check()` passar, `main()` chama `A3EtlCommand.run()`.
8. Dentro de `run()`, o primeiro passo de dominio do ETL e `A3EtlStarterAdapter.start(source_value, root_path)`.
9. Dentro de `start(...)`, a primeira acao concreta do ETL e `_IncomingResourceFactory(root_path).create(source)`, que resolve o `source` para um recurso local e verifica se ele existe.
10. Em seguida, `start(...)` chama `_load_raw_text(resource)` para transformar o recurso de entrada em texto bruto.
11. `_load_raw_text(...)` valida se o recurso e textual com `resource.is_text()` e le o conteudo com `read_text(encoding="utf-8", errors="ignore")`.
12. Depois, `start(...)` chama `_get_target_dataset(resource)` para descobrir em qual dataset registrado o recurso deve ser processado.
13. `_get_target_dataset(...)` tenta usar `resource.dataset`; no caso de `LocalFileResource`, essa property resolve o dataset de forma lazy, consultando o storage graph e subindo pelos diretorios pai ate encontrar um dataset compativel.
14. De volta em `start(...)`, o codigo valida `dataset.container`; se nao houver container associado, levanta `ValueError`.
15. Com tudo valido, o fluxo instancia `RawTextResourceAdapter(raw_text)`, grava o `raw.txt` no dataset com `raw_resource.write(dataset)`, calcula `package_path` e dispara `_start_worker(package_path)`.
16. Dentro de `_start_worker(...)`, o codigo instancia `A3LogLocalDirectoryRepository()` para registrar a execucao do worker.
17. Em seguida, cria `StateWorkerAdapter(log_repository, package_path)`, ligando o worker ao pacote que acabou de ser gerado.
18. O worker e executado em um `ThreadPoolExecutor(max_workers=1)` com `executor.submit(worker.work)`, e o fluxo bloqueia em `future.result()` ate obter `worker_result`.
19. Quando o worker termina sem erro, `start(...)` monta um `A3EtlStartResult` com `status`, `source`, `resource_location`, `package_path`, `dataset_id`, `container_id` e `worker_result`.
20. De volta em `A3EtlCommand.run()`, o comando grava parte desses valores no contexto, monta o `CommandResponse` final e devolve a resposta de sucesso para o CLI.

## O que isso significa para o refactor

Se a pergunta for "qual e a primeira coisa que acontece no sistema inteiro?", a resposta e:

- entrar em `ontobdc.cli:main`.

Se a pergunta for "qual e a primeira coisa que acontece ja dentro do modulo A3 refatorado?", a resposta e:

- o `CliCommandRunAdapter` carregar o plugin `a3` e selecionar `A3EtlCommand`.

Se a pergunta for "qual e a primeira coisa que acontece no ETL de dominio?", a resposta e:

- `_IncomingResourceFactory.create(source)`.

## Conclusao

A resposta mais precisa para o estado atual do codigo e:

- a primeira coisa que acontece e `ontobdc.cli:main` resolver o comando pelo adaptador de comandos;
- a primeira coisa especifica do `a3` nesse caminho e o carregamento do plugin `a3` e a selecao de `A3EtlCommand`;
- a primeira coisa do ETL em si e transformar o `source` em um recurso com `_IncomingResourceFactory.create(...)`.
