# Task Manager — APIView Style (matches your usual pattern)

Same task manager, rewritten to match how you normally structure Django
code:

- Model: `TextField` for almost everything, `AutoField` primary key,
  `Meta.db_table` set explicitly.
- Views: one `rest_framework.views.APIView` class per action, each
  `post()` just parses JSON and hands off to a plain
  `..._data_fun(data)` function that does the actual work and returns
  its own `JsonResponse` with `status` / `message` / `payload`
  (and `remarks` on errors) — same shape as your
  `get_duplicate_records_history_data_fun`.
- Every endpoint is called with `POST`, including "read" operations
  like listing tasks — matching how `GetDuplicateRecordsHistory` works.

## Endpoints

| URL                     | Body                                              | Purpose            |
|--------------------------|----------------------------------------------------|--------------------|
| `POST /api/get-task-list/` | `{ "status": "pending" }` (status optional)     | list/filter tasks  |
| `POST /api/create-task/`   | `{ "title": "...", "description": "...", "priority": "...", "status": "...", "due_date": "..." }` | create a task |
| `POST /api/update-task/`   | `{ "taskId": 3, "status": "completed" }` (any subset of fields) | update a task |
| `POST /api/delete-task/`   | `{ "taskId": 3 }`                                 | delete a task      |

Every response has the shape:

```json
{
  "status": "success" | "error",
  "message": "...",
  "payload": { ... }
}
```

## Setup

```bash
cd taskmanager
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Confirm `taskmanager/settings.py` `DATABASES` matches what you created
in pgAdmin, then:

```bash
python manage.py migrate
python manage.py runserver
```

Open **http://127.0.0.1:8000/** — always through Django, never through
Live Server / port 5500, or you'll hit CORS/preflight issues again.

## Note on due_date

`due_date` is stored as a `TextField`, exactly like `invoice_date` in
your `NonPOAndPOInvoiceDataDomestic` model — it's saved and returned as
whatever string the frontend sends, with no date-object conversion, so
there's nothing to break on `.isoformat()`.
