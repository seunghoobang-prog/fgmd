from __future__ import annotations

import streamlit as st

from services.database import get_products


def render_items_page() -> None:
    st.header("상조물품 안내")
    st.caption("상조물품 목록과 지급규정을 확인할 수 있습니다. (읽기 전용)")

    products = get_products()
    if not products:
        st.warning("등록된 상조물품이 없습니다.")
        return

    for product in products:
        with st.container(border=True):
            st.subheader(product.get("name", "상품"))
            if product.get("description"):
                st.markdown(product["description"])
            st.markdown(f"**기준 수량:** {product.get('standard_quantity', 1)}")
            with st.expander("지급규정", expanded=True):
                st.markdown(product.get("payment_rule") or "지급규정이 등록되지 않았습니다.")

    st.markdown("---")
    if st.button("신청하기", type="primary", use_container_width=True):
        st.session_state["current_page"] = "신청하기"
        st.rerun()