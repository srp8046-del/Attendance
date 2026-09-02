from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

final_fn = r'''function renderFinal(){const q=($('finalSearch')?.value||'').toLowerCase();const rs=state.records.filter(r=>!q||[r.employee,r.code,r.tosId,r.designation].join(' ').toLowerCase().includes(q));const em={};rs.forEach(r=>{const k=r.code+'|'+r.tosId;if(!em[k])em[k]={employee:r.employee,code:r.code,tosId:r.tosId,designation:r.designation,dates:{}};em[k].dates[r.date]=r.finalStatus});const people=Object.values(em);const dates=[...new Set(rs.map(r=>r.date))].sort();if(!people.length){$('finalWrap').innerHTML='<div class="empty">No attendance records.</div>';return}let h='<table class="finaltable"><thead><tr><th class="agent">Agent Name</th><th class="agentid">Employee ID</th><th class="agentid">Agent ID</th>';dates.forEach(d=>h+=`<th>${esc(d)}</th>`);h+='</tr></thead><tbody>';for(const p of people){h+='<tr><td class="agent"><div class="agent-name">'+esc(p.employee)+'</div></td><td class="agentid">'+esc(p.code)+'</td><td class="agentid">'+esc(p.tosId)+'</td>';for(const d of dates){const s=p.dates[d]||'NOT PUNCHED';const short=s==='PRESENT'?'P':s==='LATE'?'LC':s==='HALFDAY'?'HD':s==='ABSENT'?'A':'NP';h+='<td class="finalcell" title="'+esc(s)+'"><span class="badge '+(s==='NOT PUNCHED'?'NOT':s)+'">'+short+'</span></td>'}h+='</tr>'}h+='</tbody></table>';$('finalWrap').innerHTML=h}'''
s = re.sub(r'function renderFinal\(\)\{.*?\nfunction renderEmployees\(\)', final_fn + '\nfunction renderEmployees()', s, flags=re.S)

export_fn = r'''function exportFinalCSV(){if(!state.records.length){toast('No attendance data');return}const rs=state.records,people=[],map=new Map();rs.forEach(r=>{const k=r.code+'|'+r.tosId;if(!map.has(k))map.set(k,{employee:r.employee,code:r.code,tosId:r.tosId,designation:r.designation,dates:{}});map.get(k).dates[r.date]=r.finalStatus});people.push(...map.values());const dates=[...new Set(rs.map(r=>r.date))].sort();const rows=[['Agent Name','Employee ID','Agent ID',...dates]];people.forEach(p=>rows.push([p.employee,p.code,p.tosId,...dates.map(d=>{const s=p.dates[d]||'NOT PUNCHED';return s==='PRESENT'?'P':s==='LATE'?'LC':s==='HALFDAY'?'HD':s==='ABSENT'?'A':'NP'})]));const csv='\ufeff'+rows.map(a=>a.map(x=>'"'+String(x??'').replace(/"/g,'""')+'"').join(',')).join('\r\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));a.download='leeway_final_attendance.csv';a.click()}'''
s = re.sub(r'function exportFinalCSV\(\)\{.*?\nupdateKPIs\(\)', export_fn + '\nupdateKPIs()', s, flags=re.S)

css = '.finaltable th.agentid,.finaltable td.agentid{min-width:120px}.finaltable th.agent,.finaltable td.agent{min-width:190px;text-align:left}.finaltable .finalcell{text-align:center;min-width:55px}.finaltable .agent-name{font-weight:850;font-size:13px}'
s = s.replace('</style>', css + '\n</style>', 1)
p.write_text(s, encoding='utf-8')
print('Final attendance layout updated')
