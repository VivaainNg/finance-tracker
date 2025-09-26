from django.shortcuts import render
from django.core import serializers
from apps.pages.models import Product, Transaction

# Create your views here.


def index(request):
    products = serializers.serialize("json", Product.objects.all())
    transactions = serializers.serialize("json", Transaction.objects.all())
    context = {
        "segment": "charts",
        "products": products,
        "transactions": transactions,
        "user": request.user,
    }
    return render(request, "charts/index.html", context)
