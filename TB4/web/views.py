from django.shortcuts import render
from .decorators import jwt_required


def home_view(request):
    return render(request, 'base.html')


@jwt_required
def me_view(request):
    return render(request, 'me.html')
