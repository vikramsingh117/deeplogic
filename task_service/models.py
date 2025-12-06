from datetime import datetime
from .db import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    status = db.Column(db.String(50))
    lead_id = db.Column(db.String(255))
    notes = db.Column(db.String(500))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "lead_id": self.lead_id,
            "notes": self.notes,
            "updated_at": self.updated_at.isoformat()
        }
