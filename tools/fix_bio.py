from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

new_master_map = r'''function masterMap(){const m=new Map();function aliases(v){const raw=String(v??'').trim().toUpperCase().replace(/\s+/g,'');if(!raw)return[];const a=new Set([raw]);const digits=raw.match(/^(?:LEE)?(\d+)$/);if(digits){a.add(digits[1]);a.add('LEE'+digits[1])}if(raw.startsWith('LEE'))a.add(raw.slice(3));return[...a]}for(const e of state.master){const bio=rawVal(e,['EMPLOYEE CODE','BIO EMPLOYEE ID','BIO ID','EMPLOYEE ID']);const tos=rawVal(e,['AGENT ID','TOS AGENT ID','TOS ID']);for(const k of aliases(bio))m.set(k,e);for(const k of aliases(tos))m.set('TOS:'+k,e)}return m}'''

pattern = r'function masterMap\(\)\{.*?\}function shiftIn\(e\)'
m = re.search(pattern, s, flags=re.S)
if not m:
    raise SystemExit('BIO masterMap function not found; no file changed.')
s2 = s[:m.start()] + new_master_map + 'function shiftIn(e)' + s[m.end():]

old = "const code=rawVal(b,['EMPLOYEE CODE','EMPLOYEE ID','BIO EMPLOYEE CODE','CODE']);const e=mm.get(code.toUpperCase());"
new = "const code=rawVal(b,['EMPLOYEE CODE','EMPLOYEE ID','BIO EMPLOYEE CODE','BIO ID','CODE']);const ck=code.trim().toUpperCase().replace(/\\s+/g,'');const digits=ck.match(/^(?:LEE)?(\\d+)$/);const e=mm.get(ck)||((digits&&mm.get('LEE'+digits[1]))?mm.get('LEE'+digits[1]):null);"
if old not in s2:
    raise SystemExit('BIO rebuild mapping expression not found; no file changed.')
s2 = s2.replace(old,new,1)

marker = '<div class="notice"><b>BIO parser:</b>'
insert = '<div class="notice" style="margin-top:16px"><b>BIO cleaning:</b> Numeric Monthly WorkDuration codes are normalized to the Employee Master BIO code (for example 4170 → LEE4170). Historical IDs not present in Employee Master remain unmatched and are excluded from attendance calculation.</div>'
if insert not in s2 and marker in s2:
    s2 = s2.replace(marker, insert + marker, 1)

if s2 == s:
    raise SystemExit('No BIO changes were made.')
p.write_text(s2, encoding='utf-8')
print('BIO normalization patch written:', len(s2))
