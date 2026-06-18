import { getProfile, requireAuth } from "@/lib/auth";
import { Navbar } from "./navbar";

export async function AppShell({ children }: { children: React.ReactNode }) {
  await requireAuth();
  const profile = await getProfile();

  if (!profile) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-slate-600">프로필을 불러올 수 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar profile={profile} />
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6">{children}</main>
    </div>
  );
}