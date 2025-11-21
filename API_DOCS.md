# Pelocal Task API Documentation

Base URL: /api/tasks

Endpoints:

- GET /api/tasks
  - Returns JSON array of tasks.

- POST /api/tasks
  - Create a task. JSON body: {"title": "...", "description": "...", "due_date": "YYYY-MM-DD", "status": "pending|done"}
  - Returns 201 with created task id and fields.

- GET /api/tasks/<id>
  - Get a single task by id.

- PUT /api/tasks/<id>
  - Update fields. JSON body may contain any of title, description, due_date, status.

- DELETE /api/tasks/<id>
  - Delete the task.

All endpoints accept and return JSON. No authentication for this small demo.
