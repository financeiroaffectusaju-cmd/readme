import re,json,sys,collections,subprocess
def fetch(idc,out):
    subprocess.run(['curl','-sS','-m','60','-b','cj2.txt','-d',f'id_cliente={idc}','https://affectusaju.com/sistema/php/prontuario/historico_atendimentos_paciente.php','-o',out],check=True)
def parse(path):
    h=open(path,encoding='utf-8',errors='replace').read()
    body=h[h.find('</style>'):]
    t=re.sub(r'<script.*?</script>','',body,flags=re.S)
    txt=re.sub(r'(\|\s*)+','|',re.sub(r'\s+',' ',re.sub(r'<[^>]+>','|',t)))
    pat=re.compile(r'\|([^|]+)\|([^|]+)\|(\d\d/\d\d/\d{4})\|(\d\d:\d\d) - (\d\d:\d\d) ?\|Sessão: ([^|]*)\|([^|]+)\|#(\d+)\|(.*?)(?=\|[^|]+\|[^|]+\|\d\d/\d\d/\d{4}\|\d\d:\d\d - |\Z)')
    ents=[]
    for m in pat.finditer(txt):
        prof,esp,data,ini,fim,sess,status,aid,rest=m.groups()
        ev=re.search(r'Evolução\|(.*?)\|Observações',rest); gu=re.search(r'Nº Guia:\|([^|]*)',rest)
        ents.append(dict(profissional=prof.strip(),especialidade=esp.strip(),data=data,ini=ini,fim=fim,sessao=sess,status=status.strip(),id=aid,evolucao=(ev.group(1) if ev else ''),guia=(gu.group(1) if gu else '')))
    return ents
if __name__=='__main__':
    idc,tag=sys.argv[1:3]
    fetch(idc,f'out/{tag}_hist.html'); e=parse(f'out/{tag}_hist.html')
    e=[x for x in e if '2026-01-01'<=x['data'][6:]+'-'+x['data'][3:5]+'-'+x['data'][:2]<='2026-05-31']
    print(tag,len(e)); c=collections.Counter((x['especialidade'],x['profissional']) for x in e)
    for k,v in sorted(c.items()): print(' ',k,v)
    json.dump(e,open(f'out/{tag}_hist_ents.json','w'),ensure_ascii=False)
