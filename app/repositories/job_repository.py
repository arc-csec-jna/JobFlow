from app.models.job import Job


class JobRepository:
    def __init__(self, db):
        self.db = db
        
    def get_jobs(self,user_id):
        return (
            self.db.query(Job)
            .filter(Job.user_id == user_id)
            .all()
        )
    
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
    #poll the database for jobs runnable
    def get_job_runnable(self,current_time):
        return (
            self.db.query(Job)
            .filter(Job.next_run_at <= current_time)
            .filter(Job.enabled == True)
            .order_by(
                Job.priority.desc(),
                Job.next_run_at.asc(),
                Job.id.asc()
                )
            .all()
            )
    
    def update_next_run_at(self,job_id,next_run_at):
        return self.update_job(job_id,{"next_run_at":next_run_at})

    def update_retry_count(self,job_id,retry_count):
        return self.update_job(job_id,{"retry_count":retry_count})