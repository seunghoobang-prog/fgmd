from __future__ import annotations

import pandas as pd
import streamlit as st

from config import REGION_ORDER
from services.auth_service import get_current_user
from services.database import get_inventory_by_region, get_products, update_inventory


def render_admin_inventory() -> None:
    st.header("재고 관리")
    user = get_current_user()
    products = get_products()
    if not products:
        st.warning("등록된 상품이 없습니다.")
        return

    product_map = {p["name"]: p["id"] for p in products}

    region = st.selectbox("지역 선택", options=REGION_ORDER)
    rows = get_inventory_by_region(region)

    if not rows:
        st.info(f"{region} 지역 재고 기록이 없습니다.")
    else:
        table_rows = [
            {
                "상품명": r.get("product_name", "-"),
                "현재재고": r.get("stock", 0),
                "입고": r.get("incoming", 0),
                "출고": r.get("outgoing", 0),
                "최종수정": (r.get("updated_at") or "")[:16].replace("T", " "),
            }
            for r in rows
        ]
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

    stock_by_product = {r.get("product_name"): r for r in rows}
    default_product = list(product_map.keys())[0]
    current_row = stock_by_product.get(default_product, {})

    st.markdown("---")
    st.subheader("재고 수정")
    with st.form("inventory_update_form"):
        product_name = st.selectbox("상품", options=list(product_map.keys()), key="inv_product")
        selected_row = stock_by_product.get(product_name, current_row)
        new_stock = st.number_input(
            "현재 재고",
            min_value=0,
            value=int(selected_row.get("stock", 0)),
            step=1,
        )
        incoming = st.number_input("입고", min_value=0, value=0, step=1)
        outgoing = st.number_input("출고", min_value=0, value=0, step=1)
        reason = st.text_area("수정 사유 *", placeholder="재고 실사 반영, 긴급 입고 등")
        submitted = st.form_submit_button("저장", type="primary", use_container_width=True)

    if submitted:
        try:
            update_inventory(
                region=region,
                product_id=product_map[product_name],
                stock=int(new_stock),
                incoming=int(incoming),
                outgoing=int(outgoing),
                update_reason=reason,
                updated_by=user["id"] if user else None,
            )
            st.toast("재고가 저장되었습니다.", icon="✅")
            st.success("재고 수정이 완료되었습니다.")
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"저장 오류: {exc}")