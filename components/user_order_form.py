from __future__ import annotations

import streamlit as st

from services.order_logic import calc_boxes
from services.storage import append_order_request


def render_user_order_form() -> None:
    st.subheader("그룹웨어 정보")
    groupware_id = st.text_input("그룹웨어 ID", placeholder="사번 또는 아이디")
    groupware_pw = st.text_input("그룹웨어 PW", type="password", placeholder="비밀번호 (기록용)")

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
    st.info(f"예상 발송 박스 수: **{boxes_needed}** (조문객 300명당 1박스, 300명 미만 시 1박스)")

    can_send = (
        groupware_id.strip()
        and groupware_pw.strip()
        and venue.strip()
        and visitor_count > 0
        and boxes_needed > 0
    )

    if not groupware_id.strip() or not groupware_pw.strip():
        st.caption("그룹웨어 ID와 PW를 입력해 주세요.")
    elif not venue.strip():
        st.caption("빈소 주소를 입력해 주세요.")
    elif visitor_count <= 0:
        st.caption("조문객 수를 1명 이상 입력해 주세요.")

    submitted = st.button("전송", type="primary", disabled=not can_send, use_container_width=True)

    if submitted and can_send:
        order = append_order_request(
            groupware_id=groupware_id.strip(),
            groupware_pw=groupware_pw.strip(),
            venue=venue.strip(),
            relationship=relationship,
            visitor_count=int(visitor_count),
            boxes=boxes_needed,
        )
        st.success(
            f"요청이 접수되었습니다. (주문번호: {order['id']}) "
            "관리자 확인 후 처리됩니다."
        )
        st.rerun()