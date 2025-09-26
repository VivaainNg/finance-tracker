from django_filters import (
    FilterSet,
    CharFilter,
    ChoiceFilter,
    widgets,
    ModelMultipleChoiceFilter,
)
from django import forms
from apps.pages.models import Category, Transaction


class TransactionDataTablesFilter(FilterSet):
    """
    Filter class for Transaction's data tables.
    """

    remarks = CharFilter(
        lookup_expr="icontains",
        label="Remarks",
        widget=widgets.forms.TextInput(attrs={"class": "form-control"}),
    )
    payment_type = ChoiceFilter(
        choices=Transaction.PaymentType.choices,
        widget=widgets.forms.Select(attrs={"class": "form-control form-select"}),
    )
    transaction_type = ChoiceFilter(
        choices=Transaction.TransactionType.choices,
        widget=widgets.forms.Select(attrs={"class": "form-control form-select"}),
    )

    category = ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-control"}),
        label="Categories",
    )

    class Meta:
        model = Transaction
        fields = [
            "remarks",
            "payment_type",
            "transaction_type",
            "category",
        ]
