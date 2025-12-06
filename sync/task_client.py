import requests

BASE = "http://localhost:5001"

class TaskClient:
    def create_task_from_lead(self, lead, status="TODO"):
        payload = {
            "title": f"Follow up: {lead['name']}",
            "status": status,
            "lead_id": lead["id"],
            "notes": f"Auto-created from Sheets"
        }

        res = requests.post(f"{BASE}/tasks", json=payload)
        res.raise_for_status()
        return res.json()

    def update_task(self, task_id, lead):
        payload = {
            "title": f"Follow up: {lead['name']}",
            "status": lead["status"],
            "notes": f"Updated based on lead status"
        }
        res = requests.patch(f"{BASE}/tasks/{task_id}", json=payload)
        res.raise_for_status()
        return res.json()

    def get_all_tasks(self):
        res = requests.get(f"{BASE}/tasks")
        return res.json()
