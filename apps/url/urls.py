from django.urls import path

from apps.url.views import TransactionSignedUrlView, TransactionRedirectView

urlpatterns = [
    path('/transactions/<int:transaction_id>', TransactionSignedUrlView.as_view()),
    path('/transactions/<uuid:transaction_uuid>', TransactionRedirectView.as_view()),
]
