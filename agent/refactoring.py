"""FORGE Code Refactoring Engine

Automated refactoring tools to improve code quality, readability, and performance.
"""

import ast
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class RefactorResult:
    """Result of a refactoring operation."""
    original: str
    refactored: str
    changes: List[str]
    score_before: float
    score_after: float


class RefactoringEngine:
    """Engine for automated code refactoring and improvement."""

    def __init__(self, language: str = "python"):
        self.language = language
        self.rules = self._load_rules()

    def _load_rules(self) -> List[Dict]:
        """Load refactoring rules for the target language."""
        return [
            {"name": "extract_function", "description": "Extract repeated code into functions"},
            {"name": "rename_variables", "description": "Improve variable naming"},
            {"name": "simplify_conditions", "description": "Simplify conditional logic"},
            {"name": "remove_duplicates", "description": "Remove duplicate code blocks"},
            {"name": "optimize_imports", "description": "Clean up import statements"},
            {"name": "add_type_hints", "description": "Add type annotations"},
            {"name": "improve_docstrings", "description": "Add or improve documentation"},
        ]

    def refactor(self, code: str, rules: Optional[List[str]] = None) -> RefactorResult:
        """Refactor the given code applying specified rules.

        Args:
            code: Source code to refactor
            rules: Optional list of specific rules to apply

        Returns:
            RefactorResult with original, refactored code and change summary
        """
        if rules is None:
            rules = [r["name"] for r in self.rules]

        changes = []
        refactored = code
        score_before = self._calculate_quality_score(code)

        for rule_name in rules:
            method = getattr(self, f"_apply_{rule_name}", None)
            if method:
                refactored, rule_changes = method(refactored)
                changes.extend(rule_changes)

        score_after = self._calculate_quality_score(refactored)

        return RefactorResult(
            original=code,
            refactored=refactored,
            changes=changes,
            score_before=score_before,
            score_after=score_after,
        )

    def _apply_simplify_conditions(self, code: str) -> Tuple[str, List[str]]:
        """Simplify conditional expressions."""
        changes = []
        result = code

        # Replace "if x == True" with "if x"
        pattern = r'if\s+(\w+)\s*==\s*True:'
        if re.search(pattern, result):
            result = re.sub(pattern, r'if \1:', result)
            changes.append("Simplified '== True' comparisons")

        # Replace "if x == False" with "if not x"
        pattern = r'if\s+(\w+)\s*==\s*False:'
        if re.search(pattern, result):
            result = re.sub(pattern, r'if not \1:', result)
            changes.append("Simplified '== False' comparisons")

        return result, changes

    def _apply_optimize_imports(self, code: str) -> Tuple[str, List[str]]:
        """Sort and organize import statements."""
        changes = []
        lines = code.split('\n')
        imports = []
        non_imports = []
        in_imports = True

        for line in lines:
            stripped = line.strip()
            if in_imports and (stripped.startswith('import ') or stripped.startswith('from ')):
                imports.append(line)
            else:
                if stripped and not stripped.startswith('#'):
                    in_imports = False
                non_imports.append(line)

        if imports:
            sorted_imports = sorted(set(imports))
            if sorted_imports != imports:
                changes.append("Sorted and deduplicated imports")
                return '\n'.join(sorted_imports + [''] + non_imports), changes

        return code, changes

    def _apply_add_type_hints(self, code: str) -> Tuple[str, List[str]]:
        """Add type hints to function signatures missing them."""
        changes = []
        # Pattern for functions without return type hints
        pattern = r'(def\s+\w+\([^)]*\))\s*:'

        def add_return_hint(match):
            sig = match.group(1)
            if '->' not in sig:
                changes.append(f"Added return type hint to {sig.split('(')[0].strip()}")
                return f"{sig} -> None:"
            return match.group(0)

        result = re.sub(pattern, add_return_hint, code)
        return result, changes

    def _calculate_quality_score(self, code: str) -> float:
        """Calculate a code quality score (0-100)."""
        score = 50.0

        # Check for docstrings
        if '"""' in code or "'''" in code:
            score += 10

        # Check for type hints
        if '->' in code or ': str' in code or ': int' in code:
            score += 10

        # Penalize long functions
        lines = code.split('\n')
        if len(lines) > 50:
            score -= 5

        # Check for comments
        comment_lines = sum(1 for l in lines if l.strip().startswith('#'))
        if comment_lines > 0:
            score += min(comment_lines * 2, 10)

        return min(max(score, 0), 100)

    def analyze(self, code: str) -> Dict:
        """Analyze code and suggest refactoring opportunities."""
        suggestions = []
        score = self._calculate_quality_score(code)

        if '"""' not in code and "'''" not in code:
            suggestions.append("Add docstrings to functions and classes")

        if '->' not in code and 'def ' in code:
            suggestions.append("Add type hints to function signatures")

        if code.count('def ') > 1 and len(code.split('\n')) > 100:
            suggestions.append("Consider splitting into smaller modules")

        return {
            "quality_score": score,
            "suggestions": suggestions,
            "line_count": len(code.split('\n')),
            "function_count": code.count('def '),
        }
