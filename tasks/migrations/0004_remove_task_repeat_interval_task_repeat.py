# Generated by Django 5.1.5 on 2025-04-19 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_emailtask_sent_task_repeat_interval'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='repeat_interval',
        ),
        migrations.AddField(
            model_name='task',
            name='repeat',
            field=models.CharField(choices=[('minutely', 'Minutely'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('none', 'None')], default='none', max_length=10),
        ),
    ]
