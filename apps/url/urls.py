from django.urls import path

from apps.url.views import TransactionSignedUrlView

urlpatterns = [
    path('/transactions/<int:transaction_id>', TransactionSignedUrlView.as_view()),
]
