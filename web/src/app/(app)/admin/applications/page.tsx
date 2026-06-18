import { requireAdmin } from "@/lib/auth";
import { getAllApplications } from "@/lib/actions/applications";
import { ApplicationsManager } from "@/components/admin/applications-manager";

interface PageProps {
  searchParams: Promise<{
    status?: string;
    region?: string;
    dateFrom?: string;
    dateTo?: string;
  }>;
}

export default async function AdminApplicationsPage({ searchParams }: PageProps) {
  await requireAdmin();
  const params = await searchParams;

  const filters = {
    status: params.status,
    region: params.region,
    dateFrom: params.dateFrom,
    dateTo: params.dateTo,
  };

  const applications = await getAllApplications(filters);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">신청 관리</h1>
        <p className="mt-1 text-slate-600">신청 LOG를 조회하고 승인/반려 처리합니다.</p>
      </div>
      <ApplicationsManager initialApplications={applications} initialFilters={filters} />
    </div>
  );
}