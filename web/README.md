# 상조물품 관리 시스템 (Next.js + Supabase)

기능명세서 기반 상조물품 신청·재고 관리 웹 앱입니다.

## 기능

### 일반 사용자 (User)
- 상조물품 목록 및 지급규정 조회 (`/items`)
- 신청서 작성 및 제출 (`/apply`)
- 본인 신청 내역 조회 (`/my-applications`)

### 관리자 (Admin)
- 대시보드 — 지역별 재고 요약, 최근 신청 (`/admin`)
- 재고 관리 — 지역별 조회/수정 (`/admin/inventory`)
- 신청 관리 — 필터, 승인/반려 (`/admin/applications`)
- 상품/지급규정 CRUD (`/admin/products`)

## 사전 준비

1. [Supabase](https://supabase.com) 프로젝트 생성
2. SQL Editor에서 `../supabase/schema.sql` 실행
3. Authentication → Users에서 테스트 계정 생성
4. SQL로 관리자 권한 부여:

```sql
update public.profiles set role = 'admin' where id = 'USER_UUID';
```

## 로컬 실행

```powershell
cd C:\Users\SKILLSUPPORT\fgmd\web
copy .env.local.example .env.local
# .env.local에 Supabase URL / Anon Key 입력
npm install
npm run dev
```

http://localhost:3000

## 배포

- **Frontend**: Vercel (Hobby 플랜)
- **Backend**: Supabase
- Vercel 환경변수에 `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` 설정

## 프로젝트 구조

```
src/
  app/           # 페이지 (App Router)
  components/    # UI 컴포넌트
  lib/
    actions/     # Server Actions
    supabase/    # Supabase 클라이언트
    types/       # 타입 정의
```

## 보안

- RLS 정책으로 역할 기반 접근 제어
- 승인/반려/재고 수정은 Server Action + RPC 트랜잭션 처리
- `approve_application` RPC에서 재고 차감 및 감사 로그 기록