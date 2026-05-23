"""FORGE Code Templates

Pre-built templates for common programming patterns and structures.
"""

from typing import Dict, Optional


class TemplateLibrary:
    """Library of code templates for rapid generation."""

    TEMPLATES: Dict[str, Dict[str, str]] = {
        "python": {
            "fastapi": '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="{name}")


class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None


@app.get("/")
async def root():
    return {{"message": "Welcome to {name}"}}


@app.get("/items/{{item_id}}")
async def get_item(item_id: int):
    return {{"item_id": item_id}}
''',
            "cli": '''import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="{name}")
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        print(f"Running: {{args.command}}")

    # Execute command
    result = execute(args.command)
    print(result)


def execute(command: str) -> str:
    """Execute the given command."""
    return f"Executed: {{command}}"


if __name__ == "__main__":
    main()
''',
            "class": '''class {name}:
    """A well-structured class for {description}."""

    def __init__(self{params}):
        """Initialize {name}."""
        {init_body}

    def __repr__(self) -> str:
        return f"{name}({{repr_body}})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, {name}):
            return NotImplemented
        return {eq_body}
''',
        },
        "javascript": {
            "express": '''const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get("/", (req, res) => {{
    res.json({{ message: "Welcome to {name}" }});
}});

app.listen(PORT, () => {{
    console.log(`Server running on port ${{PORT}}`);
}});
''',
            "react-component": '''import React, {{ useState }} from "react";

const {name} = ({{ title }}) => {{
    const [state, setState] = useState(null);

    return (
        <div className="{name_lower}">
            <h1>{{title}}</h1>
            {{/* Component content */}}
        </div>
    );
}};

export default {name};
''',
        },
    }

    @classmethod
    def get_template(cls, language: str, template_name: str) -> Optional[str]:
        """Get a template by language and name."""
        lang_templates = cls.TEMPLATES.get(language, {})
        return lang_templates.get(template_name)

    @classmethod
    def list_templates(cls, language: Optional[str] = None) -> Dict[str, list]:
        """List available templates, optionally filtered by language."""
        if language:
            templates = cls.TEMPLATES.get(language, {})
            return {language: list(templates.keys())}
        return {lang: list(templates.keys()) for lang, templates in cls.TEMPLATES.items()}

    @classmethod
    def fill_template(cls, template: str, **kwargs) -> str:
        """Fill in a template with provided values."""
        return template.format(**kwargs)
