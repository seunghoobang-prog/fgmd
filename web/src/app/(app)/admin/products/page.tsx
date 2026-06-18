import { requireAdmin } from "@/lib/auth";
import { getProducts } from "@/lib/actions/products";
import { ProductsManager } from "@/components/admin/products-manager";

export default async function AdminProductsPage() {
  await requireAdmin();
  const products = await getProducts();

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">상품 및 지급규정 관리</h1>
        <p className="mt-1 text-slate-600">상조물품 마스터 데이터와 지급규정을 관리합니다.</p>
      </div>
      <ProductsManager initialProducts={products} />
    </div>
  );
}