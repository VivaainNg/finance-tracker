from django.urls import path

from apps.pages.views import (
    DashboardView,
    TransactionFormView,
    TransactionConfirmDeleteView,
    TransactionDeleteView,
    TransactionsExportView,
)

urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
    path(
        "transactions/create/",
        TransactionFormView.as_view(),
        name="transactions-create",
    ),
    path(
        "transactions/<int:pk>/update/",
        TransactionFormView.as_view(),
        name="transactions-update",
    ),
    path(
        "transactions/<int:pk>/confirm-delete/",
        TransactionConfirmDeleteView.as_view(),
        name="transactions-confirm-delete",
    ),
    path(
        "transactions/<int:pk>/delete/",
        TransactionDeleteView.as_view(),
        name="transactions-delete",
    ),
    path(
        "transactions/exports/<str:format>/",
        TransactionsExportView.as_view(),
        name="transactions-export",
    ),
]
