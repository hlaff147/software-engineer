"""SQLAlchemy Repository implementation for Order Aggregate Root."""

from __future__ import annotations

import json
from decimal import Decimal
from typing import Any

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.order_service.domain.exceptions import OptimisticConcurrencyError
from services.order_service.domain.order_aggregate import Order, OrderLineItem, OrderStatus
from services.order_service.domain.value_objects import (
    CustomerId,
    Money,
    OrderId,
    ProductId,
    Quantity,
    Sku,
)
from services.order_service.infrastructure.orm_models import (
    OrderItemModel,
    OrderModel,
    OrderOutboxEventModel,
)

__all__ = ["SqlAlchemyOrderRepository"]


class SqlAlchemyOrderRepository:
    """Repository managing persistence, optimistic locking, and transactional outbox for Order aggregate."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, order_id: OrderId) -> Order | None:
        stmt = select(OrderModel).where(OrderModel.id == str(order_id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def list_orders(self, offset: int = 0, limit: int = 10) -> tuple[list[Order], int]:
        total_stmt = select(func.count(OrderModel.id))
        total_res = await self.session.execute(total_stmt)
        total_count = total_res.scalar_one() or 0

        stmt = select(OrderModel).offset(offset).limit(limit).order_by(OrderModel.created_at.desc())
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models], total_count

    async def save(self, order: Order) -> None:
        """Atomically persists Order Aggregate, line items, and transactional outbox events."""
        order_id_str = str(order.order_id)
        events_to_persist = order.pull_domain_events()

        if order._loaded_version == 0:
            # Brand new aggregate insertion
            model = OrderModel(
                id=order_id_str,
                customer_id=str(order.customer_id),
                currency=order.currency,
                status=order.status.value,
                version=order.version,
            )
            self.session.add(model)
            await self.session.flush()

            # Insert line items
            for item in order.items:
                item_model = OrderItemModel(
                    id=item.line_item_id,
                    order_id=order_id_str,
                    product_id=int(item.product_id),
                    sku=str(item.sku),
                    product_name=item.product_name,
                    unit_price=item.unit_price.amount,
                    quantity=item.quantity.value,
                )
                self.session.add(item_model)
        else:
            # Optimistic Locking update: enforce version matches loaded_version
            stmt = (
                update(OrderModel)
                .where(
                    OrderModel.id == order_id_str,
                    OrderModel.version == order._loaded_version,
                )
                .values(
                    status=order.status.value,
                    version=order.version,
                )
            )
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                # Concurrent mutation detected!
                raise OptimisticConcurrencyError(
                    f"Order '{order_id_str}' was modified concurrently by another transaction. "
                    f"Expected version {order._loaded_version}."
                )

            # Synchronize line items: delete old items and re-insert current items
            del_stmt = delete(OrderItemModel).where(OrderItemModel.order_id == order_id_str)
            await self.session.execute(del_stmt)

            for item in order.items:
                item_model = OrderItemModel(
                    id=item.line_item_id,
                    order_id=order_id_str,
                    product_id=int(item.product_id),
                    sku=str(item.sku),
                    product_name=item.product_name,
                    unit_price=item.unit_price.amount,
                    quantity=item.quantity.value,
                )
                self.session.add(item_model)

        # Persist Domain Events into Transactional Outbox (same ACID transaction)
        for event in events_to_persist:
            outbox_model = OrderOutboxEventModel(
                id=event.event_id,
                order_id=order_id_str,
                event_type=event.event_type,
                payload_json=json.dumps(event.to_payload()),
                occurred_at=event.occurred_at,
                processed=False,
            )
            self.session.add(outbox_model)

        await self.session.commit()
        # Advance loaded version to match persisted version
        order._loaded_version = order.version

    async def list_events(self, order_id: OrderId) -> list[dict[str, Any]]:
        stmt = (
            select(OrderOutboxEventModel)
            .where(OrderOutboxEventModel.order_id == str(order_id))
            .order_by(OrderOutboxEventModel.occurred_at.asc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [
            {
                "event_id": m.id,
                "order_id": m.order_id,
                "event_type": m.event_type,
                "payload": m.payload,
                "occurred_at": m.occurred_at.isoformat(),
                "processed": m.processed,
            }
            for m in models
        ]

    def _to_domain(self, model: OrderModel) -> Order:
        order = Order(
            order_id=OrderId(model.id),
            customer_id=CustomerId(model.customer_id),
            currency=model.currency,
            status=OrderStatus(model.status),
            version=model.version,
            _loaded_version=model.version,
        )
        for item_m in model.items:
            item = OrderLineItem(
                line_item_id=item_m.id,
                product_id=ProductId(item_m.product_id),
                sku=Sku(item_m.sku),
                product_name=item_m.product_name,
                unit_price=Money(Decimal(str(item_m.unit_price)), model.currency),
                quantity=Quantity(item_m.quantity),
            )
            order._items[str(item.sku)] = item
        return order
