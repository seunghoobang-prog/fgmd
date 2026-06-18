import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "개발 기획서 | 상조물품 재고관리 시스템",
  description: "Next.js + Supabase + Vercel 상조물품 재고관리 시스템 개발 기획서",
};

function Section({ id, title, children }: { id: string; title: string; children: React.ReactNode }) {
  return (
    <section id={id} className="scroll-mt-8">
      <h2 className="mb-4 border-b border-slate-200 pb-2 text-xl font-bold text-slate-900">{title}</h2>
      {children}
    </section>
  );
}

function BulletList({ items }: { items: string[] }) {
  return (
    <ul className="list-disc space-y-1.5 pl-5 text-slate-700">
      {items.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  );
}

export default function PlanPage() {
  return (
    <div className="min-h-screen bg-white">
      <header className="border-b border-slate-200 bg-slate-50">
        <div className="mx-auto max-w-3xl px-6 py-10">
          <p className="text-sm font-medium text-slate-500">FGMD Development Plan</p>
          <h1 className="mt-2 text-3xl font-bold text-slate-900">상조물품 재고관리 시스템 개발 기획서</h1>
          <div className="mt-4 flex flex-wrap gap-3 text-sm text-slate-600">
            <span className="rounded-full bg-slate-200 px-3 py-1">Next.js + Supabase + Vercel</span>
            <span className="rounded-full bg-slate-200 px-3 py-1">예상 사용자 830명</span>
            <span className="rounded-full bg-slate-200 px-3 py-1">동시 접속 100명 미만</span>
          </div>
          <p className="mt-4 text-sm text-slate-500">작성일: 2026년 6월 18일 · v1.1 (하네스 원칙 반영)</p>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-6 py-10 space-y-12 text-sm leading-relaxed">
        <nav className="rounded-xl border border-slate-200 bg-slate-50 p-4">
          <p className="mb-2 font-semibold text-slate-800">목차</p>
          <ol className="list-decimal space-y-1 pl-5 text-slate-600">
            <li><a href="#s0" className="hover:text-slate-900">프로젝트 규칙 (하네스 원칙)</a></li>
            <li><a href="#s1" className="hover:text-slate-900">기능명세서</a></li>
            <li><a href="#s2" className="hover:text-slate-900">ERD</a></li>
            <li><a href="#s3" className="hover:text-slate-900">API 스펙</a></li>
            <li><a href="#s4" className="hover:text-slate-900">UI 목업</a></li>
            <li><a href="#s5" className="hover:text-slate-900">기타 고려사항</a></li>
            <li><a href="#s6" className="hover:text-slate-900">배포 현황</a></li>
          </ol>
        </nav>

        <Section id="s0" title="0. 프로젝트 규칙 (하네스 원칙)">
          <div className="mb-6 rounded-xl border border-amber-200 bg-amber-50 p-4 text-slate-800">
            <p className="font-semibold">CLAUDE.md 기반 개발 운영 원칙</p>
            <p className="mt-1 text-slate-600">모든 구현·수정 작업은 아래 규칙을 따릅니다.</p>
          </div>

          <h3 className="mb-2 font-semibold text-slate-800">0.1 작업 원칙</h3>
          <BulletList items={[
            "모든 작업은 Phase 단위로 나눠서 진행한다",
            "각 Phase 완료 후 반드시 검증한다",
            "에러 발생 시 현재 Phase만 되돌린다 (전체 재시작 금지)",
          ]} />

          <h3 className="mb-2 mt-6 font-semibold text-slate-800">0.2 검증 기준</h3>
          <table className="mb-6 w-full border-collapse text-left">
            <thead>
              <tr className="bg-slate-100">
                <th className="border border-slate-200 px-3 py-2">항목</th>
                <th className="border border-slate-200 px-3 py-2">기준</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-slate-200 px-3 py-2 font-medium">빌드 성공</td>
                <td className="border border-slate-200 px-3 py-2"><code className="text-xs">npm run build</code> 에러 없음</td>
              </tr>
              <tr>
                <td className="border border-slate-200 px-3 py-2 font-medium">UI 확인</td>
                <td className="border border-slate-200 px-3 py-2">브라우저에서 화면 정상 표시</td>
              </tr>
              <tr>
                <td className="border border-slate-200 px-3 py-2 font-medium">DB 연동</td>
                <td className="border border-slate-200 px-3 py-2">Supabase 데이터 저장·조회 정상</td>
              </tr>
            </tbody>
          </table>

          <h3 className="mb-2 font-semibold text-slate-800">0.3 실패 시 대응</h3>
          <BulletList items={[
            "에러 발생 시 즉시 수정하지 말고, Plan Mode로 전환하여 원인 분석 후 수정 계획을 먼저 세운다",
            "동일 에러가 3회 이상 반복되면 사용자에게 보고한다",
          ]} />

          <h3 className="mb-2 mt-6 font-semibold text-slate-800">0.4 개발 Phase 로드맵</h3>
          <table className="w-full border-collapse text-left">
            <thead>
              <tr className="bg-slate-100">
                <th className="border border-slate-200 px-3 py-2">Phase</th>
                <th className="border border-slate-200 px-3 py-2">범위</th>
                <th className="border border-slate-200 px-3 py-2">검증</th>
                <th className="border border-slate-200 px-3 py-2">상태</th>
              </tr>
            </thead>
            <tbody>
              {[
                ["P1", "Supabase 스키마 + Auth + RLS", "로그인/로그아웃, 역할 분기", "완료"],
                ["P2", "User 화면 (/items, /apply, /my-applications)", "신청 제출·조회", "완료"],
                ["P3", "Admin 화면 (대시보드, 재고, 신청, 상품)", "승인/반려·재고 차감", "완료"],
                ["P4", "Vercel + Supabase 프로덕션 배포", "빌드·환경변수·접속", "완료"],
                ["P5", "알림·주소 API 등 고도화", "요구 시 Plan 후 진행", "대기"],
              ].map(([phase, scope, verify, status]) => (
                <tr key={phase}>
                  <td className="border border-slate-200 px-3 py-2 font-mono text-xs">{phase}</td>
                  <td className="border border-slate-200 px-3 py-2">{scope}</td>
                  <td className="border border-slate-200 px-3 py-2">{verify}</td>
                  <td className="border border-slate-200 px-3 py-2">
                    <span className={status === "완료" ? "text-emerald-700" : "text-amber-700"}>{status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Section>

        <Section id="s1" title="1. 기능명세서">
          <h3 className="mb-2 font-semibold text-slate-800">1.1 사용자 역할</h3>
          <table className="mb-6 w-full border-collapse text-left">
            <thead>
              <tr className="bg-slate-100">
                <th className="border border-slate-200 px-3 py-2">역할</th>
                <th className="border border-slate-200 px-3 py-2">권한</th>
                <th className="border border-slate-200 px-3 py-2">설명</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-slate-200 px-3 py-2">User</td>
                <td className="border border-slate-200 px-3 py-2">조회 + 신청</td>
                <td className="border border-slate-200 px-3 py-2">일반 직원</td>
              </tr>
              <tr>
                <td className="border border-slate-200 px-3 py-2">Admin</td>
                <td className="border border-slate-200 px-3 py-2">전체 관리 + 승인</td>
                <td className="border border-slate-200 px-3 py-2">재고 관리자</td>
              </tr>
            </tbody>
          </table>

          <h3 className="mb-2 font-semibold text-slate-800">1.2 주요 기능</h3>
          <p className="mb-2 font-medium text-slate-700">공통 기능</p>
          <BulletList items={["Supabase Auth 기반 로그인/로그아웃", "역할 기반 메뉴 표시 (User/Admin)"]} />
          <p className="mb-2 mt-4 font-medium text-slate-700">User 기능</p>
          <BulletList items={[
            "상조물품 목록 + 지급규정 조회 (읽기 전용)",
            "신청서 작성 및 제출 (직원사번, 이름, 빈소주소, 필요수량, 본인과의 관계)",
            "본인 신청 내역 조회 (상태 포함)",
          ]} />
          <p className="mb-2 mt-4 font-medium text-slate-700">Admin 기능</p>
          <BulletList items={[
            "지역별 재고 현황 조회 및 직접 수정",
            "신청 LOG 전체 조회 (필터: 상태, 지역, 기간)",
            "신청 승인 / 반려 처리 (승인 시 자동 재고 차감)",
            "상조물품 마스터 데이터 관리 (추가/수정/삭제)",
            "지급규정 편집",
          ]} />
          <p className="mb-2 mt-4 font-medium text-slate-700">시스템 기능</p>
          <BulletList items={[
            "신청 승인/반려 시 감사 로그 기록",
            "데이터 유효성 검사 (수량 0 이상, 필수값 체크)",
            "에러 처리 및 사용자 피드백",
          ]} />
        </Section>

        <Section id="s2" title="2. ERD (Entity Relationship Diagram)">
          <div className="space-y-4 text-slate-700">
            {[
              ["profiles", "id (PK), employee_id, name, role (user/admin), created_at"],
              ["products", "id (PK), name, description, payment_rule, standard_quantity, created_at"],
              ["inventory", "id (PK), date, region, product_id (FK), stock, incoming, outgoing, update_reason, updated_by (FK), updated_at"],
              ["applications", "id (PK), user_id (FK), product_id (FK), employee_id, employee_name, region, address, quantity, relationship, status, approved_by (FK), approved_at, created_at"],
              ["application_logs", "id (PK), application_id (FK), action, performed_by (FK), comment, created_at"],
            ].map(([name, cols]) => (
              <div key={name}>
                <p className="font-semibold text-slate-900">{name}</p>
                <p className="text-slate-600">{cols}</p>
              </div>
            ))}
          </div>
          <p className="mt-4 font-medium text-slate-700">주요 포인트</p>
          <BulletList items={[
            "profiles.role로 권한 관리",
            "applications.status로 승인 흐름 제어",
            "inventory는 날짜 + 지역 + 상품 단위로 재고 기록 (히스토리 보존)",
            "application_logs로 승인/반려 감사 추적",
          ]} />
        </Section>

        <Section id="s3" title="3. API 스펙 (Next.js + Supabase)">
          <BulletList items={[
            "일반 조회/신청 → Supabase Client (Client Component)",
            "재고 수정, 승인/반려 → Server Actions (보안 강화)",
          ]} />
          <table className="mt-4 w-full border-collapse text-left">
            <thead>
              <tr className="bg-slate-100">
                <th className="border border-slate-200 px-3 py-2">기능</th>
                <th className="border border-slate-200 px-3 py-2">설명</th>
                <th className="border border-slate-200 px-3 py-2">권한</th>
              </tr>
            </thead>
            <tbody>
              {[
                ["createApplication", "신청서 제출", "User"],
                ["approveApplication", "승인 + 재고 차감 (트랜잭션)", "Admin"],
                ["rejectApplication", "반려 + 로그 기록", "Admin"],
                ["updateInventory", "지역별 재고 수정", "Admin"],
                ["getInventoryByRegion", "지역별 재고 조회", "전체"],
                ["getMyApplications", "본인 신청 내역", "User"],
                ["getAllApplications", "전체 신청 LOG", "Admin"],
              ].map(([fn, desc, role]) => (
                <tr key={fn}>
                  <td className="border border-slate-200 px-3 py-2 font-mono text-xs">{fn}</td>
                  <td className="border border-slate-200 px-3 py-2">{desc}</td>
                  <td className="border border-slate-200 px-3 py-2">{role}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="mt-4 text-slate-700">
            승인 시 applications 상태 변경 + inventory stock 차감 + application_logs 기록을
            approve_application RPC로 하나의 트랜잭션 처리합니다.
          </p>
        </Section>

        <Section id="s4" title="4. UI 목업 (주요 화면)">
          <h3 className="mb-2 font-semibold text-slate-800">4.1 사용자 화면</h3>
          <BulletList items={[
            "/items — 상조물품 안내 (목록 카드 + 지급규정 + 신청하기 버튼)",
            "/apply — 신청 페이지 (사번, 이름, 빈소주소, 수량, 관계)",
            "/my-applications — 본인 신청 내역 (상태 색상: 대기/승인/반려)",
          ]} />
          <h3 className="mb-2 mt-4 font-semibold text-slate-800">4.2 관리자 화면</h3>
          <BulletList items={[
            "/admin — 대시보드 (지역별 재고 요약 + 최근 신청 5건)",
            "/admin/inventory — 재고 관리 (지역 선택, 수정 모달)",
            "/admin/applications — 신청 관리 (필터, 승인/반려)",
            "/admin/products — 상품/지급규정 CRUD",
          ]} />
        </Section>

        <Section id="s5" title="5. 기타 고려사항">
          <table className="w-full border-collapse text-left">
            <tbody>
              {[
                ["보안", "RLS 필수, profiles.role = admin 조건"],
                ["데이터 정합성", "승인 시 트랜잭션 처리, Race condition 방지"],
                ["성능", "Next.js + Supabase로 충분, 별도 캐싱 불필요"],
                ["인덱스", "region, status, created_at, user_id"],
                ["알림", "Toast → 추후 이메일(Resend)"],
                ["배포", "Vercel + Supabase Hobby 플랜"],
              ].map(([k, v]) => (
                <tr key={k}>
                  <td className="border border-slate-200 px-3 py-2 font-medium">{k}</td>
                  <td className="border border-slate-200 px-3 py-2">{v}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Section>

        <Section id="s6" title="6. 배포 현황">
          <BulletList items={[
            "웹 앱: https://web-kappa-murex-11.vercel.app",
            "GitHub: https://github.com/seunghoobang-prog/fgmd",
            "Supabase: fgmd (Seoul) — huqychyhlflmazowocla",
          ]} />
        </Section>

        <footer className="border-t border-slate-200 pt-6 text-slate-500">
          <Link href="/login" className="text-slate-700 hover:underline">← 서비스로 이동</Link>
        </footer>
      </main>
    </div>
  );
}