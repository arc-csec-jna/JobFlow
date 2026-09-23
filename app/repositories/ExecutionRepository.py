from app.models.execution import Execution


class ExecutionRepository: 
    def __init__(self, db):
        self.db = db

    def create_execution(self, execution: Execution):
        self.db.add(execution)
        self.db.commit()
        self.db.refresh(execution)
        return execution
    
    def get_execution_by_id(self, execution_id):
        return self.db.query(Execution).filter(Execution.id == execution_id).first()
    
    def update_execution(self, execution_id, execution_data):
        execution = self.get_execution_by_id(execution_id)
        if not execution:
            return None
        for key, value in execution_data.items():
            setattr(execution, key, value)
        self.db.commit()
        self.db.refresh(execution)
        return execution
    
    def delete_execution(self, execution_id):
        execution = self.get_execution_by_id(execution_id)
        if not execution:
            return False
        self.db.delete(execution)
        self.db.commit()
        return True

    def get_executions_by_job_id(self, job_id):
        return self.db.query(Execution).filter(Execution.job_id == job_id).all()