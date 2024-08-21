from django.urls import path

from .views import ActivateReferralCodeView, SendCodeView, UserRetrieveView

urlpatterns = [
    path('auth/', SendCodeView.as_view(), name='send_code'),
    path('me/', UserRetrieveView.as_view(), name='user-detail'),
    path(
      'set-referral/',
      ActivateReferralCodeView.as_view(),
      name='set-referral'
    )
]
