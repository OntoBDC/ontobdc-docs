# Estados e transicoes do worker A3

## Pergunta

Quais sao os proximos passos do fluxo do A3 quando o foco sai do entrypoint do CLI e passa para os estados e transicoes do worker?

## Resposta curta

Depois que o ETL grava o pacote e chama `_start_worker(package_path)`, o controle passa para `StateWorkerAdapter.work()`.

Nesse ponto, o fluxo deixa de ser "comando CLI" e passa a ser "maquina de estados baseada em artefatos". O worker:

1. avalia o estado atual do pacote olhando os arquivos fisicos;
2. inicializa o statechart no estado detectado;
3. executa uma transicao por vez;
4. reavalia o pacote depois de cada capability;
5. termina quando alcanca o estado final `dispatched`.

## Estados observados no pacote

O estado atual nao e guardado em banco ou memoria persistente. Ele e inferido a partir dos arquivos existentes no diretorio do pacote.

Ordem de deteccao atual:

1. `event.jsonld` -> `DISPATCHED`
2. `reasoned.ttl` -> `REASONED`
3. `validated.txt` -> `VALIDATED`
4. `graph.ttl` -> `TRANSLATED`
5. `parsed.json` -> `PARSED`
6. `sanitized.txt` -> `SANITIZED`
7. `raw.txt` -> `RECEIVED`
8. nenhum artefato esperado -> `UNDEFINED`

## Fluxo do worker

1. `StateWorkerAdapter.work()` cria um contexto com `handler` e `EtlProcessStatePort`.
2. O worker consulta `handler.current_state`, que usa `StandardA3StateEvaluatorAdapter.evaluate(package)`.
3. O evaluator inspeciona o diretorio do pacote e converte os artefatos encontrados em um estado da enum `A3EtlProcessState`.
4. O worker registra o estado inicial no log.
5. `A3LocalStatechartRepository()` carrega o statechart `standard_a3_extraction.yaml`.
6. O worker sobrescreve o estado inicial da raiz do statechart com o estado fisico detectado no pacote.
7. O `Interpreter` do Sismic executa o statechart.
8. A cada iteracao, o worker executa uma transicao, reavalia o estado fisico do pacote e compara com o estado anterior.
9. Se nenhum artefato novo aparecer e o estado continuar igual, o worker interrompe com erro de estado travado.
10. O loop termina quando o interpreter entra no estado final `dispatched`.

## Statechart canonico

O statechart local define a sequencia linear abaixo:

1. `undefined` -> `received`
2. `received` -> `sanitized`
3. `sanitized` -> `parsed`
4. `parsed` -> `translated`
5. `translated` -> `validated`
6. `validated` -> `reasoned`
7. `reasoned` -> `dispatched`

Cada transicao segue o mesmo contrato:

1. `guard`: `handler.can_transit_to(...)`
2. `action`: `handler.perform_state_transition(...)`
3. `contract after`: `handler.validate_state_transition(...)`

## Mapa de estados e transicoes

### `UNDEFINED`

- Significado: o pacote ainda nao apresenta nenhum artefato reconhecido pela pipeline.
- Evidencia fisica: ausencia de `raw.txt`, `sanitized.txt`, `parsed.json`, `graph.ttl`, `validated.txt`, `reasoned.ttl` e `event.jsonld`.
- Proxima transicao: `UNDEFINED -> RECEIVED`
- Observacao: no fluxo atual de ingestao normal, esse estado tende a ser apenas teorico, porque o ETL grava `raw.txt` antes de acionar o worker.

### `RECEIVED`

- Significado: o pacote ja contem a entrada bruta.
- Evidencia fisica: `raw.txt`
- Proxima transicao: `RECEIVED -> SANITIZED`
- Capability executada: `org.ontobdc.a3.plugin.capability.transformation.target.sanitized`
- Efeito principal: le `raw.txt`, remove tags HTML com regex simples e grava `sanitized.txt`.

### `SANITIZED`

- Significado: o pacote ja passou por limpeza textual basica.
- Evidencia fisica: `sanitized.txt`
- Proxima transicao: `SANITIZED -> PARSED`
- Capability executada: `org.ontobdc.a3.plugin.capability.transformation.target.parsed`
- Efeito principal: usa `sanitized.txt`, chama o LLM, valida o JSON com guardrail e grava `parsed.json`.
- Erro relacionado: pode gravar `err.json` se o pacote estiver em estado invalido ou se a validacao do dado parseado falhar.

### `PARSED`

- Significado: o texto ja virou estrutura JSON.
- Evidencia fisica: `parsed.json`
- Proxima transicao: `PARSED -> TRANSLATED`
- Capability executada: `org.ontobdc.a3.plugin.capability.transformation.target.translated`
- Efeito principal: le `parsed.json`, traduz os dados para RDF e grava `graph.ttl`.

### `TRANSLATED`

- Significado: o pacote ja contem o grafo RDF gerado.
- Evidencia fisica: `graph.ttl`
- Proxima transicao: `TRANSLATED -> VALIDATED`
- Capability executada: `org.ontobdc.a3.plugin.capability.transformation.target.validated`
- Efeito principal: valida `graph.ttl` com SHACL e grava `validated.txt`.
- Erro relacionado: grava `err.json` se a validacao falhar.

### `VALIDATED`

- Significado: o grafo passou pela validacao SHACL.
- Evidencia fisica: `validated.txt`
- Proxima transicao: `VALIDATED -> REASONED`
- Capability executada: `org.ontobdc.a3.plugin.capability.transformation.target.reasoned`
- Efeito principal: copia `graph.ttl` para `reasoned.ttl`.

### `REASONED`

- Significado: o pacote ja tem um artefato de raciocinio.
- Evidencia fisica: `reasoned.ttl`
- Proxima transicao: `REASONED -> DISPATCHED`
- Capability executada: `org.ontobdc.a3.plugin.capability.transformation.target.dispatched`
- Efeito principal: le o grafo, monta um evento e grava `event.jsonld`.

### `DISPATCHED`

- Significado: o pacote chegou ao estado final da pipeline.
- Evidencia fisica: `event.jsonld`
- Tipo de estado: final
- Resultado operacional: o interpreter encerra e o worker retorna sucesso.

## Como a transicao e disparada

Para cada alvo `to_state`, `SismicA3TransitionHandlerAdapter.perform_state_transition(...)`:

1. cria `TransformableDataPackageRepository(package_path)`;
2. injeta esse pacote em um `CliContextAdapter` na chave `data_package`;
3. monta o id da capability com base no nome do estado alvo;
4. resolve a capability via `CapabilityLoader`;
5. executa a capability com `CapabilityExecutor.execute(...)`.

Em outras palavras, a maquina de estados nao "move" o estado diretamente. Ela executa uma capability que cria o artefato esperado; so depois o evaluator reconhece esse novo artefato e considera a transicao valida.

## Regra pratica de transicao

A transicao so e considerada bem-sucedida quando o estado fisico do pacote muda de verdade.

Isso ocorre assim:

1. o statechart manda executar a capability do estado alvo;
2. a capability grava o artefato correspondente;
3. o evaluator rele o pacote no disco;
4. `validate_state_transition(...)` confirma que o estado atual agora e o estado alvo.

Se a capability rodar e nenhum artefato novo alterar o estado observado, o worker acusa travamento:

- `State stuck at <estado>. No transition was made.`

## Resumo arquitetural

- O CLI inicia o ETL e dispara o worker.
- O worker inicializa a maquina de estados no estado fisico atual do pacote.
- O evaluator decide estado por artefatos no filesystem.
- O statechart define a ordem permitida das transicoes.
- O transition handler resolve e executa uma capability para cada estado alvo.
- O package so "anda" quando um novo artefato materializa o proximo estado.
