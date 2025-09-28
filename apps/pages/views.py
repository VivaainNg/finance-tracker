from decimal import Decimal
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin

from apps.pages.filters import TransactionDataTablesFilter
from apps.pages.models import Transaction
from django.db.models import Sum
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from urllib.parse import urlparse, parse_qs
from django.contrib import messages
import pandas as pd

from apps.pages.tables import TransactionDataTables
from .forms import TransactionForm
from django_tables2 import RequestConfig
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View


from django.views.generic import FormView, DetailView, DeleteView


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    View that renders results to dashboard page.

    Only authenticated/logged in user can view their own data.
    """

    template_name = "pages/dashboard.html"
    login_url = "auth_signin"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        total_income = Decimal("0")
        total_expenses = Decimal("0")

        if self.request.user.is_authenticated:
            queryset = (
                Transaction.objects.select_related("created_by", "category")
                .filter(created_by=self.request.user)
                .values("transaction_type")
                .annotate(total_amount=Sum("amount"))
                .order_by("transaction_type")
            )

            income_qs = queryset.filter(
                transaction_type=Transaction.TransactionType.INCOME
            )
            if income_qs.exists():
                total_income = income_qs.first().get("total_amount", Decimal("0"))

            expenses_qs = queryset.filter(
                transaction_type=Transaction.TransactionType.EXPENSES
            )
            if expenses_qs.exists():
                total_expenses = expenses_qs.first().get("total_amount", Decimal("0"))

        context["total_income"] = f"{total_income:.2f}"
        context["total_expenses"] = f"{total_expenses:.2f}"
        remaining_balance = total_income - total_expenses
        context["remaining_balance"] = f"{remaining_balance:.2f}"

        qs = Transaction.objects.select_related("created_by", "category").all()
        qs = (
            qs.filter(created_by=self.request.user)
            if self.request.user.is_authenticated
            else Transaction.objects.none()
        )

        # filter
        transaction_filter = TransactionDataTablesFilter(self.request.GET, queryset=qs)

        # hook queryset into table
        table = TransactionDataTables(transaction_filter.qs)

        # pagination + sorting
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)

        context.update(
            {
                "segment": "dashboard",
                "user": self.request.user,
                "table": table,
                "filter": transaction_filter,
            }
        )
        return context


class TransactionListView(LoginRequiredMixin, TemplateView):
    """
    Template views that display Transaction's datatables.
    """

    template_name = "pages/index.html"
    login_url = "auth_signin"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        qs = Transaction.objects.select_related("created_by", "category").all()
        qs = (
            qs.filter(created_by=self.request.user)
            if self.request.user.is_authenticated
            else Transaction.objects.none()
        )

        # filter
        transaction_filter = TransactionDataTablesFilter(self.request.GET, queryset=qs)

        # hook queryset into table
        table = TransactionDataTables(transaction_filter.qs)

        # pagination + sorting
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)

        context.update(
            {
                "segment": "dynamic_dt",
                "user": self.request.user,
                "table": table,
                "filter": transaction_filter,
            }
        )
        return context


class TransactionFormView(LoginRequiredMixin, FormView):
    """
    Handles both create & update of a Transaction inside a form.
    """

    form_class = TransactionForm
    template_name = "pages/transaction_modal_form.html"
    login_url = "auth_signin"

    def get_object(self):
        self.pk = self.kwargs.get("pk")
        if self.pk:
            return get_object_or_404(Transaction, pk=self.pk)
        return Transaction(created_by=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.request.user.is_authenticated:
            obj.created_by = self.request.user
        obj.save()

        response = HttpResponse()
        response["HX-Redirect"] = reverse("index")
        success_msg = (
            "Successfully updated Transaction!"
            if self.pk
            else "Successfully created new Transaction!"
        )

        messages.success(self.request, success_msg)
        return response


class TransactionConfirmDeleteView(LoginRequiredMixin, DetailView):
    """
    Renders HTMX modal popup before user confirms deletion.
    """

    model = Transaction
    template_name = "pages/transaction_delete_confirmation.html"
    context_object_name = "transaction"
    login_url = "auth_signin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transaction"] = self.object
        return context


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deletes a Transaction and returns HX-Redirect.
    """

    model = Transaction
    login_url = "auth_signin"
    success_url = reverse_lazy("index")

    def delete(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        response = HttpResponse()
        response["HX-Redirect"] = request.META.get("HTTP_REFERER")
        messages.success(request, "Successfully deleted the Transaction.")
        return response


class TransactionsExportView(LoginRequiredMixin, View):
    """
    Views to export Transactions from datatables.
    """

    login_url = "auth_signin"

    def extract_query_params(self, request: HttpRequest) -> dict[str, Any]:
        """
        Function to extract query params from HTTP_REFERER.

        I.e:

        Assuming HTTP_REFERER request URL is:
        ?remarks=a&payment_type=Card&transaction_type=Expenses&category=1

        Then extracted query params returned would be:

        {
            'remarks': ['a'],
            'payment_type': ['Card'],
            'transaction_type': ['Expenses'],
            'category': ['1'],
        }
        """

        referer = request.META.get("HTTP_REFERER", "")
        query_params = {}

        if referer:
            parsed_url = urlparse(referer)
            query_params = parse_qs(parsed_url.query)

        return query_params

    def get(self, request: HttpRequest, format: str):
        """
        Export based on format (either "csv" or "xlsx").

        Only authenticated/logged in user can export their own data.
        """

        query_params = self.extract_query_params(request)
        qs = (
            Transaction.objects.select_related(
                "category",
                "created_by",
            )
            .all()
            .filter(created_by=self.request.user)
            if self.request.user.is_authenticated
            else Transaction.objects.none()
        )
        qs = qs.values_list(
            "date_time",
            "amount",
            "payment_type",
            "category__name",
            "transaction_type",
            "remarks",
            "created_by__username",
        ).order_by("-date_time")

        if "remarks" in query_params and query_params["remarks"][0] != "":
            qs = qs.filter(remarks__icontains=query_params["remarks"][0])

        if "payment_type" in query_params and query_params["payment_type"][0] != "":
            qs = qs.filter(payment_type=query_params["payment_type"][0])

        if (
            "transaction_type" in query_params
            and query_params["transaction_type"][0] != ""
        ):
            qs = qs.filter(transaction_type=query_params["transaction_type"][0])

        if "category" in query_params and query_params["category"]:
            qs = qs.filter(category__pk__in=query_params["category"])

        df = pd.DataFrame(
            qs,
            columns=[
                "Datetime",
                "Amount(RM)",
                "Payment Type",
                "Category",
                "Transaction Type",
                "Remarks",
                "Created By",
            ],
        )
        if "Datetime" in df.columns and not df["Datetime"].isna().all():
            df["Datetime"] = df["Datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")

        if format == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="transactions.csv"'
            df.to_csv(path_or_buf=response, index=False)
            return response

        elif format == "xlsx":
            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = 'attachment; filename="transactions.xlsx"'
            with pd.ExcelWriter(response, engine="openpyxl") as writer:
                df.to_excel(writer, index=False)
            return response

        # fallback if unsupported format
        messages.warning(request, f"Format {format} not supported")
        return redirect(request.META.get("HTTP_REFERER", "dynamic_dt"))
