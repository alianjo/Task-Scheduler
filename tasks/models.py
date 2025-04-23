from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    REPEAT_CHOICES = [
        ('minutely', 'Minutely'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('none', 'None'),
    ]

    # فیلدهای اصلی
    repeat = models.CharField(
        max_length=10,
        choices=REPEAT_CHOICES,
        default='none'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    scheduled_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"


class EmailTask(models.Model):
    REPEAT_CHOICES = (
        ('none', 'No Repeat'),
        ('minutely', 'Every Minute'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    )
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent = models.BooleanField(default=False)
    recipient = models.EmailField('Email recipient')
    status = models.CharField(max_length=20, default='Pending', choices=[('Pending', 'Pending'), ('Sent', 'Sent'), ('Failed', 'Failed')])
    send_at = models.DateTimeField()  
    repeat = models.CharField(max_length=10, choices=REPEAT_CHOICES, default='none')
    
    def __str__(self):
        return f"Email to {self.recipient} - {self.status}"