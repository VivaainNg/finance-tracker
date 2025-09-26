from djangorestframework_camel_case.parser import CamelCaseJSONParser
from django_filters.rest_framework import DjangoFilterBackend
from djangorestframework_camel_case.render import (
    CamelCaseBrowsableAPIRenderer,
    CamelCaseJSONRenderer,
)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter

from apps.pages.models import Transaction
from .filters import TransactionFilter

from .serializers import TransactionSerializer

from .openapi_schema import (
    CREATE_TRANSACTION_REQUEST_PAYLOAD,
    CREATE_TRANSACTION_RESPONSE_PAYLOAD,
    UPDATE_TRANSACTION_REQUEST_PAYLOAD,
    UPDATE_TRANSACTION_RESPONSE_PAYLOAD,
)


# Hides documentation for PATCH request
@extend_schema_view(partial_update=extend_schema(exclude=True))
class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet class for Transaction data model.
    """

    http_method_names = ["get", "post", "put", "patch", "delete"]
    permission_classes = [permissions.AllowAny]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    renderer_classes = [CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer]
    parser_classes = [CamelCaseJSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TransactionFilter
    search_fields = ["remarks"]

    @extend_schema(
        summary="Endpoint to retrieve a list of all Transactions",
        description="Retrieve entire list of available Transactions",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Endpoint to create a new Transaction",
        description="Create a new Transaction based on submitted request payload",
        examples=[
            CREATE_TRANSACTION_REQUEST_PAYLOAD,
            CREATE_TRANSACTION_RESPONSE_PAYLOAD,
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Endpoint to retrieve details of a specific transaction using its ID",
        description="Retrieve a specific transaction based on given ID in the request's path parameter",
        examples=[
            CREATE_TRANSACTION_RESPONSE_PAYLOAD,
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Endpoint to fully update a transaction using its ID",
        description="Fully update a transaction based on its ID in the request's path parameter & full request payload",
        examples=[
            UPDATE_TRANSACTION_REQUEST_PAYLOAD,
            UPDATE_TRANSACTION_RESPONSE_PAYLOAD,
        ],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Endpoint to delete a transaction using its ID",
        description="Delete a specific transaction based on given ID in the request's path parameter",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
