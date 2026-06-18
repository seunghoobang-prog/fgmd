from __future__ import annotations

import pandas as pd
import streamlit as st

from config import REGION_ORDER
from services.database import STATUS_LABELS, get_all_applications, get_inventory_summary


def render_admin_dashboard() -> None:
    st.header("관리자 대시보드")

    inventory = get_inventory_summary()
    cols = st.columns(min(len(REGION_ORDER), 5))
    for idx, region in enumerate(REGION_ORDER):
        with cols[idx % len(cols)]:
            stock = inventory.get(region, 0)
            st.metric(label=region, value=f"{stock}박스")

    st.markdown("---")
    st.subheader("최근 신청 5건")
    recent = get_all_applications()[:5]
    if not recent:
        st.info("최근 신청이 없습니다.")
        return

    rows = []
    for app in recent:
        product_name = (
            app.get("products", {}).get("name")
            if isinstance(app.get("products"), dict)
            else app.get("product_name", "-")
        )
        rows.append(
            {
                "신청일": (app.get("created_at") or "")[:16].replace("T", " "),
                "신청자": app.get("employee_name", ""),
                "지역": app.get("region", ""),
                "상품": product_name,
                "수량": app.get("quantity", 0),
                "상태": STATUS_LABELS.get(app.get("status", ""), app.get("status", "")),
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)