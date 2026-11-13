"""REST API routes for Order Service."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.order_service.application.dtos import (
    AddOrderItemCommand,
    CancelOrderCommand,
    CreateOrderCommand,
    OrderResponse,
    OutboxEventResponse,
    UpdateItemQuantityCommand,
)
from services.order_service.application.order_service import OrderApplicationService
from services.order_service.infrastructure.repository import SqlAlchemyOrderRepository
from shared.constants import ApiEndpoints, HttpHeaders
from shared.pagination import PaginatedResponse

__all__ = ["get_db_session", "get_order_app_service", "router"]


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency placeholder overridden by application runtime or test fixtures."""
    raise NotImplementedError("Session dependency not provided.")
    yield  # pragma: no cover


async def get_order_app_service(
    session: AsyncSession = Depends(get_db_session),
) -> OrderApplicationService:
    repo = SqlAlchemyOrderRepository(session)
    return OrderApplicationService(repo)


router = APIRouter(prefix=ApiEndpoints.ORDERS, tags=["Orders"])


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Order Aggregate Root in DRAFT state",
)
async def create_order(
    payload: CreateOrderCommand,
    response: Response,
    app_svc: OrderApplicationService = Depends(get_order_app_service),
) -> OrderResponse:
    order = await app_svc.create_order(payload)
    response.headers[HttpHeaders.LOCATION] = f"{ApiEndpoints.ORDERS}/{order.id}"
    return order


@router.get(
    "",
    response_model=PaginatedResponse[OrderResponse],
    summary="List orders with pagination",
)
async def list_orders(
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10,
    app_svc: OrderApplicationService = Depends(get_order_app_service),
) -> PaginatedResponse[OrderResponse]:
    offset = (page - 1) * page_size
    items, total_count = await app_svc.list_orders(offset=offset, limit=page_size)
    return PaginatedResponse.create(
        items=items,
        total_count=total_count,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Get Order Aggregate Root by ID",
)
async def get_order(
    order_id: str,
    app_svc: OrderApplicationService = Depends(get_order_app_service),
) -> OrderResponse:
    return await app_svc.get_order(order_id)


@router.post(
    "/{order_id}/items",
    response_model=OrderResponse,
    summary="Add or consolidate a line item through the Aggregate Root",
)
async def add_item(
    order_id: str,
    payload: AddOrderItemCommand,
    app_svc: OrderApplicationService = Depends(get_order_app_service),
) -> OrderResponse:
    return await app_svc.add_item(order_id, payload)


@router.patch(
    "/{order_id}/items/{sku}",
    response_model=OrderResponse,
    summary="Update item quantity through Aggregate Root",
)
async def update_item_quantity(
    order_id: str,
    sku: str,
    payload: UpdateItemQuantityCommand,
    app_svc: OrderApplicationService = Depends(get_order_app_service),
) -> OrderResponse:
    return await app_svc.update_item_quantity(order_id, sku, payload)


@router.delete(
    "/{order_id}/items/{sku}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove an item from the order aggregate",
)
async def remove_item(
    order_id: str,
    sku: str,
    if_match: Annotated[str | None, Header(description="Optional aggregate ETag/version")] = None,
    app_svc: OrderApplicationService = Depends(get_order_app_service),
) -> Response:
    expected_version = int(if_match) if if_match and if_match.isdigit() else None
    await app_svc.remove_item(order_id, sku, expected_version=expected_version)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{order_id}/confirm",
    response_model=OrderResponse,
    summary="Confirm the Order Aggregate (enforces non-empty and draft invariants)",
)
async def confirm_order(
    order_id: str,
    if_match: Annotated[str | None, Header(description="Optional aggregate version")] = None,
    app_svc: OrderApplicationService = Depends(get_order_app_service),
) -> OrderResponse:
    expected_version = int(if_match) if if_match and if_match.isdigit() else None
    return await app_svc.confirm_order(order_id, expected_version=expected_version)


@router.post(
    "/{order_id}/cancel",
    response_model=OrderResponse,
    summary="Cancel order",
)
async def cancel_order(
    order_id: str,
    payload: CancelOrderCommand,
    app_svc: OrderApplicationService = Depends(get_order_app_service),
) -> OrderResponse:
    return await app_svc.cancel_order(order_id, payload)


@router.get(
    "/{order_id}/events",
    response_model=list[OutboxEventResponse],
    summary="Inspect domain events stored in Transactional Outbox for this aggregate",
)
async def list_order_events(
    order_id: str,
    app_svc: OrderApplicationService = Depends(get_order_app_service),
) -> list[OutboxEventResponse]:
    return await app_svc.list_events(order_id)
