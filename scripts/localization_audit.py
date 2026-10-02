#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

UI_HINTS = (
    "Text(", "Button(", "Label(", "Menu(", "Picker(", "Toggle(",
    "Section(", "GroupBox(", ".help(", "navigationTitle(",
    "String(localized:", "localized(", "withTitle:", "messageText",
    "informativeText", "title:", "prompt:", "NSMenuItem(",
)

STRING_RE = re.compile(r'"((?:\\.|[^"\\])*)"')
UI_CALL_RE = re.compile(r"(?<![A-Za-z0-9_])(Text|Button|Label|Menu|Picker|Toggle|Section|GroupBox)\(")


def has_ui_hint(text: str) -> bool:
    return bool(UI_CALL_RE.search(text)) or any(hint in text for hint in (
        ".help(", "navigationTitle(", "String(localized:", "localized(",
        "withTitle:", "messageText", "informativeText", "title:", "prompt:",
        "NSMenuItem(",
    ))


def git_diff(base_ref: str, latest_ref: str) -> str:
    if not base_ref or not latest_ref or base_ref == latest_ref:
        return ""
    proc = subprocess.run(
        ["git", "diff", "--unified=4", base_ref, latest_ref, "--", "Compositor"],
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout


def unescape_swift(value: str) -> str:
    # Preserve real UTF-8 characters such as · and Chinese text. Only decode
    # the small set of escapes that commonly occur in Swift UI literals.
    return (value
            .replace(r'\\n', '\n')
            .replace(r'\\t', '\t')
            .replace(r'\\"', '"')
            .replace(r'\\\\', '\\'))


def probable_ui_literal(line: str, value: str) -> bool:
    if not has_ui_hint(line):
        return False
    if len(value.strip()) < 2:
        return False
    if "\\(" in value:
        return False
    if not re.search(r"[A-Za-z]", value):
        return False
    if value.startswith(("http://", "https://")):
        return False
    return True


def zh_status(entry: dict) -> tuple[bool, str]:
    loc = entry.get("localizations", {}).get("zh-Hans", {})
    unit = loc.get("stringUnit", {})
    state = unit.get("state", "")
    value = unit.get("value", "")
    ok = state == "translated" and bool(str(value).strip())
    return ok, str(value)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", default="Compositor/Localizable.xcstrings")
    ap.add_argument("--base-ref", default="")
    ap.add_argument("--latest-ref", default="")
    ap.add_argument("--output", default="localization-audit.md")
    args = ap.parse_args()

    catalog_path = Path(args.catalog)
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    strings = data.get("strings", {})

    missing = []
    for key, entry in sorted(strings.items()):
        ok, value = zh_status(entry)
        if not ok:
            missing.append((key, value))

    diff = git_diff(args.base_ref, args.latest_ref)
    added_candidates: set[str] = set()
    recent: list[str] = []

    for raw in diff.splitlines():
        if raw.startswith(("+++", "---", "@@", "diff ", "index ")):
            recent.clear()
            continue
        if not raw:
            continue

        prefix = raw[0]
        if prefix not in {"+", " ", "-"}:
            continue

        line = raw[1:]

        # Keep nearby added/context lines so strings split across a multi-line
        # SwiftUI/localization call inherit the call site's UI context.
        if prefix != "-":
            recent.append(line)
            recent = recent[-8:]

        if prefix != "+":
            continue

        context = "\n".join(recent)
        if not has_ui_hint(context):
            continue

        for match in STRING_RE.finditer(line):
            # SF Symbol names are identifiers, not user-facing strings.
            before = line[:match.start()]
            if re.search(r"(?:systemName|accessibilityIdentifier):\s*$", before):
                continue

            raw_value = match.group(1)
            if probable_ui_literal(context, raw_value):
                added_candidates.add(unescape_swift(raw_value))

    missing_added = []
    covered_added = []
    for value in sorted(added_candidates):
        entry = strings.get(value)
        if not entry:
            missing_added.append((value, "missing catalog key"))
            continue
        ok, zh = zh_status(entry)
        if not ok:
            missing_added.append((value, "missing/incomplete zh-Hans"))
        else:
            covered_added.append((value, zh))

    out = []
    out.append("# Aips localization audit")
    out.append("")
    out.append(f"- Catalog: `{args.catalog}`")
    out.append(f"- Catalog keys: **{len(strings)}**")
    out.append(f"- Missing/incomplete zh-Hans keys: **{len(missing)}**")
    if args.base_ref and args.latest_ref:
        out.append(f"- Upstream diff: `{args.base_ref}` → `{args.latest_ref}`")
        out.append(f"- Added UI string candidates: **{len(added_candidates)}**")
        out.append(f"- Added candidates missing Chinese coverage: **{len(missing_added)}**")
    out.append("")

    out.append("## Catalog missing/incomplete zh-Hans")
    out.append("")
    if not missing:
        out.append("None.")
    else:
        for key, _ in missing:
            out.append(f"- `{key}`")
    out.append("")

    out.append("## Upstream-added UI strings missing Chinese coverage")
    out.append("")
    if not missing_added:
        out.append("None.")
    else:
        for value, reason in missing_added:
            out.append(f"- `{value}` — {reason}")
    out.append("")

    out.append("## Upstream-added UI strings already covered")
    out.append("")
    if not covered_added:
        out.append("None.")
    else:
        for value, zh in covered_added:
            out.append(f"- `{value}` → {zh}")

    Path(args.output).write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
