from __future__ import annotations

from html import escape


def generate_order_sheet_html(order: dict) -> str:
    venue = escape(order["venue"])
    relationship = escape(order["relationship"])
    visitor_count = order["visitor_count"]
    boxes = order["boxes"]
    region = escape(order["fulfillment_region"])
    timestamp = escape(order["timestamp"])
    order_id = escape(order["id"])

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>상조물품 주문서 {order_id}</title>
  <style>
    body {{ font-family: "Malgun Gothic", sans-serif; margin: 40px; color: #222; }}
    h1 {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 12px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 24px; }}
    th, td {{ border: 1px solid #ccc; padding: 12px; text-align: left; }}
    th {{ background: #f5f5f5; width: 30%; }}
    .footer {{ margin-top: 32px; font-size: 0.9em; color: #666; }}
    @media print {{
      body {{ margin: 20px; }}
      button {{ display: none; }}
    }}
  </style>
</head>
<body>
  <h1>상조물품 주문서</h1>
  <table>
    <tr><th>주문번호</th><td>{order_id}</td></tr>
    <tr><th>주문일시</th><td>{timestamp}</td></tr>
    <tr><th>빈소</th><td>{venue}</td></tr>
    <tr><th>가족관계</th><td>{relationship}</td></tr>
    <tr><th>조문객 수</th><td>{visitor_count:,}명</td></tr>
    <tr><th>발송 박스 수</th><td>{boxes}박스</td></tr>
    <tr><th>출고 창고</th><td>{region}</td></tr>
  </table>
  <div class="footer">삼천리 상조물품 관리 시스템 (FGMD)</div>
  <button onclick="window.print()">인쇄</button>
</body>
</html>"""