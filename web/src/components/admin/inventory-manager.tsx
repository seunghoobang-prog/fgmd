"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { updateInventory } from "@/lib/actions/inventory";
import { REGIONS } from "@/lib/constants";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Modal } from "@/components/ui/modal";
import { Textarea } from "@/components/ui/textarea";
import type { InventoryRecord } from "@/lib/types/database";
import { toast } from "sonner";

interface InventoryManagerProps {
  initialRegion: string;
  initialRecords: InventoryRecord[];
}

export function InventoryManager({ initialRegion, initialRecords }: InventoryManagerProps) {
  const router = useRouter();
  const [region, setRegion] = useState(initialRegion);
  const [editing, setEditing] = useState<InventoryRecord | null>(null);
  const [stock, setStock] = useState(0);
  const [incoming, setIncoming] = useState(0);
  const [outgoing, setOutgoing] = useState(0);
  const [reason, setReason] = useState("");
  const [loading, setLoading] = useState(false);

  function openEdit(record: InventoryRecord) {
    setEditing(record);
    setStock(record.stock);
    setIncoming(0);
    setOutgoing(0);
    setReason("");
  }

  async function handleSave() {
    if (!editing) return;
    setLoading(true);

    const result = await updateInventory({
      region,
      productId: editing.product_id,
      stock,
      incoming,
      outgoing,
      updateReason: reason,
    });

    setLoading(false);

    if (!result.success) {
      toast.error(result.error);
      return;
    }

    toast.success("재고가 수정되었습니다.");
    setEditing(null);
    router.refresh();
  }

  function handleRegionChange(newRegion: string) {
    setRegion(newRegion);
    router.push(`/admin/inventory?region=${encodeURIComponent(newRegion)}`);
  }

  return (
    <div className="space-y-6">
      <Select
        label="지역 선택"
        value={region}
        onChange={(e) => handleRegionChange(e.target.value)}
        options={REGIONS.map((r) => ({ value: r, label: r }))}
      />

      <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-100 bg-slate-50 text-left text-slate-600">
              <th className="px-4 py-3 font-medium">상품명</th>
              <th className="px-4 py-3 font-medium">현재재고</th>
              <th className="px-4 py-3 font-medium">최근 입고</th>
              <th className="px-4 py-3 font-medium">최근 출고</th>
              <th className="px-4 py-3 font-medium"></th>
            </tr>
          </thead>
          <tbody>
            {initialRecords.map((record) => (
              <tr key={record.product_id} className="border-b border-slate-50">
                <td className="px-4 py-3 font-medium text-slate-900">
                  {record.products?.name || "-"}
                </td>
                <td className="px-4 py-3">{record.stock}</td>
                <td className="px-4 py-3 text-emerald-600">{record.incoming}</td>
                <td className="px-4 py-3 text-red-600">{record.outgoing}</td>
                <td className="px-4 py-3">
                  <Button size="sm" variant="secondary" onClick={() => openEdit(record)}>
                    수정
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal
        open={!!editing}
        onClose={() => setEditing(null)}
        title={`재고 수정 — ${editing?.products?.name}`}
        footer={
          <>
            <Button variant="secondary" onClick={() => setEditing(null)}>
              취소
            </Button>
            <Button onClick={handleSave} loading={loading}>
              저장
            </Button>
          </>
        }
      >
        <div className="space-y-4">
          <Input
            label="현재재고"
            type="number"
            min={0}
            value={stock}
            onChange={(e) => setStock(Number(e.target.value))}
          />
          <Input
            label="입고"
            type="number"
            min={0}
            value={incoming}
            onChange={(e) => setIncoming(Number(e.target.value))}
          />
          <Input
            label="출고"
            type="number"
            min={0}
            value={outgoing}
            onChange={(e) => setOutgoing(Number(e.target.value))}
          />
          <Textarea
            label="수정 사유"
            required
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="재고 조정 사유를 입력하세요"
          />
        </div>
      </Modal>
    </div>
  );
}