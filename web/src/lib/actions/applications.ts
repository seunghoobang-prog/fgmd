"use server";

import { revalidatePath } from "next/cache";
import { getProfile, requireAuth } from "@/lib/auth";
import { createClient } from "@/lib/supabase/server";
import type { ActionResult, Application } from "@/lib/types/database";

export interface CreateApplicationInput {
  productId: string;
  employeeId: string;
  employeeName: string;
  region: string;
  address: string;
  quantity: number;
  relationship: string;
}

export async function createApplication(
  input: CreateApplicationInput,
): Promise<ActionResult<{ id: string }>> {
  const user = await requireAuth();
  const profile = await getProfile();

  if (!input.employeeId?.trim()) return { success: false, error: "직원사번을 입력해주세요." };
  if (!input.employeeName?.trim()) return { success: false, error: "이름을 입력해주세요." };
  if (!input.region?.trim()) return { success: false, error: "지역을 선택해주세요." };
  if (!input.address?.trim()) return { success: false, error: "빈소주소를 입력해주세요." };
  if (!input.relationship?.trim()) return { success: false, error: "본인과의 관계를 입력해주세요." };
  if (!input.quantity || input.quantity < 1) {
    return { success: false, error: "필요수량은 1 이상이어야 합니다." };
  }

  const supabase = await createClient();

  const { data, error } = await supabase
    .from("applications")
    .insert({
      user_id: user.id,
      product_id: input.productId,
      employee_id: input.employeeId.trim(),
      employee_name: input.employeeName.trim(),
      region: input.region,
      address: input.address.trim(),
      quantity: input.quantity,
      relationship: input.relationship.trim(),
      status: "pending",
    })
    .select("id")
    .single();

  if (error) return { success: false, error: error.message };

  await supabase.from("application_logs").insert({
    application_id: data.id,
    action: "created",
    performed_by: user.id,
    comment: "신청서 제출",
  });

  revalidatePath("/my-applications");
  revalidatePath("/admin");
  revalidatePath("/admin/applications");

  return { success: true, data: { id: data.id } };
}

export async function getMyApplications(): Promise<Application[]> {
  const user = await requireAuth();
  const supabase = await createClient();

  const { data, error } = await supabase
    .from("applications")
    .select("*, products(name)")
    .eq("user_id", user.id)
    .order("created_at", { ascending: false });

  if (error) throw new Error(error.message);
  return (data ?? []) as Application[];
}

export interface ApplicationFilters {
  status?: string;
  region?: string;
  dateFrom?: string;
  dateTo?: string;
}

export async function getAllApplications(
  filters: ApplicationFilters = {},
): Promise<Application[]> {
  const profile = await getProfile();
  if (!profile || profile.role !== "admin") {
    throw new Error("관리자 권한이 필요합니다.");
  }

  const supabase = await createClient();
  let query = supabase
    .from("applications")
    .select("*, products(name)")
    .order("created_at", { ascending: false });

  if (filters.status) query = query.eq("status", filters.status);
  if (filters.region) query = query.eq("region", filters.region);
  if (filters.dateFrom) query = query.gte("created_at", filters.dateFrom);
  if (filters.dateTo) query = query.lte("created_at", `${filters.dateTo}T23:59:59`);

  const { data, error } = await query;
  if (error) throw new Error(error.message);
  return (data ?? []) as Application[];
}

export async function approveApplication(
  applicationId: string,
  comment?: string,
): Promise<ActionResult> {
  const profile = await getProfile();
  if (!profile || profile.role !== "admin") {
    return { success: false, error: "관리자 권한이 필요합니다." };
  }

  const supabase = await createClient();
  const { error } = await supabase.rpc("approve_application", {
    p_application_id: applicationId,
    p_admin_id: profile.id,
    p_comment: comment || null,
  });

  if (error) return { success: false, error: error.message };

  revalidatePath("/admin");
  revalidatePath("/admin/applications");
  revalidatePath("/admin/inventory");
  revalidatePath("/my-applications");

  return { success: true };
}

export async function rejectApplication(
  applicationId: string,
  comment?: string,
): Promise<ActionResult> {
  const profile = await getProfile();
  if (!profile || profile.role !== "admin") {
    return { success: false, error: "관리자 권한이 필요합니다." };
  }

  const supabase = await createClient();
  const { error } = await supabase.rpc("reject_application", {
    p_application_id: applicationId,
    p_admin_id: profile.id,
    p_comment: comment || null,
  });

  if (error) return { success: false, error: error.message };

  revalidatePath("/admin");
  revalidatePath("/admin/applications");
  revalidatePath("/my-applications");

  return { success: true };
}