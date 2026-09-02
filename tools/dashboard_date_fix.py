from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Add a date selector to the Dashboard without changing attendance calculation logic.
old = '<div class="grid"><div class="card kpi"><small>Employees</small>'
new = '<div class="card" style="margin-bottom:16px"><div class="filters" style="margin-bottom:0;align-items:center"><b style="margin-right:4px">Attendance Date</b><input id="dashboardDate" type="date" onchange="updateKPIs()"><button class="btn" onclick="$(\'dashboardDate\').value=\'\';updateKPIs()">All Dates</button></div></div><div class="grid"><div class="card kpi"><small>Employees</small>'
if old in s and 'id="dashboardDate"' not in s:
    s = s.replace(old, new, 1)

# Make dashboard KPIs respond to the selected date.
pattern = r'function updateKPIs\(\)\{.*?\}\nfunction updateFileState\(\)'
replacement = '''function updateKPIs(){const df=$(\'dashboardDate\')?.value||\'\';const r0=state.records;const r=df?r0.filter(x=>x.date===df):r0;const p=r.filter(x=>x.finalStatus===\'PRESENT\').length,l=r.filter(x=>x.finalStatus===\'LATE\').length,h=r.filter(x=>x.finalStatus===\'HALFDAY\').length,a=r.filter(x=>x.finalStatus===\'ABSENT\').length,np=r.filter(x=>x.finalStatus===\'NOT PUNCHED\').length;$(\'kEmp\').textContent=df?[...new Set(r.map(x=>x.code))].length:state.master.length;$(\'kPresent\').textContent=p;$(\'kPresentPct\').textContent=(r.length?(p/r.length*100):0).toFixed(1)+\'%\';$(\'kLate\').textContent=l+h;$(\'kAbsent\').textContent=a+np;$(\'mP\').textContent=p;$(\'mL\').textContent=l;$(\'mH\').textContent=h;$(\'mA\').textContent=a+np}\nfunction updateFileState()'''
s2, n = re.subn(pattern, replacement, s, count=1, flags=re.S)
if n:
    s = s2

# Use the latest attendance date when data is first loaded, while allowing All Dates.
marker = "function updateFileState(){"
if 'function setDashboardDate()' not in s and marker in s:
    s = s.replace(marker, "function setDashboardDate(){const el=$(\'dashboardDate\');if(!el||!state.records.length)return;const dates=state.records.map(r=>r.date).filter(Boolean).sort();if(!el.value&&dates.length)el.value=dates[dates.length-1]}\n"+marker, 1)
    s = s.replace('rebuild();updateFileState();if(type===\'master\')renderEmployees()', 'rebuild();setDashboardDate();updateFileState();if(type===\'master\')renderEmployees()', 1)

p.write_text(s, encoding='utf-8')
