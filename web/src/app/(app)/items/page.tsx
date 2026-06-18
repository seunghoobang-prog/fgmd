import Link from "next/link";
import { ChevronDown } from "lucide-react";
import { getProducts } from "@/lib/actions/products";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default async function ItemsPage() {
  const products = await getProducts();

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">상조물품 안내</h1>
        <p className="mt-1 text-slate-600">상조물품 목록과 지급규정을 확인할 수 있습니다.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {products.map((product) => (
          <Card key={product.id} className="flex flex-col">
            <CardHeader>
              <CardTitle>{product.name}</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-1 flex-col gap-4">
              <p className="text-sm text-slate-600 flex-1">
                {product.description || "설명이 없습니다."}
              </p>
              <details className="group rounded-lg border border-slate-200">
                <summary className="flex cursor-pointer items-center justify-between px-4 py-3 text-sm font-medium text-slate-700">
                  지급규정
                  <ChevronDown className="h-4 w-4 transition-transform group-open:rotate-180" />
                </summary>
                <div className="border-t border-slate-100 px-4 py-3 text-sm text-slate-600">
                  {product.payment_rule || "등록된 지급규정이 없습니다."}
                </div>
              </details>
              <p className="text-xs text-slate-500">
                기준 수량: {product.standard_quantity}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {products.length === 0 && (
        <p className="text-center text-slate-500 py-12">등록된 상조물품이 없습니다.</p>
      )}

      <div className="flex justify-center pt-4">
        <Link href="/apply">
          <Button size="lg">신청하기</Button>
        </Link>
      </div>
    </div>
  );
}