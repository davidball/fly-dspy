Template to start a new project hosted on fly.io using DSPy and a SQLite database stored on a persistent fly.io volume.



Install [flyctl](https://fly.io/docs/flyctl/install/).


After cloning this repo:

### 1. Create Your fly.toml

```bash
cp fly.toml.example fly.toml
```

Replace "REPLACE_WITH_YOUR_UNIQUE_APP_NAME" with a real, unique name (e.g., my-dspy-project-2025)


### 2.Fly launch
Run `fly launch --no-deploy`



### 3. Setting API Keys (Secrets)

You need at least one API key for the language model (OpenAI, Grok, Venice, etc.).

#### Sample One-line CLI commands

```bash
# For Grok (xAI)
fly secrets set XAI_API_KEY=your_xai_key_here

# For Venice.ai
fly secrets set VENICE_API_KEY=your_venice_key_here

# For OpenAI (fall  back)
fly secrets set OPENAI_API_KEY=sk-...

```

#### Deploy for real

`fly deploy`

# Making Something New
This template is intended to be simply an easy way to get started very quickly with a cheaply hosted DSPy pipeline. 

All the basic routes and simplistic DSPy model are in main.py waiting for you to extend.


### Test the full Docker image locally (optional but recommended)

This runs exactly what Fly.io will run — great for catching environment issues early.

```bash
# Build the image
docker build -t flydspy .

# Run it (maps port 8080, mounts a temporary data folder so SQLite persists during testing)
docker run -p 8080:8080 -e XAI_API_KEY=$XAI_API_KEY -v $(pwd)/local_data:/data flydspy
```


### Run locally without Docker (fastest for development)

```bash
# First time (or when dependencies change)
uv sync

# Run the app
uv run uvicorn main:app --host 0.0.0.0 --port 8080
```


### Persistent Volume
  
The app uses a Fly volume for persistent SQLite storage at `/data/app.db`.
  
Currently the fly launch command will set this up for you automatically based on the default in fly.toml.example. 

If you prefer to create a volume yourself here is a sample command.

  ```bash
  fly volumes create data --region ord --size 1
```
