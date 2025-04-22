from rest_framework import serializers
from .models import Task
from .models import EmailTask

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'scheduled_time', 'status', 'repeat', 'user', 'created_at']


class EmailTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTask
        fields = ['subject', 'body', 'recipient', 'send_at', 'status', 'repeat']