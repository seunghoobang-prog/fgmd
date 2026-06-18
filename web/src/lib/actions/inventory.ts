"use server";

import { revalidatePath } from "next/cache";
import { getProfile } from "@/lib/auth";
import { createClient } from "@/lib/supabase/server";
import type { ActionResult, InventoryRecord } from "@/lib/types/database";

export interface UpdateInventoryInput {
  region: string;
  productId: string;
  stock: number;
  incoming?: number;
  outgoing?: number;
  updateReason: string;
}

export async function getInventoryByRegion(
  region: string,
): Promise<InventoryRecord[]> {
  const supabase = await createClient();

  const { data: products } = await supabase.from("products").select("id, name");

  if (!products?.length) return [];

  const results: InventoryRecord[] = [];

  for (const product of products) {
    const { data } = await supabase
      .from("inventory")
      .select("*, products(name)")
      .eq("region", region)
      .eq("product_id", product.id)
      .order("date", { ascending: false })
      .order("updated_at", { ascending: false })
      .limit(1)
      .maybeSingle();

    if (data) {
      results.push(data as InventoryRecord);
    } else {
      results.push({
        id: "",
        date: new Date().toISOString().slice(0, 10),
        region,
        product_id: product.id,
        stock: 0,
        incoming: 0,
        outgoing: 0,
        update_reason: null,
        updated_by: null,
        updated_at: new Date().toISOString(),
        products: { name: product.name },
      });
    }
  }

  return results;
}

export async function getRegionalStockSummary(): Promise<
  { region: string; totalStock: number }[]
> {
  const supabase = await createClient();
  const { data: products } = await supabase.from("products").select("id");
  if (!products?.length) return [];

  const { REGIONS } = await import("@/lib/constants");
  const summary: { region: string; totalStock: number }[] = [];

  for (const region of REGIONS) {
    let totalStock = 0;
    for (const product of products) {
      const { data } = await supabase
        .from("inventory")
        .select("stock")
        .eq("region", region)
        .eq("product_id", product.id)
        .order("date", { ascending: false })
        .order("updated_at", { ascending: false })
        .limit(1)
        .maybeSingle();
      totalStock += data?.stock ?? 0;
    }
    summary.push({ region, totalStock });
  }

  return summary;
}

export async function updateInventory(
  input: UpdateInventoryInput,
): Promise<ActionResult> {
  const profile = await getProfile();
  if (!profile || profile.role !== "admin") {
    return { success: false, error: "관리자 권한이 필요합니다." };
  }

  if (input.stock < 0) return { success: false, error: "재고는 0 이상이어야 합니다." };
  if (!input.updateReason?.trim()) {
    return { success: false, error: "수정 사유를 입력해주세요." };
  }

  const supabase = await createClient();

  const { error } = await supabase.from("inventory").insert({
    date: new Date().toISOString().slice(0, 10),
    region: input.region,
    product_id: input.productId,
    stock: input.stock,
    incoming: input.incoming ?? 0,
    outgoing: input.outgoing ?? 0,
    update_reason: input.updateReason.trim(),
    updated_by: profile.id,
  });

  if (error) return { success: false, error: error.message };

  revalidatePath("/admin");
  revalidatePath("/admin/inventory");

  return { success: true };
}