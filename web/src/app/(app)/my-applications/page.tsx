import { getMyApplications } from "@/lib/actions/applications";
import { formatDate } from "@/lib/utils";
import { StatusBadge } from "@/components/ui/status-badge";

export default async function MyApplicationsPage() {
  const applications = await getMyApplications();

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">내 신청 내역</h1>
        <p className="mt-1 text-slate-600">제출한 신청서의 처리 상태를 확인할 수 있습니다.</p>
      </div>

      <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-100 bg-slate-50 text-left text-slate-600">
              <th className="px-4 py-3 font-medium">신청일</th>
              <th className="px-4 py-3 font-medium">상품</th>
              <th className="px-4 py-3 font-medium">지역</th>
              <th className="px-4 py-3 font-medium">수량</th>
              <th className="px-4 py-3 font-medium">상태</th>
              <th className="px-4 py-3 font-medium">승인일</th>
            </tr>
          </thead>
          <tbody>
            {applications.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-4 py-8 text-center text-slate-500">
                  신청 내역이 없습니다.
                </td>
              </tr>
            ) : (
              applications.map((app) => (
                <tr key={app.id} className="border-b border-slate-50">
                  <td className="px-4 py-3">{formatDate(app.created_at)}</td>
                  <td className="px-4 py-3">{app.products?.name || "-"}</td>
                  <td className="px-4 py-3">{app.region}</td>
                  <td className="px-4 py-3">{app.quantity}</td>
                  <td className="px-4 py-3">
                    <StatusBadge status={app.status} />
                  </td>
                  <td className="px-4 py-3">{formatDate(app.approved_at)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}