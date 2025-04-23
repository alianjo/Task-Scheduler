from celery import shared_task

@shared_task
def run_scheduled_task():
    print("Scheduled task is running!")