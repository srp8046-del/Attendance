from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Keep the spreadsheet dependency valid and remove all previously generated UI/theme patches.
s = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/xlsx@0\.18\.5/dist/xlsx\.full\.min\.js">.*?</script>\s*</script>', '<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>', s, flags=re.S)
for marker in ['LEEWAY_COMPLETE_THEME_V1', 'LEEWAY_COMPLETE_THEME_V2', 'LEEWAY_FINAL_UI', 'LEEWAY_LOGO_FIT_V2']:
    s = re.sub(r'\n?/\* ' + re.escape(marker) + r' \*/.*?(?=</style>)', '', s, flags=re.S)

theme_js = r"<script>\(function\(\)\{function apply\(\)\{var d=localStorage\.getItem\('leeway-theme'\)==='dark';document\.body\.classList\.toggle\('dark',d\)\}window\.toggleTheme=function\(\)\{var d=!document\.body\.classList\.contains\('dark'\);document\.body\.classList\.toggle\('dark',d\);localStorage\.setItem\('leeway-theme',d\?'dark':'light'\)\};if\(document\.readyState==='loading'\)document\.addEventListener\('DOMContentLoaded',apply\);else apply\(\)\}\)\(\);</script>"
s = re.sub(theme_js, '', s)

css = r'''
/* LEEWAY_FINAL_UI */
.brandrow{width:100%!important;height:82px!important;margin:0 0 12px!important;display:flex!important;align-items:center!important;justify-content:center!important}
.side .brandmark{width:100%!important;height:82px!important;display:flex!important;align-items:center!important;justify-content:center!important;background:#fff!important;border:1px solid #d6b86a!important;border-radius:12px!important;padding:6px!important;overflow:hidden!important;box-shadow:0 5px 16px #8b6a1f18!important}
.side .brandmark img{display:block!important;width:220px!important;height:68px!important;max-width:100%!important;max-height:68px!important;object-fit:contain!important;margin:auto!important}
.login .brandrow{height:82px!important;margin:0 0 14px!important}
.login .brandmark{width:100%!important;height:82px!important;padding:8px!important;display:flex!important;align-items:center!important;justify-content:center!important;background:#fff!important;border:1px solid #d6b86a!important;border-radius:12px!important;overflow:hidden!important}
.login .brandmark img{display:block!important;width:290px!important;height:64px!important;max-width:100%!important;max-height:64px!important;object-fit:contain!important;margin:auto!important}
body.dark{background:#090c11!important;color:#f5f1e8!important;color-scheme:dark}
body.dark .app,body.dark .main,body.dark .content,body.dark .page{background:transparent!important;color:#f5f1e8!important}
body.dark .side{background:linear-gradient(180deg,#18150f 0%,#0d1015 100%)!important;color:#f5f1e8!important;border-right:1px solid #5d4717!important;box-shadow:8px 0 30px #000b!important}
body.dark .logo,body.dark .nav-label{color:#d9bd72!important}
body.dark .logo b{color:#d6b86a!important}
body.dark .nav button{background:transparent!important;color:#ddd5c4!important}
body.dark .nav button:hover{background:#d6b86a18!important;color:#fff!important}
body.dark .nav button.active{background:linear-gradient(90deg,#9d7518,#c9a64f)!important;color:#fff!important}
body.dark header{background:#12161c!important;color:#f5f1e8!important;border-bottom:1px solid #4e3c16!important;box-shadow:0 3px 18px #0008!important}
body.dark header h1,body.dark .hero h2,body.dark .section-title,body.dark .rule-card h3,body.dark .loginbox h1{color:#f5f1e8!important}
body.dark .eyebrow{color:#d6b86a!important}
body.dark .hero p,body.dark .drop p,body.dark .rule-card p,body.dark .empty,body.dark .setting-row,body.dark .kpi small,body.dark .kpi span,body.dark #dataStatus,body.dark #rowStat,body.dark .loginbox>p{color:#aaa99f!important}
body.dark .card{background:#151a21!important;border:1px solid #3f331c!important;color:#f5f1e8!important;box-shadow:0 10px 30px #0006!important}
body.dark .mini div{background:#0f1319!important;border:1px solid #34302a!important;color:#aaa99f!important}
body.dark .mini b{color:#f5f1e8!important}
body.dark .drop{background:#10141a!important;border:1.5px dashed #5d4a20!important;color:#f5f1e8!important}
body.dark .drop:hover{border-color:#d6b86a!important;background:#191710!important}
body.dark .notice{background:#271a17!important;border-color:#69352d!important;color:#efb1a8!important}
body.dark .filters input,body.dark .filters select,body.dark .loginbox input{background:#0d1117!important;color:#f5f1e8!important;border:1px solid #403a2d!important}
body.dark .filters input:focus,body.dark .filters select:focus,body.dark .loginbox input:focus{border-color:#d6b86a!important;box-shadow:0 0 0 3px #d6b86a18!important;outline:none!important}
body.dark .tablewrap{background:#0d1117!important;border:1px solid #383323!important}
body.dark .table{color:#eeeae0!important;background:#0d1117!important}
body.dark .table th{background:#191d24!important;color:#d2c9b7!important;border-bottom:1px solid #403a2d!important}
body.dark .table td{background:#0d1117!important;color:#eeeae0!important;border-bottom:1px solid #282b31!important}
body.dark .table tbody tr:hover td{background:#211d12!important}
body.dark .btn{background:#171b21!important;color:#f0eadc!important;border:1px solid #55451f!important}
body.dark .btn:hover{background:#211f18!important;border-color:#d6b86a!important;color:#fff!important}
body.dark .primary{background:linear-gradient(90deg,#9d7518,#d6b86a)!important;color:#fff!important;border-color:#b88a20!important}
body.dark .progress{background:#292d34!important}
body.dark .progress i{background:linear-gradient(90deg,#9d7518,#d6b86a)!important}
body.dark .pill{background:#143526!important;color:#79d7a5!important}
body.dark .toast{background:#f4f0e6!important;color:#11151b!important}
body.dark .login{background:radial-gradient(circle at 80% 15%,#342910 0,#17140f 38%,#080a0e 100%)!important}
body.dark .loginbox{background:#151a21!important;color:#f5f1e8!important;border:1px solid #6a511c!important;box-shadow:0 30px 90px #000d!important}
body.dark .loginbox .error{color:#ff9b91!important}
body.dark .side .brandmark,body.dark .login .brandmark{background:#fff!important;border-color:#c49b3a!important}
body.dark .PRESENT{background:#123a29!important;color:#7be0ab!important}
body.dark .LATE{background:#422f12!important;color:#f3c56c!important}
body.dark .HALFDAY{background:#472719!important;color:#f3a86e!important}
body.dark .ABSENT{background:#481d1b!important;color:#ff9289!important}
body.dark .NOT{background:#1b2a40!important;color:#9ebce8!important}
.finaltable th.agent,.finaltable td.agent{position:sticky;left:0;text-align:left;min-width:190px}.finaltable th.agent{z-index:3}.finaltable td.agent{z-index:1;background:#fff}.finaltable th.agentid,.finaltable td.agentid{min-width:110px}.finaltable .finalcell{text-align:center;min-width:55px}.agent-name{font-weight:850;font-size:13px}.agent-ids{display:block;margin-top:4px;color:#7b8492;font-size:10px;font-weight:650}
@media(max-width:850px){.brandrow{height:64px!important;margin-bottom:10px!important}.side .brandmark{width:58px!important;height:64px!important;padding:4px!important}.side .brandmark img{width:52px!important;height:54px!important;max-width:52px!important;max-height:54px!important}.login .brandrow{height:72px!important}.login .brandmark{height:72px!important}.login .brandmark img{width:250px!important;height:56px!important;max-height:56px!important}.logo{font-size:0!important}.logo b{font-size:0!important}}
'''
s = s.replace('</style>', css + '\n</style>', 1)

# Final Attendance: Agent Name | Employee ID | Agent ID | Dates, with P/LC/HD/A/NP shortcuts.
final_fn = r'''function renderFinal(){const q=($('finalSearch')?.value||'').toLowerCase();const rs=state.records.filter(r=>!q||[r.employee,r.code,r.tosId,r.designation].join(' ').toLowerCase().includes(q));const em={};rs.forEach(r=>{const k=r.code+'|'+r.tosId;if(!em[k])em[k]={employee:r.employee,code:r.code,tosId:r.tosId,designation:r.designation,dates:{}};em[k].dates[r.date]=r.finalStatus});const people=Object.values(em);const dates=[...new Set(rs.map(r=>r.date))].sort();if(!people.length){$('finalWrap').innerHTML='<div class="empty">No attendance records.</div>';return}let h='<table class="finaltable"><thead><tr><th class="agent">Agent Name</th><th class="agentid">Employee ID</th><th class="agentid">Agent ID</th>';dates.forEach(d=>h+=`<th>${esc(d)}</th>`);h+='</tr></thead><tbody>';for(const p of people){h+='<tr><td class="agent"><div class="agent-name">'+esc(p.employee)+'</div></td><td class="agentid">'+esc(p.code)+'</td><td class="agentid">'+esc(p.tosId)+'</td>';for(const d of dates){const s=p.dates[d]||'NOT PUNCHED';const short=s==='PRESENT'?'P':s==='LATE'?'LC':s==='HALFDAY'?'HD':s==='ABSENT'?'A':'NP';h+='<td class="finalcell" title="'+esc(s)+'"><span class="badge '+(s==='NOT PUNCHED'?'NOT':s)+'">'+short+'</span></td>'}h+='</tr>'}h+='</tbody></table>';$('finalWrap').innerHTML=h}'''
s = re.sub(r'function renderFinal\(\)\{.*?\nfunction renderEmployees\(\)', final_fn + '\nfunction renderEmployees()', s, flags=re.S)

export_fn = r'''function exportFinalCSV(){if(!state.records.length){toast('No attendance data');return}const rs=state.records,people=[],map=new Map();rs.forEach(r=>{const k=r.code+'|'+r.tosId;if(!map.has(k))map.set(k,{employee:r.employee,code:r.code,tosId:r.tosId,designation:r.designation,dates:{}});map.get(k).dates[r.date]=r.finalStatus});people.push(...map.values());const dates=[...new Set(rs.map(r=>r.date))].sort();const rows=[['Agent Name','Employee ID','Agent ID',...dates]];people.forEach(p=>rows.push([p.employee,p.code,p.tosId,...dates.map(d=>{const s=p.dates[d]||'NOT PUNCHED';return s==='PRESENT'?'P':s==='LATE'?'LC':s==='HALFDAY'?'HD':s==='ABSENT'?'A':'NP'})]));const csv='\ufeff'+rows.map(a=>a.map(x=>'"'+String(x??'').replace(/"/g,'""')+'"').join(',')).join('\r\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));a.download='leeway_final_attendance.csv';a.click()}'''
s = re.sub(r'function exportFinalCSV\(\)\{.*?\nupdateKPIs\(\)', export_fn + '\nupdateKPIs()', s, flags=re.S)

s = re.sub(r'<script>\(function\(\)\{function apply\(\).*?</script>', '', s, flags=re.S)
p.write_text(s, encoding='utf-8')
print('Final attendance layout made persistent')
