from django.urls import path
from .views import ValidateTokenView, UpdateProfileView, GetProfileView

urlpatterns = [
    path('validate-token/', ValidateTokenView.as_view(), name='validate-teacher-token'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-teacher-profile'),
    path('get-profile/', GetProfileView.as_view(), name='get-teacher-profile'),
    
]