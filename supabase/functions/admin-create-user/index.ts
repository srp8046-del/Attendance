import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type'
};

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const serviceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const admin = createClient(supabaseUrl, serviceKey);

    const auth = req.headers.get('Authorization') || '';
    const token = auth.replace(/^Bearer\s+/i, '');
    if (!token) throw new Error('Missing authorization token');

    const { data: callerData, error: callerError } = await admin.auth.getUser(token);
    if (callerError || !callerData.user) throw new Error('Invalid session');

    const { data: caller } = await admin.from('user_profiles').select('role,active').eq('id', callerData.user.id).maybeSingle();
    if (!caller || caller.role !== 'admin' || !caller.active) throw new Error('Admin access required');

    const body = await req.json();
    const username = String(body.username || '').trim().toLowerCase();
    const password = String(body.password || '');
    const display_name = String(body.display_name || '').trim();
    const designation = String(body.designation || '').trim();
    const employee_code = body.employee_code ? String(body.employee_code).trim() : null;
    const manager_employee_code = body.manager_employee_code ? String(body.manager_employee_code).trim() : null;
    const role = String(body.role || 'viewer').trim();
    const can_view_all = Boolean(body.can_view_all);
    const can_upload = Boolean(body.can_upload);

    if (!/^[a-z0-9._-]{3,40}$/.test(username)) throw new Error('Username must be 3-40 characters: letters, numbers, dot, underscore or hyphen.');
    if (password.length < 8) throw new Error('Password must be at least 8 characters.');
    if (!['admin','manager','tele_sales_executive','viewer','uploader'].includes(role)) throw new Error('Invalid role');
    if (!display_name) throw new Error('Display name is required');

    const email = `${username}@login.leeway.local`;
    const { data: created, error: createError } = await admin.auth.admin.createUser({ email, password, email_confirm: true });
    if (createError) throw createError;

    const { error: profileError } = await admin.from('user_profiles').insert({
      id: created.user.id, username, display_name, designation, employee_code,
      manager_employee_code, role, can_view_all, can_upload, active: true
    });
    if (profileError) {
      await admin.auth.admin.deleteUser(created.user.id);
      throw profileError;
    }

    return new Response(JSON.stringify({ ok: true, username, user_id: created.user.id }), {
      headers: { ...cors, 'Content-Type': 'application/json' }, status: 200
    });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: e instanceof Error ? e.message : String(e) }), {
      headers: { ...cors, 'Content-Type': 'application/json' }, status: 400
    });
  }
});
