import django_tables2 as tables
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from apps.pages.models import Transaction


class TransactionDataTables(tables.Table):
    """
    Datatables class for Transaction model.
    """

    actions = tables.TemplateColumn(
        verbose_name=_("Actions"),
        template_name="pages/transaction_action.html",
        attrs={"td": {"class": "actions-col"}},
        orderable=False,
    )

    class Meta:
        model = Transaction
        order_by = "-date_time"
        attrs = {
            "id": "transactions_table_id",
            "class": "table table-striped table-hover",
        }
        fields = [
            "date_time",
            "amount",
            "payment_type",
            "category",
            "transaction_type",
            "remarks",
            "created_by",
            "actions",
        ]

    def render_amount(self, value: Decimal, record: Transaction):
        return f"RM {value}"

    def render_actions(
        self, column, record: Transaction, table, value, bound_column, **kwargs
    ):
        column.extra_context = {
            "transaction": record,
        }

        return column.render(record, table, value, bound_column, **kwargs)
