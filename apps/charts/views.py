from typing import Any
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import TemplateView
from apps.pages.models import Transaction


class DisplayChartsView(LoginRequiredMixin, TemplateView):
    """
    View to display charts/graphs.

    Only authenticated/logged in user can view their own data.
    """

    template_name = "charts/index.html"
    login_url = "auth_signin"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        amounts, categories = [], []

        queryset = Transaction.objects.select_related("created_by", "category").all()

        if self.request.user.is_authenticated:
            queryset = (
                queryset.filter(created_by=self.request.user)
                .values("category__name")
                .annotate(total_amount=Sum("amount"))
                .order_by("category__name")
            )
        else:
            queryset = (
                queryset.values("category__name")
                .annotate(total_amount=Sum("amount"))
                .order_by("category__name")
            )

        for result in queryset:
            amounts.append(float(result.get("total_amount", 0)))
            categories.append(result.get("category__name"))

        context["segment"] = "charts"

        # Need to serialize so JS can extract these values
        context["amounts"] = json.dumps(amounts)
        context["categories"] = json.dumps(categories)
        return context
