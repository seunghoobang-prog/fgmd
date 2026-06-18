from __future__ import annotations

import streamlit as st

from components.admin_applications import render_admin_applications
from components.admin_dashboard import render_admin_dashboard
from components.admin_inventory import render_admin_inventory
from components.admin_products import render_admin_products
from components.application_form import render_application_form
from components.auth_login import render_auth_header, render_login_page
from components.items_view import render_items_page
from components.map_view import render_map
from components.my_applications import render_my_applications
from services.auth_service import is_admin, is_authenticated
from services.database import get_inventory_summary

USER_PAGES = {
    "상조물품 안내": render_items_page,
    "신청하기": render_application_form,
    "내 신청 내역": render_my_applications,
}

ADMIN_PAGES = {
    "대시보드": render_admin_dashboard,
    "재고 관리": render_admin_inventory,
    "신청 관리": render_admin_applications,
    "마스터 데이터": render_admin_products,
}

st.set_page_config(
    page_title="상조물품현황",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not is_authenticated():
    render_login_page()
    st.stop()

render_auth_header()

pages = ADMIN_PAGES if is_admin() else USER_PAGES
page_names = list(pages.keys())
default_page = page_names[0]
current = st.session_state.get("current_page", default_page)
if current not in page_names:
    current = default_page

with st.sidebar:
    st.markdown("### 메뉴")
    role_label = "Admin" if is_admin() else "User"
    st.caption(f"역할: **{role_label}**")
    selected = st.radio(
        "페이지",
        options=page_names,
        index=page_names.index(current),
        label_visibility="collapsed",
    )
    if selected != current:
        st.session_state["current_page"] = selected
        st.rerun()

    if is_admin():
        st.markdown("---")
        st.subheader("전국 재고 지도")
        inventory = get_inventory_summary()
        render_map(inventory)

st.session_state["current_page"] = selected
pages[selected]()