from __future__ import annotations

import streamlit as st


def is_supabase_configured() -> bool:
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["anon_key"]
        return bool(url and key)
    except (KeyError, FileNotFoundError, AttributeError):
        return False


def get_supabase_client():
    if not is_supabase_configured():
        return None
    from supabase import create_client

    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["anon_key"],
    )