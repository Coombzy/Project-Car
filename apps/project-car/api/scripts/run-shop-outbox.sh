#!/bin/sh
# LaunchAgent com.projectcar.shop-outbox. Runs the sender from the shop API tree.
set -eu
cd "$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
exec python -m app.outbox
