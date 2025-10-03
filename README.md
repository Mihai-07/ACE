# ACE - Agentic Code Executor 🤖

ACE is an AI-powered assistant that can execute Python code to solve complex problems. This demo allows you to interact with the agent in a single chat session.

## Features ✨
- 💬 Ask the agent any question or give it a task
- 🐍 The agent can execute Python code to help solve your problems
- 👁️ All code executed by the agent is shown for transparency

## Installation 🚀

### Using pip
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```

### Using conda
```bash
conda create -n ace python=3.11
conda activate ace
pip install -r requirements.txt
streamlit run main.py
```

### Using uv (recommended)
```bash
uv add -r requirements.txt
uv run streamlit run main.py
```

## Configuration 🔧
- **OpenAI API key (required)**: The app now uses the official OpenAI API via `langchain-openai`.
  - Recommended (Streamlit secrets): create `.streamlit/secrets.toml` with:

    ```toml
    [api_keys]
    openai = "YOUR_OPENAI_API_KEY"
    ```

  - Or set an environment variable before running Streamlit:

    ```bash
    export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```

- **Model selection**: The default model is set in `app_utilities.py` via `ChatOpenAI`. Update the `model` parameter there if you want to change it.

## Usage 📖
1. Run the app with Streamlit
2. Enter your question or task in the chat input
3. View the agent's response and any code it runs

## Security 🔒
- The agent will only execute code that complies with the included SECURITY NOTE
- Use at your own risk

---

**GitHub Repository URL:** [https://github.com/Mihai-07/ACE](https://github.com/Mihai-07/ACE)

**Streamlit Cloud URL:** [https://mihai-07-ace.streamlit.app](https://mihai-07-ace.streamlit.app)

**License:** GNU General Public License v3.0 ([GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html))

This is a demo version with a single chat session. For advanced use cases, see future releases.
