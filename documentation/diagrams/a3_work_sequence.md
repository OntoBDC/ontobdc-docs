# A3 Work Pipeline Sequence

This diagram illustrates the sequence of operations when executing the `ontobdc a3 --work` command. It shows how the concurrent workers, the physical package state evaluator, and the Sismic state machine interact to process each ETL package.

```mermaid
sequenceDiagram
    participant CLI as CLI (ontobdc a3 --work)
    participant Core as work.main()
    participant Executor as ThreadPoolExecutor
    participant Worker as StateWorkerAdapter
    participant Handler as SismicA3TransitionHandlerAdapter
    participant Evaluator as StandardA3StateEvaluatorAdapter
    participant Sismic as Sismic Interpreter
    participant FS as File System (Package)

    CLI->>Core: Execute main()
    Core->>FS: list_package()
    FS-->>Core: List of LocalPackages
    
    loop For each Package
        Core->>Worker: Instantiate(package)
        Worker->>Handler: Instantiate(package)
        Handler->>Evaluator: Instantiate()
    end

    Core->>Executor: Submit workers (concurrently)
    
    par For each Submitted Worker
        Executor->>Worker: work()
        
        %% Determine initial state
        Worker->>Handler: get current_state
        Handler->>Evaluator: evaluate(package)
        Evaluator->>FS: Check existing files (reverse pipeline order)
        FS-->>Evaluator: Return most advanced file (e.g. raw.txt)
        Evaluator-->>Handler: Return A3EtlProcessState (e.g. RECEIVED)
        Handler-->>Worker: Return A3EtlProcessState
        
        %% Load and Initialize Machine
        Worker->>Worker: Load YAML Statechart
        Worker->>Sismic: Instantiate(statechart, context)
        Note right of Worker: Context injects handler<br/>and EtlProcessStatePort aliases
        Worker->>Sismic: Set initial state = current_state
        
        %% Execution Loop
        Worker->>Sismic: execute_once()
        loop while not Sismic.final
            Sismic->>Handler: evaluate guards (can_transit_to)
            Handler-->>Sismic: True/False
            
            opt If guard passes
                Sismic->>Handler: perform_state_transition(to_state)
                Note right of Handler: (Future) Execute Use Case
                Handler->>FS: Process & write new file (e.g. sanitized.txt)
                Sismic->>Handler: validate_state_transition()
                Handler-->>Sismic: True
            end
            
            Worker->>Sismic: execute_once()
            Worker->>Handler: get current_state
            Handler->>Evaluator: evaluate(package)
            Evaluator->>FS: Check files
            FS-->>Evaluator: Return new advanced file (e.g. sanitized.txt)
            Evaluator-->>Handler: Return new state (e.g. SANITIZED)
            Handler-->>Worker: Return new state
            
            opt If state did not change
                Worker-->>Executor: raise RuntimeError("State stuck")
            end
        end
        
        Worker-->>Executor: Return Success Result
    end
    
    Executor-->>Core: Return all results
    Core-->>CLI: message_box(Success)
```