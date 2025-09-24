from rest_framework import serializers

from apps.pages.models import Transaction, Category


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction's data model.
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category's data model.
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
