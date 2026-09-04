#!/usr/bin/env python3
"""Build the immutable, self-describing site artifact consumed by Githook."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import pathlib
import tarfile


def build_bundle(public: pathlib.Path, output: pathlib.Path, repository: str, run_id: int, sha: str, epoch: int) -> pathlib.Path:
    if len(sha) != 40 or any(c not in "0123456789abcdefABCDEF" for c in sha):
        raise ValueError("sha must be a full hexadecimal Git commit")
    if not public.is_dir():
        raise ValueError("public directory does not exist")
    output.mkdir(parents=True, exist_ok=True)
    archive_name = f"gnailuy.com-{sha.lower()}.tar.gz"
    archive_path = output / archive_name
    entries = sorted(public.rglob("*"), key=lambda p: p.relative_to(public).as_posix())
    if not entries:
        raise ValueError("public directory is empty")
    for entry in entries:
        if entry.is_symlink() or not (entry.is_file() or entry.is_dir()):
            raise ValueError(f"unsafe public entry: {entry}")
    with archive_path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=epoch) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                for entry in entries:
                    name = entry.relative_to(public).as_posix()
                    info = archive.gettarinfo(str(entry), arcname=name)
                    info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    info.mtime = epoch
                    if info.isfile():
                        with entry.open("rb") as source:
                            archive.addfile(info, source)
                    else:
                        archive.addfile(info)
    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    (output / f"{archive_name}.sha256").write_text(f"{digest}  {archive_name}\n", encoding="utf-8")
    manifest = {"archive": archive_name, "head_sha": sha.lower(), "repository": repository, "workflow_run_id": run_id}
    (output / "manifest.json").write_text(json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    return archive_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--run-id", type=int, required=True)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--epoch", type=int, default=int(os.environ.get("SOURCE_DATE_EPOCH", "0")))
    args = parser.parse_args()
    build_bundle(args.public, args.output, args.repository, args.run_id, args.sha, args.epoch)


if __name__ == "__main__":
    main()
