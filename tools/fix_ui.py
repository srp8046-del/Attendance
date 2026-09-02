from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

s = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/xlsx@0\.18\.5/dist/xlsx\.full\.min\.js"><script>.*?</script>\s*</script>', '<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>', s, flags=re.S)
s = re.sub(r'<script>if\(localStorage\.getItem\("leeway-theme"\).*?</script>', '', s, flags=re.S)
for marker in ['LEEWAY_COMPLETE_THEME_V1', 'LEEWAY_COMPLETE_THEME_V2', 'LEEWAY_FINAL_UI', 'LEEWAY_LOGO_FIT_V2']:
    s = re.sub(r'\n?/\* ' + re.escape(marker) + r' \*/.*?(?=</style>)', '', s, flags=re.S)

s = s.replace('.logo b{color:#ff2638}', '.logo b{color:#b88a20}')
s = s.replace('.drop:hover{border-color:#e60012;background:#fff8f8}', '.drop:hover{border-color:#b88a20;background:#fffdf5}')
s = s.replace('border-color:#e60012;box-shadow:0 0 0 3px #e6001212', 'border-color:#b88a20;box-shadow:0 0 0 3px #d6b86a22')
s = s.replace('.table tbody tr:hover{background:#fff8f8}', '.table tbody tr:hover{background:#fffaf0}')

css = '''
/* LEEWAY_FINAL_UI */
.brandrow{width:100%;height:82px!important;margin:0 0 12px!important;display:flex!important;align-items:center!important;justify-content:center!important}
.side .brandmark{width:100%!important;height:82px!important;display:flex!important;align-items:center!important;justify-content:center!important;background:#fff!important;border:1px solid #d6b86a!important;border-radius:12px!important;padding:6px!important;overflow:hidden!important}
.side .brandmark img{display:block!important;width:auto!important;height:auto!important;max-width:100%!important;max-height:68px!important;object-fit:contain!important;margin:auto!important}
.login .brandrow{height:auto!important;margin:0 0 12px!important}
.login .brandmark{width:100%!important;height:82px!important;padding:8px!important;display:flex!important;align-items:center!important;justify-content:center!important;background:#fff!important;border:1px solid #d6b86a!important;overflow:hidden!important}
.login .brandmark img{display:block!important;width:auto!important;height:auto!important;max-width:94%!important;max-height:64px!important;object-fit:contain!important;margin:auto!important}
body.dark{background:#090c11!important;color:#f5f1e8!important;color-scheme:dark}
body.dark .app,body.dark .main,body.dark .content,body.dark .page{background:transparent!important;color:#f5f1e8!important}
body.dark .side{background:linear-gradient(180deg,#18150f,#0d1015)!important;color:#f5f1e8!important;border-right:1px solid #5d4717!important}
body.dark .logo,body.dark .nav-label{color:#d9bd72!important}
body.dark .logo b{color:#d6b86a!important}
body.dark .nav button{color:#ddd5c4!important;background:transparent!important}
body.dark .nav button:hover{background:#d6b86a18!important;color:#fff!important}
body.dark .nav button.active{background:linear-gradient(90deg,#9d7518,#c9a64f)!important;color:#fff!important}
body.dark header{background:#12161c!important;color:#f5f1e8!important;border-bottom:1px solid #4e3c16!important}
body.dark header h1,body.dark .hero h2,body.dark .section-title,body.dark .rule-card h3,body.dark .loginbox h1{color:#f5f1e8!important}
body.dark .eyebrow{color:#d6b86a!important}
body.dark .hero p,body.dark .drop p,body.dark .rule-card p,body.dark .empty,body.dark .setting-row,body.dark .kpi small,body.dark .kpi span,body.dark #dataStatus,body.dark #rowStat,body.dark .loginbox>p{color:#aaa99f!important}
body.dark .card{background:#151a21!important;border-color:#3f331c!important;color:#f5f1e8!important}
body.dark .mini div{background:#0f1319!important;border-color:#34302a!important;color:#aaa99f!important}
body.dark .mini b{color:#f5f1e8!important}
body.dark .drop{background:#10141a!important;border-color:#5d4a20!important;color:#f5f1e8!important}
body.dark .drop:hover{border-color:#d6b86a!important;background:#191710!important}
body.dark .notice{background:#271a17!important;border-color:#69352d!important;color:#efb1a8!important}
body.dark .filters input,body.dark .filters select,body.dark .loginbox input{background:#0d1117!important;color:#f5f1e8!important;border-color:#403a2d!important}
body.dark .filters input:focus,body.dark .filters select:focus,body.dark .loginbox input:focus{border-color:#d6b86a!important;box-shadow:0 0 0 3px #d6b86a18!important}
body.dark .tablewrap{background:#0d1117!important;border-color:#383323!important}
body.dark .table th{background:#191d24!important;color:#d2c9b7!important;border-color:#403a2d!important}
body.dark .table td{background:#0d1117!important;color:#eeeae0!important;border-color:#282b31!important}
body.dark .table tbody tr:hover td{background:#211d12!important}
body.dark .btn{background:#171b21!important;color:#f0eadc!important;border-color:#55451f!important}
body.dark .btn:hover{border-color:#d6b86a!important}
body.dark .primary{background:linear-gradient(90deg,#9d7518,#d6b86a)!important;color:#fff!important}
body.dark .progress{background:#292d34!important}
body.dark .progress i{background:linear-gradient(90deg,#9d7518,#d6b86a)!important}
body.dark .login{background:radial-gradient(circle at 80% 15%,#342910,#17140f 38%,#080a0e)!important}
body.dark .loginbox{background:#151a21!important;color:#f5f1e8!important;border-color:#6a511c!important}
body.dark .side .brandmark,body.dark .login .brandmark{background:#fff!important;border-color:#c49b3a!important}
body.dark .PRESENT{background:#123a29!important;color:#7be0ab!important}
body.dark .LATE{background:#422f12!important;color:#f3c56c!important}
body.dark .HALFDAY{background:#472719!important;color:#f3a86e!important}
body.dark .ABSENT{background:#481d1b!important;color:#ff9289!important}
body.dark .NOT{background:#1b2a40!important;color:#9ebce8!important}
@media(max-width:850px){.brandrow{height:64px!important;margin-bottom:10px!important}.side .brandmark{width:58px!important;height:64px!important;padding:4px!important}.side .brandmark img{max-width:100%!important;max-height:54px!important}.logo{font-size:0!important}.logo b{font-size:0!important}}
'''
s = s.replace('</style>', css + '\n</style>', 1)

js = """<script>(function(){function apply(){var d=localStorage.getItem('leeway-theme')==='dark';document.body.classList.toggle('dark',d)}window.toggleTheme=function(){var d=!document.body.classList.contains('dark');document.body.classList.toggle('dark',d);localStorage.setItem('leeway-theme',d?'dark':'light')};if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply);else apply()})();</script>"""
s = s.replace('</body>', js + '\n</body>', 1)
s = re.sub(r'<meta name="theme-color" content="#[0-9a-fA-F]+">', '<meta name="theme-color" content="#b88a20">', s, count=1)
p.write_text(s, encoding='utf-8')
print('UI fix written:', len(s))
