from openpyxl import load_workbook
import html
P="/home/user/readme/projeto-neurodivergentes/"
wb=load_workbook(P+"agenda-atendimentos.xlsx",data_only=True)
CLS={"BDD7EE":"p1","C6E0B4":"p2","FFE699":"p3","F8CBAD":"p4","D9C3E8":"p5","B7E1E0":"p6","FFF2CC":"hl","FFFF00":"hl",
     "EDEDED":"mut","D9D9D9":"mut","E2EFDA":"ok","FCE4D6":"mae","DDEBF7":"pai"}
def fmt(v,pct=False):
    if v is None: return ""
    if pct and isinstance(v,(int,float)): return f"{round(v*100)}%"
    if isinstance(v,float):
        if abs(v-round(v))<1e-9: return f"{int(round(v)):,}".replace(",",".")
        return f"{v:.1f}".replace(".",",")
    if isinstance(v,int): return f"{v:,}".replace(",",".") if v>9999 else str(v)
    return html.escape(str(v)).replace("\n","<br>")
def sheet(name):
    ws=wb[name]; merged={}
    for mr in ws.merged_cells.ranges:
        merged[(mr.min_row,mr.min_col)]=(mr.max_row-mr.min_row+1,mr.max_col-mr.min_col+1)
        for r in range(mr.min_row,mr.max_row+1):
            for c in range(mr.min_col,mr.max_col+1):
                if (r,c)!=(mr.min_row,mr.min_col): merged[(r,c)]=None
    out=[]; title=None; notes=[]
    for r in range(1,ws.max_row+1):
        nn=[c for c in range(1,ws.max_column+1) if ws.cell(r,c).value is not None]
        if not nn: continue
        if len(nn)==1 and nn[0]==1 and ws.cell(r,1).fill.fill_type is None and (r,1) not in merged:
            txt=fmt(ws.cell(r,1).value); b=ws.cell(r,1).font.bold
            if r==1 and title is None: title=txt; continue
            out.append(f'<tr class="note"><td colspan="{ws.max_column}"{" class=b" if b else ""}>{"<b>"+txt+"</b>" if b else txt}</td></tr>'); continue
        cells=[]
        for c in range(1,ws.max_column+1):
            if (r,c) in merged and merged[(r,c)] is None: continue
            cell=ws.cell(r,c); v=cell.value
            fill=cell.fill.fgColor.rgb[-6:] if cell.fill and cell.fill.fill_type=="solid" else None
            tag="td"; cl=[]
            if fill=="1F4E79": tag="th"
            elif fill in CLS: cl.append(CLS[fill])
            if cell.font and cell.font.bold and tag=="td": cl.append("b")
            if v is None and not cl and tag=="td": cells.append('<td class="e"></td>'); continue
            span=""
            if (r,c) in merged and merged[(r,c)]:
                rs,cs=merged[(r,c)]; span=f' colspan="{cs}"'+(f' rowspan="{rs}"' if rs>1 else "")
            cells.append(f'<{tag}{" class=\""+" ".join(cl)+"\"" if cl else ""}{span}>{fmt(v,cell.number_format=="0%")}</{tag}>')
        out.append("<tr>"+"".join(cells)+"</tr>")
    return title,"".join(out)
def tab(token,label,name,lead=""):
    title,t=sheet(name)
    return token,label,f'<h2>{html.escape(title or name)}</h2>{lead}<div class="tw"><table>{t}</table></div>'
li=lambda xs:"<ul>"+"".join(f"<li>{x}</li>" for x in xs)+"</ul>"
visao=f'''<h2>Visão geral</h2>
<p class="lead">Plano de atendimentos do Instituto Affectus para crianças neurodivergentes. Estrutura separada da clínica atual, em elaboração. Ano de referência: julho/2026 a junho/2027, 246 dias de atendimento em Aracaju/SE.</p>
<p><b>Plano adotado em 22/10/2026:</b> 300 crianças, cada uma com 16 sessões de terapia de 30 min por mês, em 1 visita de 2 h por semana, sempre no mesmo dia, horário e sala (8 horas de terapia por mês).</p>
<div class="cards">
<div class="card"><span class="k">Cenário adotado: 100% de ocupação</span><b>300 crianças</b><p>60 visitas por dia, sem vaga livre para reposição.</p></div>
<div class="card"><span class="k">Alternativa não adotada: 10% de reposição</span><b>270 crianças</b><p>54 visitas por dia e 6 vagas livres por dia para reposição.</p></div>
</div>
<p class="muted">A clínica entrega cerca de 53 a 59 mil sessões por ano. A grade nominal está na aba Grade semanal (C001 a C300). As opções avaliadas e descartadas ficam na aba Opções avaliadas.</p>
<h3>Em aberto</h3>
{li(["<b>São João (24/06/2027):</b> decidir depois. A chave está na aba Calendário (hoje descontado, 246 dias; funcionando seriam 247).",
"<b>8/12 (N. Sra. da Conceição):</b> conferir o decreto da Prefeitura. Carnaval e Corpus Christi estão confirmados como dias sem atendimento.",
"<b>Oficinas, origem dos pacientes e remuneração por turno:</b> serão definidos depois que a capacidade de atendimento estiver fechada em 100%.",
"<b>Perfil da demanda:</b> em aberto até a triagem. Os pacotes da grade são ilustrativos.",
"<b>Reposição:</b> no cenário de 300 crianças não há vaga reservada; a vaga de quem falta no dia pode repor outra criança do mesmo pacote."])}
<h3>Como foi calculado</h3>
{li(["Todas as sessões têm 30 min, em horários seguidos, e o dia vai das 7h às 19h com almoço das 12h às 13h.",
"Um solver montou a grade do dia e provou que cabem <b>60 visitas por dia</b> respeitando as vagas de cada sala. Mais de 62 visitas por dia não foram provadas nem descartadas.",
"Cada bloco recebe 1 criança por dia da semana: 60 blocos × 5 dias = 300 crianças.",
"<b>Atendimento médico:</b> 1 dia por mês por médico, com rodízio dos dias da semana. Todas as 300 crianças têm pelo menos 1 consulta no primeiro ano e o ciclo com os 3 médicos fecha em 20 meses (15 com consultas de 20 min).",
"Pacotes-modelo: cada criança tem 3 ou 4 especialidades e pelo menos 2 entre Psicologia, TO e Fonoaudiologia."])}'''
dec=f'''<h2>Decisões registradas</h2>
<h3>Terapias seriadas e salas</h3>
<div class="tw"><table class="wrap"><tr><th>Serviço</th><th>Estrutura</th></tr>
<tr><td>Fonoaudiologia, Terapia Ocupacional, Psicopedagogia, Psicomotricidade</td><td>1 sala cada, 2 profissionais por sala, cada um com 1 criança</td></tr>
<tr><td>Psicologia</td><td>1 sala dividida, 2 profissionais, cada um com seu paciente (conforme orientação do conselho)</td></tr>
<tr><td>Musicoterapia</td><td>1 sala, 1 profissional, individual</td></tr>
<tr><td>Terapia alimentar</td><td>1 sala, 1 nutricionista, 2 pacientes por vez</td></tr>
<tr><td>Atendimento médico</td><td>Neuropediatra, psiquiatra infantil e pediatra, 1 dia por mês de cada especialidade, consultas de 30 min, das 8h às 12h e das 13h às 17h. A criança passa pelos 3 médicos, não necessariamente no mesmo mês. Disponibilidade confirmada: 1 dia por mês por médico. Os dias médicos rodam entre os dias da semana e cada criança consulta no dia em que já vem (aba Médicos). Retorno a critério do médico.</td></tr>
<tr><td>Odontologia</td><td>2 dentistas, 1 por dia em todos os dias de atendimento (podem ser profissionais diferentes por dia). Consultas de 40 min. Primeira consulta e retorno em 4 a 5 meses, conforme a necessidade. Atendimento especializado para neurodivergentes.</td></tr>
<tr><td>Capoeira</td><td>1 sala, 1 profissional por vez, 1 por turno</td></tr>
<tr><td>Xadrez</td><td>1 sala, profissional próprio, 1 por turno</td></tr>
<tr><td>Oficinas profissionalizantes</td><td>1 sala única para todas, turmas fixas, para pais e mães</td></tr>
<tr><td>Psicóloga dos pais</td><td>1 sala, 1 psicóloga exclusiva, sessões de 30 min alternando individual e grupo</td></tr></table></div>
<h3>Regras do formato</h3>
{li(["Funcionamento de segunda a sexta, das 7h às 19h, almoço das 12h às 13h.",
"16 sessões de terapia por mês por criança (decisão de 22/10/2026), em 1 visita de 2 h por semana. Extras (xadrez, capoeira, oficinas, médicos, odontologia) ficam fora da conta.",
"Cada criança faz 3 ou 4 especialidades, sempre com pelo menos 2 das 3 principais: Psicologia, Terapia Ocupacional e Fonoaudiologia.",
"Todas as sessões de 30 min (formato C), horários seguidos, sem intervalo entre uma sala e outra. Crianças fora desse formato serão tratadas caso a caso.",
"Reposição: vagas livres, sem horário fixo reservado, 10% da capacidade no cenário com reposição (6 vagas por dia).",
"Remuneração dos profissionais por turno (manhã das 7h às 12h e tarde das 13h às 19h).",
"Estrutura separada: as regras e profissionais da agenda de reagendamento atual não se aplicam aqui."])}
<h3>Fluxos propostos</h3>
<div class="cols">
<div><h4>Terapia alimentar</h4><ol><li>Triagem com a família: histórico alimentar, sensibilidades, recusas, engasgos.</li><li>Avaliação da nutricionista e plano com metas graduais.</li><li>Sessões com exposição progressiva aos alimentos, no ritmo da criança.</li><li>Orientação aos pais ao fim de cada sessão e plano para casa.</li><li>Reavaliação periódica.</li></ol></div>
<div><h4>Xadrez e capoeira</h4><ul><li>Turmas por faixa etária e nível: xadrez com até 6 crianças, capoeira com até 10.</li><li>Aulas de 1 h no horário cheio, encaixadas antes ou depois da visita da criança, alternando uma e outra.</li><li>Xadrez: iniciação, prática guiada e mini-torneios internos.</li></ul></div>
<div><h4>Atendimento aos pais</h4><ul><li>Entrevista individual no início para criar vínculo.</li><li>1 sessão de 30 min a cada 2 visitas, alternando individual e grupo (grupos de até 8).</li><li>Nas visitas em que o pai ou a mãe não está com a psicóloga, vai para a oficina.</li></ul></div>
<div><h4>Oficinas (1 sala)</h4><ul><li>Mães: confeitaria e panificação, artesanato e personalizados, estética básica.</li><li>Pais: elétrica e instalações básicas, informática e manutenção de celulares, barbearia.</li><li>7 encontros de 1h30 por dia. Distribuição provisória na aba Serviços extras.</li></ul></div>
</div>'''
tabs=[("visao","Visão geral",visao),("decisoes","Decisões",dec)]
tabs.append(tab("plano","Plano adotado","Resumo"))
tabs.append(tab("semanal","Grade semanal","Semanal 16 sessões"))
tabs.append(tab("medicos","Médicos","Médicos"))
tabs.append(tab("agenda","Agenda médica","Agenda médica"))
tabs.append(tab("grade","Grade do dia","Grade do dia",'<p class="muted">Cada célula mostra o bloco de visita (B01 a B60) naquela vaga e horário; a cor é o pacote-modelo.</p>'))
tabs.append(tab("blocos","Blocos","Blocos"))
tabs.append(tab("calendario","Calendário","Calendário"))
tabs.append(tab("servicos","Serviços extras","Serviços extras"))
tabs.append(tab("equipe","Equipe e turnos","Equipe e turnos"))
tabs.append(tab("comparativo","Opções avaliadas","Comparativo"))
nav="".join(f'<button role="tab" data-t="{t}" id="b-{t}">{html.escape(l)}</button>' for t,l,_ in tabs)
secs="".join(f'<section id="s-{t}" role="tabpanel" hidden>{c}</section>' for t,l,c in tabs)
page=f'''<title>Instituto Affectus</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700&family=Figtree:wght@400;500;600&display=swap">
<style>
/* Layout: cabeçalho compacto, abas em linha rolável, uma seção por vez; tabelas largas rolam dentro do próprio contêiner. */
:root{{--bg:#F4F7F8;--surface:#FFFFFF;--fg:#14232B;--mut:#52646D;--line:#D3DCE0;--accent:#0E6B73;--th:#17414B;--thfg:#FFFFFF;
--p1:#CFE0F2;--p2:#D2E7C4;--p3:#F6E6A8;--p4:#F5D3BF;--p5:#E1D3EF;--p6:#C5E6E4;--hl:#FCEFC2;--mut2:#E7EBED;--ok:#DDEBD3;--mae:#F6D9D3;--pai:#D6E6F5;
--display:"Bricolage Grotesque","Trebuchet MS",system-ui,sans-serif;--body:"Figtree",system-ui,-apple-system,"Segoe UI",sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0E1A20;--surface:#15252D;--fg:#E3ECEF;--mut:#96A8B1;--line:#2B3E48;--accent:#5EC4CC;--th:#1F4D58;--thfg:#F2F8F9;
--p1:#263E56;--p2:#2B4529;--p3:#574A1C;--p4:#5C3B28;--p5:#40355A;--p6:#1F4D4C;--hl:#5A4B1E;--mut2:#25343B;--ok:#2B4529;--mae:#5B3131;--pai:#263E56;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0E1A20;--surface:#15252D;--fg:#E3ECEF;--mut:#96A8B1;--line:#2B3E48;--accent:#5EC4CC;--th:#1F4D58;--thfg:#F2F8F9;
--p1:#263E56;--p2:#2B4529;--p3:#574A1C;--p4:#5C3B28;--p5:#40355A;--p6:#1F4D4C;--hl:#5A4B1E;--mut2:#25343B;--ok:#2B4529;--mae:#5B3131;--pai:#263E56;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 var(--body);padding-inline:max(16px,env(safe-area-inset-left,0px)) max(16px,env(safe-area-inset-right,0px));padding-block:20px 40px}}
.wrap{{max-width:1180px;margin:0 auto}}
header{{display:flex;flex-direction:column;gap:4px;padding-bottom:14px}}
h1{{font:700 clamp(26px,5vw,38px)/1.1 var(--display);margin:0;letter-spacing:-.01em}}
.sub{{color:var(--mut);margin:0}}
nav{{display:flex;gap:6px;overflow-x:auto;padding:8px 0 12px;position:sticky;top:env(safe-area-inset-top,0px);background:var(--bg);z-index:5;border-bottom:1px solid var(--line);scrollbar-width:thin}}
nav button{{flex:none;font:500 14px var(--body);color:var(--fg);background:transparent;border:1px solid var(--line);border-radius:999px;padding:7px 14px;cursor:pointer}}
nav button[aria-selected="true"]{{background:var(--accent);border-color:var(--accent);color:var(--bg)}}
nav button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
section{{padding-top:18px}}
h2{{font:700 22px/1.2 var(--display);margin:0 0 10px}}
h3{{font:700 17px/1.3 var(--display);margin:26px 0 8px}}
h4{{font:700 15px/1.3 var(--display);margin:0 0 6px}}
p{{margin:0 0 10px;max-width:72ch}}
.lead{{font-size:16px}}
.muted{{color:var(--mut)}}
ul,ol{{margin:0 0 10px;padding-left:20px;max-width:78ch}} li{{margin:3px 0}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:14px 0}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px 16px;min-width:0}}
.card .k{{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}}
.card b{{display:block;font:700 26px/1.2 var(--display);margin:2px 0 6px;color:var(--accent)}}
.card p{{margin:0;font-size:14px}}
.cols{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}}
.cols>div{{min-width:0}}
.tw{{overflow-x:auto;margin:10px 0 6px;border:1px solid var(--line);border-radius:8px;background:var(--surface)}}
table{{border-collapse:collapse;font-size:13.5px;font-variant-numeric:tabular-nums;width:max-content;min-width:100%}}
th,td{{border:1px solid var(--line);padding:5px 9px;text-align:left;vertical-align:middle}}
th{{background:var(--th);color:var(--thfg);text-align:center;font-weight:600}}
td.b,td .b{{font-weight:600}} td.e{{border-color:transparent}}
tr.note td{{border:0;background:transparent;white-space:normal;max-width:80ch;padding-left:2px}}
td.p1{{background:var(--p1)}}td.p2{{background:var(--p2)}}td.p3{{background:var(--p3)}}td.p4{{background:var(--p4)}}td.p5{{background:var(--p5)}}td.p6{{background:var(--p6)}}
td.hl{{background:var(--hl)}}td.mut{{background:var(--mut2)}}td.ok{{background:var(--ok)}}td.mae{{background:var(--mae)}}td.pai{{background:var(--pai)}}
table.wrap{{width:100%}}table.wrap td{{white-space:normal;min-width:180px}}table.wrap th{{text-align:left}}
@media (max-width:600px){{table{{font-size:12.5px}}th,td{{padding:4px 6px}}}}
</style>
<div class="wrap">
<header><h1>Instituto Affectus</h1><p class="sub">16 sessões por mês, 1 visita por semana · crianças neurodivergentes · modelo de trabalho jul/2026 a jun/2027 · atualizado em 22/10/2026</p></header>
<nav role="tablist" aria-label="Seções">{nav}</nav>
{secs}
</div>
<script>
(function(){{
var tabs=[].slice.call(document.querySelectorAll('nav button'));
function show(t){{
  var ok=tabs.some(function(b){{return b.dataset.t===t}}); if(!ok) t='visao';
  tabs.forEach(function(b){{b.setAttribute('aria-selected',b.dataset.t===t?'true':'false')}});
  [].forEach.call(document.querySelectorAll('section'),function(s){{s.hidden=s.id!=='s-'+t}});
  var cur=document.getElementById('b-'+t); if(cur&&cur.scrollIntoView){{try{{cur.scrollIntoView({{block:'nearest',inline:'center'}})}}catch(e){{}}}}
}}
tabs.forEach(function(b){{b.addEventListener('click',function(){{show(b.dataset.t)}})}});
show((location.hash||'').slice(1)||'visao');
}})();
</script>'''
open(P+"instituto-affectus.html","w").write(page)
print(len(page))
