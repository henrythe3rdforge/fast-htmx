#!/usr/bin/env python3
"""Flask + HTMX + Tailwind Project Generator"""

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
    print("\n━━━ Flask + HTMX + Tailwind Generator ━━━\n")
    
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
    (p / "static" / "js").mkdir(parents=True)
    
    # Generate files
    (p / "app.py").write_text(render("_app", name=name))
    (p / "requirements.txt").write_text("flask\npython-dotenv\ngunicorn\n")
    (p / ".gitignore").write_text("__pycache__/\nvenv/\n*.pid\n*.port\n*.log\n")
    
    # Templates
    for tmpl in ["base", "index", "about", "contact"]:
        (p / "templates" / f"{tmpl}.html").write_text(render(tmpl, name=name))
    
    # Partials
    for partial in ["contact_success", "click_response"]:
        (p / "templates" / "partials" / f"{partial}.html").write_text(render(partial, name=name))
    
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
