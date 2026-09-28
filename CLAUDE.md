# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A minimal Spanish-language CLI chat agent built on Groq's OpenAI-compatible chat completions API. It is packaged as `agent1` (src layout) with tools that call free public APIs (Open-Meteo for weather, open.er-api.com for exchange rates) and an in-memory rolling conversation buffer.

## Running

```
source venv/bin/activate
pip install -e .   # once; makes `agent1` importable and installs the console script
agent1             # or: python -m agent1
```

Requires a `.env` file (gitignored) in the repo root with `GROQ_API_KEY=...`; `config.py` calls `load_dotenv()`, which walks up from its own file, so the command works from any directory. Type `exit`/`salir` (or Ctrl+C / Ctrl+D) to quit.

There is no test suite or linter config. `pyproject.toml` holds project metadata (setuptools backend, deps, `agent1 = "agent1.cli:main"` script) and `basedpyright` config (Python 3.14, standard mode, `include = ["src"]`, imports resolved from `./venv`) — run `basedpyright` for type diagnostics; it is currently clean. `requirements.txt` pins exact tested versions; `pyproject.toml` lists unpinned deps.

## Architecture (`src/agent1/`)

- **`cli.py`** `main()` wires everything (`Groq` client, `MODEL`, `ALL_TOOLS`, `SimpleMemory`) into an `Agent` and runs the `Tú:`/`Asistente:` input loop. `__main__.py` just calls it.
- **`config.py`**: `MODEL` (`openai/gpt-oss-120b`), `MEMORY_MAX_MESSAGES` (10), and `groq_api_key()` which exits with a Spanish message if the key is missing.
- **`agent.py`** `Agent.chat(user_text)` runs the tool-calling loop: builds system + memory + user messages, calls the model with `tool.schema()` for every registered tool, dispatches each `tool_call` by name through a `{name: Tool}` dict (`_run_tool` → `tool.func(**json_args)`; unknown tool or bad args → `{"error": ...}` returned to the model), appends results as `role: tool` messages (strings verbatim, else JSON with `ensure_ascii=False`), and loops until plain content. Only the final user/assistant text is added to memory, not tool-call messages. `SYSTEM_PROMPT` is generic — tool guidance lives in each tool's description.
- **`tools/base.py`** `Tool` frozen dataclass: `name`, `description`, `parameters` (JSON Schema dict), `func`; `schema()` returns the Groq `ChatCompletionToolParam`.
- **`tools/__init__.py`** `ALL_TOOLS` concatenates each tool module's `TOOLS` list. **Adding a tool = new module with a function + `TOOLS` list, then add it to `ALL_TOOLS`.** No changes to `agent.py` needed.
- **`tools/clima.py`**: `obtener_lat_long(ciudad)` (Open-Meteo geocoding, returns first result or an error string if not found) and `obtener_clima_api(lat, long)` (current weather). The model chains them.
- **`tools/tipo_cambio.py`**: `obtener_tipo_cambio(moneda)` (ISO 4217 code, uppercased) → open.er-api.com latest rates.
- Tool functions return a dict on success or a Spanish `"ERROR: ..."` string on bad input / `requests.RequestException`, and print a `Herramienta ... llamada con ...` trace line.
- **`memory.py`** `SimpleMemory`: fixed-size `deque` of typed user/assistant messages — naive sliding window, no summarization or token-aware trimming.

## History

- Commit `1ab8662` and before: Google Calendar tools (`check_availability`, `create_event`, OAuth installed-app flow).
- Then a mocked `obtener_clima` weather tool, replaced by the Open-Meteo tools in `998aa2c`.
- Originally flat top-level scripts (`agent.py`, `tools.py`, `simple_memory.py`, plus a copy-pasted `src/agent2.py` for exchange rates); reorganized into the `src/agent1` package with a tool registry and a single `Agent` class.
