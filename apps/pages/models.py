from django.db import models
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from .utils import localtime_now
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    info = models.CharField(max_length=100, default="")
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Model for User class, inheriting from AbstractUser which
    serves as a blueprint for User model.
    """

    pass


class Category(models.Model):
    """Model for storing Category information."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=128,
        unique=True,
    )

    class Meta:
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return self.name


class Transaction(models.Model):
    """Model for storing Transaction information."""

    class TransactionType(models.TextChoices):
        INCOME = "Income", _("Income")
        EXPENSES = "Expenses", _("Expenses")
        MISCELLANEOUS = "Miscellaneous", _("Miscellaneous")

    class PaymentType(models.TextChoices):
        CASH = "Cash", _("Cash")
        CARD = "Card", _("Card")
        ACCOUNT = "Account", _("Account")

    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        verbose_name=_("Amount"),
        max_digits=19,
        decimal_places=2,
        default=Decimal("0.0"),
        blank=True,
    )
    date_time = models.DateTimeField(verbose_name=_("Datetime"), default=localtime_now)
    payment_type = models.CharField(
        verbose_name=_("Payment Type"),
        max_length=16,
        choices=PaymentType.choices,
        default=PaymentType.ACCOUNT,
    )
    transaction_type = models.CharField(
        verbose_name=_("Transaction Type"),
        max_length=16,
        choices=TransactionType.choices,
        default=TransactionType.INCOME,
    )
    remarks = models.TextField(verbose_name=_("Remarks"), max_length=256, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created by"),
        related_name="+",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.date_time} :: {self.transaction_type} :: {self.amount}"
