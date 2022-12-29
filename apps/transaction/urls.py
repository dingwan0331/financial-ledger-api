from django.urls import path

from apps.transaction.views import TransactionsView

urlpatterns = [
    path('', TransactionsView.as_view())
]
