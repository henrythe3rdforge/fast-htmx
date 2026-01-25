#!/usr/bin/env python3
"""Flask + HTMX + Tailwind project generator with local assets."""

import secrets
import subprocess
from pathlib import Path

HTMX_URL = "https://unpkg.com/htmx.org@1.9.10/dist/htmx.min.js"
TAILWIND_URL = "https://cdn.tailwindcss.com/3.4.1"

def download(url: str, dest: Path) -> bool:
    try:
        subprocess.run(["curl", "-sL", "-o", str(dest), url], check=True)
        return True
    except:
        return False

def main():
    print("\n Flask + HTMX Project Generator\n")
    name = input("Project name: ").strip()
    if not name:
        return
    
    p = Path(name)
    if p.exists():
        print(f"'{name}' already exists")
        return
    
    p.mkdir()
    (p / "templates" / "partials").mkdir(parents=True)
    (p / "static" / "js").mkdir(parents=True)
    
    # Download assets
    print("  Downloading assets...")
    download(HTMX_URL, p / "static" / "js" / "htmx.min.js")
    download(TAILWIND_URL, p / "static" / "js" / "tailwind.js")
    print("  ✓ Assets downloaded")

    # app.py
    (p / "app.py").write_text(f'''import os
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")
CSRFProtect(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact", methods=["POST"])
def contact_submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    # Process form here (save to db, send email, etc.)
    return render_template("partials/contact_success.html", name=name)
''')

    # templates/base.html
    (p / "templates" / "base.html").write_text(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{% block title %}}{name}{{% endblock %}}</title>
    <script src="{{{{ url_for('static', filename='js/tailwind.js') }}}}"></script>
    <script src="{{{{ url_for('static', filename='js/htmx.min.js') }}}}"></script>
    <style>
        [x-cloak] {{ display: none !important; }}
    </style>
</head>
<body class="bg-slate-50 min-h-screen flex flex-col">
    <nav class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <a href="{{{{ url_for('index') }}}}" class="flex items-center gap-2 text-xl font-bold text-indigo-600">
                        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                        </svg>
                        {name}
                    </a>
                </div>
                <div class="hidden md:flex items-center gap-1">
                    <a href="{{{{ url_for('index') }}}}" class="px-4 py-2 rounded-lg text-slate-600 hover:text-indigo-600 hover:bg-indigo-50 transition-colors {{{{ 'bg-indigo-50 text-indigo-600' if request.endpoint == 'index' else '' }}}}">Home</a>
                    <a href="{{{{ url_for('features') }}}}" class="px-4 py-2 rounded-lg text-slate-600 hover:text-indigo-600 hover:bg-indigo-50 transition-colors {{{{ 'bg-indigo-50 text-indigo-600' if request.endpoint == 'features' else '' }}}}">Features</a>
                    <a href="{{{{ url_for('about') }}}}" class="px-4 py-2 rounded-lg text-slate-600 hover:text-indigo-600 hover:bg-indigo-50 transition-colors {{{{ 'bg-indigo-50 text-indigo-600' if request.endpoint == 'about' else '' }}}}">About</a>
                    <a href="{{{{ url_for('contact') }}}}" class="ml-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">Contact</a>
                </div>
                <div class="md:hidden flex items-center">
                    <button onclick="document.getElementById('mobile-menu').classList.toggle('hidden')" class="p-2 rounded-lg text-slate-600 hover:bg-slate-100">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <div id="mobile-menu" class="hidden md:hidden border-t border-slate-200 bg-white">
            <div class="px-4 py-3 space-y-1">
                <a href="{{{{ url_for('index') }}}}" class="block px-4 py-2 rounded-lg text-slate-600 hover:bg-indigo-50 hover:text-indigo-600">Home</a>
                <a href="{{{{ url_for('features') }}}}" class="block px-4 py-2 rounded-lg text-slate-600 hover:bg-indigo-50 hover:text-indigo-600">Features</a>
                <a href="{{{{ url_for('about') }}}}" class="block px-4 py-2 rounded-lg text-slate-600 hover:bg-indigo-50 hover:text-indigo-600">About</a>
                <a href="{{{{ url_for('contact') }}}}" class="block px-4 py-2 rounded-lg text-slate-600 hover:bg-indigo-50 hover:text-indigo-600">Contact</a>
            </div>
        </div>
    </nav>

    <main class="flex-1">
        {{% block content %}}{{% endblock %}}
    </main>

    <footer class="bg-slate-800 text-slate-400 py-8 mt-auto">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex flex-col md:flex-row justify-between items-center gap-4">
                <p>&copy; 2025 {name}. All rights reserved.</p>
                <div class="flex gap-6">
                    <a href="#" class="hover:text-white transition-colors">Privacy</a>
                    <a href="#" class="hover:text-white transition-colors">Terms</a>
                    <a href="#" class="hover:text-white transition-colors">Support</a>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>
''')

    # templates/index.html
    (p / "templates" / "index.html").write_text('''{% extends "base.html" %}

{% block content %}
<section class="relative overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 opacity-10"></div>
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32 relative">
        <div class="text-center max-w-3xl mx-auto">
            <h1 class="text-4xl md:text-6xl font-bold text-slate-900 mb-6">
                Build something <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">amazing</span>
            </h1>
            <p class="text-xl text-slate-600 mb-10">
                A modern Flask starter with HTMX for dynamic interactions and Tailwind CSS for beautiful styling. No JavaScript frameworks required.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="{{ url_for('features') }}" class="px-8 py-4 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-500/30">
                    Explore Features
                </a>
                <a href="{{ url_for('about') }}" class="px-8 py-4 bg-white text-slate-700 rounded-xl font-semibold hover:bg-slate-50 transition-colors border border-slate-200">
                    Learn More
                </a>
            </div>
        </div>
    </div>
</section>

<section class="py-20 bg-white">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid md:grid-cols-3 gap-8">
            <div class="p-6 rounded-2xl bg-slate-50 hover:bg-indigo-50 transition-colors group">
                <div class="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-indigo-200 transition-colors">
                    <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                    </svg>
                </div>
                <h3 class="text-lg font-semibold text-slate-900 mb-2">Lightning Fast</h3>
                <p class="text-slate-600">HTMX enables dynamic updates without the overhead of heavy JavaScript frameworks.</p>
            </div>
            <div class="p-6 rounded-2xl bg-slate-50 hover:bg-indigo-50 transition-colors group">
                <div class="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-indigo-200 transition-colors">
                    <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"/>
                    </svg>
                </div>
                <h3 class="text-lg font-semibold text-slate-900 mb-2">Beautiful Design</h3>
                <p class="text-slate-600">Tailwind CSS provides utility-first styling for rapid, consistent UI development.</p>
            </div>
            <div class="p-6 rounded-2xl bg-slate-50 hover:bg-indigo-50 transition-colors group">
                <div class="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-indigo-200 transition-colors">
                    <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2"/>
                    </svg>
                </div>
                <h3 class="text-lg font-semibold text-slate-900 mb-2">Simple Stack</h3>
                <p class="text-slate-600">Flask on the backend keeps things simple, flexible, and easy to understand.</p>
            </div>
        </div>
    </div>
</section>
{% endblock %}
''')

    # templates/features.html
    (p / "templates" / "features.html").write_text('''{% extends "base.html" %}

{% block title %}Features - {{ super() }}{% endblock %}

{% block content %}
<section class="py-20">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
            <h1 class="text-4xl font-bold text-slate-900 mb-4">Features</h1>
            <p class="text-xl text-slate-600 max-w-2xl mx-auto">Everything you need to build modern web applications</p>
        </div>
        
        <div class="grid md:grid-cols-2 gap-8">
            <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 hover:border-indigo-300 hover:shadow-md transition-all">
                <div class="flex items-start gap-4">
                    <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                        </svg>
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold text-slate-900 mb-2">HTMX Integration</h3>
                        <p class="text-slate-600">Dynamic page updates without writing JavaScript. AJAX requests with simple HTML attributes.</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 hover:border-indigo-300 hover:shadow-md transition-all">
                <div class="flex items-start gap-4">
                    <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                        </svg>
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold text-slate-900 mb-2">Tailwind CSS</h3>
                        <p class="text-slate-600">Utility-first CSS framework for rapid UI development with consistent design.</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 hover:border-indigo-300 hover:shadow-md transition-all">
                <div class="flex items-start gap-4">
                    <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                        </svg>
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold text-slate-900 mb-2">CSRF Protection</h3>
                        <p class="text-slate-600">Built-in security with Flask-WTF for safe form submissions.</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 hover:border-indigo-300 hover:shadow-md transition-all">
                <div class="flex items-start gap-4">
                    <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                        </svg>
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold text-slate-900 mb-2">Production Ready</h3>
                        <p class="text-slate-600">Gunicorn server configuration included for deployment.</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 hover:border-indigo-300 hover:shadow-md transition-all">
                <div class="flex items-start gap-4">
                    <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                        </svg>
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold text-slate-900 mb-2">Local Assets</h3>
                        <p class="text-slate-600">HTMX and Tailwind served locally for faster loads and offline development.</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 hover:border-indigo-300 hover:shadow-md transition-all">
                <div class="flex items-start gap-4">
                    <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                        </svg>
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold text-slate-900 mb-2">Easy Scripts</h3>
                        <p class="text-slate-600">Simple start/stop/status scripts for managing your application.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}
''')

    # templates/about.html
    (p / "templates" / "about.html").write_text('''{% extends "base.html" %}

{% block title %}About - {{ super() }}{% endblock %}

{% block content %}
<section class="py-20">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 class="text-4xl font-bold text-slate-900 mb-8">About</h1>
        
        <div class="prose prose-slate prose-lg max-w-none">
            <div class="bg-white rounded-2xl p-8 shadow-sm border border-slate-200 mb-8">
                <h2 class="text-2xl font-semibold text-slate-900 mb-4">Our Mission</h2>
                <p class="text-slate-600 leading-relaxed mb-4">
                    We believe in building web applications that are fast, accessible, and maintainable. 
                    This starter template combines the best tools for creating modern web experiences without 
                    the complexity of heavy JavaScript frameworks.
                </p>
                <p class="text-slate-600 leading-relaxed">
                    By leveraging HTMX for dynamic interactions and Tailwind CSS for styling, you can build 
                    beautiful, interactive applications while keeping your codebase simple and your page loads fast.
                </p>
            </div>
            
            <div class="bg-white rounded-2xl p-8 shadow-sm border border-slate-200 mb-8">
                <h2 class="text-2xl font-semibold text-slate-900 mb-4">The Stack</h2>
                <div class="grid sm:grid-cols-3 gap-6">
                    <div class="text-center p-4">
                        <div class="text-4xl font-bold text-indigo-600 mb-2">Flask</div>
                        <p class="text-sm text-slate-500">Python web framework</p>
                    </div>
                    <div class="text-center p-4">
                        <div class="text-4xl font-bold text-indigo-600 mb-2">HTMX</div>
                        <p class="text-sm text-slate-500">Dynamic HTML</p>
                    </div>
                    <div class="text-center p-4">
                        <div class="text-4xl font-bold text-indigo-600 mb-2">Tailwind</div>
                        <p class="text-sm text-slate-500">Utility-first CSS</p>
                    </div>
                </div>
            </div>
            
            <div class="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl p-8 text-white">
                <h2 class="text-2xl font-semibold mb-4">Get Started</h2>
                <p class="opacity-90 mb-6">
                    Ready to build something amazing? Check out our features or get in touch with us.
                </p>
                <div class="flex flex-wrap gap-4">
                    <a href="{{ url_for('features') }}" class="px-6 py-3 bg-white text-indigo-600 rounded-lg font-semibold hover:bg-indigo-50 transition-colors">
                        View Features
                    </a>
                    <a href="{{ url_for('contact') }}" class="px-6 py-3 bg-indigo-700 text-white rounded-lg font-semibold hover:bg-indigo-800 transition-colors">
                        Contact Us
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}
''')

    # templates/contact.html
    (p / "templates" / "contact.html").write_text('''{% extends "base.html" %}

{% block title %}Contact - {{ super() }}{% endblock %}

{% block content %}
<section class="py-20">
    <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
            <h1 class="text-4xl font-bold text-slate-900 mb-4">Get in Touch</h1>
            <p class="text-xl text-slate-600">We\'d love to hear from you</p>
        </div>
        
        <div class="bg-white rounded-2xl p-8 shadow-sm border border-slate-200">
            <form hx-post="{{ url_for('contact') }}" hx-target="#form-container" hx-swap="innerHTML" id="form-container">
                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                
                <div class="mb-6">
                    <label for="name" class="block text-sm font-medium text-slate-700 mb-2">Name</label>
                    <input type="text" id="name" name="name" required
                           class="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-shadow"
                           placeholder="Your name">
                </div>
                
                <div class="mb-6">
                    <label for="email" class="block text-sm font-medium text-slate-700 mb-2">Email</label>
                    <input type="email" id="email" name="email" required
                           class="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-shadow"
                           placeholder="you@example.com">
                </div>
                
                <div class="mb-6">
                    <label for="message" class="block text-sm font-medium text-slate-700 mb-2">Message</label>
                    <textarea id="message" name="message" rows="5" required
                              class="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-shadow resize-none"
                              placeholder="How can we help?"></textarea>
                </div>
                
                <button type="submit" 
                        class="w-full px-6 py-4 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition-colors flex items-center justify-center gap-2">
                    <span>Send Message</span>
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                    </svg>
                </button>
            </form>
        </div>
    </div>
</section>
{% endblock %}
''')

    # templates/partials/contact_success.html
    (p / "templates" / "partials" / "contact_success.html").write_text('''<div class="text-center py-8">
    <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
    </div>
    <h3 class="text-2xl font-semibold text-slate-900 mb-2">Thank you, {{ name }}!</h3>
    <p class="text-slate-600 mb-6">Your message has been sent successfully. We\'ll get back to you soon.</p>
    <a href="{{ url_for('index') }}" class="inline-flex items-center gap-2 text-indigo-600 hover:text-indigo-700 font-medium">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
        Back to Home
    </a>
</div>
''')

    # requirements.txt
    (p / "requirements.txt").write_text("""flask
flask-wtf
python-dotenv
gunicorn
""")

    # .env
    (p / ".env").write_text(f"SECRET_KEY={secrets.token_hex(32)}\n")

    # .gitignore
    (p / ".gitignore").write_text("__pycache__/\nvenv/\n.env\n*.db\ninstance/\n*.pid\n*.port\n")

    # start.sh
    (p / "start.sh").write_text(f"""#!/bin/bash
cd "$(dirname "$0")"

[ -f app.pid ] && kill $(cat app.pid) 2>/dev/null && rm -f app.pid

[ ! -d venv ] && python3 -m venv venv && venv/bin/pip install -q -r requirements.txt

get_free_port() {{
    python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()"
}}

PORT=$(get_free_port)

nohup venv/bin/gunicorn -w 4 -b 0.0.0.0:$PORT app:app > app.log 2>&1 &
echo $! > app.pid
echo $PORT > app.port

echo "Started on http://localhost:$PORT (PID: $(cat app.pid))"
""")
    (p / "start.sh").chmod(0o755)

    # stop.sh
    (p / "stop.sh").write_text("""#!/bin/bash
cd "$(dirname "$0")"
if [ -f app.pid ]; then
    kill $(cat app.pid) 2>/dev/null
    rm -f app.pid app.port
    echo "Stopped"
else
    echo "Not running"
fi
""")
    (p / "stop.sh").chmod(0o755)

    # status.sh
    (p / "status.sh").write_text("""#!/bin/bash
cd "$(dirname "$0")"
if [ -f app.pid ] && kill -0 $(cat app.pid) 2>/dev/null; then
    echo "Running on http://localhost:$(cat app.port) (PID: $(cat app.pid))"
else
    rm -f app.pid app.port 2>/dev/null
    echo "Not running"
fi
""")
    (p / "status.sh").chmod(0o755)

    # LICENSE
    (p / "LICENSE").write_text("""MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
""")

    print(f"  ✓ Created {name}/\n")
    print(f"  ./start.sh   → Start (random port)")
    print(f"  ./stop.sh    → Stop")
    print(f"  ./status.sh  → Check status & port\n")

if __name__ == "__main__":
    main()
