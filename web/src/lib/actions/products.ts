"use server";

import { revalidatePath } from "next/cache";
import { getProfile } from "@/lib/auth";
import { createClient } from "@/lib/supabase/server";
import type { ActionResult, Product } from "@/lib/types/database";

export async function getProducts(): Promise<Product[]> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("products")
    .select("*")
    .order("created_at", { ascending: true });

  if (error) throw new Error(error.message);
  return (data ?? []) as Product[];
}

export interface ProductInput {
  name: string;
  description?: string;
  paymentRule?: string;
  standardQuantity: number;
}

export async function createProduct(input: ProductInput): Promise<ActionResult> {
  const profile = await getProfile();
  if (!profile || profile.role !== "admin") {
    return { success: false, error: "관리자 권한이 필요합니다." };
  }

  if (!input.name?.trim()) return { success: false, error: "상품명을 입력해주세요." };
  if (input.standardQuantity < 0) {
    return { success: false, error: "기준 수량은 0 이상이어야 합니다." };
  }

  const supabase = await createClient();
  const { error } = await supabase.from("products").insert({
    name: input.name.trim(),
    description: input.description?.trim() || null,
    payment_rule: input.paymentRule?.trim() || null,
    standard_quantity: input.standardQuantity,
  });

  if (error) return { success: false, error: error.message };

  revalidatePath("/items");
  revalidatePath("/admin/products");
  revalidatePath("/apply");

  return { success: true };
}

export async function updateProduct(
  id: string,
  input: ProductInput,
): Promise<ActionResult> {
  const profile = await getProfile();
  if (!profile || profile.role !== "admin") {
    return { success: false, error: "관리자 권한이 필요합니다." };
  }

  if (!input.name?.trim()) return { success: false, error: "상품명을 입력해주세요." };

  const supabase = await createClient();
  const { error } = await supabase
    .from("products")
    .update({
      name: input.name.trim(),
      description: input.description?.trim() || null,
      payment_rule: input.paymentRule?.trim() || null,
      standard_quantity: input.standardQuantity,
    })
    .eq("id", id);

  if (error) return { success: false, error: error.message };

  revalidatePath("/items");
  revalidatePath("/admin/products");
  revalidatePath("/apply");

  return { success: true };
}

export async function deleteProduct(id: string): Promise<ActionResult> {
  const profile = await getProfile();
  if (!profile || profile.role !== "admin") {
    return { success: false, error: "관리자 권한이 필요합니다." };
  }

  const supabase = await createClient();
  const { error } = await supabase.from("products").delete().eq("id", id);

  if (error) return { success: false, error: error.message };

  revalidatePath("/items");
  revalidatePath("/admin/products");

  return { success: true };
}