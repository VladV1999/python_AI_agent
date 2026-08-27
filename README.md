# Python AI Agent

A small AI coding agent built on Google's Gemini API. It takes a prompt, lets
the model plan and call functions, and loops until it gives you a final answer.

This agent gives you 4 functions to work with:

1. **Reading a file**
2. **Writing to a file** (creates it if it doesn't exist)
3. **Listing the files** in a specified directory
4. **Running a python file**

Though I do intend to add more functionality later :D

All of this is sandboxed to a single working directory, so the agent can't
read/write/run anything outside of it.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management
(see `pyproject.toml` / `uv.lock` — no `requirements.txt` here).

```bash
uv sync
```

Create a `.env` file in the root directory with your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

Simply supply the prompt after running with:

```bash
uv run main.py "<insert prompt here>"
```

Add `--verbose` if you want to see the full function calls and their results.

Do note that you do have to be in the root directory for this to work!
