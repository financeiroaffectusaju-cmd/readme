from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
OUT="/home/user/readme/projeto-neurodivergentes/resumo-volume-atendimentos.xlsx"
F="Arial"; bf=Font(name=F); bold=Font(name=F,bold=True); blue=Font(name=F,color="0000FF"); title=Font(name=F,bold=True,size=14)
hf=Font(name=F,bold=True,color="FFFFFF"); hfill=PatternFill("solid",fgColor="1F4E79"); sec=PatternFill("solid",fgColor="DDEBF7"); tot=PatternFill("solid",fgColor="E2EFDA")
thin=Side(style="thin",color="BFBFBF"); bd=Border(left=thin,right=thin,top=thin,bottom=thin)
ctr=Alignment(horizontal="center",vertical="center",wrap_text=True); left=Alignment(vertical="center",wrap_text=True)
wb=Workbook(); wp=wb.active; wp.title="Premissas"
wp["A1"]="Premissas (azul = informado; pode ser alterado e tudo se recalcula)"; wp["A1"].font=title
P=[("Dias de atendimento por ano",246,"Calendário de Aracaju, jul/2026 a jun/2027 (inclui São João descontado; funcionando seriam 247)"),
("Dias de atendimento por semana",5,"Segunda a sexta"),
("Meses por ano",12,""),
("Crianças atendidas",300,"Cenário de 100% de ocupação"),
("Visitas por dia",60,"Grade comprovada: 60 blocos de visita por dia, 1 criança por bloco e por dia da semana"),
("Sessões de 30 min por visita",4,"4 especialidades por criança"),
("Minutos por sessão",30,""),
("Vagas de sessão por sala por dia",22,"11 horas úteis ÷ 30 min"),
("Consultas médicas por dia médico",16,"30 min, das 8h às 12h e das 13h às 17h"),
("Dias médicos por ano",36,"1 dia por mês por médico, 3 médicos"),
("Consultas odontológicas por criança por ano",3,"Primeira consulta e retornos a cada 4 a 5 meses"),
("Vagas de consulta odontológica por dia",16,"1 dentista por dia, 40 min por consulta"),
("Parcela das visitas com xadrez",0.5,"Xadrez e capoeira alternam a cada visita"),
("Crianças por turma de xadrez",6,""),("Crianças por turma de capoeira",10,""),
("Parcela das visitas com sessão da psicóloga dos pais",0.5,"1 sessão a cada 2 visitas"),
("Parcela das sessões da psicóloga em grupo",0.5,"Alterna individual e grupo"),
("Pais por grupo da psicóloga",8,""),
("Pais por turma de oficina",10,"Estimativa; funcionamento das oficinas a definir")]
for i,(a,b,c) in enumerate(P):
    r=3+i; wp.cell(r,1,a).font=bf; x=wp.cell(r,2,b); x.font=blue; wp.cell(r,3,c).font=bf
    if isinstance(b,float): x.number_format="0%"
    for k in (1,2,3): wp.cell(r,k).border=bd
wp.column_dimensions["A"].width=52; wp.column_dimensions["B"].width=12; wp.column_dimensions["C"].width=88
ref={n:f"Premissas!$B${3+i}" for i,(n,_,_) in enumerate(P)}
D=ref["Dias de atendimento por ano"]; SEM=ref["Dias de atendimento por semana"]; MES=ref["Meses por ano"]
K=ref["Crianças atendidas"]; V=ref["Visitas por dia"]; SV=ref["Sessões de 30 min por visita"]; MIN=ref["Minutos por sessão"]; VAG=ref["Vagas de sessão por sala por dia"]

ws=wb.create_sheet("Resumo",0)
ws["A1"]="Instituto Affectus – volume de atendimentos para validação"; ws["A1"].font=title
ws["A2"]="Cenário: 300 crianças, 16 sessões de 30 min por mês, 1 visita de 2 h por semana. Semana = 5 dias de atendimento; mês = média de 246 dias ÷ 12; ano = 246 dias."; ws["A2"].font=bf
H=["Atendimento","Por dia","Por semana","Por mês","Por ano","Como foi calculado"]
def hdr(r,cols=H):
    for i,v in enumerate(cols):
        c=ws.cell(r,1+i,v); c.font=hf; c.fill=hfill; c.alignment=ctr; c.border=bd
r=4; hdr(r)
rows=[]  # guarda linhas para total
def section(t):
    global r
    r+=1
    for c in range(1,8): ws.cell(r,c).fill=sec; ws.cell(r,c).border=bd
    ws.cell(r,1,t).font=bold
def line(name,annual,note,fmt="#,##0",boldrow=False,occ=None,fill=None):
    global r
    r+=1
    ws.cell(r,1,name).font=bold if boldrow else bf
    ws.cell(r,5,annual)
    ws.cell(r,2,f"=E{r}/{D}"); ws.cell(r,3,f"=E{r}/({D}/{SEM})"); ws.cell(r,4,f"=E{r}/{MES}")
    ws.cell(r,6,note).font=bf
    for c in range(1,7):
        x=ws.cell(r,c); x.border=bd
        if c in (2,3,4,5): x.number_format=fmt; x.font=bold if boldrow else bf; x.alignment=ctr
        if c in (1,6): x.alignment=left
        if fill: x.fill=fill
    return r
# resumo geral
section("Números-chave")
rk=line("Famílias presentes (visitas)",f"={V}*{D}","60 visitas por dia: cada criança vem 1 vez por semana")
section("Terapias seriadas (todas as especialidades)")
rv=line("Visitas de 2 h",f"={V}*{D}","60 visitas por dia")
rs=line("Sessões de 30 min",f"=E{rv}*{SV}","4 sessões por visita; 16 por criança a cada 4 semanas",boldrow=True,fill=tot)
rh=line("Horas de terapia",f"=E{rs}*{MIN}/60","Sessões × 30 min",fmt="#,##0")
section("Sessões por especialidade (pacotes-modelo; a composição real depende da triagem)")
SP=[("Psicologia",42,2),("Terapia Ocupacional",39,2),("Fonoaudiologia",39,2),("Psicopedagogia",33,2),("Psicomotricidade",39,2),("Musicoterapia",18,1),("Terapia alimentar",30,2)]
first=r+1
for n,d,v in SP:
    rr=line(n,f"={d}*{D}",f"{d} sessões por dia na grade; {v} vaga(s) simultânea(s)")
    ws.cell(rr,7,f"=B{rr}/({v}*{VAG})").number_format="0%"; ws.cell(rr,7).alignment=ctr; ws.cell(rr,7).border=bd; ws.cell(rr,7).font=bf
    ws.cell(rr,2).font=blue if False else bf
    ws.cell(rr,5).value=f"={d}*{D}"
last=r
rr=line("Conferência: soma das especialidades",f"=SUM(E{first}:E{last})","Deve ser igual às sessões de 30 min")
section("Demais atendimentos")
rm=line("Consultas médicas (neuropediatra, psiquiatra infantil e pediatra)",f"={ref['Consultas médicas por dia médico']}*{ref['Dias médicos por ano']}","16 consultas por dia médico; 36 dias médicos por ano. 'Por dia' é a média dos 246 dias; em cada dia médico são 16.")
ro=line("Consultas odontológicas",f"={K}*{ref['Consultas odontológicas por criança por ano']}","300 crianças × 3 consultas por ano. Capacidade: 16 vagas por dia.")
rx=line("Xadrez: participações de crianças",f"={V}*{ref['Parcela das visitas com xadrez']}*{D}","Metade das visitas")
rxa=line("Xadrez: aulas de 1 h",f"=ROUNDUP({V}*{ref['Parcela das visitas com xadrez']}/{ref['Crianças por turma de xadrez']},0)*{D}","Turmas de 6 crianças")
rc=line("Capoeira: participações de crianças",f"={V}*(1-{ref['Parcela das visitas com xadrez']})*{D}","Outra metade das visitas")
rca=line("Capoeira: aulas de 1 h",f"=ROUNDUP({V}*(1-{ref['Parcela das visitas com xadrez']})/{ref['Crianças por turma de capoeira']},0)*{D}","Turmas de 10 crianças")
rpi=line("Psicóloga dos pais: sessões individuais de 30 min",f"={V}*{ref['Parcela das visitas com sessão da psicóloga dos pais']}*(1-{ref['Parcela das sessões da psicóloga em grupo']})*{D}","1 sessão a cada 2 visitas; metade individual")
rpg=line("Psicóloga dos pais: participações em grupo",f"={V}*{ref['Parcela das visitas com sessão da psicóloga dos pais']}*{ref['Parcela das sessões da psicóloga em grupo']}*{D}","Metade em grupo")
rpe=line("Psicóloga dos pais: encontros de grupo de 30 min",f"=ROUNDUP({V}*{ref['Parcela das visitas com sessão da psicóloga dos pais']}*{ref['Parcela das sessões da psicóloga em grupo']}/{ref['Pais por grupo da psicóloga']},0)*{D}","Grupos de 8 pais")
rf=line("Oficinas: participações de pais e mães",f"={V}*(1-{ref['Parcela das visitas com sessão da psicóloga dos pais']})*{D}","Pais que não estão com a psicóloga na visita. Estimativa; funcionamento a definir.")
rfa=line("Oficinas: encontros de 1h30",f"=ROUNDUP({V}*(1-{ref['Parcela das visitas com sessão da psicóloga dos pais']})/{ref['Pais por turma de oficina']},0)*{D}","Turmas de 10 pessoas. Capacidade: 7 encontros por dia")
section("Total")
rt=line("Total de atendimentos e participações",f"=E{rs}+E{rm}+E{ro}+E{rx}+E{rc}+E{rpi}+E{rpg}+E{rf}","Terapias + consultas médicas e odontológicas + participações de crianças (xadrez, capoeira) e de pais (psicóloga, oficinas). Não soma aulas e encontros de grupo.",boldrow=True,fill=tot)
ws.cell(r+2,1,"Observações").font=bold
obs=["Os números de terapias por especialidade vêm de pacotes-modelo; quando a triagem mostrar a demanda real, a divisão entre especialidades muda, mas o total de 240 sessões por dia não muda.",
"Os valores 'por dia' dos serviços que não funcionam todo dia (consultas médicas) são médias; no dia médico são 16 consultas por médico.",
"Terapias, xadrez, capoeira, psicóloga dos pais e consultas médicas já constam da grade e das abas Médicos e Agenda médica do artefato Instituto Affectus. Odontologia e oficinas são estimativas de demanda.",
"Crianças de segunda e sexta fazem 48 visitas por ano; as de terça a quinta, 50 (feriados). A diferença é de até 4 sessões por criança no ano.",
"Pontos ainda abertos: São João (24/06/2027), oficinas, origem dos pacientes e remuneração por turno."]
for i,t in enumerate(obs):
    c=ws.cell(r+3+i,1,t); c.font=bf
for col,w in zip("ABCDEFG",(58,12,13,12,13,86,16)): ws.column_dimensions[col].width=w
ws.cell(4,7,"Ocupação das vagas").font=hf; ws.cell(4,7).fill=hfill; ws.cell(4,7).alignment=ctr; ws.cell(4,7).border=bd
ws.row_dimensions[4].height=30; ws.freeze_panes="B5"
wb.save(OUT); print("ok",r)
