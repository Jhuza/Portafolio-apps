"""Catalog of the owner's confirmed Streamlit deployments."""
import json
from pathlib import Path

TARGET_COUNT = 18
PROJECTS = json.loads(Path(__file__).with_name("projects.json").read_text(encoding="utf-8"))
