from rest_framework import serializers

from apps.pages.models import Transaction, Category


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction's data model.
    """

    id = serializers.IntegerField(read_only=True)
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = "__all__"

    def get_category_name(self, obj: Transaction):
        return obj.category.name if obj and obj.category else None


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category's data model.
    """

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
