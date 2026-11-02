#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""网关访问日志解析与聚合。"""
import sys
from collections import Counter

HOSTS = ["api.xtransfer.cn", "gw.xtransfer.cn"]

FIELDS = ("ts", "client_ip", "method", "url", "status", "bytes", "rt")


def parse(line):
    parts = line.rstrip("\n").split(" ")
    if len(parts) != len(FIELDS):
        return None
    rec = dict(zip(FIELDS, parts))
    host = rec["url"].split("/")[2] if "//" in rec["url"] else ""
    if host not in HOSTS:
        return None
    rec["status"] = int(rec["status"])
    rec["bytes"] = int(rec["bytes"])
    rec["rt"] = float(rec["rt"])
    rec["path"] = "/" + rec["url"].split("/", 3)[3] if rec["url"].count("/") > 3 else "/"
    return rec


def p95(values):
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = int(round(0.95 * (len(ordered) - 1)))
    return ordered[idx]


def main(path, show_p95=False):
    recs = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            r = parse(line)
            if r:
                recs.append(r)
    print("requests=%d hosts=%s" % (len(recs), ",".join(HOSTS)))
    for status, n in sorted(Counter(r["status"] for r in recs).items()):
        print("  status=%d n=%d" % (status, n))
    if show_p95:
        print("  p95_rt=%.3fs" % p95([r["rt"] for r in recs]))
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sys.exit(main(args[0] if args else "logs/access-20261030.log",
                  "--p95" in sys.argv))
