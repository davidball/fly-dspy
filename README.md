# Fly-DSPy
Quick-start template for deploying a DSPy pipeline to Fly.io with SQLite on a persistent Fly.io volume.


Install [flyctl](https://fly.io/docs/flyctl/install/).


After cloning this repo:

### 1. Create Your fly.toml

```bash
cp fly.toml.example fly.toml
```

Replace "REPLACE_WITH_YOUR_UNIQUE_APP_NAME" with a real, unique name (e.g., my-dspy-project-2025)


### 2. Launch the App Skeleton
```
fly launch --no-deploy
```

### 3. Set Your LLM API Key (Do This Before First Deploy!)

You need at least one API key for the language model (OpenAI, Grok, Venice, etc.).

#### Sample One-line CLI commands
```bash
# For Grok (xAI)
fly secrets set XAI_API_KEY=your_xai_key_here

# For Venice.ai
fly secrets set VENICE_API_KEY=your_venice_key_here

# For OpenAI (fallback)
fly secrets set OPENAI_API_KEY=sk-...
```

#### 4. Deploy
```
fly deploy
```

#### 5. Open Your app
```
fly open
```

Done! Your DSPy app is live with persistent SQLite at /data/app.db.
Visit /history to see saved queries (proves persistence works).

# Extending the App
Everything lives in main.py and models.py.
Replace the simple QA signature with your own pipeline.

## JSON API

Call your pipeline programmatically from anywhere:

```bash
# Local development
curl -X POST http://localhost:8080/api/ask -H "Content-Type: application/json" -d '{"question": "What is DSPy?"}'

# Production (Fly.io)
curl -X POST https://your-app.fly.dev/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is DSPy?"}'
```

Response:
```json
{"question": "What is DSPy?", "answer": "..."}
```

This lets you deploy a DSPy pipeline once and call it from scripts, other apps, or workflows.



## Local development

### Without Docker (fastest)

```bash
uv sync
export OPENAI_API_KEY=sk-...   # or XAI_API_KEY / VENICE_API_KEY
uv run uvicorn main:app --host 0.0.0.0 --port 8080
```

### With Docker (exact production match)
```bash
docker build -t flydspy .
docker run -p 8080:8080 -e XAI_API_KEY=YOURAPIKEY -v $(pwd)/local_data:/data flydspy
```

## Notes

Locked to 1 machine for SQLite consistency (volumes don't share across machines).
For scaling later: switch to Fly Postgres and remove machine limits.

That's it — deploy a new DSPy idea in minutes. 🚀
