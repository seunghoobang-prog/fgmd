import Link from "next/link";
import { requireAdmin } from "@/lib/auth";
import { getAllApplications } from "@/lib/actions/applications";
import { getRegionalStockSummary } from "@/lib/actions/inventory";
import { formatDate } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { Button } from "@/components/ui/button";

export default async function AdminDashboardPage() {
  await requireAdmin();

  const [stockSummary, recentApplications] = await Promise.all([
    getRegionalStockSummary(),
    getAllApplications(),
  ]);

  const recent = recentApplications.slice(0, 5);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">관리자 대시보드</h1>
        <p className="mt-1 text-slate-600">지역별 재고 현황과 최근 신청을 확인합니다.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
        {stockSummary.map((item) => (
          <Card key={item.region}>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">{item.region}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-slate-900">{item.totalStock}</p>
              <p className="text-xs text-slate-500 mt-1">총 재고</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>최근 신청 5건</CardTitle>
          <Link href="/admin/applications">
            <Button variant="secondary" size="sm">
              전체 보기
            </Button>
          </Link>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-100 bg-slate-50 text-left text-slate-600">
                  <th className="px-4 py-3 font-medium">신청일</th>
                  <th className="px-4 py-3 font-medium">신청자</th>
                  <th className="px-4 py-3 font-medium">지역</th>
                  <th className="px-4 py-3 font-medium">수량</th>
                  <th className="px-4 py-3 font-medium">상태</th>
                </tr>
              </thead>
              <tbody>
                {recent.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-4 py-8 text-center text-slate-500">
                      신청 내역이 없습니다.
                    </td>
                  </tr>
                ) : (
                  recent.map((app) => (
                    <tr key={app.id} className="border-b border-slate-50">
                      <td className="px-4 py-3">{formatDate(app.created_at)}</td>
                      <td className="px-4 py-3">{app.employee_name}</td>
                      <td className="px-4 py-3">{app.region}</td>
                      <td className="px-4 py-3">{app.quantity}</td>
                      <td className="px-4 py-3">
                        <StatusBadge status={app.status} />
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}