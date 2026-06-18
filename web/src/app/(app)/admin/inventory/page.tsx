import { requireAdmin } from "@/lib/auth";
import { getInventoryByRegion } from "@/lib/actions/inventory";
import { REGIONS } from "@/lib/constants";
import { InventoryManager } from "@/components/admin/inventory-manager";

interface PageProps {
  searchParams: Promise<{ region?: string }>;
}

export default async function AdminInventoryPage({ searchParams }: PageProps) {
  await requireAdmin();
  const params = await searchParams;
  const region = params.region && REGIONS.includes(params.region as typeof REGIONS[number])
    ? params.region
    : REGIONS[0];

  const records = await getInventoryByRegion(region);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">재고 관리</h1>
        <p className="mt-1 text-slate-600">지역별 재고를 조회하고 수정할 수 있습니다.</p>
      </div>
      <InventoryManager initialRegion={region} initialRecords={records} />
    </div>
  );
}