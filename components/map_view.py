from __future__ import annotations

import folium
import streamlit as st
from folium import DivIcon
from streamlit_folium import st_folium

from config import (
    BOXES_PER_ICON,
    ICON_SIZE_MAX,
    ICON_SIZE_MIN,
    ICON_SIZE_PER_UNIT,
    MAP_CENTER,
    MAP_ZOOM,
    REGIONS,
    REGION_ORDER,
)


def _icon_size(stock: int) -> float:
    icon_boxes = stock / BOXES_PER_ICON
    size = ICON_SIZE_MIN + icon_boxes * ICON_SIZE_PER_UNIT
    return max(ICON_SIZE_MIN, min(ICON_SIZE_MAX, size))


def _box_icon_html(stock: int, region: str) -> str:
    size = _icon_size(stock)
    icon_boxes = stock / BOXES_PER_ICON
    label = f"{icon_boxes:.1f}" if icon_boxes % 1 else f"{int(icon_boxes)}"
    return f"""
    <div style="
        width:{size}px;
        height:{size}px;
        background:linear-gradient(145deg,#c9a227,#8b6914);
        border:2px solid #5c4a0e;
        border-radius:4px;
        display:flex;
        align-items:center;
        justify-content:center;
        color:white;
        font-weight:bold;
        font-size:{max(10, size * 0.28):.0f}px;
        box-shadow:2px 3px 6px rgba(0,0,0,0.35);
    " title="{region}: {stock}박스">{label}</div>
    """


def render_map(inventory: dict[str, int]) -> None:
    m = folium.Map(location=MAP_CENTER, zoom_start=MAP_ZOOM, tiles="CartoDB positron")

    for region in REGION_ORDER:
        stock = int(inventory.get(region, 0))
        coords = REGIONS[region]
        icon_boxes = stock / BOXES_PER_ICON

        folium.Marker(
            location=[coords["lat"], coords["lng"]],
            popup=folium.Popup(
                f"<b>{region}</b><br>재고: {stock}박스<br>아이콘: {icon_boxes:.1f}개",
                max_width=200,
            ),
            tooltip=f"{region}: {stock}박스",
            icon=DivIcon(
                icon_size=(_icon_size(stock), _icon_size(stock)),
                icon_anchor=(_icon_size(stock) / 2, _icon_size(stock) / 2),
                html=_box_icon_html(stock, region),
            ),
        ).add_to(m)

        folium.map.Marker(
            [coords["lat"], coords["lng"] - 0.15],
            icon=DivIcon(
                icon_size=(60, 20),
                icon_anchor=(30, 10),
                html=f'<div style="font-size:12px;font-weight:bold;text-align:center;color:#333;">{region}</div>',
            ),
        ).add_to(m)

    st_folium(m, width=None, height=520, returned_objects=[])
    st.caption("지도 박스 아이콘 크기: 재고 ÷ 10 (예: 충청 30박스 → 3개 아이콘)")