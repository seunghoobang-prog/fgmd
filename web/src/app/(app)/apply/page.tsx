import { getProfile } from "@/lib/auth";
import { getProducts } from "@/lib/actions/products";
import { ApplicationForm } from "@/components/applications/application-form";

export default async function ApplyPage() {
  const [products, profile] = await Promise.all([getProducts(), getProfile()]);

  if (!profile) return null;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">상조물품 신청</h1>
        <p className="mt-1 text-slate-600">필수 항목을 입력하고 신청서를 제출하세요.</p>
      </div>
      <ApplicationForm products={products} profile={profile} />
    </div>
  );
}