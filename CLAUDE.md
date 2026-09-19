# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A minimal Spanish-language CLI chat agent (`agent.py`) built on Groq's OpenAI-compatible chat completions API, with a Google Calendar tool layer (`tools.py`) and an in-memory rolling conversation buffer (`simple_memory.py`).

## Running

```
source env/bin/activate
python agent.py
```

Requires a `.env` file (gitignored) with `GROQ_API_KEY=...`. Type `exit` or `salir` to quit the chat loop.

`tools.py` when run directly (`python tools.py`) exercises `check_availability` standalone; it needs a Google OAuth `credentials.json` in the working directory and will open a local server flow to mint `token.json` on first use.

There is no test suite, linter config, or build step in this repo. `pyproject.toml` only configures `basedpyright` (Python 3.14, standard type-checking mode) — run `basedpyright` if you want type diagnostics.

## Architecture

- **`agent.py`** is a single-file chat loop: it holds `SYSTEM_PROMPT` (Spanish instructions) and the `TOOLS` schema (currently declares only `obtener_clima`) passed to the Groq model (`qwen/qwen3-32b`). `process_response()` runs the standard tool-calling loop — call model, check `msg.tool_calls`, dispatch, append tool results as `role: tool` messages, loop until the model returns plain content.
- Tool dispatch inside `process_response()` is an `if/elif` on `tool_call.function.name` that currently only handles `check_availability` and `create_event` (both from `tools.py`) — it does **not** implement `obtener_clima`, the only tool actually declared in `TOOLS`. Any real call to `obtener_clima` falls through to the "herramienta desconocida" branch. When adding tools, both the `TOOLS` schema and this dispatch block need to be kept in sync.
- **`tools.py`**'s `Tools` class wraps the Google Calendar API (`freebusy.query` for `check_availability`, `events.insert` for `create_event`), using OAuth installed-app flow (`credentials.json` → `token.json`, both expected in the working directory, both gitignored-adjacent but not currently in `.gitignore`).
- **`simple_memory.py`**'s `SimpleMemory` is a fixed-size `deque` (default `maxlen=10`, set via `MEMORY_MAX_MESSAGES` in `agent.py`) of `{role, content}` dicts — a naive sliding window, no summarization or token-aware trimming. Tool-call messages are not persisted into this memory; only the final user/assistant text turns are added after `process_response` returns.
- Dates/times passed to the calendar tools are ISO 8601 strings with explicit offsets (e.g. `2025-12-30T10:00:00-06:00`); `agent.py` computes `now` in the `America/Tijuana` timezone at import time but does not currently inject it into the system prompt or tool calls.
