#!/usr/bin/env python3
"""taskboard - FastAPI + HTMX"""

import os, sys, atexit, signal, json
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SERVICE = "taskboard"
PID_FILE = Path(__file__).parent.parent / "services.pid"
DATA_FILE = Path(__file__).parent / "tasks.json"

COLUMNS = ["todo", "doing", "done"]


# --- PID management ---

def register_pid():
    pid, port = os.getpid(), os.environ.get("PORT", "5000")
    entries = [l for l in PID_FILE.read_text().splitlines() if l and not l.startswith(f"{SERVICE}:")] if PID_FILE.exists() else []
    entries.append(f"{SERVICE}:{pid}:{port}")
    PID_FILE.write_text("\n".join(entries) + "\n")

def unregister_pid():
    if not PID_FILE.exists(): return
    entries = [l for l in PID_FILE.read_text().splitlines() if l and not l.startswith(f"{SERVICE}:")]
    PID_FILE.write_text("\n".join(entries) + "\n") if entries else PID_FILE.unlink(missing_ok=True)

def sig_handler(s, f): unregister_pid(); sys.exit(0)

register_pid()
atexit.register(unregister_pid)
signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGINT, sig_handler)


# --- Data ---

def load_tasks() -> list:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []

def save_tasks(tasks: list):
    DATA_FILE.write_text(json.dumps(tasks, indent=2))

def next_id(tasks: list) -> int:
    return max((t["id"] for t in tasks), default=0) + 1


# --- Routes ---

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    tasks = load_tasks()
    return templates.TemplateResponse(request, "index.html", {"tasks": tasks, "columns": COLUMNS})

@app.post("/tasks", response_class=HTMLResponse)
def add_task(request: Request, title: str = Form(...), column: str = Form("todo")):
    tasks = load_tasks()
    tasks.append({"id": next_id(tasks), "title": title, "column": column if column in COLUMNS else "todo"})
    save_tasks(tasks)
    return templates.TemplateResponse(request, "partials/board.html", {"tasks": tasks, "columns": COLUMNS})

@app.put("/tasks/{task_id}/move", response_class=HTMLResponse)
def move_task(request: Request, task_id: int, to: str = Form(...)):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id and to in COLUMNS:
            t["column"] = to
    save_tasks(tasks)
    return templates.TemplateResponse(request, "partials/board.html", {"tasks": tasks, "columns": COLUMNS})

@app.delete("/tasks/{task_id}", response_class=HTMLResponse)
def delete_task(request: Request, task_id: int):
    tasks = [t for t in load_tasks() if t["id"] != task_id]
    save_tasks(tasks)
    return templates.TemplateResponse(request, "partials/board.html", {"tasks": tasks, "columns": COLUMNS})

@app.get("/health")
def health():
    return {"status": "ok", "service": SERVICE, "pid": os.getpid()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
