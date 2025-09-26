from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.status import is_success
from apps.pages.models import Transaction, Category
from model_bakery import baker

from django.contrib.auth import get_user_model

User = get_user_model()


class TransactionViewSetTestCase(APITestCase):
    """
    Unit tests for Transaction endpoints (CRUD).
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="tester", password="password123")
        cls.category = baker.make(Category, name="Food")
        cls.transaction = baker.make(
            Transaction,
            category=cls.category,
            amount="150.50",
            payment_type=Transaction.PaymentType.CASH,
            transaction_type=Transaction.TransactionType.EXPENSES,
            remarks="Lunch",
            created_by=cls.user,
        )

    def setUp(self):
        self.list_endpoint = reverse("transactions-list")

    def test_list(self):
        """Test GET all transactions"""
        response = self.client.get(self.list_endpoint)
        self.assertTrue(is_success(response.status_code))
        self.assertTrue(response.json())

    def test_get(self):
        """Test GET single transaction by ID"""
        transaction = Transaction.objects.first()
        response = self.client.get(
            reverse("transactions-detail", args=[transaction.pk])
        )
        json_data = response.json()

        self.assertTrue(is_success(response.status_code))
        self.assertEqual(json_data["amount"], "150.50")
        self.assertEqual(json_data["paymentType"], Transaction.PaymentType.CASH)
        self.assertEqual(
            json_data["transactionType"], Transaction.TransactionType.EXPENSES
        )
        self.assertEqual(json_data["remarks"], "Lunch")

    def test_post(self):
        """Test POST create a new transaction"""
        payload = {
            "category": self.category.pk,
            "amount": "222.22",
            "paymentType": Transaction.PaymentType.CARD,
            "transactionType": Transaction.TransactionType.INCOME,
            "remarks": "Salary",
            "createdBy": self.user.pk,
        }
        response = self.client.post(self.list_endpoint, data=payload, format="json")
        json_data = response.json()

        self.assertTrue(is_success(response.status_code))
        self.assertEqual(json_data["amount"], "222.22")
        self.assertEqual(json_data["remarks"], "Salary")
        self.assertEqual(json_data["paymentType"], Transaction.PaymentType.CARD)

    def test_put(self):
        """Test PUT full update of transaction"""
        transaction = Transaction.objects.first()
        put_url = reverse("transactions-detail", args=[transaction.pk])
        payload = {
            "category": self.category.pk,
            "amount": "333.33",
            "paymentType": Transaction.PaymentType.ACCOUNT,
            "transactionType": Transaction.TransactionType.EXPENSES,
            "remarks": "Bills",
            "createdBy": self.user.pk,
        }
        response = self.client.put(put_url, data=payload, format="json")
        json_data = response.json()

        self.assertTrue(is_success(response.status_code))
        self.assertEqual(json_data["amount"], "333.33")
        self.assertEqual(json_data["remarks"], "Bills")

    def test_patch(self):
        """Test PATCH partial update of transaction"""
        transaction = Transaction.objects.first()
        patch_url = reverse("transactions-detail", args=[transaction.pk])
        payload = {"remarks": "Updated remarks"}
        response = self.client.patch(patch_url, data=payload, format="json")
        json_data = response.json()

        self.assertTrue(is_success(response.status_code))
        self.assertEqual(json_data["remarks"], "Updated remarks")

    def test_delete(self):
        """Test DELETE a transaction"""
        transaction = Transaction.objects.first()
        delete_url = reverse("transactions-detail", args=[transaction.pk])

        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Transaction.objects.filter(pk=transaction.pk).exists())
