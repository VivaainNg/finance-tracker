from drf_spectacular.utils import OpenApiExample


CREATE_TRANSACTION_REQUEST_PAYLOAD = OpenApiExample(
    name="Sample Request Body",
    value={
        "amount": "66.00",
        "date_time": "2025-09-15T13:04:00+08:00",
        "payment_type": "Card",
        "transaction_type": "Expenses",
        "remarks": "test ",
        "category": 2,
        "created_by": 1,
    },
    request_only=True,
)

CREATE_TRANSACTION_RESPONSE_PAYLOAD = OpenApiExample(
    name="Sample Response Body",
    value={
        "id": 24,
        "amount": "66.00",
        "dateTime": "2025-09-15T13:04:00+08:00",
        "paymentType": "Card",
        "transactionType": "Expenses",
        "remarks": "test",
        "category": 2,
        "createdBy": 1,
    },
    response_only=True,
)

UPDATE_TRANSACTION_REQUEST_PAYLOAD = OpenApiExample(
    name="Sample Request Body",
    value={
        "amount": "5555",
        "date_time": "2025-09-24T21:45:00+08:00",
        "payment_type": "Cash",
        "transaction_type": "Income",
        "remarks": "update remarks via Postman",
        "category": 3,
        "created_by": 1,
    },
    request_only=True,
)

UPDATE_TRANSACTION_RESPONSE_PAYLOAD = OpenApiExample(
    name="Sample Response Body",
    value={
        "id": 5,
        "amount": "5555.00",
        "dateTime": "2025-09-24T21:45:00+08:00",
        "paymentType": "Cash",
        "transactionType": "Income",
        "remarks": "update remarks via Postman",
        "category": 3,
        "createdBy": 1,
    },
    response_only=True,
)
