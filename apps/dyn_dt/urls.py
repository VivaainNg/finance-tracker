from django.urls import path
from apps.dyn_dt import views

urlpatterns = [
    path("dynamic-dt/", views.index, name="dynamic_dt"),
    path("create-filter/<str:model_name>/", views.create_filter, name="create_filter"),
    path(
        "create-page-items/<str:model_name>/",
        views.create_page_items,
        name="create_page_items",
    ),
    path(
        "create-hide-show-items/<str:model_name>/",
        views.create_hide_show_filter,
        name="create_hide_show_filter",
    ),
    path(
        "delete-filter/<str:model_name>/<int:id>/",
        views.delete_filter,
        name="delete_filter",
    ),
    path("create/<str:model_path>/", views.create, name="create"),
    path("delete/<str:model_path>/<int:id>/", views.delete, name="delete"),
    path("update/<str:model_path>/<int:id>/", views.update, name="update"),
    path("transactions/create/", views.transaction_modal, name="transactions-create"),
    path(
        "transactions/<int:pk>/edit/", views.transaction_modal, name="transactions-edit"
    ),
    path(
        "transactions/<int:pk>/confirm-delete/",
        views.transaction_confirm_delete,
        name="transactions-confirm-delete",
    ),
    path(
        "transactions/<int:pk>/delete/",
        views.transaction_delete,
        name="transactions-delete",
    ),
    path(
        "transactions/exports/<str:format>/",
        views.TransactionsExportView.as_view(),
        name="transactions-export",
    ),
    path(
        "export-csv/<str:model_path>/", views.ExportCSVView.as_view(), name="export_csv"
    ),
    path(
        "dynamic-dt/<str:model_path>/",
        views.display_datatables,
        name="display-datatables",
    ),
]
