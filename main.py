"""FORGE - AI Code Generation Agent

Main entry point for the FORGE agent system.
FORGE writes, reviews, refactors, and tests code through an intelligent CLI interface.
"""

from agent.codegen import CodeGenerator
from agent.templates import TemplateLibrary
from agent.refactoring import RefactoringEngine
from agent.reviewer import CodeReviewer


class Forge:
    """Main FORGE orchestrator that coordinates all code generation tasks."""

    def __init__(self, model: str = "default", temperature: float = 0.7):
        self.generator = CodeGenerator(model=model, temperature=temperature)
        self.templates = TemplateLibrary()
        self.refactorer = RefactoringEngine()
        self.reviewer = CodeReviewer()

    def generate(self, prompt: str, language: str = "python") -> str:
        """Generate code from a natural language prompt."""
        return self.generator.generate(prompt, language=language)

    def review(self, code: str, language: str = "python"):
        """Review code and return issues and score."""
        return self.reviewer.review(code, language=language)

    def refactor(self, code: str, rules=None):
        """Refactor code to improve quality."""
        return self.refactorer.refactor(code, rules=rules)

    def get_template(self, language: str, template_name: str):
        """Get a pre-built code template."""
        return self.templates.get_template(language, template_name)

    def info(self) -> dict:
        """Get information about FORGE capabilities."""
        return {
            "name": "FORGE",
            "version": "1.0.0",
            "description": "AI Code Generation Agent",
            "languages": self.generator.list_languages(),
            "features": [
                "Code Generation",
                "Automated Review",
                "Refactoring",
                "Template Library",
                "Multi-language Support",
            ],
        }


if __name__ == "__main__":
    forge = Forge()
    info = forge.info()
    print(f"🔨 {info['name']} v{info['version']} - {info['description']}")
    print(f"   Supporting {len(info['languages'])} languages")
    print(f"   Features: {', '.join(info['features'])}")
