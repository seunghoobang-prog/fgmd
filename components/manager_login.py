from __future__ import annotations

import streamlit as st

from services.auth_service import (
    is_manager_authenticated,
    set_manager_authenticated,
    verify_manager,
)


def render_manager_login() -> bool:
    if is_manager_authenticated():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success(f"관리자 로그인: {st.session_state.get('manager_username', '')}")
        with col2:
            if st.button("로그아웃", use_container_width=True):
                set_manager_authenticated(False)
                st.session_state.pop("manager_username", None)
                st.rerun()
        return True

    st.subheader("관리자 로그인")
    username = st.text_input("관리자 ID")
    password = st.text_input("관리자 PW", type="password")

    if st.button("로그인", type="primary", use_container_width=True):
        if verify_manager(username, password):
            set_manager_authenticated(True)
            st.session_state["manager_username"] = username
            st.rerun()
        else:
            st.error("ID 또는 PW가 올바르지 않습니다.")
    return False