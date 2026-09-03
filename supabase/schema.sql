-- Leeway International Attendance Master
-- Supabase RBAC schema. Run this in Supabase SQL Editor.
create extension if not exists pgcrypto;

create table if not exists public.user_profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  username text not null unique,
  display_name text not null default '',
  designation text not null default '',
  employee_code text,
  manager_employee_code text,
  role text not null default 'viewer' check (role in ('admin','manager','tele_sales_executive','viewer','uploader')),
  can_view_all boolean not null default false,
  can_upload boolean not null default false,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.user_profiles enable row level security;

drop policy if exists "profiles own read" on public.user_profiles;
create policy "profiles own read" on public.user_profiles
for select to authenticated using (id = auth.uid());

drop policy if exists "admin read profiles" on public.user_profiles;
create policy "admin read profiles" on public.user_profiles
for select to authenticated using (
  exists (select 1 from public.user_profiles p where p.id=auth.uid() and p.role='admin' and p.active)
);

create or replace function public.my_profile()
returns public.user_profiles
language sql stable security definer set search_path=public
as $$ select * from public.user_profiles where id=auth.uid() and active limit 1 $$;

grant execute on function public.my_profile() to authenticated;

-- Optional helper for managers: returns their own employee code from the profile.
create or replace function public.my_access_scope()
returns jsonb
language sql stable security definer set search_path=public
as $$
  select jsonb_build_object(
    'role', role,
    'employee_code', employee_code,
    'manager_employee_code', manager_employee_code,
    'can_view_all', can_view_all,
    'can_upload', can_upload
  ) from public.user_profiles where id=auth.uid() and active limit 1
$$;

grant execute on function public.my_access_scope() to authenticated;

-- IMPORTANT: user creation must be done server-side with Supabase service-role key.
-- Do NOT put the service-role key in index.html or GitHub Pages.
