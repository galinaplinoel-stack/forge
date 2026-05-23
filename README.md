# 🔥 FORGE - AI Code Generation Agent

<p align="center">
  <strong>Generate • Review • Refactor • Test</strong>
</p>

---

**FORGE** is an AI-powered code generation agent that writes, reviews, refactors, and tests code through an intelligent CLI interface. Like a blacksmith shaping metal, FORGE hammers raw ideas into production-ready code.

## ✨ Features

- **🔨 Code Generation** — Describe what you need in plain English, get clean, documented code
- **📋 Auto Review** — Automated code review with security, style, and performance checks
- **🔧 Refactoring** — Intelligent code improvement with quality scoring
- **🧪 Test Writing** — Generate comprehensive test suites for your code
- **🌐 Multi-language** — Supports 20+ programming languages
- **📝 Documentation** — Auto-generated docstrings and inline comments

## 🚀 Quick Start

```bash
# Generate code from a prompt
python cli.py generate "create a REST API with user authentication" --language python

# Review existing code
python cli.py review app.py --language python

# Refactor code
python cli.py refactor app.py --output app_improved.py

# List available templates
python cli.py templates --language python
```

## 📦 Installation

```bash
git clone https://github.com/galinaplinoel-stack/forge.git
cd forge
pip install -r requirements.txt
```

## 🏗️ Architecture

```
forge/
├── agent/
│   ├── codegen.py       # Core code generation engine
│   ├── templates.py     # Pre-built code templates
│   ├── refactoring.py   # Automated refactoring engine
│   └── reviewer.py      # Code review engine
├── cli.py               # Command-line interface
├── main.py              # Main orchestrator
└── requirements.txt
```

## 🛠️ Usage as a Library

```python
from main import Forge

forge = Forge()

# Generate code
code = forge.generate("a binary search function", language="python")

# Review code
result = forge.review(code)
print(result.summary)  # "Code Review Score: 85/100 | ✅ Review passed"

# Refactor code
refactored = forge.refactor(code)
print(f"Quality: {refactored.score_before} → {refactored.score_after}")
```

## 🌍 Supported Languages

Python • JavaScript • TypeScript • Rust • Go • Java • C • C++ • C# • Ruby • PHP • Swift • Kotlin • Scala • Haskell • Elixir • Clojure • Lua • Perl • R

## 📊 Code Review Categories

| Category | Checks |
|----------|--------|
| **Security** | eval/exec usage, hardcoded secrets, SQL injection |
| **Style** | Line length, trailing whitespace, indentation |
| **Performance** | String concatenation, loop optimization |
| **Best Practices** | Exception handling, mutable defaults, docstrings |

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with 🔥 by the FORGE team
</p>
