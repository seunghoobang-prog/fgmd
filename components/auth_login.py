from __future__ import annotations

import streamlit as st

from services.auth_service import get_current_user, is_authenticated, login, logout
from services.supabase_client import is_supabase_configured


def render_login_page() -> None:
    st.title("상조물품 관리 시스템")
    st.caption("FGMD — Funeral Goods Management Dashboard")

    if not is_supabase_configured():
        st.info(
            "로컬 개발 모드입니다. "
            "테스트 계정: `user@fgmd.local` / `user123` (User), "
            "`admin@fgmd.local` / `admin123` (Admin)"
        )

    with st.form("login_form"):
        email = st.text_input("이메일", placeholder="user@company.com")
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("로그인", type="primary", use_container_width=True)

    if submitted:
        try:
            login(email, password)
            st.success("로그인되었습니다.")
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"로그인 오류: {exc}")


def render_auth_header() -> None:
    user = get_current_user()
    if not user:
        return

    col1, col2, col3 = st.columns([4, 2, 1])
    with col1:
        role_label = "관리자" if user.get("role") == "admin" else "사용자"
        st.markdown(f"**{user.get('name', '')}** ({role_label}) · {user.get('email', '')}")
    with col2:
        st.caption(f"사번: {user.get('employee_id') or '-'}")
    with col3:
        if st.button("로그아웃", use_container_width=True):
            logout()
            st.rerun()