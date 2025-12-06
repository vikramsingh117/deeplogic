from flask import Flask, request, jsonify
from .db import db
from .models import Task

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.post("/tasks")
    def create_task():
        data = request.json
        task = Task(
            title=data["title"],
            status=data["status"],
            lead_id=data["lead_id"],
            notes=data.get("notes")
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

    @app.patch("/tasks/<int:id>")
    def update_task(id):
        task = Task.query.get(id)
        if not task:
            return {"error": "Not found"}, 404

        data = request.json
        for k, v in data.items():
            setattr(task, k, v)

        db.session.commit()
        return jsonify(task.to_dict())

    @app.get("/tasks")
    def all_tasks():
        tasks = Task.query.all()
        return jsonify([t.to_dict() for t in tasks])

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5001, debug=True)
