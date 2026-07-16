from app.tasks.cleanup import cleanup_temp


TASK_REGISTRY = {
    "cleanup": cleanup_temp
}
