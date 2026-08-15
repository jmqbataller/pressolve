#!/usr/bin/env python3
"""Create a deterministic first-pass summary of pressolve-report.json."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def nested(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    value: Any = data
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]
    return value


def human_bytes(value: Any) -> str:
    if not isinstance(value, (int, float)) or value < 0:
        return "Unknown"
    size = float(value)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}"
        size /= 1024
    return "Unknown"


def memory_bytes(value: Any) -> int | None:
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*([KMG]?)B?\s*", value, re.I)
    if not match:
        return None
    number = float(match.group(1))
    power = {"": 0, "K": 1, "M": 2, "G": 3}[match.group(2).upper()]
    return int(number * (1024**power))


def add_finding(
    findings: list[tuple[str, str, str, str]],
    severity: str,
    finding: str,
    evidence: str,
    next_step: str,
) -> None:
    findings.append((severity, finding, evidence.replace("|", "\\|"), next_step.replace("|", "\\|")))


def analyze(report: dict[str, Any]) -> str:
    if report.get("schema") != "pressolve-report/v1":
        raise ValueError("Unsupported or missing report schema")

    findings: list[tuple[str, str, str, str]] = []
    environment_type = nested(report, "environment", "type", default="unknown")
    wp_version = nested(report, "environment", "wordpress", default="unknown")
    php_version = nested(report, "environment", "php", default="unknown")
    memory_limit = nested(report, "environment", "memory_limit", default="unknown")
    plugin_count = nested(report, "plugins", "active_count", default=0)
    multisite = bool(nested(report, "environment", "multisite", default=False))

    if not nested(report, "site", "https", default=False):
        add_finding(findings, "High", "HTTPS is not detected", "site.https is false", "Confirm proxy/TLS detection and enforce HTTPS before transmitting credentials.")

    if nested(report, "site", "debug_display", default=False):
        add_finding(findings, "High", "Debug output may be public", "WP_DEBUG_DISPLAY is enabled", "Disable public error display and keep logging private.")

    if environment_type == "production" and nested(report, "site", "debug", default=False):
        add_finding(findings, "Medium", "Debug mode is enabled in production", "WP_DEBUG is enabled", "Confirm the temporary logging window and restore production-safe settings.")

    rest_status = nested(report, "rest", "status")
    rest_error = nested(report, "rest", "error_code")
    if rest_error:
        add_finding(findings, "High", "REST self-check failed", str(rest_error), "Inspect loopback, authentication, firewall, and permalink behavior.")
    elif isinstance(rest_status, int) and not 200 <= rest_status < 400:
        add_finding(findings, "High", "REST self-check returned an error", f"HTTP {rest_status}", "Inspect the response path, security/CDN rules, and WordPress REST availability.")

    overdue = nested(report, "cron", "overdue_events", default=0)
    if isinstance(overdue, int) and overdue > 0:
        severity = "High" if overdue >= 10 else "Medium"
        add_finding(findings, severity, "Scheduled events are overdue", f"{overdue} overdue events", "Inspect WP-Cron configuration, loopback, Action Scheduler, and the responsible hooks without running production jobs blindly.")

    fatals = report.get("recent_fatals", [])
    if isinstance(fatals, list) and fatals:
        add_finding(findings, "High", "Recent fatal errors were detected", f"{len(fatals)} redacted log lines", "Correlate timestamps and affected plugin/theme files with the reported symptom.")

    autoload = nested(report, "database", "autoload_bytes")
    if isinstance(autoload, (int, float)):
        if autoload >= 3 * 1024 * 1024:
            add_finding(findings, "High", "Autoloaded options are very large", human_bytes(autoload), "Profile the largest autoloaded options on staging before changing values.")
        elif autoload >= 1024 * 1024:
            add_finding(findings, "Medium", "Autoloaded options need review", human_bytes(autoload), "Identify owners and confirm unused options before cleanup.")

    if isinstance(plugin_count, int) and plugin_count >= 50:
        add_finding(findings, "Medium", "Large active plugin surface", f"{plugin_count} active plugins", "Check overlapping functionality, maintenance status, and request-level cost; do not remove plugins by count alone.")
    elif isinstance(plugin_count, int) and plugin_count >= 30:
        add_finding(findings, "Low", "Review plugin overlap", f"{plugin_count} active plugins", "Inventory duplicated features and critical dependencies.")

    limit_bytes = memory_bytes(memory_limit)
    if limit_bytes is not None and limit_bytes < 128 * 1024 * 1024:
        add_finding(findings, "Low", "WordPress memory limit may be restrictive", str(memory_limit), "Confirm actual exhaustion in PHP logs before increasing limits.")

    if environment_type == "production" and nested(report, "site", "search_engine_visible", default=True) is False:
        add_finding(findings, "Medium", "Search engines are discouraged", "blog_public is disabled", "Confirm whether this production site is intentionally non-indexable.")

    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    findings.sort(key=lambda item: order.get(item[0], 9))

    lines = [
        "# Pressolve Scan",
        "",
        "## Environment",
        "",
        f"- Generated: {report.get('generated_at', 'unknown')}",
        f"- Environment: {environment_type}",
        f"- WordPress: {wp_version}",
        f"- PHP: {php_version}",
        f"- Multisite: {'Yes' if multisite else 'No'}",
        f"- Active plugins: {plugin_count}",
        f"- Database size: {human_bytes(nested(report, 'database', 'size_bytes'))}",
        f"- Autoloaded options: {human_bytes(autoload)}",
        "",
        "## Prioritized findings",
        "",
    ]

    if findings:
        lines.extend(["| Priority | Finding | Evidence | Next step |", "|---|---|---|---|"])
        lines.extend(f"| {severity} | {finding} | {evidence} | {next_step} |" for severity, finding, evidence, next_step in findings)
    else:
        lines.append("No deterministic warning threshold was triggered. This does not prove that the site is healthy; correlate the snapshot with the reported symptom and authoritative logs.")

    lines.extend(
        [
            "",
            "## Required human review",
            "",
            "- Confirm the report came from the affected environment and time window.",
            "- Verify current compatibility and security facts through official sources.",
            "- Inspect the exact failing request, log, or user journey before changing production.",
            "- Prepare backup, rollback, and success criteria for every risky action.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Path to pressolve-report.json")
    args = parser.parse_args()
    try:
        data = json.loads(args.report.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Report root must be a JSON object")
        print(analyze(data), end="")
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise SystemExit(f"Pressolve Scan failed: {error}") from error


if __name__ == "__main__":
    main()
