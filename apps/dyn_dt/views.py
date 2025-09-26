from decimal import Decimal
from typing import Any
from urllib.parse import urlparse, parse_qs
from django.contrib import messages
import pandas as pd
from django.views.decorators.http import require_http_methods
from .forms import TransactionForm
from apps.dyn_dt.filters import TransactionDataTablesFilter
from apps.dyn_dt.tables import TransactionDataTables
from django_tables2 import RequestConfig
import django
from django.db.models.base import ModelBase
import json
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from django.db import models
import importlib

from apps.dyn_dt.models import ModelFilter, PageItems, HideShowFilter
from apps.dyn_dt.utils import user_filter
from apps.pages.models import Transaction
from apps.pages.utils import localtime_now

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin


class TransactionListView(SingleTableMixin, FilterView):
    """
    Views to display Transaction's datatables.
    """

    table_class = TransactionDataTables
    model = Transaction
    filterset_class = TransactionDataTablesFilter
    template_name = "dyn_dt/datatables_layout.html"


# @login_required
@require_http_methods(["GET", "POST"])
def transaction_modal(request: HttpRequest, pk: int | None = None):
    """
    Function to create an new Transaction model,
    or updates an existing ones via modal.
    """

    transaction = (
        get_object_or_404(Transaction, pk=pk)
        if pk
        else Transaction(created_by=request.user)
    )

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            obj = form.save(commit=False)
            if request.user.is_authenticated:
                obj.created_by = request.user
            obj.save()

            # redirects to same page that made this POST request
            response = HttpResponse()
            response["HX-Redirect"] = request.META.get("HTTP_REFERER")
            messages.success(request, "Success!")
            return response
    else:
        form = TransactionForm(instance=transaction)

    context = {"form": form}

    return render(request, "dyn_dt/transaction_modal_form.html", context=context)


# @login_required
@require_http_methods(["GET"])
def transaction_confirm_delete(request: HttpRequest, pk: int):
    """
    A get request to display modal popups right
    before user proceeds with deleting a Transaction.
    """

    transaction = get_object_or_404(Transaction, pk=pk)
    context = {"transaction": transaction}
    return render(
        request,
        "dyn_dt/transaction_delete_confirmation.html",
        context=context,
    )


# @login_required
@require_http_methods(["DELETE"])
def transaction_delete(request: HttpRequest, pk: int):
    """
    Function to delete an existing Transaction.
    """

    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()

    # redirects to same page that made this POST request
    response = HttpResponse()
    response["HX-Redirect"] = request.META.get("HTTP_REFERER")
    messages.success(request, "Successfully deleted the Transaction.")
    return response


class TransactionsExportView(View):
    """
    Views to export Transactions from datatables.
    """

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
        """

        query_params = self.extract_query_params(request)
        qs = (
            Transaction.objects.select_related(
                "category",
                "created_by",
            )
            .all()
            .values_list(
                "date_time",
                "amount",
                "payment_type",
                "category__name",
                "transaction_type",
                "remarks",
                "created_by__username",
            )
            .order_by("-date_time")
        )

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
        return HttpResponse("Format not supported", status=400)


def name_to_class(name: str) -> ModelBase | None:
    """
    Takes in name path, and returns the Class.
    """

    try:
        # Process the path
        cls_name = name.split(".")[-1]  # Extract Class Name
        cls_import = name.replace("." + cls_name, "")  # Extract Import path

        module = importlib.import_module(cls_import)  # Here is expected a valid package

        # If all good, a class is returned
        return getattr(module, cls_name)
    except Exception:
        # Nothing found, bozzo input
        return None


def get_model_fk(model_class):
    retVal = {}
    for f in model_class._meta.fields:
        if type(f) is django.db.models.fields.related.ForeignKey:
            # print( ' FK: ' +  )
            f_class = f.related_model.__module__ + "." + f.related_model.__name__
            retVal[f.name] = f_class
    return retVal


def get_model_fk_values(model_class):
    retVal = {}
    for f in model_class._meta.fields:
        if type(f) is django.db.models.fields.related.ForeignKey:
            f_class = f.related_model.__module__ + "." + f.related_model.__name__
            retVal[f.name] = list(name_to_class(f_class).objects.all())
    return retVal


# Create your views here.


def index(request):
    # filter queryset with query params
    qs = Transaction.objects.all()
    transaction_filter = TransactionDataTablesFilter(request.GET, queryset=qs)

    # hook queryset into table
    table = TransactionDataTables(transaction_filter.qs)

    # apply pagination + sorting
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    context = {
        "routes": settings.DYNAMIC_DATATB.keys(),
        "segment": "dynamic_dt",
        "user": request.user,
        "table": table,
        "filter": transaction_filter,
    }

    return render(request, "dyn_dt/index.html", context)


def create_filter(request, model_name):
    model_name = model_name.lower()
    if request.method == "POST":
        keys = request.POST.getlist("key")
        values = request.POST.getlist("value")
        for i in range(len(keys)):
            key = keys[i]
            value = values[i]

            ModelFilter.objects.update_or_create(
                parent=model_name, key=key, defaults={"value": value}
            )

        return redirect(reverse("display-datatables", args=[model_name]))


def create_page_items(request, model_name):
    model_name = model_name.lower()
    if request.method == "POST":
        items = request.POST.get("items")
        page_items, created = PageItems.objects.update_or_create(
            parent=model_name, defaults={"items_per_page": items}
        )
        return redirect(reverse("display-datatables", args=[model_name]))


def create_hide_show_filter(request, model_name):
    model_name = model_name.lower()
    if request.method == "POST":
        data_str = list(request.POST.keys())[0]
        data = json.loads(data_str)

        HideShowFilter.objects.update_or_create(
            parent=model_name,
            key=data.get("key"),
            defaults={"value": data.get("value")},
        )

        response_data = {"message": "Model updated successfully"}
        return JsonResponse(response_data)

    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_filter(request, model_name, id):
    model_name = model_name.lower()
    filter_instance = ModelFilter.objects.get(id=id, parent=model_name)
    filter_instance.delete()
    return redirect(reverse("display-datatables", args=[model_name]))


def get_model_field_names(model, field_type):
    """Returns a list of field names based on the given field type."""
    return [
        field.name
        for field in model._meta.get_fields()
        if isinstance(field, field_type)
    ]


def display_datatables(request, model_path: str):
    """
    Function to display datatables on the frontend.
    """
    # filter queryset with query params
    qs = Transaction.objects.all()
    transaction_filter = TransactionDataTablesFilter(request.GET, queryset=qs)

    # hook queryset into table
    table = TransactionDataTables(transaction_filter.qs)

    # apply pagination + sorting
    RequestConfig(request, paginate={"per_page": 5}).configure(table)

    model_name = None
    model_class = None
    choices_dict = {}

    if model_path in settings.DYNAMIC_DATATB.keys():
        model_name = settings.DYNAMIC_DATATB[model_path]
        model_class = name_to_class(model_name)

    if not model_class:
        return HttpResponse(f" > ERR: Getting ModelClass for path: {model_path}")

    if model_class == Transaction:
        db_fields = [
            "date_time",
            "transaction_type",
            "amount",
            "category",
            "payment_type",
            "remarks",
            "created_by",
        ]
    else:
        db_fields = [field.name for field in model_class._meta.fields]

    fk_fields = get_model_fk_values(model_class)
    db_filters, field_names = [], []
    model_series = {}

    for field in model_class._meta.fields:
        if field.choices:
            choices_dict[field.name] = field.choices

    for field_name in db_fields:
        if field_name not in fk_fields.keys():
            db_filters.append(field_name)

        fields, _ = HideShowFilter.objects.get_or_create(
            key=field_name, parent=model_path.lower()
        )
        if fields.key in db_fields:
            field_names.append(fields)

        f_values = list(model_class.objects.values_list(field_name, flat=True))
        model_series[field_name] = ", ".join(str(i) for i in f_values)

    # model filter
    filter_string = {}
    filter_instance = ModelFilter.objects.filter(parent=model_path.lower())
    for filter_data in filter_instance:
        if filter_data.key in db_fields:
            filter_string[f"{filter_data.key}__icontains"] = filter_data.value

    order_by = request.GET.get("order_by", "id")
    if "date_time" in db_fields:
        order_by = "-date_time"
    elif order_by not in db_fields:
        order_by = "id"

    queryset = model_class.objects.filter(**filter_string).order_by(order_by)

    if not request.user.is_anonymous and "created_by" in db_fields:
        queryset = queryset.filter(created_by=request.user.id)

    item_list = user_filter(request, queryset, db_fields, fk_fields.keys())

    # pagination
    page_items = PageItems.objects.filter(parent=model_path.lower()).last()
    p_items = 25
    if page_items:
        p_items = page_items.items_per_page

    page = request.GET.get("page", 1)
    paginator = Paginator(item_list, p_items)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        return redirect(reverse("display-datatables", args=[model_path]))
    except EmptyPage:
        return redirect(reverse("display-datatables", args=[model_path]))

    read_only_fields = ("id",)

    integer_fields = get_model_field_names(model_class, models.IntegerField)
    date_time_fields = get_model_field_names(model_class, models.DateTimeField)
    email_fields = get_model_field_names(model_class, models.EmailField)
    text_fields = get_model_field_names(
        model_class, (models.TextField, models.CharField)
    )

    context = {
        "page_title": "Dynamic DataTable - " + model_path.lower().title(),
        "link": model_path,
        "field_names": field_names,
        "db_field_names": db_fields,
        "db_filters": db_filters,
        "items": items,
        "page_items": p_items,
        "filter_instance": filter_instance,
        "read_only_fields": read_only_fields,
        "integer_fields": integer_fields,
        "date_time_fields": date_time_fields,
        "email_fields": email_fields,
        "text_fields": text_fields,
        "fk_fields_keys": list(fk_fields.keys()),
        "fk_fields": fk_fields,
        "choices_dict": choices_dict,
        "segment": "dynamic_dt",
        "user": request.user,
        "table": table,
        "filter": transaction_filter,
    }
    return render(request, "dyn_dt/datatables.html", context)


# @login_required(login_url="/accounts/login/")
def create(request, model_path):
    model_class = None

    if model_path in settings.DYNAMIC_DATATB.keys():
        model_name = settings.DYNAMIC_DATATB[model_path]
        model_class = name_to_class(model_name)

    if not model_class:
        return HttpResponse(" > ERR: Getting ModelClass for path: " + model_path)

    if request.method == "POST":
        data = {}
        fk_fields = get_model_fk(model_class)

        for attribute, value in request.POST.items():
            if attribute == "csrfmiddlewaretoken":
                continue

            # Process FKs
            if attribute in fk_fields.keys():
                value = (
                    name_to_class(fk_fields[attribute]).objects.filter(id=value).first()
                )

            data[attribute] = value if value else ""

        if not data.get("amount"):
            data["amount"] = Decimal("0.0")
        if not data.get("date_time"):
            data["date_time"] = localtime_now()

        data["created_by"] = request.user
        model_class.objects.create(**data)

    return redirect(request.META.get("HTTP_REFERER"))


# @login_required(login_url="/accounts/login/")
def delete(request, model_path, id):
    model_class = None

    if model_path in settings.DYNAMIC_DATATB.keys():
        model_name = settings.DYNAMIC_DATATB[model_path]
        model_class = name_to_class(model_name)

    if not model_class:
        return HttpResponse(" > ERR: Getting ModelClass for path: " + model_path)

    item = model_class.objects.get(id=id)
    item.delete()
    return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/accounts/login/")
def update(request, model_path, id):
    """
    Function to allow users to Edit Dynamic tables.
    """
    model_class = None

    if model_path in settings.DYNAMIC_DATATB.keys():
        model_name = settings.DYNAMIC_DATATB[model_path]
        model_class = name_to_class(model_name)

    if not model_class:
        return HttpResponse(" > ERR: Getting ModelClass for path: " + model_path)

    item = model_class.objects.get(id=id)
    fk_fields = get_model_fk(model_class)

    if request.method == "POST":
        for attribute, value in request.POST.items():
            if attribute == "csrfmiddlewaretoken":
                continue

            if getattr(item, attribute, value) is not None:
                # Process FKs
                if attribute in fk_fields.keys():
                    if attribute == "created_by":
                        value = request.user
                    else:
                        value = (
                            name_to_class(fk_fields[attribute])
                            .objects.filter(id=value)
                            .first()
                        )

                setattr(item, attribute, value)

        item.save()

    return redirect(request.META.get("HTTP_REFERER"))


# Export as CSV
class ExportCSVView(View):
    def get(self, request, model_path):
        model_name = None
        model_class = None

        if model_path in settings.DYNAMIC_DATATB.keys():
            model_name = settings.DYNAMIC_DATATB[model_path]
            model_class = name_to_class(model_name)

        if not model_class:
            return HttpResponse(" > ERR: Getting ModelClass for path: " + model_path)

        db_field_names = [field.name for field in model_class._meta.get_fields()]
        fields = []
        show_fields = HideShowFilter.objects.filter(
            value=False, parent=model_path.lower()
        )

        for field in show_fields:
            if field.key in db_field_names:
                fields.append(field.key)
            else:
                print(f"Field {field.key} does not exist in {model_class} model.")

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="{model_path.lower()}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(fields)  # Write the header

        filter_string = {}
        filter_instance = ModelFilter.objects.filter(parent=model_path.lower())
        for filter_data in filter_instance:
            filter_string[f"{filter_data.key}__icontains"] = filter_data.value

        order_by = request.GET.get("order_by", "id")
        queryset = model_class.objects.filter(**filter_string).order_by(order_by)

        items = user_filter(request, queryset, db_field_names)

        for item in items:
            row_data = []
            for field in fields:
                try:
                    row_data.append(getattr(item, field))
                except AttributeError:
                    row_data.append("")
            writer.writerow(row_data)

        return response
