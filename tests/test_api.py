import os
import tempfile
import json
import sqlite3
import pytest

from taskapp.app import create_app
from taskapp.db_init import SCHEMA


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / 'test.db'
    # create DB
    conn = sqlite3.connect(db_file)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()

    app = create_app()
    # set g.db_path via before_request hook
    @app.before_request
    def _set_db_path():
        from flask import g
        g.db_path = str(db_file)

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_create_and_get_task(client):
    payload = {"title": "Test Task", "description": "desc", "due_date": "2025-12-01", "status": "pending"}
    rv = client.post('/api/tasks', json=payload)
    assert rv.status_code == 201
    data = rv.get_json()
    assert 'id' in data
    task_id = data['id']

    rv2 = client.get(f'/api/tasks/{task_id}')
    assert rv2.status_code == 200
    t = rv2.get_json()
    assert t['title'] == payload['title']


def test_list_tasks(client):
    # ensure list endpoint works even if empty
    rv = client.get('/api/tasks')
    assert rv.status_code == 200
    assert isinstance(rv.get_json(), list)


def test_update_task(client):
    rv = client.post('/api/tasks', json={"title": "Old"})
    tid = rv.get_json()['id']
    rv2 = client.put(f'/api/tasks/{tid}', json={"title": "New", "status": "done"})
    assert rv2.status_code == 200
    t = client.get(f'/api/tasks/{tid}').get_json()
    assert t['title'] == 'New' and t['status'] == 'done'


def test_delete_task(client):
    rv = client.post('/api/tasks', json={"title": "ToDelete"})
    tid = rv.get_json()['id']
    rv2 = client.delete(f'/api/tasks/{tid}')
    assert rv2.status_code == 200
    rv3 = client.get(f'/api/tasks/{tid}')
    assert rv3.status_code == 404
