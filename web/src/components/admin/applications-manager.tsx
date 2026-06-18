"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  approveApplication,
  rejectApplication,
  getAllApplications,
} from "@/lib/actions/applications";
import { REGIONS, APPLICATION_STATUS } from "@/lib/constants";
import { formatDate, formatDateTime } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Modal } from "@/components/ui/modal";
import { Textarea } from "@/components/ui/textarea";
import { StatusBadge } from "@/components/ui/status-badge";
import type { Application } from "@/lib/types/database";
import { toast } from "sonner";

interface ApplicationsManagerProps {
  initialApplications: Application[];
  initialFilters: {
    status?: string;
    region?: string;
    dateFrom?: string;
    dateTo?: string;
  };
}

export function ApplicationsManager({
  initialApplications,
  initialFilters,
}: ApplicationsManagerProps) {
  const router = useRouter();
  const [applications, setApplications] = useState(initialApplications);
  const [filters, setFilters] = useState(initialFilters);

  useEffect(() => {
    setApplications(initialApplications);
  }, [initialApplications]);
  const [selected, setSelected] = useState<Application | null>(null);
  const [comment, setComment] = useState("");
  const [loading, setLoading] = useState(false);

  async function applyFilters() {
    setLoading(true);
    try {
      const data = await getAllApplications(filters);
      setApplications(data);
      const params = new URLSearchParams();
      if (filters.status) params.set("status", filters.status);
      if (filters.region) params.set("region", filters.region);
      if (filters.dateFrom) params.set("dateFrom", filters.dateFrom);
      if (filters.dateTo) params.set("dateTo", filters.dateTo);
      router.push(`/admin/applications?${params.toString()}`);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "조회 실패");
    } finally {
      setLoading(false);
    }
  }

  async function handleApprove() {
    if (!selected) return;
    setLoading(true);
    const result = await approveApplication(selected.id, comment);
    setLoading(false);
    if (!result.success) {
      toast.error(result.error);
      return;
    }
    toast.success("승인되었습니다. 재고가 차감되었습니다.");
    setSelected(null);
    setComment("");
    router.refresh();
  }

  async function handleReject() {
    if (!selected) return;
    setLoading(true);
    const result = await rejectApplication(selected.id, comment);
    setLoading(false);
    if (!result.success) {
      toast.error(result.error);
      return;
    }
    toast.success("반려되었습니다.");
    setSelected(null);
    setComment("");
    router.refresh();
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-4 rounded-xl border border-slate-200 bg-white p-4 sm:grid-cols-2 lg:grid-cols-5">
        <Select
          label="상태"
          value={filters.status || ""}
          onChange={(e) => setFilters({ ...filters, status: e.target.value || undefined })}
          options={[
            { value: "", label: "전체" },
            ...Object.entries(APPLICATION_STATUS).map(([k, v]) => ({
              value: k,
              label: v.label,
            })),
          ]}
        />
        <Select
          label="지역"
          value={filters.region || ""}
          onChange={(e) => setFilters({ ...filters, region: e.target.value || undefined })}
          options={[{ value: "", label: "전체" }, ...REGIONS.map((r) => ({ value: r, label: r }))]}
        />
        <Input
          label="시작일"
          type="date"
          value={filters.dateFrom || ""}
          onChange={(e) => setFilters({ ...filters, dateFrom: e.target.value || undefined })}
        />
        <Input
          label="종료일"
          type="date"
          value={filters.dateTo || ""}
          onChange={(e) => setFilters({ ...filters, dateTo: e.target.value || undefined })}
        />
        <div className="flex items-end">
          <Button onClick={applyFilters} loading={loading} className="w-full">
            필터 적용
          </Button>
        </div>
      </div>

      <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-100 bg-slate-50 text-left text-slate-600">
              <th className="px-4 py-3 font-medium">신청일</th>
              <th className="px-4 py-3 font-medium">신청자</th>
              <th className="px-4 py-3 font-medium">지역</th>
              <th className="px-4 py-3 font-medium">수량</th>
              <th className="px-4 py-3 font-medium">상태</th>
              <th className="px-4 py-3 font-medium"></th>
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
                  <td className="px-4 py-3">
                    {app.employee_name}
                    <span className="block text-xs text-slate-500">{app.employee_id}</span>
                  </td>
                  <td className="px-4 py-3">{app.region}</td>
                  <td className="px-4 py-3">{app.quantity}</td>
                  <td className="px-4 py-3">
                    <StatusBadge status={app.status} />
                  </td>
                  <td className="px-4 py-3">
                    <Button size="sm" variant="secondary" onClick={() => setSelected(app)}>
                      상세
                    </Button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <Modal
        open={!!selected}
        onClose={() => setSelected(null)}
        title="신청 상세"
        footer={
          selected?.status === "pending" ? (
            <>
              <Button variant="secondary" onClick={() => setSelected(null)}>
                닫기
              </Button>
              <Button variant="danger" onClick={handleReject} loading={loading}>
                반려
              </Button>
              <Button onClick={handleApprove} loading={loading}>
                승인
              </Button>
            </>
          ) : (
            <Button variant="secondary" onClick={() => setSelected(null)}>
              닫기
            </Button>
          )
        }
      >
        {selected && (
          <div className="space-y-3 text-sm">
            <div className="grid grid-cols-2 gap-2">
              <p className="text-slate-500">신청자</p>
              <p className="font-medium">{selected.employee_name} ({selected.employee_id})</p>
              <p className="text-slate-500">상품</p>
              <p className="font-medium">{selected.products?.name || "-"}</p>
              <p className="text-slate-500">지역</p>
              <p className="font-medium">{selected.region}</p>
              <p className="text-slate-500">빈소주소</p>
              <p className="font-medium">{selected.address}</p>
              <p className="text-slate-500">수량</p>
              <p className="font-medium">{selected.quantity}</p>
              <p className="text-slate-500">관계</p>
              <p className="font-medium">{selected.relationship}</p>
              <p className="text-slate-500">상태</p>
              <div><StatusBadge status={selected.status} /></div>
              <p className="text-slate-500">신청일</p>
              <p className="font-medium">{formatDateTime(selected.created_at)}</p>
              {selected.approved_at && (
                <>
                  <p className="text-slate-500">처리일</p>
                  <p className="font-medium">{formatDateTime(selected.approved_at)}</p>
                </>
              )}
            </div>
            {selected.status === "pending" && (
              <Textarea
                label="처리 코멘트"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="승인/반려 사유 (선택)"
              />
            )}
          </div>
        )}
      </Modal>
    </div>
  );
}