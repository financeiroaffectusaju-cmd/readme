from datetime import date, timedelta
from dateutil.easter import easter
import calendar, json
ini, fim = date(2026,7,1), date(2027,6,30)
easter27 = easter(2027)
nac = {
 date(2026,9,7):"Independência", date(2026,10,12):"N.Sra Aparecida", date(2026,11,2):"Finados",
 date(2026,11,15):"Proclamação", date(2026,11,20):"Consciência Negra", date(2026,12,25):"Natal",
 date(2027,1,1):"Confraternização", easter27-timedelta(days=2):"Sexta-feira Santa",
 date(2027,4,21):"Tiradentes", date(2027,5,1):"Trabalho",
}
fac = {easter27-timedelta(days=48):"Carnaval (seg, facultativo)", easter27-timedelta(days=47):"Carnaval (ter, facultativo)",
       easter27+timedelta(days=60):"Corpus Christi (facultativo)"}
loc = {date(2026,7,8):"Emancipação SE (se aplicável)", date(2026,12,8):"N.Sra Conceição (se aplicável)",
       date(2027,3,17):"Aniversário Aracaju (se aplicável)", date(2027,6,24):"São João (se aplicável)"}
def wk(d): return d.weekday()<5
rows=[]; d=ini
from collections import OrderedDict
m=OrderedDict()
while d<=fim:
    k=(d.year,d.month)
    m.setdefault(k,{"uteis":0,"nac":0,"fac":0,"loc":0})
    if wk(d):
        m[k]["uteis"]+=1
        if d in nac: m[k]["nac"]+=1
        if d in fac: m[k]["fac"]+=1
        if d in loc: m[k]["loc"]+=1
    d+=timedelta(days=1)
tot={"uteis":0,"nac":0,"fac":0,"loc":0}
for k,v in m.items():
    liq=v["uteis"]-v["nac"]
    print(f"{k[1]:02d}/{k[0]} uteis={v['uteis']:2d} nac={v['nac']} fac={v['fac']} loc={v['loc']} -> base nac={liq}, c/fac={liq-v['fac']}, c/fac+loc={liq-v['fac']-v['loc']}")
    for t in tot: tot[t]+=v[t]
print(tot, "base nacional:", tot['uteis']-tot['nac'], "c/ facultativos:", tot['uteis']-tot['nac']-tot['fac'], "c/ locais tambem:", tot['uteis']-tot['nac']-tot['fac']-tot['loc'])
print("Pascoa 2027:", easter27)
for dd,n in sorted({**nac,**fac,**loc}.items()):
    print(dd, dd.strftime('%a'), n, "(dia util)" if wk(dd) else "(fim de semana)")
