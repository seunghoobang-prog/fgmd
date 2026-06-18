# FGMD 배포 정보

## 프로덕션 URL

| 서비스 | URL |
|--------|-----|
| **웹 앱 (Vercel)** | https://web-kappa-murex-11.vercel.app |
| **Vercel 대시보드** | https://vercel.com/seunghoo-s-projects/web |
| **Supabase 대시보드** | https://supabase.com/dashboard/project/huqychyhlflmazowocla |

## Supabase 프로젝트

| 항목 | 값 |
|------|-----|
| 프로젝트명 | `fgmd` |
| Project Ref | `huqychyhlflmazowocla` |
| 리전 | Northeast Asia (Seoul) |
| API URL | `https://huqychyhlflmazowocla.supabase.co` |

스키마: `supabase/schema.sql` (SQL Editor 또는 `supabase db query --linked -f supabase/schema.sql`)

## 환경변수 (Vercel / 로컬)

`web/.env.local.example` 참고. 실제 값은 Vercel 대시보드 또는 로컬 `.env.local`에 설정.

```
NEXT_PUBLIC_SUPABASE_URL=https://huqychyhlflmazowocla.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<Supabase Dashboard → Settings → API → anon key>
```

## 테스트 계정

| 역할 | 이메일 | 비밀번호 |
|------|--------|----------|
| 관리자 | admin@samchully.co.kr | FgmdAdmin2026! |
| 일반 사용자 | user@samchully.co.kr | FgmdUser2026! |

## 로컬 실행 (Next.js)

```powershell
cd web
copy .env.local.example .env.local
# .env.local에 Supabase 키 입력
npm install
npm run dev
```

## Vercel 재배포

```powershell
cd web
vercel --prod
```

## GitHub

- Repository: https://github.com/seunghoobang-prog/fgmd