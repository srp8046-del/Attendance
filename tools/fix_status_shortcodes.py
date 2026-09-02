from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Status helper: keep internal full statuses, display compact codes everywhere.
helper="""\nfunction statusCode(s){return s==='PRESENT'?'P':s==='LATE'?'LC':s==='HALFDAY'?'HD':s==='ABSENT'?'A':s==='NOT PUNCHED'?'NP':''}\nfunction statusLabel(s){return s==='PRESENT'?'Present':s==='LATE'?'Late':s==='HALFDAY'?'Halfday':s==='ABSENT'?'Absent':s==='NOT PUNCHED'?'Not Punched':''}\n"""
if 'function statusCode(s)' not in s:
    s=s.replace('function renderTable(){',helper+'function renderTable(){',1)

# Dashboard health labels use shortcuts while keeping KPI logic unchanged.
s=s.replace('<div>Present<b id="mP">0</b></div><div>Late<b id="mL">0</b></div><div>Halfday<b id="mH">0</b></div><div>Absent<b id="mA">0</b></div>',
            '<div>P <small>Present</small><b id="mP">0</b></div><div>LC <small>Late</small><b id="mL">0</b></div><div>HD <small>Halfday</small><b id="mH">0</b></div><div>A/NP <small>Absent / Not Punched</small><b id="mA">0</b></div>')

# Dashboard KPI headings.
s=s.replace('<small>Present</small>','<small>P — Present</small>')
s=s.replace('<small>Late / Halfday</small>','<small>LC / HD — Late / Halfday</small>')
s=s.replace('<small>Absent / Not Punched</small>','<small>A / NP — Absent / Not Punched</small>')

# Replace detailed table renderer so displayed status values are compact codes.
new_render="""function renderTable(){const q=($('search')?.value||'').toLowerCase(),sf=$('statusFilter')?.value||'',df=$('dateFilter')?.value||'',rows=state.records.filter(r=>(!q||[r.employee,r.code,r.tosId].join(' ').toLowerCase().includes(q))&&(!sf||r.finalStatus===sf)&&(!df||r.date===df));$('tbody').innerHTML=rows.length?rows.map(r=>`<tr><td>${esc(r.date)}</td><td><b>${esc(r.employee)}</b></td><td>${esc(r.code)}</td><td>${esc(r.tosId)}</td><td>${esc(r.designation)}</td><td>${esc(r.shift)}</td><td>${esc(r.shiftIn)}</td><td>${esc(r.bioIn)}</td><td>${esc(r.bioOut)}</td><td>${fmt(r.bioMin)}</td><td><span class="badge ${r.bioStatus==='NOT PUNCHED'?'NOT':r.bioStatus}">${statusCode(r.bioStatus)}</span></td><td>${fmt(r.tosMin)}</td><td><span class="badge ${r.tosStatus?(r.tosStatus==='NOT PUNCHED'?'NOT':r.tosStatus):'NOT'}">${r.tosStatus?statusCode(r.tosStatus):'NP'}</span></td><td><span class="badge ${r.finalStatus==='NOT PUNCHED'?'NOT':r.finalStatus}">${statusCode(r.finalStatus)}</span></td></tr>`).join(''):'<tr><td colspan="14" class="empty">No attendance records.</td></tr>'}\n"""
s=re.sub(r'function renderTable\(\)\{.*?\nfunction renderFinal\(\)', new_render+'function renderFinal()', s, count=1, flags=re.S)

# Replace final renderer with requested agent-row/date-column orientation and shortcuts.
new_final="""function renderFinal(){const q=($('finalSearch')?.value||'').toLowerCase();const rs=state.records.filter(r=>!q||[r.employee,r.code,r.tosId,r.designation].join(' ').toLowerCase().includes(q));const em={};rs.forEach(r=>{const k=r.code+'|'+r.tosId;if(!em[k])em[k]={employee:r.employee,code:r.code,tosId:r.tosId,dates:{}};em[k].dates[r.date]=r.finalStatus});const people=Object.values(em);const dates=[...new Set(rs.map(r=>r.date))].sort();if(!people.length){$('finalWrap').innerHTML='<div class="empty">No attendance records.</div>';return}let h='<table class="finaltable"><thead><tr><th class="agent">Agent Name</th><th class="agentid">Employee ID</th><th class="agentid">Agent ID</th>';dates.forEach(d=>h+=`<th>${esc(d)}</th>`);h+='</tr></thead><tbody>';for(const p of people){h+=`<tr><td class="agent"><b>${esc(p.employee)}</b></td><td>${esc(p.code)}</td><td>${esc(p.tosId)}</td>`;for(const d of dates){const st=p.dates[d]||'NOT PUNCHED';h+=`<td class="finalcell"><span class="badge ${st==='NOT PUNCHED'?'NOT':st}">${statusCode(st)}</span></td>`}h+='</tr>'}h+='</tbody></table>';$('finalWrap').innerHTML=h}\n"""
s=re.sub(r'function renderFinal\(\)\{.*?\nfunction renderEmployees\(\)', new_final+'function renderEmployees()', s, count=1, flags=re.S)

# Final legend.
s=re.sub(r'<div class="finalnote">.*?</div>', '<div class="finalnote">Agent Name | Employee ID | Agent ID | Dates · P = Present | LC = Late | HD = Halfday | A = Absent | NP = Not Punched</div>', s, count=1, flags=re.S)

# Ensure final-table styling supports the two ID columns and compact cells.
s=s.replace('.finaltable th.agent{', '.finaltable th.agentid{position:sticky;left:0;z-index:3;background:#f7f8fa}.finaltable th.agent{')
s=s.replace('.finaltable td.agent{', '.finaltable td.agentid{font-weight:700;text-align:left}.finaltable td.agent{')
s=s.replace('.finalcell{font-weight:850;min-width:70px}', '.finalcell{font-weight:850;min-width:52px}.finaltable td.agent{min-width:170px}.finaltable td.agentid{min-width:120px}')

p.write_text(s,encoding='utf-8')
