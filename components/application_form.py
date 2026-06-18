from __future__ import annotations

import streamlit as st

from config import REGION_ORDER
from services.auth_service import get_current_user
from services.database import create_application, get_products


RELATIONSHIP_OPTIONS = ["배우자", "자녀", "부모", "형제/자매", "친척", "동료", "기타"]


def render_application_form() -> None:
    st.header("신청서 작성")
    user = get_current_user()
    if not user:
        st.warning("로그인이 필요합니다.")
        return

    products = get_products()
    if not products:
        st.error("신청 가능한 상조물품이 없습니다.")
        return

    product_options = {p["name"]: p["id"] for p in products}

    with st.form("application_form", clear_on_submit=True):
        st.markdown("#### 신청자 정보")
        employee_id = st.text_input(
            "직원 사번 *",
            value=user.get("employee_id", ""),
            placeholder="예: EMP001",
        )
        employee_name = st.text_input(
            "이름 *",
            value=user.get("name", ""),
            placeholder="홍길동",
        )

        st.markdown("#### 신청 내용")
        product_name = st.selectbox("상조물품 *", options=list(product_options.keys()))
        region = st.selectbox("지역 *", options=REGION_ORDER)
        address = st.text_input("빈소 주소 *", placeholder="예: 서울특별시 강남구 ...")
        quantity = st.number_input("필요 수량 *", min_value=1, value=1, step=1)
        relationship = st.selectbox("본인과의 관계 *", options=RELATIONSHIP_OPTIONS)

        submitted = st.form_submit_button("제출", type="primary", use_container_width=True)

    if submitted:
        try:
            app = create_application(
                user_id=user["id"],
                product_id=product_options[product_name],
                employee_id=employee_id,
                employee_name=employee_name,
                region=region,
                address=address,
                quantity=int(quantity),
                relationship=relationship,
            )
            st.toast("신청서가 제출되었습니다.", icon="✅")
            st.success(
                f"신청이 접수되었습니다. (번호: {str(app['id'])[:8]}) "
                "관리자 승인 후 처리됩니다."
            )
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"제출 중 오류가 발생했습니다: {exc}")