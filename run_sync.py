from lead.sheets_client import SheetsClient
from sync.task_client import TaskClient
from sync.sync_logic import SyncManager
import time
manager = SyncManager(SheetsClient(), TaskClient())
interval=5
while True:
    print("Running lead → task sync...")
    manager.sync_leads_to_tasks()

    print("Running task → lead sync...")
    manager.sync_tasks_to_leads()


    print("Sync complete.")
    time.sleep(interval)
