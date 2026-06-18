from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
INVENTORY_PATH = DATA_DIR / "inventory.json"
ORDERS_PATH = DATA_DIR / "orders.json"


def _read_json(path: Path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_inventory() -> dict[str, int]:
    return _read_json(INVENTORY_PATH, {})


def save_inventory(inventory: dict[str, int]) -> None:
    _write_json(INVENTORY_PATH, inventory)


def load_orders() -> list[dict]:
    return _read_json(ORDERS_PATH, [])


def append_order(
    *,
    venue: str,
    relationship: str,
    visitor_count: int,
    boxes: int,
    fulfillment_region: str,
) -> dict:
    order = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "venue": venue,
        "relationship": relationship,
        "visitor_count": visitor_count,
        "boxes": boxes,
        "fulfillment_region": fulfillment_region,
        "status": "submitted",
    }
    orders = load_orders()
    orders.append(order)
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