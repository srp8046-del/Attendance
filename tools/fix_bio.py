from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# The real Monthly WorkDuration XLS is a block report:
# Employee Code row -> day labels -> Status -> In Time -> Out Time -> T Duration.
# Day labels are like 1-Mon (not full dates), while the report title contains
# the actual month/year (for example 01-Jun-2026 to 30-Jun-2026).
new_parser = r'''function parseBIOWorkbook(buf){
  if(typeof XLSX==='undefined')throw new Error('Spreadsheet engine unavailable. Refresh and try again.');
  const wb=XLSX.read(buf,{type:'array',cellDates:false,raw:false});
  let out=[], reportYear=null, reportMonth=null;
  const monthMap={JAN:0,FEB:1,MAR:2,APR:3,MAY:4,JUN:5,JUL:6,AUG:7,SEP:8,OCT:9,NOV:10,DEC:11};
  function cleanCell(v){return String(v??'').replace(/\u00a0/g,' ').trim()}
  function parseReportPeriod(a){
    for(let r=0;r<Math.min(a.length,12);r++)for(const c of a[r]){
      const s=cleanCell(c);
      const m=s.match(/\b\d{1,2}[-\/]([A-Za-z]{3,9})[-\/](\d{4})\b/);
      if(m){const mon=monthMap[m[1].slice(0,3).toUpperCase()];if(mon!==undefined)return{year:+m[2],month:mon}}
    }
    return null;
  }
  function dayNumber(v){const m=cleanCell(v).match(/^(\d{1,2})\s*[-\/]\s*[A-Za-z]{3,9}$/);return m?+m[1]:null}
  function findDayRow(a,start){
    for(let j=start+1;j<=start+3&&j<a.length;j++){
      const row=a[j]||[];let n=0;
      for(const c of row)if(dayNumber(c)!=null)n++;
      if(n>=5)return j;
    }
    return -1;
  }
  function findFollowing(a,start,label){
    const wanted=label.toUpperCase();
    for(let j=start;j<=start+6&&j<a.length;j++){
      const row=a[j]||[];
      for(const c of row)if(cleanCell(c).toUpperCase().includes(wanted))return j;
    }
    return -1;
  }
  for(const sn of wb.SheetNames){
    const a=XLSX.utils.sheet_to_json(wb.Sheets[sn],{header:1,defval:'',raw:false});
    const period=parseReportPeriod(a);if(period){reportYear=reportYear??period.year;reportMonth=reportMonth??period.month}
    for(let i=0;i<a.length;i++){
      const row=a[i]||[];
      let ei=-1;
      for(let c=0;c<row.length;c++)if(cleanCell(row[c]).toUpperCase().includes('EMPLOYEE CODE')){ei=c;break}
      if(ei<0)continue;
      let code=cleanCell(row[ei+1]);
      if(!code){for(let c=ei+1;c<row.length;c++){if(cleanCell(row[c])){code=cleanCell(row[c]);break}}}
      if(!code)continue;
      const dr=findDayRow(a,i);if(dr<0)continue;
      const sr=findFollowing(a,dr+1,'STATUS');
      const ir=findFollowing(a,dr+1,'IN TIME');
      const or=findFollowing(a,dr+1,'OUT TIME');
      const du=findFollowing(a,dr+1,'T DURATION');
      if(ir<0||or<0)continue;
      const days=a[dr]||[],stats=sr>=0?(a[sr]||[]):[],ins=a[ir]||[],outs=a[or]||[],durs=du>=0?(a[du]||[]):[];
      for(let c=0;c<days.length;c++){
        const day=dayNumber(days[c]);
        if(day==null||reportYear==null||reportMonth==null)continue;
        const d=new Date(reportYear,reportMonth,day);
        if(isNaN(d.getTime())||d.getMonth()!==reportMonth)continue;
        out.push({DATE:d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'),'EMPLOYEE CODE':code,'STATUS':cleanCell(stats[c]),'IN TIME':cleanCell(ins[c]),'OUT TIME':cleanCell(outs[c]),'T DURATION':cleanCell(durs[c]),SHEET:sn});
      }
    }
  }
  if(!out.length)throw new Error('No BIO daily rows detected. Monthly WorkDuration format was not recognized.');
  state.bioYear=reportYear;return out;
}'''

pattern=r'function parseBIOWorkbook\(buf\)\{.*?\nfunction masterMap\(\)'
m=re.search(pattern,s,flags=re.S)
if not m: raise SystemExit('BIO parser function boundary not found; no file changed.')
s=s[:m.start()]+new_parser+'\nfunction masterMap()'+s[m.end():]

# Keep robust numeric/numeric-vs-LEE mapping in the calculation engine.
new_master_map=r'''function masterMap(){const m=new Map();function aliases(v){const raw=String(v??'').trim().toUpperCase().replace(/\s+/g,'');if(!raw)return[];const a=new Set([raw]);const digits=raw.match(/^(?:LEE)?(\d+)$/);if(digits){a.add(digits[1]);a.add('LEE'+digits[1])}if(raw.startsWith('LEE'))a.add(raw.slice(3));return[...a]}for(const e of state.master){const bio=rawVal(e,['EMPLOYEE CODE','BIO EMPLOYEE ID','BIO ID','EMPLOYEE ID']);const tos=rawVal(e,['AGENT ID','TOS AGENT ID','TOS ID']);for(const k of aliases(bio))m.set(k,e);for(const k of aliases(tos))m.set('TOS:'+k,e)}return m}'''
pattern2=r'function masterMap\(\)\{.*?\}function shiftIn\(e\)'
m=re.search(pattern2,s,flags=re.S)
if not m: raise SystemExit('BIO masterMap function not found; no file changed.')
s=s[:m.start()]+new_master_map+'function shiftIn(e)'+s[m.end():]

old="const code=rawVal(b,['EMPLOYEE CODE','EMPLOYEE ID','BIO EMPLOYEE CODE','BIO ID','CODE']);const ck=code.trim().toUpperCase().replace(/\\s+/g,'');const digits=ck.match(/^(?:LEE)?(\\d+)$/);const e=mm.get(ck)||((digits&&mm.get('LEE'+digits[1]))?mm.get('LEE'+digits[1]):null);"
new="const code=rawVal(b,['EMPLOYEE CODE','EMPLOYEE ID','BIO EMPLOYEE CODE','BIO ID','CODE']);const ck=code.trim().toUpperCase().replace(/\\s+/g,'');const digits=ck.match(/^(?:LEE)?(\\d+)$/);const e=mm.get(ck)||((digits&&mm.get('LEE'+digits[1]))?mm.get('LEE'+digits[1]):null);"
if old not in s: raise SystemExit('BIO rebuild mapping expression not found; no file changed.')

marker='<div class="notice"><b>BIO parser:</b>'
insert='<div class="notice" style="margin-top:16px"><b>BIO cleaning:</b> Monthly WorkDuration block format supported: Employee Code → day labels → Status → In Time → Out Time → T Duration. Numeric BIO IDs are normalized against Employee Master (4170 = LEE4170).</div>'
if marker in s:
    s=s.replace(marker,insert+marker,1)

p.write_text(s,encoding='utf-8')
print('Monthly WorkDuration BIO parser fixed:',len(s))
