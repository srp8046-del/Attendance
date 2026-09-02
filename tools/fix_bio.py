from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# The Monthly WorkDuration report exports BIO Employee Code as a numeric value
# (for example 4170), while Employee Master stores the same BIO identity as
# LEE4170. Normalize both forms without changing attendance-status rules.
new_master_map = r'''function masterMap(){
  const m=new Map();
  function aliases(v){
    const raw=String(v??'').trim().toUpperCase().replace(/\s+/g,'');
    if(!raw)return[];
    const a=new Set([raw]);
    const digits=raw.match(/^(?:LEE)?(\d+)$/);
    if(digits){a.add(digits[1]);a.add('LEE'+digits[1])}
    if(raw.startsWith('LEE'))a.add(raw.slice(3));
    return[...a];
  }
  for(const e of state.master){
    const bio=rawVal(e,['EMPLOYEE CODE','BIO EMPLOYEE ID','BIO ID','EMPLOYEE ID']);
    const tos=rawVal(e,['AGENT ID','TOS AGENT ID','TOS ID']);
    for(const k of aliases(bio))m.set(k,e);
    for(const k of aliases(tos))m.set('TOS:'+k,e);
  }
  return m
}'''

pattern = r'function masterMap\(\)\{.*?\n\}function shiftIn\(e\)'
if not re.search(pattern, s, flags=re.S):
    raise SystemExit('BIO masterMap function not found; no file changed.')
s2 = re.sub(pattern, new_master_map + '\nfunction shiftIn(e)', s, count=1, flags=re.S)

# Normalize the BIO code at the point of matching too, so numeric XLS values
# and LEE-prefixed Employee Master values always resolve to the same key.
old = "const code=rawVal(b,['EMPLOYEE CODE','EMPLOYEE ID','BIO EMPLOYEE CODE','CODE']);const e=mm.get(code.toUpperCase());"
new = "const code=rawVal(b,['EMPLOYEE CODE','EMPLOYEE ID','BIO EMPLOYEE CODE','BIO ID','CODE']);const ck=code.trim().toUpperCase().replace(/\\s+/g,'');const digits=ck.match(/^(?:LEE)?(\\d+)$/);const e=mm.get(ck)||((digits&&mm.get('LEE'+digits[1]))?mm.get('LEE'+digits[1]):null);"
if old not in s2:
    raise SystemExit('BIO rebuild mapping expression not found; no file changed.')
s2 = s2.replace(old,new,1)

# Add a visible cleaning note so the upload screen explains the normalization.
marker='</section>\n<section id="reports"'
notice='<div class="notice" style="margin-top:16px"><b>BIO cleaning:</b> Monthly WorkDuration employee codes are normalized automatically (numeric <code>4170</code> → Master BIO code <code>LEE4170</code>). Historical BIO IDs not present in Employee Master remain unmatched and are excluded from attendance calculation.</div></section>\n<section id="reports"'
s2=s2.replace(marker,notice,1)

if s2==s:
    raise SystemExit('No BIO changes were made.')
p.write_text(s2,encoding='utf-8')
print('BIO normalization patch written:',len(s2))
