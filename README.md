# yoursDaily: Your daily AI-generated podcast

## Demo

https://github.com/IronJayx/yoursDaily/assets/101343852/b26ba1e5-ef5a-4140-bede-9e52fa8dbaae


## Requirements

To run this app you need to have:

- an [OpenAI](https://platform.openai.com/api-keys) API key
- an [Exa](https://exa.ai) API key (there is a free tier available)
- an [Eleven Labs](https://elevenlabs.io/) API key (there is a free tier available)


## Installation

Set up a virtual environment and install the requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Setup the secrets in your `.env` file (use `.env.example` for reference):

```.env
# llm endpoint
OPENAI_API_KEY=""

# search
EXA_API_KEY=""

# audio
ELEVEN_LABS_API_KEY=""
```

## Usage

```bash
streamlit run app.py
```

This will open a new tab in your default browser with the app running.

Happy listening !
