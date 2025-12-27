import logging
import os
import sqlite3

import dspy
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models import grok, venice

VERBOSE = True

app = FastAPI()
templates = Jinja2Templates(directory="templates")

from models import grok, venice  # keep your model factory

# Try to configure LM — fall back to None if no keys
lm = None
missing_key_message = None

openai_key = os.getenv("OPENAI_API_KEY")
xai_key = os.getenv("XAI_API_KEY")
venice_key = os.getenv("VENICE_API_KEY")

if xai_key:
    lm = grok("grok-4-1-fast-reasoning")  # or whatever default
elif venice_key:
    lm = venice("venice-uncensored")
elif openai_key:
    lm = dspy.OpenAI(model="gpt-4o-mini")
else:
    missing_key_message = (
        "No LLM API key configured. Set one of these secrets in Fly dashboard or CLI:<br><br>"
        "<code>fly secrets set XAI_API_KEY=...</code><br>"
        "<code>fly secrets set VENICE_API_KEY=...</code><br>"
        "<code>fly secrets set OPENAI_API_KEY=sk-...</code><br><br>"
        "The app works fine otherwise — try /history to see persistent storage!"
    )

print("well what is lm?", lm)

if lm:
    dspy.settings.configure(lm=lm)


class BasicQA(dspy.Signature):
    """Answer questions with a fun twist."""

    question = dspy.InputField()
    answer = dspy.OutputField(desc="Creative, concise answer.")


qa = dspy.Predict(BasicQA)

# SQLite setup on persistent volume
DB_PATH = os.getenv("DATABASE_PATH", "/data/app.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS queries
                 (id INTEGER PRIMARY KEY, question TEXT, answer TEXT)""")
    conn.commit()
    conn.close()


init_db()  # Run on startup — safe if table exists


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.get_template("index.html").render(
        {"request": request, "result": None}
    )


@app.post("/", response_class=HTMLResponse)
async def ask(request: Request, question: str = Form(...)):
    if not lm:
        return templates.get_template("index.html").render(
            {
                "request": request,
                "question": question,
                "result": None,
                "error": missing_key_message,
            }
        )
    pred = qa(question=question)
    answer = pred.answer

    # Persist to SQLite on volume
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO queries (question, answer) VALUES (?, ?)", (question, answer)
    )
    conn.commit()
    conn.close()

    if VERBOSE:
        print("\n=== DSPy LM Call History (last 1) ===\n")
        print(lm.inspect_history(n=1))
        print("=====================================\n")

    return templates.get_template("index.html").render(
        {"request": request, "question": question, "result": answer}
    )


@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT question, answer FROM queries ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()

    return templates.get_template("history.html").render(
        {"request": request, "history": rows}
    )


@app.get("/health")
def health():
    return {"status": "ok"}
