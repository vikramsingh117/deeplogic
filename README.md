readme, only formatted by ai
---

# Lead–Task Sync Automation

A small automation system that keeps a Google Sheets “Lead Tracker” and a Flask-based “Task Tracker” in sync. The goal was to show how two different tools can stay consistent through a simple bi-directional sync flow.

The automation reads leads from Google Sheets, creates or updates tasks in a local API, and also pushes task updates back to the sheet.

---

## Overview

This project connects:

* Google Sheets as a lightweight lead tracker
* Flask + SQLite + SQLAlchemy as a small task API
* A Sync Manager that:

  * creates tasks when new leads appear
  * updates tasks when lead statuses change
  * updates leads when task statuses change

It works as a minimal workflow bridge between two systems.

---

## Tools Integrated

* Google Sheets API (service account)
* Flask
* SQLAlchemy
* SQLite
* Python requests
* Custom SyncManager

---

## Architecture & Flow

### High-Level Flow

```
Google Sheets (Leads)
        ↓ read
 Sync Manager
        ↑ write
Task Tracker API (Flask + SQLite)
```

Leads written in Google Sheets flow into the Task API.
Task status changes flow back into the sheet.

### ASCII Diagram

```
             +------------------------+
             |     Google Sheets      |
             |   (Lead Management)    |
             +-----------+------------+
                         |
                         | read/write via SheetsClient
                         v
                +----------------+
                | Sync Manager   |
                |  - sync_leads_to_tasks
                |  - sync_tasks_to_leads
                +----------------+
                         ^
                         |
                         | REST (POST/PATCH/GET)
             +-----------+------------+
             |     Task Tracker       |
             | Flask API + SQLite DB  |
             +------------------------+
```

---

## Setup Instructions

### 1. Google Sheets Setup

* Create a Google Cloud Project
* Enable the Google Sheets API
* Create a service account
* Download the JSON key
* Share the sheet with the service-account email

This gives programmatic read/write access.

### 2. API Keys / Credentials

Place your key file:

```
service_account.json
```

Optional environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="service_account.json"
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

`requirements.txt`:

```
flask
sqlalchemy
google-api-python-client
google-auth
requests
```

### 4. Running the Task API

```
python app.py
```

Endpoints:

* POST /tasks
* PATCH /tasks/<id>
* GET /tasks

`tasks.db` (SQLite) is created automatically.

---

## Usage

### 1. Start the Task API

```
python app.py
```

Available at:

```
http://localhost:5001
```

### 2. Add or Modify Leads in Google Sheets

Example:

| id | name   | status | task_id |
| -- | ------ | ------ | ------- |
| 12 | Vikram | NEW    |         |

* If `task_id` is empty → a task is created
* If the status changes → the task is updated

### 3. Run the Sync

```python
sync_manager.sync_leads_to_tasks()
sync_manager.sync_tasks_to_leads()
```

This creates missing tasks, updates existing tasks, and pushes task-derived statuses back into Sheets.

### 4. View Tasks

```
GET /tasks
```

Example response:

```json
[
  {
    "id": 1,
    "title": "Follow up: Vikram",
    "status": "TODO",
    "lead_id": "12",
    "notes": "Auto-created from Sheets"
  }
]
```

---

## Assumptions & Limitations

* Only one direction is synced at a time
* Sheet columns must remain consistent (`id`, `status`, `task_id`)
* No retry logic for API rate-limits
* Static status mapping (`status_map.py`)
* No authentication on the Task API

The project is intentionally minimal.

---

## Error Handling & Idempotency

### Error Handling

* `raise_for_status()` is used on API calls
* Missing or inconsistent sheet rows are skipped
* Only valid mappings are applied

### Idempotency

* Tasks are not duplicated (created only when `task_id` is empty)
* Running sync multiple times produces the same result
* Updates overwrite existing values cleanly

---
