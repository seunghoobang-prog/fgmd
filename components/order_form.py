from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from config import REGION_ORDER
from services.email_service import send_order_email
from services.order_logic import calc_boxes
from services.print_service import generate_order_sheet_html
from services.storage import append_order, deduct_inventory, load_inventory


def render_order_form(inventory: dict[str, int]) -> None:
    st.markdown("---")
    st.markdown("**빈소** : 배송 주소")
    venue = st.text_input("빈소 (A)", placeholder="예: 서울특별시 강남구 ...", label_visibility="collapsed")

    st.markdown("**가족관계** : B")
    relationship = st.selectbox(
        "가족관계 (B)",
        options=["배우자", "자녀", "형제/자매", "친척", "기타"],
        label_visibility="collapsed",
    )

    st.markdown("**조문객 수** : C")
    visitor_count = st.number_input(
        "조문객 수 (C)",
        min_value=0,
        value=0,
        step=1,
        label_visibility="collapsed",
    )

    boxes_needed = calc_boxes(int(visitor_count)) if visitor_count > 0 else 0
    st.info(f"발송 박스 수: **{boxes_needed}** (조문객 300명당 1박스, 300명 미만 시 1박스)")

    available_regions = [r for r in REGION_ORDER if inventory.get(r, 0) > 0]
    if not available_regions:
        st.warning("전체 재고가 없습니다. 재고를 추가한 뒤 주문해 주세요.")
        return

    fulfillment_region = st.selectbox(
        "출고 창고",
        options=available_regions,
        format_func=lambda r: f"{r} (재고 {inventory.get(r, 0)}박스)",
    )

    region_stock = inventory.get(fulfillment_region, 0)
    can_order = region_stock >= boxes_needed and boxes_needed > 0 and venue.strip()

    if region_stock < boxes_needed:
        st.error(
            f"{fulfillment_region} 재고 부족: 필요 {boxes_needed}박스, "
            f"보유 {region_stock}박스"
        )
    elif not venue.strip():
        st.caption("빈소 주소를 입력하면 주문할 수 있습니다.")
    elif visitor_count <= 0:
        st.caption("조문객 수를 1명 이상 입력하면 주문할 수 있습니다.")

    submitted = st.button("ORDER", type="primary", disabled=not can_order, use_container_width=True)

    if submitted and can_order:
        try:
            order = append_order(
                venue=venue.strip(),
                relationship=relationship,
                visitor_count=int(visitor_count),
                boxes=boxes_needed,
                fulfillment_region=fulfillment_region,
            )
            deduct_inventory(fulfillment_region, boxes_needed)
            html_sheet = generate_order_sheet_html(order)

            try:
                send_order_email(order, html_sheet)
                st.success(
                    f"주문 완료! {fulfillment_region}에서 {boxes_needed}박스 출고. "
                    f"이메일이 발송되었습니다."
                )
            except Exception as email_err:
                st.warning(f"주문은 저장되었으나 이메일 발송 실패: {email_err}")

            st.download_button(
                label="주문서 다운로드 (HTML)",
                data=html_sheet,
                file_name=f"order_{order['id']}.html",
                mime="text/html",
            )

            components.html(
                html_sheet + "<script>setTimeout(() => window.print(), 500);</script>",
                height=0,
            )
            st.rerun()

        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"주문 처리 중 오류: {exc}")