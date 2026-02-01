#!/usr/bin/env python3
"""bookmarks - FastAPI + HTMX"""

import os, sys, atexit, signal, json
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SERVICE = "bookmarks"
PID_FILE = Path(__file__).parent.parent / "services.pid"
DATA_FILE = Path(__file__).parent / "bookmarks.json"


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

def load_bookmarks() -> list:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []

def save_bookmarks(bookmarks: list):
    DATA_FILE.write_text(json.dumps(bookmarks, indent=2))

def next_id(bookmarks: list) -> int:
    return max((b["id"] for b in bookmarks), default=0) + 1


# --- Routes ---

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    bookmarks = load_bookmarks()
    return templates.TemplateResponse(request, "index.html", {"bookmarks": bookmarks})

@app.post("/bookmarks", response_class=HTMLResponse)
def add_bookmark(request: Request, url: str = Form(...), title: str = Form(""), tag: str = Form("")):
    bookmarks = load_bookmarks()
    bookmarks.append({"id": next_id(bookmarks), "url": url, "title": title or url, "tag": tag})
    save_bookmarks(bookmarks)
    return templates.TemplateResponse(request, "partials/bookmark_list.html", {"bookmarks": bookmarks})

@app.delete("/bookmarks/{bookmark_id}", response_class=HTMLResponse)
def delete_bookmark(request: Request, bookmark_id: int):
    bookmarks = [b for b in load_bookmarks() if b["id"] != bookmark_id]
    save_bookmarks(bookmarks)
    return templates.TemplateResponse(request, "partials/bookmark_list.html", {"bookmarks": bookmarks})

@app.get("/bookmarks/search", response_class=HTMLResponse)
def search_bookmarks(request: Request, q: str = ""):
    bookmarks = load_bookmarks()
    if q:
        q_lower = q.lower()
        bookmarks = [b for b in bookmarks if q_lower in b["title"].lower() or q_lower in b["url"].lower() or q_lower in b.get("tag", "").lower()]
    return templates.TemplateResponse(request, "partials/bookmark_list.html", {"bookmarks": bookmarks})

@app.get("/health")
def health():
    return {"status": "ok", "service": SERVICE, "pid": os.getpid()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
