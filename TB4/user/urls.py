from django.urls import path

from .views import SendCodeView

urlpatterns = [
    path('auth/', SendCodeView.as_view(), name='send_code'),
]
