# Self-bot

A basic tool based on [Simplemind](https://github.com/kennethreitz/simplemind/)
to quickly play with different LLMs and discuss with them about a provided text document.

<hr>

### Installation

- Install `uv`: https://docs.astral.sh/uv/getting-started/installation/
- Install project: `uv venv && uv sync`
- Create the `.env` file based on the provided `.env.example` (with only one LLM API key)
- Tweak `cli/config.py` to use the LLM you want (here we use either Anthropic or OpenAI)
- For details about the supported LLMs, see the [Simplemind repository](https://github.com/kennethreitz/simplemind#supported-apis)

<br>

### CLI

```
# import CV from a S3 bucket
uv run cli/main.py import-resume

# OR import CV from a local file
uv run cli/main.py import-resume <filepath>

# ask questions
uv run cli/main.py ask-question "How many years of experience do they have?"

# reset bot
uv run cli/main.py reset
```

<br>

### Vue App

Run in 2 terminals:

```
# Start Web server
uv run app/server.py

# Start Vue app (dev mode)
cd app
npm run dev

# OR Start Vue app (prod mode)
npm run preview -- --port 3000 --host
```

<br>

### Terraform deployment

Based on the chosen LLM, adapt [`terraform/main.tf`](terraform/main.tf#L171) and eventually create more API keys secrets/variables in both `.github/workflows/cd.yml` and `terraform/variables.tf`.
