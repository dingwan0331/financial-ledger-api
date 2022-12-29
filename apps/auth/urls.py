from django.urls import path

from .views import UserView, SignInView, TokenView

urlpatterns = [
    path('', UserView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/token', TokenView.as_view())
]
