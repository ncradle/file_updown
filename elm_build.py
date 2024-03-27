import os
import shutil
import subprocess
from pathlib import Path

CWD = Path(__file__).parent
FRONT = "frontend"
FRONT_PATH = CWD / FRONT
INDEX_HTML = "index.html"
INDEX_HTML_PATH = FRONT_PATH / INDEX_HTML
BACKEND = CWD / "backend"
TEMPLATES = BACKEND / "templates"

try:
    os.chdir(CWD / FRONT_PATH)
    cp = subprocess.run(
        ["elm", "make", "src/Main.elm", "--optimize"], stdout=subprocess.PIPE
    )
    if cp.returncode != 0:
        print("Build error")
        exit(1)
    os.chdir(CWD)
    if not TEMPLATES.exists():
        os.mkdir(TEMPLATES)
    shutil.move(FRONT_PATH / INDEX_HTML, TEMPLATES / INDEX_HTML)
finally:
    if INDEX_HTML_PATH.exists():
        os.remove(INDEX_HTML_PATH)
