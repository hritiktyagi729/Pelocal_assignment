# Task Manager (Flask)

A small Flask application providing JSON REST APIs and HTML templates to manage tasks (create, read, update, delete) using raw SQLite (no ORM).

Requirements
- Python 3.8+

Setup
1. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize the database:

```bash
python -m taskapp.db_init
```

4. Run the app:

```bash
export FLASK_APP=taskapp.app:create_app
export FLASK_ENV=development
flask run
```

The app will be available at http://127.0.0.1:5000

Testing

Run tests with pytest:

```bash
pytest -q
```

API Documentation

See `API_DOCS.md` for endpoint descriptions and request/response examples.

Notes

- This project intentionally uses raw sqlite3 access (no ORM) and function-based routes (no generic viewsets).
