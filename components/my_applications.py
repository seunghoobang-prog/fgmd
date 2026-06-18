from __future__ import annotations

import pandas as pd
import streamlit as st

from services.auth_service import get_current_user
from services.database import STATUS_COLORS, STATUS_LABELS, get_my_applications


def _status_badge(status: str) -> str:
    label = STATUS_LABELS.get(status, status)
    color = STATUS_COLORS.get(status, "#666")
    return f'<span style="background:{color};color:white;padding:2px 8px;border-radius:4px;">{label}</span>'


def render_my_applications() -> None:
    st.header("내 신청 내역")
    user = get_current_user()
    if not user:
        st.warning("로그인이 필요합니다.")
        return

    applications = get_my_applications(user["id"])
    if not applications:
        st.info("신청 내역이 없습니다.")
        return

    rows = []
    for app in applications:
        product_name = app.get("products", {}).get("name") if isinstance(app.get("products"), dict) else app.get("product_name", "-")
        status = app.get("status", "pending")
        rows.append(
            {
                "신청일": (app.get("created_at") or "")[:19].replace("T", " "),
                "상품": product_name,
                "지역": app.get("region", ""),
                "수량": app.get("quantity", 0),
                "상태": STATUS_LABELS.get(status, status),
                "승인일": (app.get("approved_at") or "-")[:19].replace("T", " ") if app.get("approved_at") else "-",
            }
        )

    df = pd.DataFrame(rows)

    def _highlight_status(row):
        status = row["상태"]
        color_map = {"대기": "#fff3cd", "승인": "#d4edda", "반려": "#f8d7da"}
        return [f"background-color: {color_map.get(status, '')}"] * len(row)

    st.dataframe(
        df.style.apply(_highlight_status, axis=1),
        use_container_width=True,
        hide_index=True,
    )

    st.caption("상태: 대기(노랑) · 승인(초록) · 반려(빨강)")