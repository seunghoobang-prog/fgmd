"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createApplication } from "@/lib/actions/applications";
import { REGIONS } from "@/lib/constants";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import type { Product, Profile } from "@/lib/types/database";
import { toast } from "sonner";

interface ApplicationFormProps {
  products: Product[];
  profile: Profile;
}

export function ApplicationForm({ products, profile }: ApplicationFormProps) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const defaultProduct = products[0];

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!defaultProduct) {
      toast.error("등록된 상조물품이 없습니다.");
      return;
    }

    setLoading(true);
    const form = new FormData(e.currentTarget);

    const result = await createApplication({
      productId: defaultProduct.id,
      employeeId: form.get("employeeId") as string,
      employeeName: form.get("employeeName") as string,
      region: form.get("region") as string,
      address: form.get("address") as string,
      quantity: Number(form.get("quantity")),
      relationship: form.get("relationship") as string,
    });

    setLoading(false);

    if (!result.success) {
      toast.error(result.error);
      return;
    }

    toast.success("신청서가 제출되었습니다.");
    router.push("/my-applications");
  }

  if (!products.length) {
    return (
      <p className="text-slate-600 text-center py-8">
        등록된 상조물품이 없습니다. 관리자에게 문의해주세요.
      </p>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="mx-auto max-w-lg space-y-5">
      <Input
        name="employeeId"
        label="직원사번"
        defaultValue={profile.employee_id || ""}
        required
      />
      <Input
        name="employeeName"
        label="이름"
        defaultValue={profile.name}
        required
      />
      <Select
        name="region"
        label="지역"
        required
        defaultValue={REGIONS[0]}
        options={REGIONS.map((r) => ({ value: r, label: r }))}
      />
      <Input name="address" label="빈소주소" placeholder="상세 주소를 입력하세요" required />
      <Input
        name="quantity"
        label="필요수량"
        type="number"
        min={1}
        defaultValue={1}
        required
      />
      <Input
        name="relationship"
        label="본인과의 관계"
        placeholder="예: 부친, 모친, 배우자"
        required
      />
      <Button type="submit" size="lg" className="w-full" loading={loading}>
        신청서 제출
      </Button>
    </form>
  );
}