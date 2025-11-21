import sqlite3
import logging
from datetime import datetime
from flask import Flask, g, jsonify, request, render_template, redirect, url_for

DEFAULT_DB_PATH = "./tasks.db"

def get_db(path=None):
    if path is None:
        path = getattr(g, 'db_path', None) or DEFAULT_DB_PATH
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(path)
        db.row_factory = sqlite3.Row
    return db

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.teardown_appcontext(close_db)

    # logging
    logging.basicConfig(level=logging.INFO)

    # API: create task
    @app.route('/api/tasks', methods=['POST'])
    def create_task():
        try:
            data = request.get_json(force=True)
            title = data.get('title')
            description = data.get('description')
            due_date = data.get('due_date')
            status = data.get('status', 'pending')

            if not title:
                return jsonify({'error': 'title is required'}), 400

            db = get_db()
            cur = db.cursor()
            cur.execute("""
                INSERT INTO tasks (title, description, due_date, status, created_at)
                VALUES (?, ?, ?, ?, ?)
            """,
            (title, description, due_date, status, datetime.utcnow().isoformat()))
            db.commit()
            task_id = cur.lastrowid
            return jsonify({'id': task_id, 'title': title, 'description': description, 'due_date': due_date, 'status': status}), 201
        except Exception as e:
            logging.exception("Failed to create task")
            return jsonify({'error': 'internal server error'}), 500

    # API: list tasks
    @app.route('/api/tasks', methods=['GET'])
    def list_tasks():
        try:
            db = get_db()
            cur = db.execute('SELECT id, title, description, due_date, status, created_at FROM tasks ORDER BY id DESC')
            rows = cur.fetchall()
            tasks = [dict(r) for r in rows]
            return jsonify(tasks)
        except Exception:
            logging.exception('Failed to list tasks')
            return jsonify({'error': 'internal server error'}), 500

    # API: retrieve single task
    @app.route('/api/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        try:
            db = get_db()
            cur = db.execute('SELECT id, title, description, due_date, status, created_at FROM tasks WHERE id = ?', (task_id,))
            row = cur.fetchone()
            if not row:
                return jsonify({'error': 'not found'}), 404
            return jsonify(dict(row))
        except Exception:
            logging.exception('Failed to get task')
            return jsonify({'error': 'internal server error'}), 500

    # API: update
    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        try:
            data = request.get_json(force=True)
            fields = {}
            for f in ('title', 'description', 'due_date', 'status'):
                if f in data:
                    fields[f] = data[f]
            if not fields:
                return jsonify({'error': 'no fields to update'}), 400
            set_clause = ', '.join([f"{k} = ?" for k in fields.keys()])
            params = list(fields.values()) + [task_id]
            db = get_db()
            cur = db.cursor()
            cur.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", params)
            if cur.rowcount == 0:
                return jsonify({'error': 'not found'}), 404
            db.commit()
            return jsonify({'id': task_id, **fields})
        except Exception:
            logging.exception('Failed to update task')
            return jsonify({'error': 'internal server error'}), 500

    # API: delete
    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        try:
            db = get_db()
            cur = db.cursor()
            cur.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            if cur.rowcount == 0:
                return jsonify({'error': 'not found'}), 404
            db.commit()
            return jsonify({'deleted': task_id})
        except Exception:
            logging.exception('Failed to delete task')
            return jsonify({'error': 'internal server error'}), 500

    # Templates: list and add
    @app.route('/')
    def index():
        # server-side render initial page; real data loaded via JS
        return render_template('index.html')

    @app.route('/add')
    def add():
        return render_template('add.html')

    return app

