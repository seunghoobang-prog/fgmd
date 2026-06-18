from __future__ import annotations

import pandas as pd
import streamlit as st

from config import REGION_ORDER
from services.email_service import send_order_email
from services.print_service import generate_order_sheet_html
from services.storage import (
    approve_order,
    fulfill_order,
    load_inventory,
    load_orders,
    reject_order,
)

STATUS_LABELS = {
    "pending": "대기",
    "approved": "승인됨",
    "fulfilled": "출고완료",
    "rejected": "거절",
}


def _mask_pw(pw: str) -> str:
    return "****" if pw else ""


def render_order_logs(manager_username: str) -> None:
    orders = load_orders()
    inventory = load_inventory()

    if not orders:
        st.info("주문 로그가 없습니다.")
        return

    st.caption("최신 주문이 위에 표시됩니다. 대기 → 승인 → 출고 완료 순으로 처리하세요.")

    for order in reversed(orders):
        status = order.get("status", "pending")
        with st.expander(
            f"[{STATUS_LABELS.get(status, status)}] {order['id']} · "
            f"{order.get('groupware_id', '')} · {order['venue'][:30]}",
            expanded=(status in ("pending", "approved")),
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**주문번호:** {order['id']}")
                st.markdown(f"**접수일시:** {order['timestamp']}")
                st.markdown(f"**그룹웨어 ID:** {order.get('groupware_id', '-')}")
                st.markdown(f"**그룹웨어 PW:** {_mask_pw(order.get('groupware_pw', ''))}")
                st.markdown(f"**빈소:** {order['venue']}")
            with col2:
                st.markdown(f"**가족관계:** {order['relationship']}")
                st.markdown(f"**조문객 수:** {order['visitor_count']:,}명")
                st.markdown(f"**발송 박스:** {order['boxes']}박스")
                st.markdown(f"**상태:** {STATUS_LABELS.get(status, status)}")
                if order.get("fulfillment_region"):
                    st.markdown(f"**출고 창고:** {order['fulfillment_region']}")

            if status == "pending":
                btn1, btn2 = st.columns(2)
                with btn1:
                    if st.button("승인", key=f"approve_{order['id']}", type="primary"):
                        try:
                            approve_order(order["id"], manager_username)
                            st.success("승인되었습니다.")
                            st.rerun()
                        except ValueError as exc:
                            st.error(str(exc))
                with btn2:
                    if st.button("거절", key=f"reject_{order['id']}"):
                        try:
                            reject_order(order["id"], manager_username)
                            st.warning("거절되었습니다.")
                            st.rerun()
                        except ValueError as exc:
                            st.error(str(exc))

            elif status == "approved":
                available = [r for r in REGION_ORDER if inventory.get(r, 0) >= order["boxes"]]
                if not available:
                    st.error(f"재고 부족: {order['boxes']}박스 이상 보유 창고가 없습니다.")
                else:
                    region = st.selectbox(
                        "출고 창고",
                        options=available,
                        format_func=lambda r: f"{r} (재고 {inventory.get(r, 0)}박스)",
                        key=f"region_{order['id']}",
                    )
                    if st.button("출고 완료", key=f"fulfill_{order['id']}", type="primary"):
                        try:
                            fulfilled = fulfill_order(order["id"], region)
                            html_sheet = generate_order_sheet_html(fulfilled)
                            try:
                                send_order_email(fulfilled, html_sheet)
                                st.success(
                                    f"출고 완료! {region}에서 {fulfilled['boxes']}박스 출고. "
                                    "이메일 발송됨."
                                )
                            except Exception as email_err:
                                st.warning(f"출고 완료, 이메일 발송 실패: {email_err}")
                            st.download_button(
                                label="주문서 다운로드",
                                data=html_sheet,
                                file_name=f"order_{fulfilled['id']}.html",
                                mime="text/html",
                                key=f"dl_{order['id']}",
                            )
                            st.rerun()
                        except ValueError as exc:
                            st.error(str(exc))
                        except Exception as exc:
                            st.error(f"출고 처리 중 오류: {exc}")

    st.markdown("---")
    summary_rows = [
        {
            "주문번호": o["id"],
            "시간": o["timestamp"],
            "그룹웨어ID": o.get("groupware_id", ""),
            "빈소": o["venue"][:20],
            "박스": o["boxes"],
            "상태": STATUS_LABELS.get(o.get("status", ""), o.get("status", "")),
        }
        for o in reversed(orders)
    ]
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)