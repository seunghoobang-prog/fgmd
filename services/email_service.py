from __future__ import annotations

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st

from config import ORDER_EMAIL_TO


def _smtp_config() -> dict | None:
    try:
        smtp = st.secrets["smtp"]
        return {
            "host": smtp["host"],
            "port": int(smtp.get("port", 587)),
            "username": smtp["username"],
            "password": smtp["password"],
            "from_email": smtp.get("from_email", smtp["username"]),
            "to_email": smtp.get("to_email", ORDER_EMAIL_TO),
            "use_tls": bool(smtp.get("use_tls", True)),
        }
    except (KeyError, FileNotFoundError, AttributeError):
        return None


def send_order_email(order: dict, html_attachment: str) -> None:
    cfg = _smtp_config()
    if cfg is None:
        raise RuntimeError(
            "SMTP 설정이 필요합니다. .streamlit/secrets.toml 파일을 생성해 주세요."
        )

    subject = f"[상조물품 주문] {order['venue']} / {order['timestamp']}"
    body = (
        f"상조물품 주문이 접수되었습니다.\n\n"
        f"주문번호: {order['id']}\n"
        f"빈소: {order['venue']}\n"
        f"가족관계: {order['relationship']}\n"
        f"조문객 수: {order['visitor_count']}\n"
        f"발송 박스 수: {order['boxes']}\n"
        f"출고 창고: {order['fulfillment_region']}\n"
    )

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = cfg["from_email"]
    msg["To"] = cfg["to_email"]
    msg.attach(MIMEText(body, "plain", "utf-8"))

    attachment = MIMEApplication(html_attachment.encode("utf-8"), _subtype="html")
    attachment.add_header(
        "Content-Disposition",
        "attachment",
        filename=f"order_{order['id']}.html",
    )
    msg.attach(attachment)

    with smtplib.SMTP(cfg["host"], cfg["port"], timeout=30) as server:
        if cfg["use_tls"]:
            server.starttls()
        server.login(cfg["username"], cfg["password"])
        server.sendmail(cfg["from_email"], [cfg["to_email"]], msg.as_string())