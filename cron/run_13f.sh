#!/usr/bin/env bash
set -euo pipefail
cd /opt/13f-tracker
source .venv/bin/activate
set -a; source .env; set +a
13f-ingest --cik "${TRACKER_CIK}" --quarters "${TRACKER_QUARTERS:-4}" --output-dir data/raw --dashboard "output/13f_dashboard.xlsx"
