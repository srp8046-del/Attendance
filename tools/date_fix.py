from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Fix the India timezone/off-by-one issue: toISOString() converts local midnight to the previous UTC date.
local_iso = "function localISO(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}"
s = s.replace("function cleanDate(v){", local_iso + "\nfunction cleanDate(v){", 1)
s = s.replace("if(!s)return'';let m=s.match(/^(\\d{1,2})[-\\/]([A-Za-z]{3,9})[-\\/](\\d{4})$/);", "if(!s)return'';let ymd=s.match(/^(\\d{4})-(\\d{1,2})-(\\d{1,2})$/);if(ymd)return ymd[1]+'-'+String(+ymd[2]).padStart(2,'0')+'-'+String(+ymd[3]).padStart(2,'0');let m=s.match(/^(\\d{1,2})[-\\/]([A-Za-z]{3,9})[-\\/](\\d{4})$/);", 1)
s = s.replace("d.toISOString().slice(0,10)", "localISO(d)")
s = s.replace("const d=new Date(reportYear,reportMonth,day);if(d.getMonth()!==reportMonth)continue;out.push({DATE:d.toISOString().slice(0,10)", "const d=new Date(reportYear,reportMonth,day);if(d.getMonth()!==reportMonth)continue;out.push({DATE:localISO(d)")

# Final Attendance legend + correct orientation note.
s = s.replace("Dates are rows · Employee/agent details are columns · each cell shows final attendance.", "Agent Name | Employee ID | Agent ID | Dates · P = Present | LC = Late | HD = Halfday | A = Absent | NP = Not Punched", 1)

# Ensure the requested final orientation is present even if an earlier UI patch changed it.
final_fn = r'''function renderFinal(){const q=($('finalSearch')?.value||'').toLowerCase();const rs=state.records.filter(r=>!q||[r.employee,r.code,r.tosId,r.designation].join(' ').toLowerCase().includes(q));const em={};rs.forEach(r=>{const k=r.code+'|'+r.tosId;if(!em[k])em[k]={employee:r.employee,code:r.code,tosId:r.tosId,dates:{}};em[k].dates[r.date]=r.finalStatus});const people=Object.values(em);const dates=[...new Set(rs.map(r=>r.date))].sort();if(!people.length){$('finalWrap').innerHTML='<div class="empty">No attendance records.</div>';return}let h='<table class="finaltable"><thead><tr><th class="agent">Agent Name</th><th class="agentid">Employee ID</th><th class="agentid">Agent ID</th>';dates.forEach(d=>h+=`<th>${esc(d)}</th>`);h+='</tr></thead><tbody>';for(const p of people){h+='<tr><td class="agent">'+esc(p.employee)+'</td><td class="agentid">'+esc(p.code)+'</td><td class="agentid">'+esc(p.tosId)+'</td>';for(const d of dates){const s=p.dates[d]||'NOT PUNCHED';const short=s==='PRESENT'?'P':s==='LATE'?'LC':s==='HALFDAY'?'HD':s==='ABSENT'?'A':'NP';h+='<td class="finalcell" title="'+esc(s)+'"><span class="badge '+(s==='NOT PUNCHED'?'NOT':s)+'">'+short+'</span></td>'}h+='</tr>'}h+='</tbody></table>';$('finalWrap').innerHTML=h}'''
s = re.sub(r'function renderFinal\(\)\{.*?\nfunction renderEmployees\(\)', final_fn + '\nfunction renderEmployees()', s, flags=re.S)

export_fn = r'''function exportFinalCSV(){if(!state.records.length){toast('No attendance data');return}const rs=state.records,map=new Map();rs.forEach(r=>{const k=r.code+'|'+r.tosId;if(!map.has(k))map.set(k,{employee:r.employee,code:r.code,tosId:r.tosId,dates:{}});map.get(k).dates[r.date]=r.finalStatus});const people=[...map.values()],dates=[...new Set(rs.map(r=>r.date))].sort();const rows=[['Agent Name','Employee ID','Agent ID',...dates]];people.forEach(p=>rows.push([p.employee,p.code,p.tosId,...dates.map(d=>{const s=p.dates[d]||'NOT PUNCHED';return s==='PRESENT'?'P':s==='LATE'?'LC':s==='HALFDAY'?'HD':s==='ABSENT'?'A':'NP'})]));const csv='\ufeff'+rows.map(a=>a.map(x=>'"'+String(x??'').replace(/"/g,'""')+'"').join(',')).join('\r\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));a.download='leeway_final_attendance.csv';a.click()}'''
s = re.sub(r'function exportFinalCSV\(\)\{.*?\nupdateKPIs\(\)', export_fn + '\nupdateKPIs()', s, flags=re.S)

p.write_text(s, encoding='utf-8')
print('Final orientation, legend and date handling fixed')
