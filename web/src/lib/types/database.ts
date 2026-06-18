export type UserRole = "user" | "admin";

export interface Profile {
  id: string;
  employee_id: string | null;
  name: string;
  role: UserRole;
  created_at: string;
}

export interface Product {
  id: string;
  name: string;
  description: string | null;
  payment_rule: string | null;
  standard_quantity: number;
  created_at: string;
}

export interface Application {
  id: string;
  user_id: string;
  product_id: string;
  employee_id: string;
  employee_name: string;
  region: string;
  address: string;
  quantity: number;
  relationship: string;
  status: "pending" | "approved" | "rejected";
  approved_by: string | null;
  approved_at: string | null;
  created_at: string;
  products?: Pick<Product, "name"> | null;
}

export interface InventoryRecord {
  id: string;
  date: string;
  region: string;
  product_id: string;
  stock: number;
  incoming: number;
  outgoing: number;
  update_reason: string | null;
  updated_by: string | null;
  updated_at: string;
  products?: Pick<Product, "name"> | null;
}

export interface ApplicationLog {
  id: string;
  application_id: string;
  action: "approved" | "rejected" | "created";
  performed_by: string | null;
  comment: string | null;
  created_at: string;
}

export type ActionResult<T = void> =
  | { success: true; data?: T }
  | { success: false; error: string };