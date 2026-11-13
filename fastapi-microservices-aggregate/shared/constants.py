"""Global constants, URLs, endpoints, and static strings for microservices."""

from __future__ import annotations

from decimal import Decimal
from enum import StrEnum
from typing import Final

__all__ = [
    "ApiEndpoints",
    "DomainConstants",
    "ErrorTitles",
    "ErrorTypes",
    "HttpHeaders",
    "MediaTypes",
    "ServiceNames",
    "ServiceUrls",
    "TableNames",
]


class ServiceNames(StrEnum):
    """Canonical service identifiers."""

    GATEWAY_AGGREGATOR = "gateway-aggregator"
    PRODUCT_SERVICE = "product-service"
    INVENTORY_SERVICE = "inventory-service"
    REVIEWS_SERVICE = "reviews-service"
    ORDER_SERVICE = "order-service"


class ServiceUrls:
    """Default inter-service communication base URLs."""

    PRODUCT_SERVICE: Final[str] = "http://product-service:8001"
    INVENTORY_SERVICE: Final[str] = "http://inventory-service:8002"
    REVIEWS_SERVICE: Final[str] = "http://reviews-service:8003"
    ORDER_SERVICE: Final[str] = "http://order-service:8004"
    GATEWAY_AGGREGATOR: Final[str] = "http://localhost:8000"


class ApiEndpoints:
    """Standardized API versioned route paths."""

    HEALTH: Final[str] = "/health"
    READY: Final[str] = "/ready"

    # Microservices resource routes
    PRODUCTS: Final[str] = "/api/v1/products"
    STOCK: Final[str] = "/api/v1/stock"
    REVIEWS: Final[str] = "/api/v1/reviews"
    ORDERS: Final[str] = "/api/v1/orders"

    # Gateway Aggregator composition routes
    PAGES_PRODUCTS: Final[str] = "/api/v1/pages/products"
    PAGES_ORDERS: Final[str] = "/api/v1/pages/orders"


class HttpHeaders:
    """Standard HTTP header names."""

    CONTENT_TYPE: Final[str] = "Content-Type"
    LOCATION: Final[str] = "Location"
    IF_MATCH: Final[str] = "if-match"


class MediaTypes:
    """Standard HTTP MIME content types."""

    APPLICATION_JSON: Final[str] = "application/json"
    APPLICATION_PROBLEM_JSON: Final[str] = "application/problem+json"


class ErrorTypes:
    """RFC 7807 problem type URI identifiers."""

    BASE_URI: Final[str] = "https://api.example.com/errors"
    ABOUT_BLANK: Final[str] = "about:blank"
    HTTP_STATUS_BASE: Final[str] = "https://httpstatuses.com"

    PRODUCT_NOT_FOUND: Final[str] = f"{BASE_URI}/product-not-found"
    SKU_CONFLICT: Final[str] = f"{BASE_URI}/sku-conflict"
    STOCK_NOT_FOUND: Final[str] = f"{BASE_URI}/stock-not-found"
    GATEWAY_TIMEOUT: Final[str] = f"{BASE_URI}/gateway-timeout"
    SERVICE_UNAVAILABLE: Final[str] = f"{BASE_URI}/service-unavailable"
    BAD_GATEWAY: Final[str] = f"{BASE_URI}/bad-gateway"
    DOMAIN_INVARIANT_VIOLATION: Final[str] = f"{BASE_URI}/domain-invariant-violation"
    INVALID_ORDER_STATE: Final[str] = f"{BASE_URI}/invalid-order-state"
    CONCURRENCY_CONFLICT: Final[str] = f"{BASE_URI}/concurrency-conflict"
    ITEM_NOT_FOUND: Final[str] = f"{BASE_URI}/item-not-found"
    ORDER_NOT_FOUND: Final[str] = f"{BASE_URI}/order-not-found"
    SIMULATED_FAILURE: Final[str] = f"{BASE_URI}/simulated-failure"
    VALIDATION_ERROR: Final[str] = f"{BASE_URI}/validation-error"


class ErrorTitles:
    """RFC 7807 human-readable problem titles."""

    PRODUCT_NOT_FOUND: Final[str] = "Product Not Found"
    SKU_CONFLICT: Final[str] = "Product SKU Conflict"
    STOCK_NOT_FOUND: Final[str] = "Stock Record Not Found"
    PRODUCT_TIMEOUT: Final[str] = "Product Service Timeout"
    PRODUCT_UNAVAILABLE: Final[str] = "Product Service Unavailable"
    PRODUCT_ERROR: Final[str] = "Product Service Error"
    ORDER_NOT_FOUND: Final[str] = "Order Not Found"
    ITEM_NOT_FOUND: Final[str] = "Line Item Not Found"
    DOMAIN_INVARIANT_VIOLATION: Final[str] = "Domain Invariant Violation"
    INVALID_ORDER_STATE: Final[str] = "Invalid Order State"
    CONCURRENCY_CONFLICT: Final[str] = "Optimistic Concurrency Conflict"
    SIMULATED_FAILURE: Final[str] = "Simulated Service Failure"
    VALIDATION_ERROR: Final[str] = "Validation Error"
    HTTP_ERROR: Final[str] = "HTTP Error"


class DomainConstants:
    """Business domain rules and limits."""

    DEFAULT_CURRENCY: Final[str] = "USD"
    DEFAULT_WAREHOUSE: Final[str] = "WH-MAIN"
    MAX_ORDER_TOTAL: Final[Decimal] = Decimal("50000.00")
    MAX_QUANTITY_PER_LINE_ITEM: Final[int] = 10
    MIN_QUANTITY_PER_LINE_ITEM: Final[int] = 1
    MAX_DISTINCT_ITEMS_PER_ORDER: Final[int] = 50
    DEFAULT_TIMEOUT_MS: Final[int] = 1000


class TableNames:
    """Relational database table names."""

    PRODUCTS: Final[str] = "products"
    STOCK_ITEMS: Final[str] = "stock_items"
    REVIEWS: Final[str] = "reviews"
    ORDERS: Final[str] = "orders"
    ORDER_ITEMS: Final[str] = "order_items"
    ORDER_OUTBOX_EVENTS: Final[str] = "order_outbox_events"
