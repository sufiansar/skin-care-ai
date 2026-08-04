import uuid
import logging
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId

from app.core.database import get_db
from app.models.skincare import OrderCreateRequest, OrderResponse, OrderItem

router = APIRouter()
logger = logging.getLogger(__name__)


def serialize_order(doc: dict) -> dict:
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


@router.post("/", response_model=OrderResponse)
async def create_order(body: OrderCreateRequest):
    """
    Create an order directly from Chatbot (Cash on Delivery).
    Calculates delivery fee dynamically: Inside Dhaka ($2.00 / 60 BDT) vs Outside Dhaka ($4.00 / 120 BDT).
    """
    db = get_db()
    if not body.items:
        raise HTTPException(status_code=400, detail="Order items list cannot be empty")

    item_subtotal = sum(i.total_price for i in body.items)
    delivery_fee = 2.00 if body.is_inside_dhaka else 4.00
    location_type = "Inside Dhaka" if body.is_inside_dhaka else "Outside Dhaka"
    grand_total = round(item_subtotal + delivery_fee, 2)

    order_id = f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    doc = {
        "order_id": order_id,
        "items": [i.model_dump() for i in body.items],
        "item_subtotal": item_subtotal,
        "delivery_fee": delivery_fee,
        "location_type": location_type,
        "grand_total": grand_total,
        "currency": "USD",
        "customer_name": body.customer_name,
        "customer_phone": body.customer_phone,
        "customer_address": body.customer_address,
        "customer_email": body.customer_email,
        "notes": body.notes,
        "status": "Pending Admin Confirmation",
        "created_at": datetime.utcnow(),
    }

    if db is not None:
        try:
            result = await db["orders"].insert_one(doc)
            doc["id"] = str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting order into MongoDB: {e}")

    message = (
        f"✅ Order {order_id} placed successfully! "
        f"Total: ${grand_total} (Delivery: ${delivery_fee} - {location_type}). "
        f"An admin will call {body.customer_phone} soon to confirm your Cash on Delivery order."
    )
    doc["message"] = message

    return OrderResponse(**serialize_order(doc))


@router.get("/")
async def list_orders(
    status: Optional[str] = Query(None, description="Filter by status e.g. Pending Admin Confirmation, Confirmed, Shipped"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """Admin endpoint to list all customer orders."""
    db = get_db()
    query = {}
    if status:
        query["status"] = status

    orders = []
    total = 0
    if db is not None:
        try:
            skip = (page - 1) * limit
            total = await db["orders"].count_documents(query)
            orders = await db["orders"].find(query).skip(skip).limit(limit).to_list(length=limit)
        except Exception as e:
            logger.error(f"Error querying orders: {e}")

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "orders": [serialize_order(o) for o in orders]
    }


@router.get("/{order_id}")
async def get_order_detail(order_id: str):
    """Get single order details by Order ID string or ObjectId."""
    db = get_db()
    order = None

    if db is not None:
        try:
            if ObjectId.is_valid(order_id):
                order = await db["orders"].find_one({"_id": ObjectId(order_id)})
            if not order:
                order = await db["orders"].find_one({"order_id": order_id})
        except Exception as e:
            logger.error(f"Error fetching order detail: {e}")

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return serialize_order(order)


@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: str,
    status: str = Query(..., description="New status e.g. Confirmed by Call, Shipped, Delivered, Cancelled"),
):
    """Admin endpoint to update order status after phone call confirmation."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection unavailable")

    query = {"_id": ObjectId(order_id)} if ObjectId.is_valid(order_id) else {"order_id": order_id}
    result = await db["orders"].update_one(query, {"$set": {"status": status, "updated_at": datetime.utcnow()}})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    updated = await db["orders"].find_one(query)
    return {
        "message": f"Order status updated to '{status}'",
        "order": serialize_order(updated)
    }
