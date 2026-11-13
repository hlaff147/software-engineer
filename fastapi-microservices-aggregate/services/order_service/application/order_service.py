"""Application Service orchestrating use cases on the Order Aggregate Root."""

from __future__ import annotations

import uuid

from fastapi import status

from services.order_service.application.dtos import (
    AddOrderItemCommand,
    CancelOrderCommand,
    CreateOrderCommand,
    OrderLineItemResponse,
    OrderResponse,
    OutboxEventResponse,
    UpdateItemQuantityCommand,
)
from services.order_service.domain.exceptions import (
    DomainInvariantViolation,
    InvalidOrderStateError,
    LineItemNotFoundError,
    OptimisticConcurrencyError,
)
from services.order_service.domain.order_aggregate import Order
from services.order_service.domain.value_objects import (
    CustomerId,
    Money,
    OrderId,
    ProductId,
    Quantity,
    Sku,
)
from services.order_service.infrastructure.repository import SqlAlchemyOrderRepository
from shared.constants import ErrorTitles, ErrorTypes
from shared.errors import ProblemDetailsException

__all__ = ["OrderApplicationService"]


class OrderApplicationService:
    """Coordinates business operations through the Order Aggregate boundary."""

    def __init__(self, repository: SqlAlchemyOrderRepository) -> None:
        self.repository = repository

    async def create_order(self, command: CreateOrderCommand) -> OrderResponse:
        order_id = OrderId(str(uuid.uuid4()))
        customer_id = CustomerId(command.customer_id)

        order = Order.create(order_id, customer_id, currency=command.currency)
        await self.repository.save(order)
        return self._to_response(order)

    async def get_order(self, order_id_str: str) -> OrderResponse:
        order = await self._load_order(order_id_str)
        return self._to_response(order)

    async def list_orders(
        self, offset: int = 0, limit: int = 10
    ) -> tuple[list[OrderResponse], int]:
        orders, total = await self.repository.list_orders(offset=offset, limit=limit)
        return [self._to_response(o) for o in orders], total

    async def add_item(self, order_id_str: str, command: AddOrderItemCommand) -> OrderResponse:
        order = await self._load_order(order_id_str)
        self._check_expected_version(order, command.expected_version)

        try:
            order.add_item(
                product_id=ProductId(command.product_id),
                sku=Sku(command.sku),
                product_name=command.product_name,
                unit_price=Money(command.unit_price, order.currency),
                quantity=Quantity(command.quantity),
            )
            await self.repository.save(order)
            return self._to_response(order)
        except (ValueError, DomainInvariantViolation) as err:
            raise ProblemDetailsException(
                status=422,
                title=ErrorTitles.DOMAIN_INVARIANT_VIOLATION,
                detail=str(err),
                type_uri=ErrorTypes.DOMAIN_INVARIANT_VIOLATION,
            ) from err
        except InvalidOrderStateError as err:
            raise ProblemDetailsException(
                status=status.HTTP_409_CONFLICT,
                title=ErrorTitles.INVALID_ORDER_STATE,
                detail=str(err),
                type_uri=ErrorTypes.INVALID_ORDER_STATE,
            ) from err
        except OptimisticConcurrencyError as err:
            raise ProblemDetailsException(
                status=status.HTTP_409_CONFLICT,
                title=ErrorTitles.CONCURRENCY_CONFLICT,
                detail=str(err),
                type_uri=ErrorTypes.CONCURRENCY_CONFLICT,
            ) from err

    async def update_item_quantity(
        self,
        order_id_str: str,
        sku_str: str,
        command: UpdateItemQuantityCommand,
    ) -> OrderResponse:
        order = await self._load_order(order_id_str)
        self._check_expected_version(order, command.expected_version)

        try:
            order.update_item_quantity(sku=Sku(sku_str), new_quantity=Quantity(command.quantity))
            await self.repository.save(order)
            return self._to_response(order)
        except LineItemNotFoundError as err:
            raise ProblemDetailsException(
                status=status.HTTP_404_NOT_FOUND,
                title=ErrorTitles.ITEM_NOT_FOUND,
                detail=str(err),
                type_uri=ErrorTypes.ITEM_NOT_FOUND,
            ) from err
        except (ValueError, DomainInvariantViolation) as err:
            raise ProblemDetailsException(
                status=422,
                title=ErrorTitles.DOMAIN_INVARIANT_VIOLATION,
                detail=str(err),
                type_uri=ErrorTypes.DOMAIN_INVARIANT_VIOLATION,
            ) from err
        except InvalidOrderStateError as err:
            raise ProblemDetailsException(
                status=status.HTTP_409_CONFLICT,
                title=ErrorTitles.INVALID_ORDER_STATE,
                detail=str(err),
                type_uri=ErrorTypes.INVALID_ORDER_STATE,
            ) from err
        except OptimisticConcurrencyError as err:
            raise ProblemDetailsException(
                status=status.HTTP_409_CONFLICT,
                title=ErrorTitles.CONCURRENCY_CONFLICT,
                detail=str(err),
                type_uri=ErrorTypes.CONCURRENCY_CONFLICT,
            ) from err

    async def remove_item(
        self,
        order_id_str: str,
        sku_str: str,
        expected_version: int | None = None,
    ) -> OrderResponse:
        order = await self._load_order(order_id_str)
        self._check_expected_version(order, expected_version)

        try:
            order.remove_item(sku=Sku(sku_str))
            await self.repository.save(order)
            return self._to_response(order)
        except LineItemNotFoundError as err:
            raise ProblemDetailsException(
                status=status.HTTP_404_NOT_FOUND,
                title=ErrorTitles.ITEM_NOT_FOUND,
                detail=str(err),
                type_uri=ErrorTypes.ITEM_NOT_FOUND,
            ) from err
        except InvalidOrderStateError as err:
            raise ProblemDetailsException(
                status=status.HTTP_409_CONFLICT,
                title=ErrorTitles.INVALID_ORDER_STATE,
                detail=str(err),
                type_uri=ErrorTypes.INVALID_ORDER_STATE,
            ) from err
        except OptimisticConcurrencyError as err:
            raise ProblemDetailsException(
                status=status.HTTP_409_CONFLICT,
                title=ErrorTitles.CONCURRENCY_CONFLICT,
                detail=str(err),
                type_uri=ErrorTypes.CONCURRENCY_CONFLICT,
            ) from err

    async def confirm_order(
        self,
        order_id_str: str,
        expected_version: int | None = None,
    ) -> OrderResponse:
        order = await self._load_order(order_id_str)
        self._check_expected_version(order, expected_version)

        try:
            order.confirm()
            await self.repository.save(order)
            return self._to_response(order)
        except DomainInvariantViolation as err:
            raise ProblemDetailsException(
                status=422,
                title=ErrorTitles.DOMAIN_INVARIANT_VIOLATION,
                detail=str(err),
                type_uri=ErrorTypes.DOMAIN_INVARIANT_VIOLATION,
            ) from err
        except InvalidOrderStateError as err:
            raise ProblemDetailsException(
                status=status.HTTP_409_CONFLICT,
                title=ErrorTitles.INVALID_ORDER_STATE,
                detail=str(err),
                type_uri=ErrorTypes.INVALID_ORDER_STATE,
            ) from err
        except OptimisticConcurrencyError as err:
            raise ProblemDetailsException(
                status=status.HTTP_409_CONFLICT,
                title=ErrorTitles.CONCURRENCY_CONFLICT,
                detail=str(err),
                type_uri=ErrorTypes.CONCURRENCY_CONFLICT,
            ) from err

    async def cancel_order(
        self,
        order_id_str: str,
        command: CancelOrderCommand,
    ) -> OrderResponse:
        order = await self._load_order(order_id_str)
        self._check_expected_version(order, command.expected_version)

        try:
            order.cancel(reason=command.reason)
            await self.repository.save(order)
            return self._to_response(order)
        except InvalidOrderStateError as err:
            raise ProblemDetailsException(
                status=status.HTTP_409_CONFLICT,
                title=ErrorTitles.INVALID_ORDER_STATE,
                detail=str(err),
                type_uri=ErrorTypes.INVALID_ORDER_STATE,
            ) from err
        except OptimisticConcurrencyError as err:
            raise ProblemDetailsException(
                status=status.HTTP_409_CONFLICT,
                title=ErrorTitles.CONCURRENCY_CONFLICT,
                detail=str(err),
                type_uri=ErrorTypes.CONCURRENCY_CONFLICT,
            ) from err

    async def list_events(self, order_id_str: str) -> list[OutboxEventResponse]:
        await self._load_order(order_id_str)
        raw_events = await self.repository.list_events(OrderId(order_id_str))
        return [OutboxEventResponse(**ev) for ev in raw_events]

    async def _load_order(self, order_id_str: str) -> Order:
        order = await self.repository.get_by_id(OrderId(order_id_str))
        if order is None:
            raise ProblemDetailsException(
                status=status.HTTP_404_NOT_FOUND,
                title=ErrorTitles.ORDER_NOT_FOUND,
                detail=f"Order '{order_id_str}' does not exist.",
                type_uri=ErrorTypes.ORDER_NOT_FOUND,
            )
        return order

    def _check_expected_version(self, order: Order, expected_version: int | None) -> None:
        if expected_version is not None and order.version != expected_version:
            raise ProblemDetailsException(
                status=status.HTTP_409_CONFLICT,
                title=ErrorTitles.CONCURRENCY_CONFLICT,
                detail=(
                    f"Order aggregate version mismatch. Current version is {order.version}, "
                    f"but expected version was {expected_version}."
                ),
                type_uri=ErrorTypes.CONCURRENCY_CONFLICT,
            )

    def _to_response(self, order: Order) -> OrderResponse:
        item_responses = [
            OrderLineItemResponse(
                line_item_id=it.line_item_id,
                product_id=int(it.product_id),
                sku=str(it.sku),
                product_name=it.product_name,
                unit_price=it.unit_price.amount,
                quantity=it.quantity.value,
                subtotal=it.subtotal.amount,
            )
            for it in order.items
        ]
        return OrderResponse(
            id=str(order.order_id),
            customer_id=str(order.customer_id),
            currency=order.currency,
            status=order.status.value,
            version=order.version,
            total_amount=order.total_amount.amount,
            items=item_responses,
        )
