from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from services.database import _read_json, _write_json
from services.supabase_client import get_supabase_client, is_supabase_configured

PROFILES_PATH = Path(__file__).resolve().parent.parent / "data" / "profiles.json"


def _ensure_profiles_seed() -> None:
    if not PROFILES_PATH.exists():
        from services.database import _ensure_local_seed

        _ensure_local_seed()


def is_authenticated() -> bool:
    return st.session_state.get("auth_user") is not None


def get_current_user() -> dict | None:
    return st.session_state.get("auth_user")


def get_user_role() -> str | None:
    user = get_current_user()
    return user.get("role") if user else None


def is_admin() -> bool:
    return get_user_role() == "admin"


def login(email: str, password: str) -> dict:
    email = email.strip()
    password = password.strip()
    if not email or not password:
        raise ValueError("이메일과 비밀번호를 입력해 주세요.")

    if is_supabase_configured():
        client = get_supabase_client()
        auth = client.auth.sign_in_with_password({"email": email, "password": password})
        session = auth.session
        user = auth.user
        if not session or not user:
            raise ValueError("로그인에 실패했습니다.")

        profile_result = (
            client.table("profiles").select("*").eq("id", user.id).single().execute()
        )
        profile = profile_result.data or {}
        auth_user = {
            "id": user.id,
            "email": user.email,
            "employee_id": profile.get("employee_id", ""),
            "name": profile.get("name", user.email.split("@")[0]),
            "role": profile.get("role", "user"),
            "access_token": session.access_token,
        }
    else:
        _ensure_profiles_seed()
        profiles = _read_json(PROFILES_PATH, [])
        matched = next(
            (
                p
                for p in profiles
                if p.get("email", "").lower() == email.lower()
                and p.get("password") == password
            ),
            None,
        )
        if matched is None:
            raise ValueError("이메일 또는 비밀번호가 올바르지 않습니다.")
        auth_user = {
            "id": matched["id"],
            "email": matched["email"],
            "employee_id": matched.get("employee_id", ""),
            "name": matched.get("name", ""),
            "role": matched.get("role", "user"),
            "access_token": None,
        }

    st.session_state["auth_user"] = auth_user
    return auth_user


def logout() -> None:
    if is_supabase_configured():
        try:
            client = get_supabase_client()
            client.auth.sign_out()
        except Exception:
            pass
    st.session_state.pop("auth_user", None)
    st.session_state.pop("current_page", None)


def update_profile_name(user_id: str, name: str) -> None:
    if is_supabase_configured():
        client = get_supabase_client()
        client.table("profiles").update({"name": name.strip()}).eq("id", user_id).execute()
        return

    profiles = _read_json(PROFILES_PATH, [])
    for idx, profile in enumerate(profiles):
        if profile["id"] == user_id:
            profile["name"] = name.strip()
            profiles[idx] = profile
            _write_json(PROFILES_PATH, profiles)
            if st.session_state.get("auth_user", {}).get("id") == user_id:
                st.session_state["auth_user"]["name"] = name.strip()
            return