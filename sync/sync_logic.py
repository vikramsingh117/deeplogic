from utils.logger import logger
from .status_map import lead_to_task, task_to_lead

class SyncManager:
    def __init__(self, sheets, tasks):
        self.sheets = sheets
        self.tasks = tasks

    def sync_leads_to_tasks(self):
        leads = self.sheets.get_all_leads()

        for i, lead in enumerate(leads, start=2):  
            lead_id = lead["id"]
            task_id = lead.get("task_id")

            if not task_id:  
                logger.info(f"Creating task for lead {lead_id}")
                task = self.tasks.create_task_from_lead(lead, status=lead_to_task.get(lead["status"], "TODO"))

                self.sheets.update_cell(i, "task_id", str(task["id"]))
            else:
                logger.info(f"Updating task {task_id} for lead {lead_id}")
                self.tasks.update_task(task_id, lead)

    def sync_tasks_to_leads(self):
        tasks = self.tasks.get_all_tasks()

        for task in tasks:
            lead_status = task_to_lead.get(task["status"])
            if not lead_status:
                continue

            row = self.sheets.find_row_by_lead_id(task["lead_id"])
            if not row:
                continue

            self.sheets.update_cell(row, "status", lead_status)
            logger.info(f"Updated lead {task['lead_id']} → {lead_status}")
