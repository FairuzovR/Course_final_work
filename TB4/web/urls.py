from django.urls import path

from .views import home_view, me_view, get_codes_list, get_refs_list

urlpatterns = [
    path('', home_view, name='home'),
    path('me/', me_view, name='me'),
    path('get-codes/', get_codes_list, name='get-codes'),
    path('get-refs/', get_refs_list, name='get-refs'),
]
