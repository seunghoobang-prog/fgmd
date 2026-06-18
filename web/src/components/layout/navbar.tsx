"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Package, ClipboardList, FileText, LayoutDashboard, Boxes, LogOut } from "lucide-react";
import { signOut } from "@/lib/actions/auth";
import { cn } from "@/lib/utils";
import type { Profile } from "@/lib/types/database";

interface NavbarProps {
  profile: Profile;
}

export function Navbar({ profile }: NavbarProps) {
  const pathname = usePathname();
  const isAdmin = profile.role === "admin";

  const userLinks = [
    { href: "/items", label: "상조물품 안내", icon: Package },
    { href: "/apply", label: "신청하기", icon: FileText },
    { href: "/my-applications", label: "내 신청 내역", icon: ClipboardList },
  ];

  const adminLinks = [
    { href: "/admin", label: "대시보드", icon: LayoutDashboard },
    { href: "/admin/inventory", label: "재고 관리", icon: Boxes },
    { href: "/admin/applications", label: "신청 관리", icon: ClipboardList },
    { href: "/admin/products", label: "상품/규정", icon: Package },
  ];

  const links = isAdmin ? [...userLinks, ...adminLinks] : userLinks;

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
        <div className="flex items-center gap-6">
          <Link href="/items" className="text-lg font-bold text-slate-900">
            상조물품 관리
          </Link>
          <nav className="hidden md:flex items-center gap-1">
            {links.map((link) => {
              const Icon = link.icon;
              const active = pathname === link.href || pathname.startsWith(`${link.href}/`);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={cn(
                    "flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                    active
                      ? "bg-slate-100 text-slate-900"
                      : "text-slate-600 hover:bg-slate-50 hover:text-slate-900",
                  )}
                >
                  <Icon className="h-4 w-4" />
                  {link.label}
                </Link>
              );
            })}
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-medium text-slate-900">{profile.name}</p>
            <p className="text-xs text-slate-500">
              {profile.employee_id || "-"} · {isAdmin ? "관리자" : "일반"}
            </p>
          </div>
          <form action={signOut}>
            <button
              type="submit"
              className="flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm text-slate-600 hover:bg-slate-100"
            >
              <LogOut className="h-4 w-4" />
              <span className="hidden sm:inline">로그아웃</span>
            </button>
          </form>
        </div>
      </div>
      <nav className="flex md:hidden gap-1 overflow-x-auto px-4 pb-2">
        {links.map((link) => {
          const active = pathname === link.href;
          return (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "whitespace-nowrap rounded-lg px-3 py-1.5 text-xs font-medium",
                active ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-600",
              )}
            >
              {link.label}
            </Link>
          );
        })}
      </nav>
    </header>
  );
}