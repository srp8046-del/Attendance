# Attendance Master — Supabase Authentication & RBAC

This folder contains the secure backend pieces for the Attendance Master login and role model.

## Roles

- `admin`: view all + upload + create users
- `manager`: own attendance + direct team attendance; no upload by default
- `tele_sales_executive`: own attendance only; no upload
- `viewer`: view-all users who cannot upload
- `uploader`: view-all + upload, but not user administration

A user's `employee_code` identifies the employee. A manager's `manager_employee_code` is used to identify the reporting relationship.

## Username + password

The UI can remain Username + Password. Supabase Auth itself uses email/password, so the implementation maps a username to an internal synthetic login email such as `username@login.leeway.local`. The synthetic email is never shown to the user.

## Setup

1. Run `schema.sql` in Supabase SQL Editor.
2. Deploy `functions/admin-create-user/index.ts` as the `admin-create-user` Edge Function.
3. Keep the Supabase secret/service key only in the Edge Function environment. Never put it in `index.html` or GitHub Pages.
4. Create the first admin from the Supabase dashboard (Auth user + matching `user_profiles` row), then use the application's admin user-management screen for subsequent users.

The browser may use the Supabase publishable key. Supabase RLS must remain enabled for database authorization.
