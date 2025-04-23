from celery import shared_task
from .models import Task, EmailTask
from celery.utils.log import get_task_logger
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from celery.signals import task_failure
from datetime import timedelta

logger = get_task_logger(__name__)

@shared_task
def run_scheduled_task(task_id):
    try:
        task = Task.objects.get(id=task_id)
        
        print(f"Running task: {task.title}")
        
        task.status = 'completed'
        task.save()
        print("Task completed.")

        if task.user and task.user.email:
            logger.info(f"Creating email task for user: {task.user.email}")
            email_task = EmailTask.objects.create(
                subject=f"Task {task.title} Completed",
                body=f"The task '{task.title}' has been completed successfully.",
                recipient=task.user.email,
                send_at=timezone.now() + timedelta(minutes=1)
            )
            send_task_email.apply_async(args=[email_task.id], eta=email_task.send_at)
        else:
            logger.warning(f"No recipient email found for task ID {task.id}. Skipping email task creation.")

        if task.repeat and task.repeat != 'none':
            if task.repeat_interval == 'minutely':
                next_time = task.scheduled_time + timedelta(minutes=5)
            elif task.repeat_interval == 'daily':
                next_time = task.scheduled_time + timedelta(days=1)
            elif task.repeat_interval == 'weekly':
                next_time = task.scheduled_time + timedelta(weeks=1)
            else:
                next_time = None

            if next_time:
                new_task = Task.objects.create(
                    user=task.user,
                    title=task.title,
                    description=task.description,
                    scheduled_time=next_time,
                    repeat=task.repeat,
                    status='pending'
                )
                print(f"Created repeated task for: {next_time}")
                run_scheduled_task.apply_async(args=[new_task.id], eta=new_task.scheduled_time)

    except Task.DoesNotExist:
        print(f"Task with id {task_id} does not exist.")


@shared_task
def send_task_email(email_task_id):
    try:
        email_task = EmailTask.objects.get(id=email_task_id)

        logger.info(f"Email task found: {email_task.id}")
        logger.info(f"Recipient: {email_task.recipient}")
        logger.info(f"Subject: {email_task.subject}")
        logger.info(f"Repeat value: {email_task.repeat}")

        if not email_task.recipient:
            logger.warning(f"EmailTask {email_task.id} has no recipient. Skipping sending.")
            return

        # Send the email
        send_mail(
            email_task.subject,
            email_task.body,
            'Email sender',
            [email_task.recipient],
            fail_silently=False,
        )
        logger.info(f"Email sent to {email_task.recipient}")

        # Update status
        email_task.status = 'Sent'
        email_task.save()

        # Handle repeat logic
        if email_task.repeat != 'none':
            next_time = email_task.send_at
            if email_task.repeat == 'minutely':
                next_time += timedelta(minutes=1)
            elif email_task.repeat == 'daily':
                next_time += timedelta(days=1)
            elif email_task.repeat == 'weekly':
                next_time += timedelta(weeks=1)

            logger.info(f"Scheduling next email for {next_time}")

            next_email = EmailTask.objects.create(
                subject=email_task.subject,
                body=email_task.body,
                recipient=email_task.recipient,
                send_at=next_time,
                status='Pending',
                repeat=email_task.repeat
            )
            logger.info(f"Next email task created: {next_email.id}")

            send_task_email.apply_async(
                args=[next_email.id],
                eta=next_time,
                retry=True,
                retry_policy={
                    'max_retries': 3,
                    'interval_start': 0,
                    'interval_step': 0.2,
                    'interval_max': 0.2,
                }
            )

    except EmailTask.DoesNotExist:
        print(f"EmailTask with id {email_task_id} does not exist.")


@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, args=None, kwargs=None, traceback=None, einfo=None, **other):
    subject = f"Task Failure Alert - ID: {task_id}"
    message = f"""
    A task has failed!

    Task ID: {task_id}
    Exception: {exception}
    Args: {args}
    Kwargs: {kwargs}
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ["Email recipient"],
        fail_silently=False
    )


@shared_task
def fail_me():
    raise ValueError("این تسک عمداً fail شد!")
