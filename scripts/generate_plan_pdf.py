"""Generate development planning document as PDF."""

from pathlib import Path

from fpdf import FPDF

FONT_PATH = Path(r"C:\Windows\Fonts\malgun.ttf")
OUTPUT = Path(__file__).resolve().parent.parent / "docs" / "상조물품_재고관리_시스템_개발기획서.pdf"


class PlanPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Malgun", size=9)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, "상조물품 재고관리 시스템 개발 기획서", align="R", new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(0, 0, 0)
            self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Malgun", size=9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"- {self.page_no()} -", align="C")

    def section_title(self, text: str):
        self.ln(4)
        self.set_font("Malgun", "B", 14)
        self.set_text_color(30, 64, 120)
        self.multi_cell(0, 9, text)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def sub_title(self, text: str):
        self.ln(2)
        self.set_font("Malgun", "B", 11)
        self.multi_cell(0, 8, text)
        self.ln(1)

    def body(self, text: str):
        self.set_font("Malgun", size=10)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def bullet(self, text: str):
        self.set_font("Malgun", size=10)
        self.multi_cell(0, 6, f"  • {text}")


def build_pdf() -> None:
    pdf = PlanPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_font("Malgun", "", str(FONT_PATH))
    pdf.add_font("Malgun", "B", str(FONT_PATH))
    pdf.add_page()

    # Cover
    pdf.ln(30)
    pdf.set_font("Malgun", "B", 22)
    pdf.multi_cell(0, 12, "상조물품 재고관리 시스템\n개발 기획서", align="C")
    pdf.ln(10)
    pdf.set_font("Malgun", size=11)
    pdf.multi_cell(
        0,
        8,
        "기술 스택: Next.js + Supabase + Vercel\n"
        "예상 사용자 수: 830명 (월 2~3회 사용)\n"
        "최대 트래픽: 동시 100명 미만 (가벼운 구조)",
        align="C",
    )
    pdf.ln(8)
    pdf.set_font("Malgun", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "작성일: 2026년 6월 18일", align="C")
    pdf.set_text_color(0, 0, 0)

    # 1. 기능명세서
    pdf.add_page()
    pdf.section_title("1. 기능명세서")
    pdf.sub_title("1.1 사용자 역할")
    pdf.body(
        "역할 | 권한 | 설명\n"
        "User | 조회 + 신청 | 일반 직원\n"
        "Admin | 전체 관리 + 승인 | 재고 관리자"
    )

    pdf.sub_title("1.2 주요 기능")
    pdf.body("공통 기능")
    for item in [
        "Supabase Auth 기반 로그인/로그아웃",
        "역할 기반 메뉴 표시 (User/Admin)",
    ]:
        pdf.bullet(item)

    pdf.body("User 기능")
    for item in [
        "상조물품 목록 + 지급규정 조회 (읽기 전용)",
        "신청서 작성 및 제출 (직원사번, 이름, 빈소주소, 필요수량, 본인과의 관계)",
        "본인 신청 내역 조회 (상태 포함)",
    ]:
        pdf.bullet(item)

    pdf.body("Admin 기능")
    for item in [
        "지역별 재고 현황 조회 및 직접 수정",
        "신청 LOG 전체 조회 (필터: 상태, 지역, 기간)",
        "신청 승인 / 반려 처리 (승인 시 자동 재고 차감)",
        "상조물품 마스터 데이터 관리 (추가/수정/삭제)",
        "지급규정 편집",
    ]:
        pdf.bullet(item)

    pdf.body("시스템 기능")
    for item in [
        "신청 승인/반려 시 감사 로그 기록",
        "데이터 유효성 검사 (수량 0 이상, 필수값 체크)",
        "에러 처리 및 사용자 피드백",
    ]:
        pdf.bullet(item)

    # 2. ERD
    pdf.add_page()
    pdf.section_title("2. ERD (Entity Relationship Diagram)")
    pdf.sub_title("주요 테이블")

    tables = [
        (
            "profiles",
            "id (PK), employee_id, name, role (user/admin), created_at",
        ),
        (
            "products",
            "id (PK), name, description, payment_rule, standard_quantity, created_at",
        ),
        (
            "inventory",
            "id (PK), date, region, product_id (FK), stock, incoming, outgoing, "
            "update_reason, updated_by (FK), updated_at",
        ),
        (
            "applications",
            "id (PK), user_id (FK), product_id (FK), employee_id, employee_name, region, "
            "address, quantity, relationship, status (pending/approved/rejected), "
            "approved_by (FK), approved_at, created_at",
        ),
        (
            "application_logs",
            "id (PK), application_id (FK), action (approved/rejected/created), "
            "performed_by (FK), comment, created_at",
        ),
    ]
    for name, cols in tables:
        pdf.set_font("Malgun", "B", 10)
        pdf.multi_cell(0, 6, f"• {name}")
        pdf.set_font("Malgun", size=10)
        pdf.multi_cell(0, 6, f"  {cols}")
        pdf.ln(1)

    pdf.sub_title("주요 포인트")
    for item in [
        "profiles.role 컬럼으로 권한 관리",
        "applications.status로 승인 흐름 제어",
        "inventory는 날짜 + 지역 + 상품 단위로 재고 기록 (히스토리 보존)",
        "application_logs로 승인/반려 감사 추적",
    ]:
        pdf.bullet(item)

    # 3. API
    pdf.add_page()
    pdf.section_title("3. API 스펙 (Next.js + Supabase)")
    pdf.sub_title("기본 원칙")
    for item in [
        "일반 조회/신청 → Supabase Client 직접 사용 (Client Component)",
        "재고 수정, 승인/반려 → Server Actions 사용 (보안 강화)",
    ]:
        pdf.bullet(item)

    pdf.sub_title("주요 Server Actions")
    actions = [
        ("createApplication", "신청서 제출", "User"),
        ("approveApplication", "승인 + 재고 차감 (트랜잭션)", "Admin"),
        ("rejectApplication", "반려 + 로그 기록", "Admin"),
        ("updateInventory", "지역별 재고 수정", "Admin"),
        ("getInventoryByRegion", "지역별 재고 조회", "전체"),
        ("getMyApplications", "본인 신청 내역", "User"),
        ("getAllApplications", "전체 신청 LOG", "Admin"),
    ]
    pdf.set_font("Malgun", "B", 9)
    pdf.cell(55, 7, "기능", border=1)
    pdf.cell(75, 7, "설명", border=1)
    pdf.cell(25, 7, "권한", border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Malgun", size=9)
    for name, desc, role in actions:
        pdf.cell(55, 7, name, border=1)
        pdf.cell(75, 7, desc, border=1)
        pdf.cell(25, 7, role, border=1, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(3)
    pdf.sub_title("트랜잭션 처리 (승인 시)")
    for item in [
        "applications 상태 변경",
        "inventory stock 차감",
        "application_logs 기록",
        "→ Supabase RPC 함수(approve_application)로 begin/commit 처리",
    ]:
        pdf.bullet(item)

    # 4. UI
    pdf.add_page()
    pdf.section_title("4. UI 목업 (주요 화면)")
    pdf.sub_title("4.1 사용자 화면")
    screens_user = [
        ("/items", "상조물품 안내 — 목록 카드 + 지급규정 아코디언 + 신청하기 버튼"),
        ("/apply", "신청 페이지 — 사번, 이름, 빈소주소, 수량, 관계 입력 폼"),
        (
            "/my-applications",
            "내 신청 내역 — 테이블 (신청일, 지역, 수량, 상태, 승인일), "
            "상태 색상: 대기(노랑), 승인(초록), 반려(빨강)",
        ),
    ]
    for path, desc in screens_user:
        pdf.set_font("Malgun", "B", 10)
        pdf.multi_cell(0, 6, path)
        pdf.set_font("Malgun", size=10)
        pdf.multi_cell(0, 6, f"  {desc}")
        pdf.ln(1)

    pdf.sub_title("4.2 관리자 화면")
    screens_admin = [
        ("/admin", "대시보드 — 지역별 재고 요약 카드(5개 지역) + 최근 신청 5건"),
        (
            "/admin/inventory",
            "재고 관리 — 지역 선택 → 테이블(상품명|현재재고|입고|출고|수정) + 수정 모달",
        ),
        (
            "/admin/applications",
            "신청 관리 — 필터(상태/지역/기간) + 승인/반려 버튼 + 상세 모달",
        ),
        ("/admin/products", "상품/지급규정 — 마스터 데이터 CRUD"),
    ]
    for path, desc in screens_admin:
        pdf.set_font("Malgun", "B", 10)
        pdf.multi_cell(0, 6, path)
        pdf.set_font("Malgun", size=10)
        pdf.multi_cell(0, 6, f"  {desc}")
        pdf.ln(1)

    # 5. 기타
    pdf.add_page()
    pdf.section_title("5. 기타 고려사항")
    considerations = [
        ("보안", "RLS 필수. profiles.role = 'admin' 조건으로 정책 작성"),
        ("데이터 정합성", "승인 시 재고 차감 — 반드시 트랜잭션 처리, Race condition 방지"),
        ("성능", "트래픽 매우 낮음. Next.js + Supabase 조합으로 충분, 별도 캐싱 불필요"),
        ("인덱스", "inventory, applications — region, status, created_at, user_id 인덱스 권장"),
        ("알림", "초기: Toast. 추후 이메일(Supabase + Resend) 고도화"),
        ("로그", "application_logs 테이블 필수 — 누가 언제 승인했는지 기록"),
        ("배포", "Vercel + Supabase Hobby 플랜으로 충분"),
        ("확장성", "현재 규모에서 Realtime, Edge Functions 거의 불필요"),
        ("백업", "Supabase 자동 백업 활성화 + 주기적 수동 다운로드 권장"),
        ("모바일", "PC 위주이나 반응형으로 모바일 조회 가능하게 구성"),
    ]
    pdf.set_font("Malgun", "B", 9)
    pdf.cell(35, 7, "항목", border=1)
    pdf.cell(0, 7, "내용", border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Malgun", size=9)
    for key, val in considerations:
        x, y = pdf.get_x(), pdf.get_y()
        pdf.cell(35, 7, key, border=1)
        pdf.multi_cell(0, 7, val, border=1)
        pdf.set_xy(pdf.l_margin, y + 7)

    pdf.ln(4)
    pdf.sub_title("추가 제안")
    for item in [
        "초기에는 Admin 계정 2~3명만 만들고 운영",
        "재고 수정 시 '수정 사유' 입력 필드 필수 (감사 목적)",
        "빈소주소 필수 — 추후 다음 주소 API 연동 고려",
    ]:
        pdf.bullet(item)

    pdf.ln(4)
    pdf.sub_title("배포 현황 (구현 완료)")
    for item in [
        "프로덕션 URL: https://web-kappa-murex-11.vercel.app",
        "Supabase 프로젝트: fgmd (Seoul)",
        "GitHub: https://github.com/seunghoobang-prog/fgmd",
    ]:
        pdf.bullet(item)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT))
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()