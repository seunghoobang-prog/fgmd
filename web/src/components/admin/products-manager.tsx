"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createProduct, updateProduct, deleteProduct } from "@/lib/actions/products";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Modal } from "@/components/ui/modal";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Product } from "@/lib/types/database";
import { toast } from "sonner";
import { Pencil, Plus, Trash2 } from "lucide-react";

export function ProductsManager({ initialProducts }: { initialProducts: Product[] }) {
  const router = useRouter();
  const [products, setProducts] = useState(initialProducts);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Product | null>(null);
  const [loading, setLoading] = useState(false);

  function openCreate() {
    setEditing(null);
    setModalOpen(true);
  }

  function openEdit(product: Product) {
    setEditing(product);
    setModalOpen(true);
  }

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);

    const form = new FormData(e.currentTarget);
    const input = {
      name: form.get("name") as string,
      description: form.get("description") as string,
      paymentRule: form.get("paymentRule") as string,
      standardQuantity: Number(form.get("standardQuantity")),
    };

    const result = editing
      ? await updateProduct(editing.id, input)
      : await createProduct(input);

    setLoading(false);

    if (!result.success) {
      toast.error(result.error);
      return;
    }

    toast.success(editing ? "상품이 수정되었습니다." : "상품이 추가되었습니다.");
    setModalOpen(false);
    router.refresh();
  }

  async function handleDelete(id: string) {
    if (!confirm("정말 삭제하시겠습니까?")) return;
    setLoading(true);
    const result = await deleteProduct(id);
    setLoading(false);
    if (!result.success) {
      toast.error(result.error);
      return;
    }
    toast.success("삭제되었습니다.");
    setProducts(products.filter((p) => p.id !== id));
    router.refresh();
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-end">
        <Button onClick={openCreate}>
          <Plus className="h-4 w-4" />
          상품 추가
        </Button>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {products.map((product) => (
          <Card key={product.id}>
            <CardHeader className="flex flex-row items-start justify-between">
              <CardTitle>{product.name}</CardTitle>
              <div className="flex gap-1">
                <Button size="sm" variant="ghost" onClick={() => openEdit(product)}>
                  <Pencil className="h-4 w-4" />
                </Button>
                <Button size="sm" variant="ghost" onClick={() => handleDelete(product.id)}>
                  <Trash2 className="h-4 w-4 text-red-500" />
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-2 text-sm text-slate-600">
              <p>{product.description || "설명 없음"}</p>
              <div className="rounded-lg bg-slate-50 p-3">
                <p className="text-xs font-medium text-slate-500 mb-1">지급규정</p>
                <p className="text-slate-800">{product.payment_rule || "-"}</p>
              </div>
              <p className="text-xs text-slate-500">
                기준 수량: {product.standard_quantity}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editing ? "상품 수정" : "상품 추가"}
        footer={
          <>
            <Button variant="secondary" onClick={() => setModalOpen(false)}>
              취소
            </Button>
            <Button type="submit" form="product-form" loading={loading}>
              저장
            </Button>
          </>
        }
      >
        <form id="product-form" onSubmit={handleSubmit} className="space-y-4">
          <Input
            name="name"
            label="상품명"
            defaultValue={editing?.name}
            required
          />
          <Textarea
            name="description"
            label="설명"
            defaultValue={editing?.description || ""}
          />
          <Textarea
            name="paymentRule"
            label="지급규정"
            defaultValue={editing?.payment_rule || ""}
            placeholder="조문객 300명당 1박스 지급..."
          />
          <Input
            name="standardQuantity"
            label="기준 수량"
            type="number"
            min={0}
            defaultValue={editing?.standard_quantity ?? 1}
            required
          />
        </form>
      </Modal>
    </div>
  );
}

// Fix prop name mismatch - I used ProductsManagerProps but destructured initialProducts
// Let me fix the component - I had interface ProductsManagerProps with products but used initialProducts