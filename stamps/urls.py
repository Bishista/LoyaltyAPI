from django.urls import path
from .views import add_stamp, check_stamps

urlpatterns = [
    path('add_stamp/<int:user_id>/', add_stamp, name='add_stamp'),
    path('check_stamps/<int:user_id>/', check_stamps, name='check_stamps'),
]
