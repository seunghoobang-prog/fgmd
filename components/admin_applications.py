from __future__ import annotations

import pandas as pd
import streamlit as st

from config import REGION_ORDER
from services.auth_service import get_current_user
from services.database import (
    STATUS_LABELS,
    approve_application,
    get_all_applications,
    get_application_logs,
    reject_application,
)


def render_admin_applications() -> None:
    st.header("신청 관리")
    user = get_current_user()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.selectbox("상태", ["전체", "pending", "approved", "rejected"], format_func=lambda s: STATUS_LABELS.get(s, s) if s != "전체" else "전체")
    with col2:
        region_filter = st.selectbox("지역", ["전체"] + REGION_ORDER)
    with col3:
        date_from = st.date_input("시작일", value=None)
    with col4:
        date_to = st.date_input("종료일", value=None)

    applications = get_all_applications(
        status=status_filter,
        region=region_filter,
        date_from=date_from.isoformat() if date_from else None,
        date_to=date_to.isoformat() if date_to else None,
    )

    if not applications:
        st.info("조건에 맞는 신청이 없습니다.")
        return

    for app in applications:
        status = app.get("status", "pending")
        product_name = (
            app.get("products", {}).get("name")
            if isinstance(app.get("products"), dict)
            else app.get("product_name", "-")
        )
        short_id = str(app["id"])[:8]
        with st.expander(
            f"[{STATUS_LABELS.get(status, status)}] {short_id} · "
            f"{app.get('employee_name', '')} · {app.get('region', '')}",
            expanded=(status == "pending"),
        ):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**사번:** {app.get('employee_id', '')}")
                st.markdown(f"**이름:** {app.get('employee_name', '')}")
                st.markdown(f"**상품:** {product_name}")
                st.markdown(f"**지역:** {app.get('region', '')}")
            with c2:
                st.markdown(f"**수량:** {app.get('quantity', 0)}")
                st.markdown(f"**관계:** {app.get('relationship', '')}")
                st.markdown(f"**빈소:** {app.get('address', '')}")
                st.markdown(f"**신청일:** {(app.get('created_at') or '')[:19]}")

            logs = get_application_logs(app["id"])
            if logs:
                st.caption("감사 로그")
                for log in logs[:3]:
                    st.text(
                        f"· {log.get('action')} / "
                        f"{(log.get('created_at') or '')[:16]} / "
                        f"{log.get('comment') or ''}"
                    )

            if status == "pending":
                comment = st.text_input("코멘트", key=f"comment_{app['id']}", placeholder="승인/반려 사유 (선택)")
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("승인", key=f"approve_{app['id']}", type="primary"):
                        try:
                            approve_application(app["id"], user["id"], comment)
                            st.toast("승인되었습니다. 재고가 차감되었습니다.", icon="✅")
                            st.rerun()
                        except ValueError as exc:
                            st.error(str(exc))
                        except Exception as exc:
                            st.error(f"승인 오류: {exc}")
                with b2:
                    if st.button("반려", key=f"reject_{app['id']}"):
                        try:
                            reject_application(app["id"], user["id"], comment)
                            st.toast("반려 처리되었습니다.", icon="⚠️")
                            st.rerun()
                        except ValueError as exc:
                            st.error(str(exc))
                        except Exception as exc:
                            st.error(f"반려 오류: {exc}")

    st.markdown("---")
    summary = [
        {
            "번호": str(a["id"])[:8],
            "신청자": a.get("employee_name", ""),
            "지역": a.get("region", ""),
            "수량": a.get("quantity", 0),
            "상태": STATUS_LABELS.get(a.get("status", ""), ""),
            "신청일": (a.get("created_at") or "")[:16],
        }
        for a in applications
    ]
    st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)