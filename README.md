# Self-bot
A basic tool based on [Simplemind](https://github.com/kennethreitz/simplemind/)
to quickly play with different LLMs and discuss with them about a provided text document.

### Installation
- Install `uv`: https://docs.astral.sh/uv/getting-started/installation/
- Install project: `uv sync`

### Run

```
# import CV
uv run cli.py import-resume

# ask questions
uv run cli.py ask-question "How many years of experience do they have?"

# reset bot
uv run cli.py reset
```
