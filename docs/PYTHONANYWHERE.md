# Deploying on PythonAnywhere

PythonAnywhere runs your app with **WSGI**, not `python app.py`.

By default this project uses **SQLite** (`instance/student.db`). You do **not** need PostgreSQL on `localhost` or a MySQL database unless you choose to set `DATABASE_URL`.

---

## 1. Upload your code

- Use **Git** (recommended): open a Bash console, `git clone` your repo into `~/Student_Management` (or any folder under your home).
- Or upload a zip via **Files** and unpack it.

Replace `YOURUSERNAME` below with your PythonAnywhere username.

---

## 2. Virtual environment

In a **Bash** console:

```bash
cd ~/Student_Management
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Use the same Python version you select in the **Web** tab for your web app.

---

## 3. Database — SQLite (default, recommended on PA)

If you **do not** set `DATABASE_URL`, the app stores data in **`instance/student.db`** under your project folder. No MySQL or Postgres setup is required.

**Create tables once** (Bash console):

```bash
cd ~/Student_Management
source venv/bin/activate
export FLASK_APP=app.py
flask init-db
```

The `instance/` directory is created automatically when the app runs.

---

## 4. Database — optional: MySQL (PythonAnywhere free tier)

Only if you want MySQL instead of SQLite:

1. Open the **Databases** tab.
2. Set a MySQL password if you have not already.
3. **Create a database** (e.g. `YOURUSERNAME$student_registration`).

Build a SQLAlchemy URL for **PyMySQL** (in `requirements.txt`):

```text
mysql+pymysql://YOURUSERNAME:YOUR_MYSQL_PASSWORD@YOURUSERNAME.mysql.pythonanywhere-services.com/YOURUSERNAME$student_registration
```

- If your password has special characters (`@`, `#`, `%`, etc.), **URL-encode** them in the URI (e.g. `@` → `%40`).

Set `DATABASE_URL` in the **WSGI** file (before importing the app) or in the console before `flask init-db`:

```bash
export DATABASE_URL='mysql+pymysql://YOURUSERNAME:...@.../YOURUSERNAME$student_registration'
export FLASK_APP=app.py
flask init-db
```

---

## 5. Web app configuration

### Virtualenv path

**Web** tab → your site → **Virtualenv** field:

```text
/home/YOURUSERNAME/Student_Management/venv
```

### WSGI file

**Web** tab → **WSGI configuration file** → replace the body with something like:

```python
import sys
path = "/home/YOURUSERNAME/Student_Management"
if path not in sys.path:
    sys.path.append(path)

from wsgi import application
```

That loads `wsgi.py` in your project, which sets `application` to your Flask app.

### Static files

Still on the **Web** tab, **Static files** mapping:

| URL   | Directory (disk path)                                      |
|-------|--------------------------------------------------------------|
| `/static/` | `/home/YOURUSERNAME/Student_Management/static/` |

So `/static/uploads/photo.jpg` is served from your repo’s `static/` folder.

---

## 6. Security

Set a real secret for sessions and flash messages:

```bash
export SECRET_KEY="paste-a-long-random-string-here"
```

You can add in the **WSGI** file (before `from wsgi import application`):

```python
import os
os.environ.setdefault("SECRET_KEY", "your-long-random-secret")
os.environ.setdefault("DATABASE_URL", "mysql+pymysql://...")  # omit if using default SQLite
```

---

## 7. Reload

Click **Reload** on the Web tab. Open `https://YOURUSERNAME.pythonanywhere.com/`.

If you get a **500** error, check **Web → Log files** (`error.log`, `server.log`).

---

## 8. PostgreSQL or MySQL via `DATABASE_URL`

- **PostgreSQL** (local or hosted): set `DATABASE_URL` to `postgresql://...` (requires a running server; `psycopg2-binary` is in `requirements.txt`).
- **MySQL**: use `mysql+pymysql://...` as in section 4.

If `DATABASE_URL` is **not** set, the app uses **SQLite** only.

---

## 9. Checklist

| Step | Done |
|------|------|
| Code in `~/Student_Management` (or your path) | |
| `venv` + `pip install -r requirements.txt` | |
| (Optional) MySQL created and `DATABASE_URL` set — skip for default SQLite | |
| `flask init-db` run once | |
| Web: virtualenv path set | |
| Web: WSGI imports `application` from your project | |
| Web: `/static/` → project `static/` folder | |
| `SECRET_KEY` set | |
| Reload site | |

---

*Paths and MySQL hostnames come from your PythonAnywhere **Databases** tab; copy them exactly.*
