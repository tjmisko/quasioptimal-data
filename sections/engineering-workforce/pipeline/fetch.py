"""Fetch reachable sources into ``data/raw/`` and report on blocked ones.

Usage:
    uv run python sections/engineering-workforce/pipeline/fetch.py            # fetch all reachable
    uv run python sections/engineering-workforce/pipeline/fetch.py --status   # just print a status table

Only sources with ``reachable: here`` are downloaded. Everything else is listed
with its blocking reason and the task that owns its manual retrieval, so the
framework runs end-to-end today and a human/agent can fill the gaps later.

Downloads are logged (URL, bytes, sha256, timestamp) to
``data_acquisition/fetch_log.csv`` so raw pulls are reproducible even though the
raw files themselves are git-ignored.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
import registry  # noqa: E402

LOG = registry._section_dir() / "data_acquisition" / "fetch_log.csv"
CA = os.environ.get("REQUESTS_CA_BUNDLE") or os.environ.get("SSL_CERT_FILE") or True


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _download(url: str, dest: Path) -> tuple[bool, str]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        resp = requests.get(
            url, timeout=90, verify=CA, headers={"User-Agent": "quasioptimal-research"}
        )
    except requests.RequestException as exc:  # network/proxy/TLS
        return False, f"error: {exc}"
    if resp.status_code != 200:
        return False, f"http {resp.status_code}"
    dest.write_bytes(resp.content)
    return True, f"ok {len(resp.content)} bytes sha256={_sha256(dest)[:12]}"


def _log_row(source_id: str, url: str, dest: Path, result: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    exists = LOG.exists()
    with LOG.open("a", newline="") as fh:
        w = csv.writer(fh)
        if not exists:
            w.writerow(["source_id", "url", "raw_file", "bytes", "result"])
        size = dest.stat().st_size if dest.exists() else 0
        w.writerow([source_id, url, dest.name, size, result])


def status_table() -> None:
    rows = sorted(registry.load_sources(), key=lambda s: (s.priority, s.role, s.id))
    print(f"{'PRIO':<4} {'REACHABLE':<14} {'STATUS':<9} {'ROLE':<20} {'ID':<22} TASK")
    print("-" * 92)
    for s in rows:
        print(f"{s.priority:<4} {s.reachable:<14} {s.status:<9} {s.role:<20} {s.id:<22} {s.task}")
    reachable = [s for s in rows if s.reachable == "here"]
    blocked = [s for s in rows if s.reachable == "blocked_egress"]
    print("-" * 92)
    print(f"{len(reachable)} reachable here, {len(blocked)} blocked by egress policy.")


def fetch_reachable() -> int:
    reachable = [s for s in registry.by_reachability("here") if s.raw]
    if not reachable:
        print("No reachable sources with a raw target.")
        return 0
    failures = 0
    for s in reachable:
        dest = s.raw_file
        ok, msg = _download(s.url, dest)
        _log_row(s.id, s.url, dest, msg)
        print(f"[{'OK ' if ok else 'FAIL'}] {s.id:<22} -> {dest.name}: {msg}")
        failures += 0 if ok else 1
    blocked = registry.by_reachability("blocked_egress")
    if blocked:
        print(f"\n{len(blocked)} source(s) blocked by egress policy — see TASKS.md:")
        for s in sorted(blocked, key=lambda x: (x.priority, x.id)):
            print(f"  - [{s.task}] {s.id}: {s.url}")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--status", action="store_true", help="print status table and exit")
    args = ap.parse_args()
    if args.status:
        status_table()
        return 0
    return fetch_reachable()


if __name__ == "__main__":
    raise SystemExit(main())
