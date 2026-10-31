# eli

A small command-line coding agent. Give it a task in plain English and it explores, edits, and runs code in a sandboxed project directory until the task is done.

## How it works

eli sends your request to an LLM (via [OpenRouter](https://openrouter.ai)) along with four tools:

| Tool | What it does |
|---|---|
| `get_files_info` | List files in a directory |
| `get_file_content` | Read a file (long files are truncated) |
| `run_python_file` | Run a Python file with optional arguments |
| `write_file` | Create or overwrite a file |

The agent loops by calling the model, running whatever tools it asks for, and feeding the results back, until the model gives a final answer (capped at 20 iterations). Every tool is confined to the directory set by `WORKING_DIR` in `config.py`, and paths that escape it, including through symlinks, are rejected.

## Setup

```sh
uv sync
echo 'OPENROUTER_API_KEY=sk-or-...' > .env
```

## Usage

```sh
uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20."
uv run main.py "How does the calculator print its results?" --verbose
```

`--verbose` shows the arguments and result of each tool call, plus token usage.

The bundled `calculator/` project is the default sandbox for trying it out.

## Tests

```sh
for t in test_*.py; do python3 "$t"; done
```
