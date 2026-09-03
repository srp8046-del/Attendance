from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Definitive local date handling: never use UTC conversion for attendance dates.
local_iso="""function localISO(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}"""
if 'function localISO(d)' not in s:
    s=s.replace('</style></head>', local_iso+'\n</style></head>', 1)
s=s.replace("d.toISOString().slice(0,10)", "localISO(d)")

# Replace the final-attendance renderer with the required orientation and shortcuts.
final_fn=r'''function renderFinal(){const q=($('finalSearch')?.value||'').toLowerCase();const rs=state.records.filter(r=>!q||[r.employee,r.code,r.tosId,r.designation].join(' ').toLowerCase().includes(q));const em={};rs.forEach(r=>{const k=r.code+'|'+r.tosId;if(!em[k])em[k]={employee:r.employee,code:r.code,tosId:r.tosId,dates:{}};em[k].dates[r.date]=r.finalStatus});const people=Object.values(em);const dates=[...new Set(rs.map(r=>r.date))].sort();if(!people.length){$('finalWrap').innerHTML='<div class="empty">No attendance records.</div>';return}const short=s=>s==='PRESENT'?'P':s==='LATE'?'LC':s==='HALFDAY'?'HD':s==='ABSENT'?'A':'NP';let h='<table class="finaltable"><thead><tr><th class="agent">Agent Name</th><th class="agentid">Employee ID</th><th class="agentid">Agent ID</th>';dates.forEach(d=>h+=`<th>${esc(d)}</th>`);h+='</tr></thead><tbody>';for(const p of people){h+=`<tr><td class="agent"><b>${esc(p.employee)}</b></td><td>${esc(p.code)}</td><td>${esc(p.tosId)}</td>`;for(const d of dates){const v=short(p.dates[d]||'NOT PUNCHED');h+=`<td class="finalcell"><span class="badge ${v==='P'?'PRESENT':v==='LC'?'LATE':v==='HD'?'HALFDAY':v==='A'?'ABSENT':'NOT'}">${v}</span></td>`}h+='</tr>'}$('finalWrap').innerHTML=h+'</tbody></table>'}'''
# Replace renderFinal body/function up to renderEmployees.
s=re.sub(r'function renderFinal\(\)\{.*?\}\nfunction renderEmployees', final_fn+'\nfunction renderEmployees', s, count=1, flags=re.S)

export_fn=r'''function exportFinalCSV(){if(!state.records.length){toast('No attendance data');return}const q=($('finalSearch')?.value||'').toLowerCase();const rs=state.records.filter(r=>!q||[r.employee,r.code,r.tosId,r.designation].join(' ').toLowerCase().includes(q));const em={};rs.forEach(r=>{const k=r.code+'|'+r.tosId;if(!em[k])em[k]={employee:r.employee,code:r.code,tosId:r.tosId,dates:{}};em[k].dates[r.date]=r.finalStatus});const people=Object.values(em);const dates=[...new Set(rs.map(r=>r.date))].sort();const short=s=>s==='PRESENT'?'P':s==='LATE'?'LC':s==='HALFDAY'?'HD':s==='ABSENT'?'A':'NP';const rows=[['Agent Name','Employee ID','Agent ID',...dates],...people.map(p=>[p.employee,p.code,p.tosId,...dates.map(d=>short(p.dates[d]||'NOT PUNCHED'))])];const csv='\ufeff'+rows.map(a=>a.map(x=>'"'+String(x??'').replace(/"/g,'""')+'"').join(',')).join('\r\n');const blob=new Blob([csv],{type:'text/csv;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='Final_Attendance.csv';a.click();URL.revokeObjectURL(a.href)}'''
s=re.sub(r'function exportFinalCSV\(\)\{.*?\}\n', export_fn+'\n', s, count=1, flags=re.S)

# Ensure the visible legend is exactly the requested one.
s=re.sub(r'<div class="finalnote">.*?</div>', '<div class="finalnote">Agent Name | Employee ID | Agent ID | Dates · P = Present | LC = Late | HD = Halfday | A = Absent | NP = Not Punched</div>', s, count=1, flags=re.S)

# Ensure date parsing preserves ISO dates and does not shift them.
if 'function cleanDate' in s:
    s=re.sub(r'function cleanDate\(v\)\{.*?\}', "function cleanDate(v){const x=String(v??'').trim();if(/^\\d{4}-\\d{2}-\\d{2}$/.test(x))return x;const d=new Date(x);return Number.isNaN(d.getTime())?'':localISO(d)}", s, count=1, flags=re.S)

# CSS for the three fixed identity columns.
s=s.replace('.finaltable th.agent{', '.finaltable th.agent,.finaltable th.agentid{')
s=s.replace('.finaltable td.agent{', '.finaltable td.agent,.finaltable td.agentid{')

p.write_text(s,encoding='utf-8')
print('Emergency attendance fix applied')
