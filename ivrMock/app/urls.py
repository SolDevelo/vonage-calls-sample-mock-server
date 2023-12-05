# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.token_obtain, name='token_obtain'),
    path('calls/', views.outbound_calls, name='calls'),
]
