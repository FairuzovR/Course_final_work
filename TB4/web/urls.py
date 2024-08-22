from django.urls import path

from .views import home_view, me_view

urlpatterns = [
    path('', home_view, name='home'),
    path('me/', me_view, name='me'),
]
