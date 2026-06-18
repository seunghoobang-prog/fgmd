from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
INVENTORY_PATH = DATA_DIR / "inventory.json"
ORDERS_PATH = DATA_DIR / "orders.json"

ORDER_STATUSES = ("pending", "approved", "fulfilled", "rejected")


def _read_json(path: Path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_inventory() -> dict[str, int]:
    return _read_json(INVENTORY_PATH, {})


def save_inventory(inventory: dict[str, int]) -> None:
    _write_json(INVENTORY_PATH, inventory)


def load_orders() -> list[dict]:
    return _read_json(ORDERS_PATH, [])


def _find_order(order_id: str) -> tuple[list[dict], dict | None, int]:
    orders = load_orders()
    for idx, order in enumerate(orders):
        if order["id"] == order_id:
            return orders, order, idx
    return orders, None, -1


def append_order_request(
    *,
    groupware_id: str,
    groupware_pw: str,
    venue: str,
    relationship: str,
    visitor_count: int,
    boxes: int,
) -> dict:
    order = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": _now_iso(),
        "groupware_id": groupware_id,
        "groupware_pw": groupware_pw,
        "venue": venue,
        "relationship": relationship,
        "visitor_count": visitor_count,
        "boxes": boxes,
        "status": "pending",
        "fulfillment_region": None,
        "approved_at": None,
        "fulfilled_at": None,
        "approved_by": None,
    }
    orders = load_orders()
    orders.append(order)
    _write_json(ORDERS_PATH, orders)
    return order


def approve_order(order_id: str, manager_username: str) -> dict:
    orders, order, idx = _find_order(order_id)
    if order is None:
        raise ValueError(f"주문을 찾을 수 없습니다: {order_id}")
    if order["status"] != "pending":
        raise ValueError(f"승인할 수 없는 상태입니다: {order['status']}")
    order["status"] = "approved"
    order["approved_at"] = _now_iso()
    order["approved_by"] = manager_username
    orders[idx] = order
    _write_json(ORDERS_PATH, orders)
    return order


def reject_order(order_id: str, manager_username: str) -> dict:
    orders, order, idx = _find_order(order_id)
    if order is None:
        raise ValueError(f"주문을 찾을 수 없습니다: {order_id}")
    if order["status"] != "pending":
        raise ValueError(f"거절할 수 없는 상태입니다: {order['status']}")
    order["status"] = "rejected"
    order["approved_at"] = _now_iso()
    order["approved_by"] = manager_username
    orders[idx] = order
    _write_json(ORDERS_PATH, orders)
    return order


def fulfill_order(order_id: str, fulfillment_region: str) -> dict:
    orders, order, idx = _find_order(order_id)
    if order is None:
        raise ValueError(f"주문을 찾을 수 없습니다: {order_id}")
    if order["status"] != "approved":
        raise ValueError(f"출고 완료할 수 없는 상태입니다: {order['status']}")

    deduct_inventory(fulfillment_region, order["boxes"])
    order["status"] = "fulfilled"
    order["fulfillment_region"] = fulfillment_region
    order["fulfilled_at"] = _now_iso()
    orders[idx] = order
    _write_json(ORDERS_PATH, orders)
    return order


def deduct_inventory(region: str, boxes: int) -> dict[str, int]:
    inventory = load_inventory()
    current = inventory.get(region, 0)
    if boxes > current:
        raise ValueError(f"{region} 재고 부족: 요청 {boxes}박스, 보유 {current}박스")
    inventory[region] = current - boxes
    save_inventory(inventory)
    return inventory