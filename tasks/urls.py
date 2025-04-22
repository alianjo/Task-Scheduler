from django.urls import path
from .views import CreateEmailTaskView, TaskDetailView
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CreateEmailTaskView
from .views import trigger_failure


urlpatterns = [
    path('', CreateEmailTaskView.as_view(), name='task-list-create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-email/', CreateEmailTaskView.as_view(), name='create-email-task'),
    path('trigger-fail/', trigger_failure),
]
