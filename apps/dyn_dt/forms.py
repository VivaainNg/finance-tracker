from django import forms
from apps.pages.models import Category, Transaction


class TransactionForm(forms.ModelForm):
    """
    Forms to Create or Update Transaction model.
    """

    category = forms.ModelChoiceField(
        queryset=None,
        label="Category",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    amount = forms.DecimalField(
        label="Amount", widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    date_time = forms.DateTimeField(
        label="Datetime",
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )
    payment_type = forms.ChoiceField(
        label="Payment Type",
        choices=Transaction.PaymentType.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    transaction_type = forms.ChoiceField(
        label="Transaction Type",
        choices=Transaction.TransactionType.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    remarks = forms.CharField(
        label="Remarks",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
            }
        ),
    )

    class Meta:
        model = Transaction
        fields = [
            "category",
            "amount",
            "date_time",
            "payment_type",
            "transaction_type",
            "remarks",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
