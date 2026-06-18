from __future__ import annotations

import json
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import streamlit as st

from config import REGION_ORDER
from services.supabase_client import get_supabase_client, is_supabase_configured

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PRODUCTS_PATH = DATA_DIR / "products.json"
APPLICATIONS_PATH = DATA_DIR / "applications.json"
INVENTORY_PATH = DATA_DIR / "inventory_records.json"
LOGS_PATH = DATA_DIR / "application_logs.json"
PROFILES_PATH = DATA_DIR / "profiles.json"

APPLICATION_STATUSES = ("pending", "approved", "rejected")
STATUS_LABELS = {
    "pending": "대기",
    "approved": "승인",
    "rejected": "반려",
}
STATUS_COLORS = {
    "pending": "#f0ad4e",
    "approved": "#5cb85c",
    "rejected": "#d9534f",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _new_id() -> str:
    return str(uuid.uuid4())


def _ensure_local_seed() -> None:
    if not PRODUCTS_PATH.exists():
        product_id = _new_id()
        _write_json(
            PRODUCTS_PATH,
            [
                {
                    "id": product_id,
                    "name": "상조물품 박스",
                    "description": "조문용 상조물품 박스",
                    "payment_rule": "조문객 300명당 1박스 지급. 300명 미만 시 1박스.",
                    "standard_quantity": 1,
                    "created_at": _now_iso(),
                }
            ],
        )
    if not INVENTORY_PATH.exists():
        products = _read_json(PRODUCTS_PATH, [])
        product_id = products[0]["id"] if products else _new_id()
        today = date.today().isoformat()
        records = [
            {
                "id": _new_id(),
                "date": today,
                "region": region,
                "product_id": product_id,
                "stock": {"서울": 120, "오산": 85, "전라": 200, "경상": 150, "충청": 95}[region],
                "incoming": 0,
                "outgoing": 0,
                "update_reason": "초기 재고",
                "updated_by": None,
                "updated_at": _now_iso(),
            }
            for region in REGION_ORDER
        ]
        _write_json(INVENTORY_PATH, records)
    if not PROFILES_PATH.exists():
        _write_json(
            PROFILES_PATH,
            [
                {
                    "id": "admin-local",
                    "employee_id": "ADMIN001",
                    "name": "관리자",
                    "role": "admin",
                    "email": "admin@fgmd.local",
                    "password": "admin123",
                    "created_at": _now_iso(),
                },
                {
                    "id": "user-local",
                    "employee_id": "EMP001",
                    "name": "홍길동",
                    "role": "user",
                    "email": "user@fgmd.local",
                    "password": "user123",
                    "created_at": _now_iso(),
                },
            ],
        )


def using_supabase() -> bool:
    return is_supabase_configured()


# ── Products ──────────────────────────────────────────────────────────

def get_products() -> list[dict]:
    if using_supabase():
        client = get_supabase_client()
        result = client.table("products").select("*").order("created_at").execute()
        return result.data or []
    _ensure_local_seed()
    return _read_json(PRODUCTS_PATH, [])


def create_product(*, name: str, description: str, payment_rule: str, standard_quantity: int) -> dict:
    if standard_quantity < 0:
        raise ValueError("기준 수량은 0 이상이어야 합니다.")
    if not name.strip():
        raise ValueError("상품명은 필수입니다.")

    if using_supabase():
        client = get_supabase_client()
        result = (
            client.table("products")
            .insert(
                {
                    "name": name.strip(),
                    "description": description.strip(),
                    "payment_rule": payment_rule.strip(),
                    "standard_quantity": standard_quantity,
                }
            )
            .execute()
        )
        return result.data[0]

    _ensure_local_seed()
    product = {
        "id": _new_id(),
        "name": name.strip(),
        "description": description.strip(),
        "payment_rule": payment_rule.strip(),
        "standard_quantity": standard_quantity,
        "created_at": _now_iso(),
    }
    products = _read_json(PRODUCTS_PATH, [])
    products.append(product)
    _write_json(PRODUCTS_PATH, products)
    return product


def update_product(product_id: str, **fields: Any) -> dict:
    if using_supabase():
        client = get_supabase_client()
        result = client.table("products").update(fields).eq("id", product_id).execute()
        if not result.data:
            raise ValueError("상품을 찾을 수 없습니다.")
        return result.data[0]

    products = _read_json(PRODUCTS_PATH, [])
    for idx, product in enumerate(products):
        if product["id"] == product_id:
            product.update(fields)
            products[idx] = product
            _write_json(PRODUCTS_PATH, products)
            return product
    raise ValueError("상품을 찾을 수 없습니다.")


def delete_product(product_id: str) -> None:
    if using_supabase():
        client = get_supabase_client()
        client.table("products").delete().eq("id", product_id).execute()
        return

    products = [p for p in _read_json(PRODUCTS_PATH, []) if p["id"] != product_id]
    _write_json(PRODUCTS_PATH, products)


# ── Inventory ─────────────────────────────────────────────────────────

def _latest_inventory_records(records: list[dict]) -> dict[tuple[str, str], dict]:
    latest: dict[tuple[str, str], dict] = {}
    for record in records:
        key = (record["region"], record["product_id"])
        existing = latest.get(key)
        if existing is None or (record["date"], record["updated_at"]) >= (
            existing["date"],
            existing["updated_at"],
        ):
            latest[key] = record
    return latest


def get_inventory_summary() -> dict[str, int]:
    """Region -> total stock (primary product aggregated)."""
    records = get_inventory_records()
    summary: dict[str, int] = {region: 0 for region in REGION_ORDER}
    for record in _latest_inventory_records(records).values():
        summary[record["region"]] = summary.get(record["region"], 0) + int(record["stock"])
    return summary


def get_inventory_records(region: str | None = None, product_id: str | None = None) -> list[dict]:
    if using_supabase():
        client = get_supabase_client()
        query = client.table("inventory").select("*")
        if region:
            query = query.eq("region", region)
        if product_id:
            query = query.eq("product_id", product_id)
        result = query.order("date", desc=True).order("updated_at", desc=True).execute()
        return result.data or []

    _ensure_local_seed()
    records = _read_json(INVENTORY_PATH, [])
    if region:
        records = [r for r in records if r["region"] == region]
    if product_id:
        records = [r for r in records if r["product_id"] == product_id]
    return records


def get_inventory_by_region(region: str) -> list[dict]:
    records = get_inventory_records(region=region)
    products = {p["id"]: p for p in get_products()}
    latest = _latest_inventory_records(records)
    rows = []
    for (reg, product_id), record in latest.items():
        if reg != region:
            continue
        product = products.get(product_id, {})
        rows.append({**record, "product_name": product.get("name", "-")})
    return rows


def update_inventory(
    *,
    region: str,
    product_id: str,
    stock: int,
    incoming: int,
    outgoing: int,
    update_reason: str,
    updated_by: str | None,
) -> dict:
    if stock < 0 or incoming < 0 or outgoing < 0:
        raise ValueError("수량은 0 이상이어야 합니다.")
    if not update_reason.strip():
        raise ValueError("수정 사유를 입력해 주세요.")

    payload = {
        "date": date.today().isoformat(),
        "region": region,
        "product_id": product_id,
        "stock": stock,
        "incoming": incoming,
        "outgoing": outgoing,
        "update_reason": update_reason.strip(),
        "updated_by": updated_by,
        "updated_at": _now_iso(),
    }

    if using_supabase():
        client = get_supabase_client()
        result = client.table("inventory").insert(payload).execute()
        return result.data[0]

    record = {"id": _new_id(), **payload}
    records = _read_json(INVENTORY_PATH, [])
    records.append(record)
    _write_json(INVENTORY_PATH, records)
    return record


# ── Applications ──────────────────────────────────────────────────────

def create_application(
    *,
    user_id: str,
    product_id: str,
    employee_id: str,
    employee_name: str,
    region: str,
    address: str,
    quantity: int,
    relationship: str,
) -> dict:
    if quantity <= 0:
        raise ValueError("필요 수량은 1 이상이어야 합니다.")
    for field_name, value in [
        ("employee_id", employee_id),
        ("employee_name", employee_name),
        ("address", address),
        ("relationship", relationship),
        ("region", region),
    ]:
        if not str(value).strip():
            raise ValueError(f"{field_name}은(는) 필수입니다.")

    payload = {
        "user_id": user_id,
        "product_id": product_id,
        "employee_id": employee_id.strip(),
        "employee_name": employee_name.strip(),
        "region": region.strip(),
        "address": address.strip(),
        "quantity": quantity,
        "relationship": relationship.strip(),
        "status": "pending",
    }

    if using_supabase():
        client = get_supabase_client()
        result = client.table("applications").insert(payload).execute()
        app = result.data[0]
        client.table("application_logs").insert(
            {
                "application_id": app["id"],
                "action": "created",
                "performed_by": user_id,
                "comment": "신청서 제출",
            }
        ).execute()
        return app

    application = {
        "id": _new_id(),
        **payload,
        "approved_by": None,
        "approved_at": None,
        "created_at": _now_iso(),
    }
    applications = _read_json(APPLICATIONS_PATH, [])
    applications.append(application)
    _write_json(APPLICATIONS_PATH, applications)
    logs = _read_json(LOGS_PATH, [])
    logs.append(
        {
            "id": _new_id(),
            "application_id": application["id"],
            "action": "created",
            "performed_by": user_id,
            "comment": "신청서 제출",
            "created_at": _now_iso(),
        }
    )
    _write_json(LOGS_PATH, logs)
    return application


def get_my_applications(user_id: str) -> list[dict]:
    if using_supabase():
        client = get_supabase_client()
        result = (
            client.table("applications")
            .select("*, products(name)")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return result.data or []

    apps = [a for a in _read_json(APPLICATIONS_PATH, []) if a.get("user_id") == user_id]
    products = {p["id"]: p for p in get_products()}
    for app in apps:
        app["product_name"] = products.get(app.get("product_id", ""), {}).get("name", "-")
    return sorted(apps, key=lambda a: a.get("created_at", ""), reverse=True)


def get_all_applications(
    *,
    status: str | None = None,
    region: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[dict]:
    if using_supabase():
        client = get_supabase_client()
        query = client.table("applications").select("*, products(name)")
        if status and status != "전체":
            query = query.eq("status", status)
        if region and region != "전체":
            query = query.eq("region", region)
        if date_from:
            query = query.gte("created_at", f"{date_from}T00:00:00")
        if date_to:
            query = query.lte("created_at", f"{date_to}T23:59:59")
        result = query.order("created_at", desc=True).execute()
        return result.data or []

    apps = _read_json(APPLICATIONS_PATH, [])
    products = {p["id"]: p for p in get_products()}
    filtered = []
    for app in apps:
        if status and status != "전체" and app.get("status") != status:
            continue
        if region and region != "전체" and app.get("region") != region:
            continue
        created = app.get("created_at", "")[:10]
        if date_from and created < date_from:
            continue
        if date_to and created > date_to:
            continue
        app["product_name"] = products.get(app.get("product_id", ""), {}).get("name", "-")
        filtered.append(app)
    return sorted(filtered, key=lambda a: a.get("created_at", ""), reverse=True)


def approve_application(application_id: str, admin_id: str, comment: str = "") -> dict:
    if using_supabase():
        client = get_supabase_client()
        client.rpc(
            "approve_application",
            {
                "p_application_id": application_id,
                "p_admin_id": admin_id,
                "p_comment": comment or None,
            },
        ).execute()
        result = client.table("applications").select("*").eq("id", application_id).single().execute()
        return result.data

    applications = _read_json(APPLICATIONS_PATH, [])
    app = next((a for a in applications if a["id"] == application_id), None)
    if app is None:
        raise ValueError("신청을 찾을 수 없습니다.")
    if app["status"] != "pending":
        raise ValueError("대기 상태의 신청만 승인할 수 있습니다.")

    records = _read_json(INVENTORY_PATH, [])
    latest = _latest_inventory_records(records)
    key = (app["region"], app["product_id"])
    current = latest.get(key)
    if current is None or current["stock"] < app["quantity"]:
        raise ValueError(f"{app['region']} 재고가 부족합니다.")

    app["status"] = "approved"
    app["approved_by"] = admin_id
    app["approved_at"] = _now_iso()
    _write_json(APPLICATIONS_PATH, applications)

    new_stock = current["stock"] - app["quantity"]
    records.append(
        {
            "id": _new_id(),
            "date": date.today().isoformat(),
            "region": app["region"],
            "product_id": app["product_id"],
            "stock": new_stock,
            "incoming": 0,
            "outgoing": app["quantity"],
            "update_reason": comment or "신청 승인 출고",
            "updated_by": admin_id,
            "updated_at": _now_iso(),
        }
    )
    _write_json(INVENTORY_PATH, records)

    logs = _read_json(LOGS_PATH, [])
    logs.append(
        {
            "id": _new_id(),
            "application_id": application_id,
            "action": "approved",
            "performed_by": admin_id,
            "comment": comment,
            "created_at": _now_iso(),
        }
    )
    _write_json(LOGS_PATH, logs)
    return app


def reject_application(application_id: str, admin_id: str, comment: str = "") -> dict:
    if using_supabase():
        client = get_supabase_client()
        client.rpc(
            "reject_application",
            {
                "p_application_id": application_id,
                "p_admin_id": admin_id,
                "p_comment": comment or None,
            },
        ).execute()
        result = client.table("applications").select("*").eq("id", application_id).single().execute()
        return result.data

    applications = _read_json(APPLICATIONS_PATH, [])
    app = next((a for a in applications if a["id"] == application_id), None)
    if app is None:
        raise ValueError("신청을 찾을 수 없습니다.")
    if app["status"] != "pending":
        raise ValueError("대기 상태의 신청만 반려할 수 있습니다.")

    app["status"] = "rejected"
    app["approved_by"] = admin_id
    app["approved_at"] = _now_iso()
    _write_json(APPLICATIONS_PATH, applications)

    logs = _read_json(LOGS_PATH, [])
    logs.append(
        {
            "id": _new_id(),
            "application_id": application_id,
            "action": "rejected",
            "performed_by": admin_id,
            "comment": comment,
            "created_at": _now_iso(),
        }
    )
    _write_json(LOGS_PATH, logs)
    return app


def get_application_logs(application_id: str | None = None) -> list[dict]:
    if using_supabase():
        client = get_supabase_client()
        query = client.table("application_logs").select("*")
        if application_id:
            query = query.eq("application_id", application_id)
        result = query.order("created_at", desc=True).execute()
        return result.data or []

    logs = _read_json(LOGS_PATH, [])
    if application_id:
        logs = [log for log in logs if log["application_id"] == application_id]
    return sorted(logs, key=lambda l: l.get("created_at", ""), reverse=True)