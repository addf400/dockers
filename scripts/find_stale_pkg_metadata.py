#!/usr/bin/env python3
"""
Find (and optionally remove) stale/redundant Python package metadata directories.

Background
----------
When a Dockerfile does something like:

    pip install --force-reinstall --ignore-installed <pkg>
    pip uninstall -y <pkg>

pip does not always clean up the *old* "<name>-<old_version>.dist-info"
(or "*.egg-info") directory that shipped with the base image (e.g. it was
installed by apt / conda / a different pip run and isn't referenced by the
new install's RECORD). The result is that two (or more) metadata folders for
the same package end up living side by side on disk, e.g.:

    aiohttp-3.13.3.dist-info/METADATA   <- stale leftover
    aiohttp-3.14.0.dist-info/METADATA   <- actually installed

Vulnerability/SBOM scanners (Trivy, Grype, etc.) read *every* dist-info they
find, so the stale, no-longer-installed version keeps getting reported and
fails compliance scans even though it is not actually used at runtime.

This script scans one or more site-packages/dist-packages directories,
groups "*.dist-info" / "*.egg-info" folders by canonical package name, and
flags any package that has more than one metadata directory. For each group
it tries to figure out which version is the one Python actually resolves
(via importlib.metadata); everything else is reported as stale. If pip no
longer considers the package installed at all (e.g. it was uninstalled),
every leftover metadata directory for that name is reported as stale.

Usage
-----
    # Just report, using auto-detected site-packages/dist-packages dirs
    python3 find_stale_pkg_metadata.py

    # Scan specific directories
    python3 find_stale_pkg_metadata.py /usr/local/lib/python3.12/dist-packages

    # Delete the stale directories (dry run first is recommended!)
    python3 find_stale_pkg_metadata.py --fix

    # Only print the stale paths, one per line (handy for piping into rm)
    python3 find_stale_pkg_metadata.py --paths-only | xargs -r rm -rf
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import sysconfig
from importlib import metadata as importlib_metadata
from pathlib import Path

INFO_RE = re.compile(r"^(?P<name>.+?)-(?P<version>[^-]+)\.(?:dist-info|egg-info)$")


def canonical_name(name: str) -> str:
    """PEP 503-ish normalization so e.g. 'PyYAML' and 'pyyaml' are grouped together."""
    return re.sub(r"[-_.]+", "-", name).lower()


def version_key(version: str):
    """Best-effort sortable key for a version string (numeric-aware)."""
    parts = re.split(r"[.+-]", version)
    key = []
    for part in parts:
        key.append((0, int(part)) if part.isdigit() else (1, part))
    return key


def default_site_dirs():
    """Best-effort discovery of the current interpreter's package directories."""
    dirs = []
    for key in ("purelib", "platlib"):
        path = sysconfig.get_paths().get(key)
        if path and Path(path).is_dir():
            dirs.append(Path(path))
    # dedupe while preserving order
    seen = set()
    unique_dirs = []
    for d in dirs:
        if d not in seen:
            seen.add(d)
            unique_dirs.append(d)
    return unique_dirs


def scan(site_dir: Path):
    """Group metadata directories in `site_dir` by canonical package name."""
    groups = {}
    for entry in sorted(site_dir.iterdir()):
        if not entry.is_dir():
            continue
        m = INFO_RE.match(entry.name)
        if not m:
            continue
        name, version = m.group("name"), m.group("version")
        groups.setdefault(canonical_name(name), []).append((name, version, entry))
    return groups


def resolve_active_version(name: str):
    """Return the version importlib.metadata currently resolves for `name`, or None."""
    try:
        return importlib_metadata.version(name)
    except importlib_metadata.PackageNotFoundError:
        return None


def pip_list_versions(python_exe: str):
    """Return {canonical_name: version} as truly reported by `pip list` (source of truth)."""
    try:
        out = subprocess.check_output(
            [python_exe, "-m", "pip", "list", "--format=json", "--disable-pip-version-check"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return {}
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return {}
    return {canonical_name(pkg["name"]): pkg["version"] for pkg in data}


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "site_dirs",
        nargs="*",
        type=Path,
        help="site-packages/dist-packages dirs to scan (default: current interpreter's dirs)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="delete stale metadata dirs (keeps the active version; if none is "
        "active, keeps nothing and removes all copies for that name)",
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="python executable to run `pip list` with, to confirm the truly "
        "installed version (default: %(default)s)",
    )
    parser.add_argument(
        "--paths-only",
        action="store_true",
        help="suppress the normal report and only print stale dir paths, one per "
        "line (e.g. for piping into `xargs rm -rf`)",
    )
    args = parser.parse_args()

    site_dirs = args.site_dirs or default_site_dirs()
    if not site_dirs:
        print("No site-packages/dist-packages directories found.", file=sys.stderr)
        return 1

    pip_versions = pip_list_versions(args.python)

    found_any = False
    stale_summary = []  # (canon, version, path) across all scanned dirs
    for site_dir in site_dirs:
        if not site_dir.is_dir():
            print(f"skip (not a directory): {site_dir}", file=sys.stderr)
            continue

        groups = scan(site_dir)
        dupes = {k: v for k, v in groups.items() if len(v) > 1}
        if not dupes:
            continue

        found_any = True
        if not args.paths_only:
            print(f"\n== {site_dir} ==")
        for canon, entries in sorted(dupes.items()):
            entries_sorted = sorted(entries, key=lambda e: version_key(e[1]))
            importlib_version = resolve_active_version(entries_sorted[0][0])
            pip_version = pip_versions.get(canon)
            # `pip list` is the source of truth for "what's really installed";
            # fall back to importlib.metadata if pip couldn't be queried.
            active_version = pip_version or importlib_version

            if not args.paths_only:
                note = ""
                if pip_version and importlib_version and pip_version != importlib_version:
                    note = f"  [!] pip list={pip_version} vs importlib.metadata={importlib_version}"
                print(f"- {canon}: {len(entries_sorted)} metadata dirs found"
                      + (f" (active: {active_version})" if active_version else " (not currently installed)")
                      + note)

            to_delete = []
            for name, version, path in entries_sorted:
                is_active = active_version is not None and version == active_version
                if not args.paths_only:
                    tag = "KEEP  " if is_active else "STALE "
                    print(f"    [{tag}] {version:<15} {path}")
                if not is_active:
                    to_delete.append(path)
                    stale_summary.append((canon, version, path))

            if args.fix:
                for path in to_delete:
                    if not args.paths_only:
                        print(f"    removing {path}")
                    shutil.rmtree(path, ignore_errors=True)

    if args.paths_only:
        for _, _, path in stale_summary:
            print(path)
        return 0

    if not found_any:
        print("No redundant package metadata found.")
        return 0

    if stale_summary:
        print("\n=== Stale metadata to remove (name, version, path) ===")
        for canon, version, path in stale_summary:
            print(f"{canon}\t{version}\t{path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
