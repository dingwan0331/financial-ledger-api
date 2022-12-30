from django.urls import path

from apps.transaction.views import TransactionsView, TransactionView

urlpatterns = [
    path('', TransactionsView.as_view()),
    path('/<int:transaction_id>', TransactionView.as_view())
]
