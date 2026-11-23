#!/usr/bin/env python3
"""news-image-20261123 entry runner (stdlib only).

Copies the pre-rendered front page (entry.png) to /output/entry.png
and verifies its SHA-256 so the submitted artifact is exactly the
image reviewed in this repo.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "8aa0e02991f13c05508962eaa0904838ccd94fd1d088a361ae18be8e4bc38f0e"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    digest = sha256_file(src)
    if digest != EXPECTED_SHA256:
        print("entry.png sha256 mismatch: got %s, want %s"
              % (digest, EXPECTED_SHA256), file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    if sha256_file(dst) != EXPECTED_SHA256:
        print("output verification failed", file=sys.stderr)
        return 1
    print("entry.png -> %s (%s)" % (dst, EXPECTED_SHA256))
    return 0


if __name__ == "__main__":
    sys.exit(main())
