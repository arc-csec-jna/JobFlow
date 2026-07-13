from app.models.job import Job

class JobRepository:
    def __init__(self, db):
        self.db = db
        
    def get_jobs(self):
        return self.db.query(Job).all()
    
    def get_job_by_id(self, job_id):
        return self.db.query(Job).filter(Job.id == job_id).first()

    def create_job(self, job):
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def update_job(self, job_id, job_data):
        job = self.get_job_by_id(job_id)
        if job:
            for key, value in job_data.items():
                setattr(job, key, value)
            self.db.commit()
            return job
        return None

    def delete_job(self, job_id):
        job = self.get_job_by_id(job_id)
        if job:
            self.db.delete(job)
            self.db.commit()
            return True
        return False

    def update_job_status(self, job_id, status):
            job = self.get_job_by_id(job_id)
            if job:
                job.status = status
                self.db.commit()
                return job
            return None
        