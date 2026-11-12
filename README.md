# eli

**eli is an AI assistant that works on code for you.** You describe a task in everyday language, such as *"fix the bug in the calculator"*, and eli reads the code, makes changes, runs the program to check its work, and then tells you what it did.

You don't have to tell it which file to open or which line to change. It works that out on its own.

---

## What does it actually do?

Think of eli as a new team member who can only use four basic skills:

| Skill | In plain terms |
|---|---|
| **Look around** | See which files and folders exist |
| **Read** | Open a file and read what's inside |
| **Run** | Start a Python program and see what it prints |
| **Write** | Create a new file or change an existing one |

When you give eli a task, it works in a loop:

1. **Think.** An AI model (the "brain") decides what to do next.
2. **Act.** eli uses one of its four skills, for example reading a file.
3. **Learn.** The result goes back to the AI model.
4. **Repeat** until the task is done. eli then gives you a short summary.

To keep it from running forever, eli stops after **20 rounds** if it hasn't finished.

### Is it safe?

eli can only touch files inside **one folder** that you choose. If it tries to reach anything outside that folder, including through shortcuts (symlinks), the request is blocked. By default, that folder is `calculator/`, a small practice project that ships with eli.

> ⚠️ Inside its folder, eli **can change and overwrite files**. Point it only at a folder you're happy for it to edit, ideally one tracked by Git so you can undo changes.

---

## Try it yourself

You'll type a few commands into a **terminal**, the text window where you give your computer commands:

- **Mac:** open the **Terminal** app (press `Cmd + Space` and type "Terminal").
- **Windows:** open **PowerShell** from the Start menu.

### Step 1: Install `uv`

`uv` is a free tool that installs everything eli needs, including the right version of Python. You only do this once.

**Mac / Linux:**
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen your terminal afterwards.

### Step 2: Download eli

```sh
git clone https://github.com/Taniyakaur/eli.git
cd eli/eli
```

(No Git? On the GitHub page, click **Code → Download ZIP**, unzip it, and `cd` into the inner `eli` folder.)

### Step 3: Install eli's dependencies

```sh
uv sync
```

### Step 4: Get an OpenRouter key

eli talks to AI models through [OpenRouter](https://openrouter.ai). The key is like a password that lets eli use that service.

1. Create a free account at [openrouter.ai](https://openrouter.ai).
2. Go to **Keys** and create a new key. It starts with `sk-or-`.
3. Save it in a file called `.env` in the same folder (replace the example with your real key):

```sh
echo 'OPENROUTER_API_KEY=sk-or-your-key-here' > .env
```

eli uses a **free** model by default, so you shouldn't be charged. Keep your key private and never share or upload the `.env` file. It is already set to be ignored by Git.

### Step 5: Give eli a task

```sh
uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20."
```

eli will look through the calculator, find the problem, fix it, check the fix, and print a summary.

You can also ask it questions without changing anything:

```sh
uv run main.py "How does the calculator print its results?"
```

To watch each step eli takes, add `--verbose` at the end:

```sh
uv run main.py "How does the calculator print its results?" --verbose
```

---

## Common problems

| Message | What it means | Fix |
|---|---|---|
| `OPENROUTER_API_KEY not found` | eli can't find your key | Make sure `.env` exists in the same folder as `main.py` (Step 4) |
| `has extra spaces or quote marks` | The key was copied with extra characters | Open `.env` and make sure it reads `OPENROUTER_API_KEY=sk-or-...` with no spaces or quotes |
| `doesn't look like an OpenRouter key` | The key isn't from OpenRouter | Copy the key again from openrouter.ai. It must start with `sk-or-` |
| `Provider error on attempt…` | The free AI model is busy | eli retries on its own. If it keeps failing, wait a minute and try again |
| `Agent did not finish within 20 iterations` | The task took too many steps | Try a smaller or more specific request |

---

## For developers

### Project layout

```
eli/
├── main.py            # Entry point: the think → act → learn loop
├── prompts.py         # Instructions given to the AI model
├── config.py          # Settings: sandbox folder (WORKING_DIR) and file read limit (MAX_CHARS)
├── call_function.py   # Tool definitions and dispatch
├── functions/         # The four tools, plus sandbox path checks
├── calculator/        # Sample project the agent works on by default
└── test_*.py          # Tests for each tool
```

### How it works

- `main.py` sends the conversation and tool definitions to an OpenAI-compatible chat API hosted by OpenRouter. The default model is `nvidia/nemotron-3-ultra-550b-a55b:free`.
- When the model asks for tool calls, eli runs them through `call_function.py` and adds the results to the conversation. When it replies with plain text, that text is the final answer.
- Every tool path goes through `functions/_paths.py`, which resolves symlinks and rejects anything outside `WORKING_DIR`.
- File reads are cut off at `MAX_CHARS` (10,000 characters).

### Configuration

| Setting | Where | Default |
|---|---|---|
| Sandbox folder | `WORKING_DIR` in `config.py` | `./calculator` |
| Max characters read per file | `MAX_CHARS` in `config.py` | `10000` |
| Max loop rounds | `MAX_ITERATIONS` in `main.py` | `20` |
| AI model | `model=` in `main.py` | `nvidia/nemotron-3-ultra-550b-a55b:free` |

### Running tests

From the `eli/` folder:

```sh
for t in test_*.py; do uv run "$t"; done
```

### Requirements

- Python 3.14 or newer (`uv` installs it for you)
- Dependencies: `openai`, `python-dotenv` (see `pyproject.toml`)
