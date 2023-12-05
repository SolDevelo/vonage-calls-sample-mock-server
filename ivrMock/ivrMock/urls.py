# myproject/urls.py
from django.urls import path, include

urlpatterns = [
    path('v1/', include('app.urls')),
]
