from app.tasks.cleanup import cleanup_temp
from app.tasks.db_backup import db_backup
from app.tasks.email import email_notification_task
from app.tasks.failing_task import failing_task
from app.tasks.heatlh_check import health_check_task
from app.tasks.report_generation import report_generation_task

TASK_REGISTRY = {
    "cleanup": cleanup_temp,
    "database_backup": db_backup,
    "email_notification": email_notification_task,
    "report_generation": report_generation_task,
    "health_check": health_check_task,
    "fail": failing_task
}
