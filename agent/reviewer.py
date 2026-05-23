"""FORGE Code Review Engine

Automated code review with detailed analysis of style, security,
performance, and correctness.
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ReviewIssue:
    """A single code review issue."""
    line: int
    severity: Severity
    category: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class ReviewResult:
    """Complete code review result."""
    issues: List[ReviewIssue] = field(default_factory=list)
    score: float = 100.0
    summary: str = ""
    passed: bool = True

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity in (Severity.ERROR, Severity.CRITICAL))

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)


class CodeReviewer:
    """Automated code review engine."""

    def __init__(self, strict: bool = False):
        self.strict = strict

    def review(self, code: str, language: str = "python") -> ReviewResult:
        """Perform a comprehensive code review.

        Args:
            code: Source code to review
            language: Programming language of the code

        Returns:
            ReviewResult with issues, score, and summary
        """
        result = ReviewResult()
        lines = code.split('\n')

        # Run all checks
        self._check_style(lines, result)
        self._check_security(lines, result)
        self._check_performance(lines, result)
        self._check_best_practices(lines, result, language)

        # Calculate score
        for issue in result.issues:
            penalties = {
                Severity.INFO: 0,
                Severity.WARNING: 2,
                Severity.ERROR: 5,
                Severity.CRITICAL: 15,
            }
            result.score -= penalties[issue.severity]

        result.score = max(0, result.score)
        result.passed = result.score >= 70
        result.summary = self._generate_summary(result)

        return result

    def _check_style(self, lines: List[str], result: ReviewResult):
        """Check code style issues."""
        for i, line in enumerate(lines, 1):
            # Long lines
            if len(line) > 120:
                result.issues.append(ReviewIssue(
                    line=i,
                    severity=Severity.WARNING,
                    category="style",
                    message=f"Line too long ({len(line)} > 120 characters)",
                    suggestion="Break into multiple lines or use intermediate variables"
                ))

            # Trailing whitespace
            if line != line.rstrip():
                result.issues.append(ReviewIssue(
                    line=i,
                    severity=Severity.INFO,
                    category="style",
                    message="Trailing whitespace detected",
                    suggestion="Remove trailing spaces"
                ))

            # Mixed tabs and spaces
            if '\t' in line and '  ' in line:
                result.issues.append(ReviewIssue(
                    line=i,
                    severity=Severity.WARNING,
                    category="style",
                    message="Mixed tabs and spaces",
                    suggestion="Use consistent indentation (spaces preferred)"
                ))

    def _check_security(self, lines: List[str], result: ReviewResult):
        """Check for security vulnerabilities."""
        for i, line in enumerate(lines, 1):
            # eval/exec usage
            if re.search(r'\b(eval|exec)\s*\(', line):
                result.issues.append(ReviewIssue(
                    line=i,
                    severity=Severity.CRITICAL,
                    category="security",
                    message="Use of eval/exec is a security risk",
                    suggestion="Use ast.literal_eval() or safer alternatives"
                ))

            # Hardcoded secrets
            if re.search(r'(password|secret|api_key|token)\s*=\s*["\'][^"\']+["\']', line, re.I):
                if 'example' not in line.lower() and 'test' not in line.lower():
                    result.issues.append(ReviewIssue(
                        line=i,
                        severity=Severity.CRITICAL,
                        category="security",
                        message="Possible hardcoded secret detected",
                        suggestion="Use environment variables or a secrets manager"
                    ))

            # SQL injection risk
            if re.search(r'f".*SELECT.*{|".*SELECT.*".*\+', line, re.I):
                result.issues.append(ReviewIssue(
                    line=i,
                    severity=Severity.ERROR,
                    category="security",
                    message="Possible SQL injection vulnerability",
                    suggestion="Use parameterized queries"
                ))

    def _check_performance(self, lines: List[str], result: ReviewResult):
        """Check for performance issues."""
        for i, line in enumerate(lines, 1):
            # String concatenation in loops (simplified check)
            if '+= ""' in line or '+= ""' in line:
                result.issues.append(ReviewIssue(
                    line=i,
                    severity=Severity.WARNING,
                    category="performance",
                    message="String concatenation in loop is O(n²)",
                    suggestion="Use list.append() and ''.join() instead"
                ))

    def _check_best_practices(self, lines: List[str], result: ReviewResult, language: str):
        """Check for best practice violations."""
        if language == "python":
            self._check_python_practices(lines, result)

    def _check_python_practices(self, lines: List[str], result: ReviewResult):
        """Python-specific best practice checks."""
        has_docstring = False
        for i, line in enumerate(lines, 1):
            if '"""' in line or "'''" in line:
                has_docstring = True

            # Bare except
            if re.match(r'\s*except\s*:', line):
                result.issues.append(ReviewIssue(
                    line=i,
                    severity=Severity.ERROR,
                    category="best_practice",
                    message="Bare except clause catches all exceptions",
                    suggestion="Catch specific exceptions (e.g., except ValueError:)"
                ))

            # Mutable default arguments
            if re.search(r'def\s+\w+\(.*=\s*(\[\]|\{\})', line):
                result.issues.append(ReviewIssue(
                    line=i,
                    severity=Severity.ERROR,
                    category="best_practice",
                    message="Mutable default argument detected",
                    suggestion="Use None as default and initialize inside function"
                ))

    def _generate_summary(self, result: ReviewResult) -> str:
        """Generate a human-readable review summary."""
        parts = [f"Code Review Score: {result.score:.0f}/100"]

        if result.error_count:
            parts.append(f"🔴 {result.error_count} error(s) found")
        if result.warning_count:
            parts.append(f"🟡 {result.warning_count} warning(s) found")

        info_count = sum(1 for i in result.issues if i.severity == Severity.INFO)
        if info_count:
            parts.append(f"🔵 {info_count} info note(s)")

        if result.passed:
            parts.append("✅ Review passed")
        else:
            parts.append("❌ Review failed - please address the issues above")

        return " | ".join(parts)
