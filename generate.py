#!/usr/bin/env python3
"""FastAPI + HTMX Project Generator"""

from pathlib import Path

COMPONENTS_DIR = Path(__file__).parent / "components"


def load(name: str) -> str:
    """Load a component template."""
    return (COMPONENTS_DIR / f"{name}.html").read_text()


def render(tpl: str, **ctx) -> str:
    """Load and render a component with substitutions."""
    content = load(tpl)
    for k, v in ctx.items():
        content = content.replace(f"{{{{ {k} }}}}", str(v))
    return content


def main():
    print("\n━━━ FastAPI + HTMX Generator ━━━\n")
    
    name = input("  Project name: ").strip()
    if not name:
        return
    
    p = Path(name)
    if p.exists():
        print(f"  '{name}' already exists")
        return
    
    # Create structure
    p.mkdir()
    (p / "templates" / "partials").mkdir(parents=True)
    (p / "static" / "css").mkdir(parents=True)
    (p / "static" / "js").mkdir(parents=True)
    
    # Generate files
    (p / "app.py").write_text(render("_app", name=name))
    (p / "requirements.txt").write_text("fastapi\nuvicorn[standard]\njinja2\npython-multipart\n")
    (p / ".gitignore").write_text("__pycache__/\nvenv/\n*.pid\n*.port\n*.log\n")
    
    # CSS — plain, no framework
    (p / "static" / "css" / "style.css").write_text(render("_style", name=name))
    
    # Templates
    (p / "templates" / "base.html").write_text(render("base", name=name))
    (p / "templates" / "index.html").write_text(render("index", name=name))
    
    # Scripts
    for script in ["start", "stop", "status"]:
        path = p / f"{script}.sh"
        path.write_text(render(f"_{script}", name=name))
        path.chmod(0o755)
    
    (p / "README.md").write_text(render("_readme", name=name))
    (p / "manifesto.md").write_text(render("_manifesto", name=name))
    
    print(f"  ✓ Created {name}/")
    print(f"\n  cd {name} && ./start.sh\n")


if __name__ == "__main__":
    main()
