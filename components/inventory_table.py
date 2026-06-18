from __future__ import annotations

import pandas as pd
import streamlit as st

from config import REGION_ORDER
from services.storage import load_inventory, save_inventory


def render_inventory_table() -> dict[str, int]:
    inventory = load_inventory()

    rows = [
        {"지역": region, "재고(박스)": int(inventory.get(region, 0))}
        for region in REGION_ORDER
    ]
    df = pd.DataFrame(rows)

    st.caption("표에서 재고를 직접 수정한 뒤 저장하세요. 지도에 1 아이콘 = 10박스로 반영됩니다.")

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        column_config={
            "지역": st.column_config.TextColumn("지역", disabled=True),
            "재고(박스)": st.column_config.NumberColumn(
                "재고(박스)",
                min_value=0,
                step=1,
                format="%d",
            ),
        },
        key="inventory_editor",
    )

    total = int(edited_df["재고(박스)"].sum())
    summary = edited_df.copy()
    summary.loc[len(summary)] = {"지역": "합계", "재고(박스)": total}
    st.dataframe(summary, use_container_width=True, hide_index=True)

    if st.button("재고 저장", type="secondary", use_container_width=True):
        updated = {
            row["지역"]: int(row["재고(박스)"])
            for _, row in edited_df.iterrows()
        }
        save_inventory(updated)
        st.success("재고가 저장되었습니다. 지도 아이콘이 업데이트됩니다.")
        st.rerun()

    return load_inventory()