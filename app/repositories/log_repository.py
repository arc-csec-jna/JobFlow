from app.models.logs import Log

class LogRepository:
    def __init__(self, db):
        self.db = db

    def create_log(self, log: Log):
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_logs_by_execution_id(self, execution_id):
        return self.db.query(Log).filter(Log.execution_id == execution_id).all()