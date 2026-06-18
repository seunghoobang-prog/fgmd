"""
Publish FGMD development plan to Notion.

Usage:
  set NOTION_TOKEN=secret_xxx
  python scripts/publish_to_notion.py

Get token: https://www.notion.so/my-integrations
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request

NOTION_VERSION = "2025-09-03"
API = "https://api.notion.com/v1/pages"

MARKDOWN = """# 상조물품 재고관리 시스템 개발 기획서

**기술 스택**: Next.js + Supabase + Vercel
**예상 사용자 수**: 830명 (월 2~3회 사용)
**최대 트래픽**: 동시 100명 미만

---

## 1. 기능명세서

### 1.1 사용자 역할

| 역할 | 권한 | 설명 |
|------|------|------|
| User | 조회 + 신청 | 일반 직원 |
| Admin | 전체 관리 + 승인 | 재고 관리자 |

### 1.2 주요 기능

**공통**: Supabase Auth 로그인/로그아웃, 역할 기반 메뉴

**User**: 상조물품 조회, 신청서 제출, 본인 신청 내역

**Admin**: 재고 관리, 신청 LOG, 승인/반려, 상품/지급규정 CRUD

**시스템**: 감사 로그, 유효성 검사, 에러 피드백

## 2. ERD

- profiles, products, inventory, applications, application_logs
- inventory: 날짜+지역+상품 단위 히스토리
- application_logs: 승인/반려 감사 추적

## 3. API (Server Actions)

createApplication, approveApplication, rejectApplication, updateInventory,
getInventoryByRegion, getMyApplications, getAllApplications

승인 시 RPC 트랜잭션 처리

## 4. UI

User: /items, /apply, /my-applications
Admin: /admin, /admin/inventory, /admin/applications, /admin/products

## 5. 배포

- https://web-kappa-murex-11.vercel.app
- https://github.com/seunghoobang-prog/fgmd
"""


def notion_request(token: str, body: dict) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        API,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main() -> None:
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        print("NOTION_TOKEN 환경변수가 필요합니다.", file=sys.stderr)
        print("https://www.notion.so/my-integrations 에서 Integration 생성 후 토큰 입력", file=sys.stderr)
        sys.exit(1)

    body = {
        "parent": {"workspace": True},
        "properties": {
            "title": {
                "title": [{"text": {"content": "상조물품 재고관리 시스템 개발 기획서"}}],
            }
        },
        "markdown": MARKDOWN,
    }

    result = notion_request(token, body)
    page_id = result.get("id", "").replace("-", "")
    url = result.get("url") or f"https://www.notion.so/{page_id}"
    print(f"Created: {url}")
    print("Notion 앱에서 Share → Publish 로 웹 공개 링크를 발급하세요.")


if __name__ == "__main__":
    main()