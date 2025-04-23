from rest_framework import generics, permissions, serializers
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer
from django.utils import timezone
from .models import EmailTask
from django.utils import timezone
from .tasks import send_task_email
from rest_framework import generics
from .models import EmailTask
from .serializers import EmailTaskSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from rest_framework.decorators import api_view
from tasks.tasks import fail_me

class CreateEmailTaskView(generics.CreateAPIView):
    queryset = EmailTask.objects.all()
    serializer_class = EmailTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        recipient_email = self.request.data.get('recipient')
        subject = self.request.data.get('subject')
        body = self.request.data.get('body')
        send_at = self.request.data.get('send_at')
        repeat = self.request.data.get('repeat', 'none')

        if not all([recipient_email, subject, body, send_at]):
            raise serializers.ValidationError({
                'error': 'recipient, subject, body, and send_at are required fields'
            })

        try:
            send_at_dt = datetime.fromisoformat(send_at.replace('Z', '+00:00'))
            if send_at_dt < timezone.now():
                raise serializers.ValidationError({
                    'send_at': 'Send time must be in the future'
                })

            email_task = EmailTask.objects.create(
                subject=subject,
                body=body,
                recipient=recipient_email,
                send_at=send_at,
                status='Pending',
                repeat=repeat
            )

            send_task_email.apply_async(
                args=[email_task.id],
                eta=email_task.send_at,
                retry=True,
                retry_policy={
                    'max_retries': 3,
                    'interval_start': 0,
                    'interval_step': 0.2,
                    'interval_max': 0.2,
                }
            )

            return email_task

        except ValueError as e:
            raise serializers.ValidationError({
                'send_at': 'Invalid datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
            })

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def trigger_failure(request):
    fail_me.delay()
    return Response({"message": "Failing task has been triggered."})