from __future__ import annotations

import pandas as pd
import streamlit as st

from services.database import create_product, delete_product, get_products, update_product


def render_admin_products() -> None:
    st.header("상조물품 마스터 · 지급규정")
    products = get_products()

    tab1, tab2 = st.tabs(["상품 목록", "상품 등록"])

    with tab1:
        if not products:
            st.info("등록된 상품이 없습니다.")
        else:
            for product in products:
                with st.expander(product.get("name", "상품"), expanded=False):
                    with st.form(f"edit_product_{product['id']}"):
                        name = st.text_input("상품명", value=product.get("name", ""))
                        description = st.text_area("설명", value=product.get("description", ""))
                        payment_rule = st.text_area("지급규정", value=product.get("payment_rule", ""))
                        standard_qty = st.number_input(
                            "기준 수량",
                            min_value=0,
                            value=int(product.get("standard_quantity", 1)),
                            step=1,
                        )
                        c1, c2 = st.columns(2)
                        with c1:
                            save = st.form_submit_button("수정 저장", type="primary")
                        with c2:
                            delete = st.form_submit_button("삭제", type="secondary")

                    if save:
                        try:
                            update_product(
                                product["id"],
                                name=name.strip(),
                                description=description.strip(),
                                payment_rule=payment_rule.strip(),
                                standard_quantity=int(standard_qty),
                            )
                            st.toast("상품이 수정되었습니다.", icon="✅")
                            st.rerun()
                        except ValueError as exc:
                            st.error(str(exc))
                    if delete:
                        try:
                            delete_product(product["id"])
                            st.toast("상품이 삭제되었습니다.", icon="🗑️")
                            st.rerun()
                        except Exception as exc:
                            st.error(f"삭제 오류: {exc}")

            df = pd.DataFrame(
                [
                    {
                        "상품명": p.get("name"),
                        "기준수량": p.get("standard_quantity"),
                        "등록일": (p.get("created_at") or "")[:10],
                    }
                    for p in products
                ]
            )
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        with st.form("new_product_form", clear_on_submit=True):
            name = st.text_input("상품명 *")
            description = st.text_area("설명")
            payment_rule = st.text_area("지급규정 *", placeholder="지급 기준, 수량 규칙 등")
            standard_qty = st.number_input("기준 수량", min_value=0, value=1, step=1)
            submitted = st.form_submit_button("등록", type="primary", use_container_width=True)

        if submitted:
            try:
                create_product(
                    name=name,
                    description=description,
                    payment_rule=payment_rule,
                    standard_quantity=int(standard_qty),
                )
                st.toast("상품이 등록되었습니다.", icon="✅")
                st.success("새 상조물품이 등록되었습니다.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"등록 오류: {exc}")