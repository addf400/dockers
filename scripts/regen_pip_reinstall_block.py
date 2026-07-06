#!/usr/bin/env python3
"""
Regenerate the pip force-reinstall block of a Dockerfile from a package-inventory
file, and write the result as a new Dockerfile.

Why
---
NVIDIA base images ship a bunch of Python packages whose *outdated* versions
are never touched by the Dockerfile's `pip install --force-reinstall` line
(only a hand-picked subset is). Those untouched packages keep their old,
sometimes CVE-flagged versions and dist-info metadata around, which is what
gets reported as "过时的信息" (stale/outdated info) by vulnerability/SBOM
scanners.

`info.txt` is a snapshot of the packages actually present in the built image,
one per line, tab/whitespace separated:

    <name>    <version>    <dist-info path>

This script:
  1. Reads the existing `pip install --no-cache-dir --force-reinstall
     --ignore-installed ...` line from the Dockerfile and extracts its
     package list (de-duplicating any repeated names already in there).
  2. Reads `info.txt` and adds any package name not already covered.
  3. Rewrites the pip install line with the merged, de-duplicated list.
  4. Replaces the old single-package (pytest-only) stale dist-info cleanup
     block with a generic loop that removes stale "<pkg>-<old_version>.dist-info"
     directories for *every* package in the merged list (keeping only the
     version pip currently reports as installed).
  5. Writes the result to a new Dockerfile (default: "<Dockerfile>.new"),
     leaving the original file untouched.

Usage
-----
    python3 regen_pip_reinstall_block.py \\
        pytorch/nv26.02/Dockerfile pytorch/nv26.02/info.txt

    python3 regen_pip_reinstall_block.py \\
        pytorch/nv26.02/Dockerfile pytorch/nv26.02/info.txt -o Dockerfile.new
"""

import argparse
import re
import sys
from pathlib import Path

PIP_LINE_RE = re.compile(
    r"^(?P<indent>[ \t]*)(?P<cmd>python(?:3)? -m pip install --no-cache-dir "
    r"--force-reinstall --ignore-installed )(?P<pkgs>.+?)(?P<tail>;\s*\\?)\s*$"
)


def canonical_name(name: str) -> str:
    """PEP 503-ish normalization for comparing/de-duplicating package names."""
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_info_txt(path: Path):
    """Return package names (first column) from an info.txt inventory file, in order."""
    names = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        name = re.split(r"\s+", line, maxsplit=1)[0]
        names.append(name)
    return names


def merge_package_list(existing, extra):
    """Merge two package-name lists, de-duplicating (case/hyphen-insensitive),
    keeping `existing`'s order first, then appending new names from `extra`."""
    merged = []
    seen = set()
    for name in existing:
        canon = canonical_name(name)
        if canon not in seen:
            seen.add(canon)
            merged.append(name)
    for name in extra:
        canon = canonical_name(name)
        if canon not in seen:
            seen.add(canon)
            merged.append(name)
    return merged


def build_cleanup_block(indent: str, pkg_list):
    """Generic dynamic-version stale dist-info cleanup, replacing the old
    pytest-only special case."""
    pkg_list_str = " ".join(pkg_list)
    lines = [
        f'{indent}site_pkgs="$(python -c "import sysconfig; print(sysconfig.get_paths()[\'purelib\'])")"; \\',
        f'{indent}pkg_list="{pkg_list_str}"; \\',
        f"{indent}for pkg in $pkg_list; do \\",
        f'{indent}\tver="$(python -m pip show "$pkg" 2>/dev/null | awk \'/^Version: /{{print $2}}\')"; \\',
        f'{indent}\t[ -n "$ver" ] || continue; \\',
        f"{indent}\tpat=\"$(printf '%s' \"$pkg\" | tr '.-' '__')\"; \\",
        f'{indent}\tfind "$site_pkgs" -maxdepth 1 -type d -name "${{pat}}-*.dist-info" ! -name "${{pat}}-${{ver}}.dist-info" -exec rm -rf {{}} +; \\',
        f"{indent}done; \\",
    ]
    return lines


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("dockerfile", type=Path, help="path to the existing Dockerfile")
    parser.add_argument("info_txt", type=Path, help="path to the info.txt package inventory")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="output path for the new Dockerfile (default: <dockerfile>.new)",
    )
    args = parser.parse_args()

    dockerfile_lines = args.dockerfile.read_text().splitlines()
    extra_names = parse_info_txt(args.info_txt)

    pip_line_idx = None
    match = None
    for i, line in enumerate(dockerfile_lines):
        m = PIP_LINE_RE.match(line)
        if m:
            pip_line_idx = i
            match = m
            break

    if match is None:
        print("Could not find a `pip install --force-reinstall --ignore-installed ...` "
              "line in the Dockerfile.", file=sys.stderr)
        return 1

    existing_pkgs = match.group("pkgs").split()
    merged_pkgs = merge_package_list(existing_pkgs, extra_names)

    indent = match.group("indent")
    new_pip_line = f"{indent}{match.group('cmd')}{' '.join(merged_pkgs)}{match.group('tail')}"

    # Replace the old cleanup block (site_pkgs=/pytest_ver=/find ...) if present,
    # otherwise insert the new cleanup block right after the pip install line.
    cleanup_start = None
    cleanup_end = None
    for i in range(pip_line_idx + 1, len(dockerfile_lines)):
        stripped = dockerfile_lines[i].strip()
        if stripped.startswith("site_pkgs="):
            cleanup_start = i
        elif cleanup_start is not None and stripped.startswith("find ") and "dist-info" in stripped:
            cleanup_end = i
            break
        elif cleanup_start is not None and not (
            stripped.startswith("pytest_ver=") or stripped.startswith("site_pkgs=")
        ):
            # unrelated line reached before finding the find-command; bail out
            break

    new_cleanup_lines = build_cleanup_block(indent, merged_pkgs)

    new_lines = list(dockerfile_lines)
    new_lines[pip_line_idx] = new_pip_line
    if cleanup_start is not None and cleanup_end is not None:
        new_lines[cleanup_start:cleanup_end + 1] = new_cleanup_lines
    else:
        new_lines[pip_line_idx + 1:pip_line_idx + 1] = new_cleanup_lines

    output_path = args.output or args.dockerfile.with_suffix(args.dockerfile.suffix + ".new")
    output_path.write_text("\n".join(new_lines) + "\n")

    added = [n for n in merged_pkgs if canonical_name(n) not in
             {canonical_name(n2) for n2 in existing_pkgs}]
    print(f"Wrote {output_path}")
    print(f"Packages added from {args.info_txt.name}: {', '.join(added) if added else '(none)'}")
    removed_dupes = len(existing_pkgs) - len(
        {canonical_name(n) for n in existing_pkgs}
    )
    if removed_dupes:
        print(f"Removed {removed_dupes} duplicate package name(s) already in the Dockerfile's list")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
