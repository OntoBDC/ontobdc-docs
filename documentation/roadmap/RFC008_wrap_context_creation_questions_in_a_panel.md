# RFC 008 - Wrap Context Creation Questions In A Panel

## Status

- **Status**: requested
- **Scope**: interactive `ontobdc run` bootstrap and context-creation prompt
- **Primary surface**: `wip/src/ontobdc/run/run.py`

## Purpose

This RFC proposes that the interactive questions shown during context creation should be rendered inside a visual panel instead of being printed as loose terminal lines.

The goal is to make the creation flow easier to recognize as a single guided interaction block.

## Context

The current `ontobdc run` experience already uses a panel for the initial prompt that asks whether the user wants to start a new context.

However, the subsequent creation questions, such as:

```text
Please select your preferred language: [en/pt_BR] (en): pt_BR
Em que posso ajudar?: Minha agenda de hoje
```

may still appear as plain terminal prompts outside that same visual frame.

That creates a small but noticeable UX break:

- the first step looks like a structured guided panel
- the next step looks like unrelated raw terminal input

## Motivation

The context bootstrap flow is effectively a short interview with the user.

When some questions are presented inside a panel and others are printed outside it, the interaction looks fragmented.

This can weaken:

- continuity of the onboarding flow
- clarity that the questions belong to the same guided context-creation process
- perceived polish of the CLI interaction

## Proposal

Render the context-creation questions inside a dedicated panel or panel-like block, instead of presenting them as loose prompts.

At minimum, the flow should visually group questions such as:

- preferred language selection
- initial user request or intent prompt

Example target interaction:

```text
>_ OntoBDC Context Creation

Please select your preferred language: [en/pt_BR] (en): pt_BR
Em que posso ajudar?: Minha agenda de hoje
```

The exact layout may vary, but the questions should remain visually framed as one guided interaction surface.

## Constraints

The resulting behavior should:

- preserve the current interactive behavior
- keep the questions readable in TTY mode
- avoid mixing unrelated logs into the middle of the panel
- remain compatible with both English and Portuguese prompts
- degrade gracefully when interactive terminal features are unavailable

It should not:

- turn the creation flow into disconnected plain prompts after the user has already entered a guided panel flow
- introduce a visual wrapper that breaks input handling or terminal navigation

## Expected Impact

If implemented, this RFC would likely affect:

- `wip/src/ontobdc/run/run.py`
- any helper responsible for context bootstrap prompting
- CLI interaction screenshots or use-case documentation that capture the bootstrap flow

Likely validation or tests:

- interactive prompt rendering checks
- confirmation that language and intent questions are grouped in the same panel flow
- regression checks to ensure `Exit` and other prompt paths still behave correctly

## Correlation With Current CLI UX

This RFC does not change the logical behavior of context creation.

It only refines how the interaction is presented to the user.

In other words:

- the current flow already asks the necessary questions
- `RFC008` proposes a more coherent presentation layer for those same questions

## Open Questions

- Should the language and intent questions be shown in one persistent panel or in successive panels?
- Should the panel include a title such as `OntoBDC Context Creation`?
- Should the same pattern be extended to later guided prompts in other CLI flows?
- How should non-interactive mode render the same sequence?

## Follow-Up

If accepted, the next step should be to define:

- the panel layout for creation questions
- the rendering boundary between prompts and log messages
- the fallback behavior for non-interactive terminals
- the regression checks for the updated prompt flow
