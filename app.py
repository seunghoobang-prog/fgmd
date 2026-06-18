from __future__ import annotations

import streamlit as st

from components.inventory_table import render_inventory_table
from components.map_view import render_map
from components.order_form import render_order_form

st.set_page_config(
    page_title="상조물품현황",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("상조물품현황")

left, right = st.columns([11, 9], gap="large")

with left:
    st.subheader("재고 현황")
    inventory = render_inventory_table()

    st.subheader("주문서")
    render_order_form(inventory)

with right:
    st.subheader("전국 재고 지도")
    render_map(inventory)