"""
Publish FGMD development plan to Notion.

Usage:
  set NOTION_TOKEN=ntn_xxx
  set NOTION_PARENT_PAGE_ID=optional-page-id
  python scripts/publish_to_notion.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

NOTION_VERSION = "2022-06-28"
BASE = "https://api.notion.com/v1"


def api(token: str, method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        raise RuntimeError(f"Notion API {e.code}: {err}") from e


def rich(text: str, bold: bool = False) -> list:
    return [{"type": "text", "text": {"content": text}, "annotations": {"bold": bold}}]


def heading(level: int, text: str) -> dict:
    key = f"heading_{level}"
    return {"object": "block", "type": key, key: {"rich_text": rich(text)}}


def para(text: str) -> dict:
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich(text)}}


def bullet(text: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rich(text)},
    }


def divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def build_blocks() -> list[dict]:
    return [
        para("기술 스택: Next.js + Supabase + Vercel"),
        para("예상 사용자 수: 830명 (월 2~3회 사용) | 최대 트래픽: 동시 100명 미만"),
        divider(),
        heading(2, "0. 프로젝트 규칙 (하네스 원칙)"),
        heading(3, "작업 원칙"),
        bullet("모든 작업은 Phase 단위로 진행"),
        bullet("각 Phase 완료 후 반드시 검증"),
        bullet("에러 시 현재 Phase만 되돌림 (전체 재시작 금지)"),
        heading(3, "검증 기준"),
        bullet("빌드 성공: npm run build 에러 없음"),
        bullet("UI 확인: 브라우저 정상 표시"),
        bullet("DB 연동: Supabase 저장/조회 정상"),
        heading(3, "실패 시 대응"),
        bullet("에러 시 즉시 수정 금지 → Plan Mode로 원인 분석 후 수정 계획 수립"),
        bullet("동일 에러 3회 이상 반복 시 사용자 보고"),
        divider(),
        heading(2, "1. 기능명세서"),
        heading(3, "1.1 사용자 역할"),
        bullet("User — 조회 + 신청 (일반 직원)"),
        bullet("Admin — 전체 관리 + 승인 (재고 관리자)"),
        heading(3, "1.2 주요 기능"),
        para("공통 기능"),
        bullet("Supabase Auth 기반 로그인/로그아웃"),
        bullet("역할 기반 메뉴 표시 (User/Admin)"),
        para("User 기능"),
        bullet("상조물품 목록 + 지급규정 조회 (읽기 전용)"),
        bullet("신청서 작성 및 제출 (직원사번, 이름, 빈소주소, 필요수량, 본인과의 관계)"),
        bullet("본인 신청 내역 조회 (상태 포함)"),
        para("Admin 기능"),
        bullet("지역별 재고 현황 조회 및 직접 수정"),
        bullet("신청 LOG 전체 조회 (필터: 상태, 지역, 기간)"),
        bullet("신청 승인 / 반려 처리 (승인 시 자동 재고 차감)"),
        bullet("상조물품 마스터 데이터 관리 (추가/수정/삭제)"),
        bullet("지급규정 편집"),
        para("시스템 기능"),
        bullet("신청 승인/반려 시 감사 로그 기록"),
        bullet("데이터 유효성 검사 (수량 0 이상, 필수값 체크)"),
        bullet("에러 처리 및 사용자 피드백"),
        divider(),
        heading(2, "2. ERD"),
        bullet("profiles — id, employee_id, name, role, created_at"),
        bullet("products — id, name, description, payment_rule, standard_quantity"),
        bullet("inventory — date, region, product_id, stock, incoming, outgoing"),
        bullet("applications — user_id, region, address, quantity, status 등"),
        bullet("application_logs — application_id, action, performed_by, comment"),
        para("inventory는 날짜+지역+상품 단위 히스토리 보존. application_logs로 감사 추적."),
        divider(),
        heading(2, "3. API 스펙 (Server Actions)"),
        bullet("createApplication — 신청서 제출 (User)"),
        bullet("approveApplication — 승인 + 재고 차감 트랜잭션 (Admin)"),
        bullet("rejectApplication — 반려 + 로그 (Admin)"),
        bullet("updateInventory — 지역별 재고 수정 (Admin)"),
        bullet("getInventoryByRegion / getMyApplications / getAllApplications"),
        para("승인 시 approve_application RPC로 트랜잭션 처리"),
        divider(),
        heading(2, "4. UI 목업"),
        heading(3, "사용자 화면"),
        bullet("/items — 상조물품 안내 (카드 + 지급규정 + 신청하기)"),
        bullet("/apply — 신청 폼"),
        bullet("/my-applications — 본인 신청 내역 (상태 색상 구분)"),
        heading(3, "관리자 화면"),
        bullet("/admin — 대시보드"),
        bullet("/admin/inventory — 재고 관리"),
        bullet("/admin/applications — 신청 관리"),
        bullet("/admin/products — 상품/지급규정 CRUD"),
        divider(),
        heading(2, "5. 배포 현황"),
        bullet("웹 앱: https://web-kappa-murex-11.vercel.app"),
        bullet("기획서 웹: https://web-kappa-murex-11.vercel.app/plan"),
        bullet("GitHub: https://github.com/seunghoobang-prog/fgmd"),
        bullet("Supabase: fgmd (Seoul) — huqychyhlflmazowocla"),
    ]


def find_parent_page(token: str) -> str | None:
    explicit = os.environ.get("NOTION_PARENT_PAGE_ID", "").strip()
    if explicit:
        return explicit.replace("-", "")

    result = api(token, "POST", "/search", {"page_size": 20})
    for item in result.get("results", []):
        if item.get("object") == "page" and item.get("id"):
            return item["id"]
    return None


def append_blocks(token: str, page_id: str, blocks: list[dict]) -> None:
    chunk_size = 100
    for i in range(0, len(blocks), chunk_size):
        api(
            token,
            "PATCH",
            f"/blocks/{page_id}/children",
            {"children": blocks[i : i + chunk_size]},
        )


def main() -> None:
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        print("NOTION_TOKEN 환경변수가 필요합니다.", file=sys.stderr)
        sys.exit(1)

    parent_id = find_parent_page(token)
    if not parent_id:
        print("연결된 Notion 페이지가 없습니다.", file=sys.stderr)
        print("Notion 앱에서 페이지 열기 → ... → 연결 추가 → '상조물품관리시스템' 선택", file=sys.stderr)
        print("또는 NOTION_PARENT_PAGE_ID 환경변수에 부모 페이지 ID를 설정하세요.", file=sys.stderr)
        sys.exit(2)

    page = api(
        token,
        "POST",
        "/pages",
        {
            "parent": {"type": "page_id", "page_id": parent_id},
            "properties": {
                "title": {
                    "title": [{"type": "text", "text": {"content": "상조물품 재고관리 시스템 개발 기획서"}}],
                }
            },
            "children": build_blocks()[:100],
        },
    )

    page_id = page["id"]
    remaining = build_blocks()[100:]
    if remaining:
        append_blocks(token, page_id, remaining)

    url = page.get("url", f"https://www.notion.so/{page_id.replace('-', '')}")
    print(url)
    print("공개 웹 링크: Notion에서 Share → Publish to web")


if __name__ == "__main__":
    main()