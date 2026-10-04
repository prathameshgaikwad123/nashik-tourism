"""Filesystem and URL constants shared by every generator."""
import os

TOOLS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
REPO = os.path.normpath(os.path.join(TOOLS, ".."))
ROOT = os.path.join(REPO, "nashiktourism")      # the deployable web root
DATA = os.path.join(REPO, "data")               # editorial source of truth (not deployed)
REPORTS = os.path.join(REPO, "reports")         # generated, not deployed
SITE = "https://nashiktourism.com"
