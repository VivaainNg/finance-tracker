from rest_framework.routers import DefaultRouter

from .views import TransactionViewSet

router = DefaultRouter()
router.register("transactions", TransactionViewSet, basename="transactions")

# Base url for the api within the project
urlpatterns = router.urls
