-- FGMD Supabase Schema
-- Run in Supabase SQL Editor after creating a project.

-- Extensions
create extension if not exists "uuid-ossp";

-- Profiles (extends auth.users)
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  employee_id text,
  name text not null,
  role text not null default 'user' check (role in ('user', 'admin')),
  created_at timestamptz not null default now()
);

create index if not exists idx_profiles_role on public.profiles(role);
create index if not exists idx_profiles_employee_id on public.profiles(employee_id);

-- Products (상조물품 마스터)
create table if not exists public.products (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  description text,
  payment_rule text,
  standard_quantity int not null default 1 check (standard_quantity >= 0),
  created_at timestamptz not null default now()
);

-- Applications (신청)
create table if not exists public.applications (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid not null references public.profiles(id),
  product_id uuid not null references public.products(id),
  employee_id text not null,
  employee_name text not null,
  region text not null,
  address text not null,
  quantity int not null check (quantity > 0),
  relationship text not null,
  status text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  approved_by uuid references public.profiles(id),
  approved_at timestamptz,
  created_at timestamptz not null default now()
);

create index if not exists idx_applications_user_id on public.applications(user_id);
create index if not exists idx_applications_status on public.applications(status);
create index if not exists idx_applications_region on public.applications(region);
create index if not exists idx_applications_created_at on public.applications(created_at desc);

-- Inventory (날짜 + 지역 + 상품 단위 히스토리)
create table if not exists public.inventory (
  id uuid primary key default uuid_generate_v4(),
  date date not null default current_date,
  region text not null,
  product_id uuid not null references public.products(id),
  stock int not null default 0 check (stock >= 0),
  incoming int not null default 0 check (incoming >= 0),
  outgoing int not null default 0 check (outgoing >= 0),
  update_reason text,
  updated_by uuid references public.profiles(id),
  updated_at timestamptz not null default now()
);

create index if not exists idx_inventory_region on public.inventory(region);
create index if not exists idx_inventory_product_id on public.inventory(product_id);
create index if not exists idx_inventory_date on public.inventory(date desc);

-- Application audit logs
create table if not exists public.application_logs (
  id uuid primary key default uuid_generate_v4(),
  application_id uuid not null references public.applications(id) on delete cascade,
  action text not null check (action in ('approved', 'rejected', 'created')),
  performed_by uuid references public.profiles(id),
  comment text,
  created_at timestamptz not null default now()
);

create index if not exists idx_application_logs_application_id on public.application_logs(application_id);

-- Auto-create profile on signup
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, employee_id, name, role)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'employee_id', ''),
    coalesce(new.raw_user_meta_data->>'name', split_part(new.email, '@', 1)),
    coalesce(new.raw_user_meta_data->>'role', 'user')
  );
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- Approve application with inventory deduction (transactional)
create or replace function public.approve_application(
  p_application_id uuid,
  p_admin_id uuid,
  p_comment text default null
)
returns void
language plpgsql
security definer set search_path = public
as $$
declare
  v_app public.applications%rowtype;
  v_latest_stock int;
begin
  select * into v_app from public.applications where id = p_application_id for update;
  if not found then
    raise exception 'Application not found';
  end if;
  if v_app.status <> 'pending' then
    raise exception 'Application is not pending';
  end if;

  select stock into v_latest_stock
  from public.inventory
  where region = v_app.region and product_id = v_app.product_id
  order by date desc, updated_at desc
  limit 1
  for update;

  if v_latest_stock is null or v_latest_stock < v_app.quantity then
    raise exception 'Insufficient stock in region %', v_app.region;
  end if;

  update public.applications
  set status = 'approved', approved_by = p_admin_id, approved_at = now()
  where id = p_application_id;

  insert into public.inventory (date, region, product_id, stock, incoming, outgoing, update_reason, updated_by)
  values (
    current_date, v_app.region, v_app.product_id,
    v_latest_stock - v_app.quantity, 0, v_app.quantity,
    coalesce(p_comment, '신청 승인 출고'), p_admin_id
  );

  insert into public.application_logs (application_id, action, performed_by, comment)
  values (p_application_id, 'approved', p_admin_id, p_comment);
end;
$$;

create or replace function public.reject_application(
  p_application_id uuid,
  p_admin_id uuid,
  p_comment text default null
)
returns void
language plpgsql
security definer set search_path = public
as $$
declare
  v_status text;
begin
  select status into v_status from public.applications where id = p_application_id for update;
  if v_status is null then
    raise exception 'Application not found';
  end if;
  if v_status <> 'pending' then
    raise exception 'Application is not pending';
  end if;

  update public.applications
  set status = 'rejected', approved_by = p_admin_id, approved_at = now()
  where id = p_application_id;

  insert into public.application_logs (application_id, action, performed_by, comment)
  values (p_application_id, 'rejected', p_admin_id, p_comment);
end;
$$;

-- RLS
alter table public.profiles enable row level security;
alter table public.products enable row level security;
alter table public.applications enable row level security;
alter table public.inventory enable row level security;
alter table public.application_logs enable row level security;

create or replace function public.is_admin()
returns boolean
language sql stable security definer set search_path = public
as $$
  select exists (
    select 1 from public.profiles
    where id = auth.uid() and role = 'admin'
  );
$$;

-- Profiles policies
create policy "Users read own profile" on public.profiles
  for select using (auth.uid() = id);
create policy "Admins read all profiles" on public.profiles
  for select using (public.is_admin());
create policy "Users update own profile" on public.profiles
  for update using (auth.uid() = id);

-- Products: all authenticated read; admin write
create policy "Authenticated read products" on public.products
  for select to authenticated using (true);
create policy "Admin manage products" on public.products
  for all using (public.is_admin());

-- Applications
create policy "Users read own applications" on public.applications
  for select using (auth.uid() = user_id);
create policy "Users create own applications" on public.applications
  for insert with check (auth.uid() = user_id);
create policy "Admins read all applications" on public.applications
  for select using (public.is_admin());

-- Inventory
create policy "Authenticated read inventory" on public.inventory
  for select to authenticated using (true);

-- Application logs
create policy "Users read own application logs" on public.application_logs
  for select using (
    exists (
      select 1 from public.applications a
      where a.id = application_id and a.user_id = auth.uid()
    )
  );
create policy "Admins read all application logs" on public.application_logs
  for select using (public.is_admin());

-- RPC execute grants
grant execute on function public.approve_application(uuid, uuid, text) to authenticated;
grant execute on function public.reject_application(uuid, uuid, text) to authenticated;

-- Application log inserts (신청 생성 / 관리자 승인·반려는 RPC security definer)
create policy "Users insert application logs" on public.application_logs
  for insert to authenticated with check (performed_by = auth.uid());

-- Admin inventory write
create policy "Admin manage inventory" on public.inventory
  for insert with check (public.is_admin());
create policy "Admin update inventory" on public.inventory
  for update using (public.is_admin());

-- Seed default product (run once)
insert into public.products (name, description, payment_rule, standard_quantity)
select '상조물품 박스', '조문용 상조물품 박스', '조문객 300명당 1박스 지급. 300명 미만 시 1박스.', 1
where not exists (select 1 from public.products limit 1);

-- Seed initial inventory per region (run once after product seed)
insert into public.inventory (date, region, product_id, stock, update_reason)
select current_date, r.region, p.id, r.stock, '초기 재고'
from (
  values
    ('서울', 120),
    ('오산', 85),
    ('전라', 200),
    ('경상', 150),
    ('충청', 95)
) as r(region, stock)
cross join (select id from public.products limit 1) p
where not exists (select 1 from public.inventory limit 1);