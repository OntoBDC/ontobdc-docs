---
code: SPEC002
title: CLI Strategy Structure Specification
status: Deprecated
author: Elias M. P. Junior
date: 2026-02-26
tags: architecture, cli, adapter, strategy
---

# SPEC002: CLI Strategy Structure Specification

> **DEPRECATION NOTICE**: This specification is deprecated in favor of the new `CliContextResolver` architecture and `CliContextStrategyPort` pattern implemented in `run.py`. Argument parsing is now handled by global strategies (Chain of Responsibility), and Capabilities receive a resolved `CliContextPort` directly. The old `CliStrategy` pattern described here is being phased out, with remaining logic moved to simple Renderers/Adapters.

