"""FORGE CLI - Command Line Interface

Interactive CLI for the FORGE AI Code Generation Agent.
"""

import argparse
import sys
from main import Forge


def print_banner():
    """Print the FORGE banner."""
    banner = """
    ╔══════════════════════════════════════╗
    ║     🔥 FORGE - AI Code Agent 🔥     ║
    ║  Generate • Review • Refactor • Test ║
    ╚══════════════════════════════════════╝
    """
    print(banner)


def cmd_generate(forge: Forge, args):
    """Handle the generate command."""
    print(f"🔥 Generating {args.language} code...")
    code = forge.generate(args.prompt, language=args.language)
    print("\n" + "=" * 50)
    print(code)
    print("=" * 50)

    if args.review:
        print("\n📋 Auto-reviewing generated code...")
        result = forge.review(code, language=args.language)
        print(result.summary)


def cmd_review(forge: Forge, args):
    """Handle the review command."""
    with open(args.file, 'r') as f:
        code = f.read()

    print(f"📋 Reviewing {args.file}...")
    result = forge.review(code, language=args.language)

    for issue in result.issues:
        icon = {"info": "🔵", "warning": "🟡", "error": "🔴", "critical": "💀"}
        print(f"  {icon.get(issue.severity.value, '•')} Line {issue.line}: {issue.message}")
        if issue.suggestion:
            print(f"    💡 {issue.suggestion}")

    print(f"\n{result.summary}")


def cmd_refactor(forge: Forge, args):
    """Handle the refactor command."""
    with open(args.file, 'r') as f:
        code = f.read()

    print(f"🔧 Refactoring {args.file}...")
    result = forge.refactor(code)

    print(f"\nQuality: {result.score_before:.0f} → {result.score_after:.0f}")
    for change in result.changes:
        print(f"  ✅ {change}")

    if args.output:
        with open(args.output, 'w') as f:
            f.write(result.refactored)
        print(f"\nRefactored code written to {args.output}")
    else:
        print("\n" + "=" * 50)
        print(result.refactored)
        print("=" * 50)


def cmd_templates(forge: Forge, args):
    """Handle the templates command."""
    templates = forge.templates.list_templates(language=args.language)
    print("📦 Available Templates:\n")
    for lang, names in templates.items():
        print(f"  {lang}:")
        for name in names:
            print(f"    • {name}")


def cmd_info(forge: Forge, args):
    """Handle the info command."""
    info = forge.info()
    print(f"🔨 {info['name']} v{info['version']}")
    print(f"   {info['description']}\n")
    print(f"   Languages ({len(info['languages'])}):")
    for lang in info['languages']:
        print(f"     • {lang}")
    print(f"\n   Features:")
    for feat in info['features']:
        print(f"     ✓ {feat}")


def main():
    parser = argparse.ArgumentParser(
        prog="forge",
        description="FORGE - AI Code Generation Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    gen_parser = subparsers.add_parser("generate", aliases=["gen", "g"], help="Generate code from a prompt")
    gen_parser.add_argument("prompt", help="Description of code to generate")
    gen_parser.add_argument("--language", "-l", default="python", help="Target language (default: python)")
    gen_parser.add_argument("--review", "-r", action="store_true", help="Auto-review generated code")

    # Review command
    review_parser = subparsers.add_parser("review", aliases=["rev", "r"], help="Review existing code")
    review_parser.add_argument("file", help="File to review")
    review_parser.add_argument("--language", "-l", default="python", help="Language of the file")

    # Refactor command
    refactor_parser = subparsers.add_parser("refactor", aliases=["ref"], help="Refactor code")
    refactor_parser.add_argument("file", help="File to refactor")
    refactor_parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    # Templates command
    tpl_parser = subparsers.add_parser("templates", aliases=["tpl", "t"], help="List available templates")
    tpl_parser.add_argument("--language", "-l", help="Filter by language")

    # Info command
    subparsers.add_parser("info", aliases=["i"], help="Show FORGE capabilities")

    args = parser.parse_args()
    forge = Forge()

    commands = {
        "generate": cmd_generate, "gen": cmd_generate, "g": cmd_generate,
        "review": cmd_review, "rev": cmd_review, "r": cmd_review,
        "refactor": cmd_refactor, "ref": cmd_refactor,
        "templates": cmd_templates, "tpl": cmd_templates, "t": cmd_templates,
        "info": cmd_info, "i": cmd_info,
    }

    if not args.command:
        print_banner()
        parser.print_help()
        return

    print_banner()
    handler = commands.get(args.command)
    if handler:
        handler(forge, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
