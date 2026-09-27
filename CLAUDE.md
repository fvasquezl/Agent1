# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A minimal Spanish-language CLI chat agent (`agent.py`) built on Groq's OpenAI-compatible chat completions API, with a mocked tool layer (`tools.py`) and an in-memory rolling conversation buffer (`simple_memory.py`).

## Running

```
source env/bin/activate
python agent.py
```

Requires a `.env` file (gitignored) with `GROQ_API_KEY=...`. Type `exit` or `salir` to quit the chat loop.

There is no test suite, linter config, or build step in this repo. `pyproject.toml` only configures `basedpyright` (Python 3.14, standard type-checking mode) — run `basedpyright` if you want type diagnostics.

## Architecture

- **`agent.py`** is a single-file chat loop: it holds `SYSTEM_PROMPT` (Spanish instructions describing the weather tool) and the `TOOLS` schema (declares only `obtener_clima`, with required `ciudad` string) passed to the Groq model (`openai/gpt-oss-120b`). `process_response()` runs the standard tool-calling loop — call model, check `msg.tool_calls`, dispatch, append tool results as `role: tool` messages (JSON-encoded with `ensure_ascii=False`), loop until the model returns plain content.
- Tool dispatch inside `process_response()` is an `if/elif` on `tool_call.function.name` (currently only `obtener_clima` → `Tools().obtener_clima(ciudad=...)`); anything else falls through to the "herramienta desconocida" branch. When adding tools, the `TOOLS` schema, `SYSTEM_PROMPT`, and this dispatch block all need to be kept in sync.
- **`tools.py`**'s `Tools` class currently has a single mocked method, `obtener_clima(ciudad)`, which returns a hardcoded Spanish string (a "beautiful" message for Tijuana, case-insensitive; a "horrible" message for any other city). No external API is called.
- **`simple_memory.py`**'s `SimpleMemory` is a fixed-size `deque` (default `maxlen=10`, set via `MEMORY_MAX_MESSAGES` in `agent.py`) of `{role, content}` dicts — a naive sliding window, no summarization or token-aware trimming. Tool-call messages are not persisted into this memory; only the final user/assistant text turns are added after `process_response` returns.
- `agent.py` computes `now` in the `America/Tijuana` timezone at import time but does not currently use it anywhere.

## History

An earlier version (commit `1ab8662` and before) had Google Calendar tools in `tools.py` (`check_availability` via `freebusy.query`, `create_event` via `events.insert`, OAuth installed-app flow with `credentials.json` → `token.json`). These were removed in favor of the mocked weather tool. The Google client libraries are still pinned in `requirements.txt` but are no longer imported.
