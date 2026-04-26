"""
WSGI entry point for PythonAnywhere (and other WSGI servers).

Web tab → WSGI configuration file → point the "import" at this file
and expose `application` (PythonAnywhere expects that name).
"""
import os
import sys

_project_dir = os.path.dirname(os.path.abspath(__file__))
if _project_dir not in sys.path:
    sys.path.insert(0, _project_dir)

# Set DATABASE_URL / SECRET_KEY here if you prefer not to use the PA env UI:
# os.environ.setdefault("DATABASE_URL", "mysql+pymysql://user:pass@host/dbname")
# os.environ.setdefault("SECRET_KEY", "long-random-string")

from app import app as application
