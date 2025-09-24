from django_filters import rest_framework as filters

from apps.pages.models import Category, Transaction


class TransactionFilter(filters.FilterSet):
    """
    The filter set to perform dynamic QuerySet filtering from URL parameters
    based on Transaction model.
    """

    id = filters.NumberFilter()
    date_time_min = filters.DateTimeFilter(field_name="date_time", lookup_expr="gte")
    date_time_max = filters.DateTimeFilter(field_name="date_time", lookup_expr="lte")
    amount_min = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = filters.NumberFilter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = Transaction
        fields = [
            "id",
            "date_time_min",
            "date_time_max",
            "amount_min",
            "amount_max",
            "created_by",
        ]


class CategoryFilter(filters.FilterSet):
    """
    The filter set to perform dynamic QuerySet filtering from URL parameters
    based on Category model.
    """

    id = filters.NumberFilter()
    name = filters.CharFilter(field_name="name")

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]
