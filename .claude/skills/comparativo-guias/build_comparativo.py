import json,collections,re,sys
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os
S=os.environ.get("WORKDIR",".").rstrip("/")+"/"
paciente,sessf,guif,outf,periodo=sys.argv[1:6]
sess=json.load(open(S+sessf)); guias=json.load(open(S+guif))
fixn={'RIVâNIA DOS REIS':'RIVÂNIA DOS REIS'}
for r in sess:
    r['profissional']=fixn.get(r['profissional'],r['profissional']).strip()
    r['evolucao']=re.sub(r'\n\s*\n+','\n',re.sub(r'[ \t]+',' ',(r['evolucao'] or '').replace('\xa0',' '))).strip(); r['usada']=False
sess.sort(key=lambda r:(r['data'][6:]+r['data'][3:5]+r['data'][:2],r['ini']))
OK={'CONCLUIDO','FORÇA TAREFA'}
guias.sort(key=lambda g:(g['emissao'][6:]+g['emissao'][3:5]+g['emissao'][:2],g['guia']))
res=[];inc=0
for g in guias:
    rows=[];cnt=collections.Counter(g['datas'])
    for i,d in enumerate(g['datas'],1):
        cand=[r for r in sess if r['especialidade']==g['esp'] and r['data'][:5]==d and not r['usada']]
        att=[r for r in cand if r['status'] in OK]
        nota=(g.get('nota') or {}).get(str(i),'')
        if att:
            m=att[0];m['usada']=True
            obs=nota or ('Sessão da Força Tarefa (sem evolução no prontuário)' if m['status']=='FORÇA TAREFA' else ('Concluído, sem evolução registrada' if not m['evolucao'] else ''))
            rows.append((i,d,f"{m['profissional']} - {m['ini']}",'Força Tarefa' if m['status']=='FORÇA TAREFA' else m['status'].title(),'OK',obs))
        elif cand:
            m=cand[0];m['usada']=True;inc+=1
            rows.append((i,d,f"{m['profissional']} - {m['ini']}",m['status'].title(),'INC',(nota+'. ' if nota else '')+f"Data assinada na guia, mas no sistema a sessão consta como {m['status'].title()}"))
        else:
            same=[r for r in sess if r['data'][:5]==d and r['especialidade']==g['esp']]
            msg='Não há atendimento desta especialidade nesta data no sistema' if not same else f"Todas as sessões desta data já foram contadas ({len(same)}); assinada {cnt[d]}x na guia"
            inc+=1;rows.append((i,d,'-','Sem atendimento','INC',(nota+'. ' if nota else '')+msg))
    res.append((g,rows))
espg={g['esp'] for g in guias}
orf=[r for r in sess if not r['usada'] and r['status'] in OK and r['especialidade'] in espg]
print('inconsistências:',inc,'| sem data em guia:',len(orf))
for g,rows in res: print(g['guia'],g['esp'],sum(1 for r in rows if r[4]=='OK'),'/',len(rows),'assinadas; autorizadas',g['qtd'])
ss=getSampleStyleSheet()
cell=ParagraphStyle('c',parent=ss['BodyText'],fontSize=8.5,leading=10.5)
head=ParagraphStyle('h',parent=cell,textColor=colors.white,fontName='Helvetica-Bold')
vazio=ParagraphStyle('v',parent=cell,textColor=colors.grey,fontName='Helvetica-Oblique')
body=ParagraphStyle('b',parent=ss['BodyText'],fontSize=9.5,leading=12)
TEAL=colors.HexColor('#01a6a9');RED=colors.HexColor('#fde2e2');GRN=colors.HexColor('#e6f6ec')
def P(t,s=cell): return Paragraph(escape(str(t)),s)
d=SimpleDocTemplate(S+outf,pagesize=A4,leftMargin=30,rightMargin=30,topMargin=32,bottomMargin=32,title="Comparativo guias x atendimentos - "+paciente)
esps=collections.Counter(g['esp'] for g in guias)
el=[Paragraph("Comparativo: datas assinadas nas guias x atendimentos no sistema",ss['Title']),
 Paragraph(f"<b>Paciente:</b> {escape(paciente)} (Hapvida)<br/><b>Período analisado:</b> {periodo}<br/><b>Guias analisadas:</b> {len(guias)} ("+", ".join(f"{e.title()} {n}" for e,n in esps.items())+")",body),Spacer(1,6),
 Paragraph(f"<b>Resultado:</b> {inc} datas assinadas nas guias sem atendimento concluído correspondente no sistema, e {len(orf)} atendimentos realizados sem data assinada em nenhuma das guias anexadas.",body),Spacer(1,4),
 Paragraph("<b>Como a comparação foi feita:</b> cada data assinada no campo 63 da guia foi conferida com as sessões da mesma especialidade no sistema (agenda do profissional). Contam como atendimento as sessões com situação Concluído ou Força Tarefa. Duas assinaturas na mesma data exigem duas sessões nesse dia. As datas foram lidas à mão a partir do escaneamento; confira nas guias as que forem decisivas.",body),Spacer(1,8)]
rs=[[P(x,head) for x in ['Guia','Especialidade','Emissão','Autorizadas','Assinadas','OK','Inconsist.']]]
for g,rows in res:
    ok=sum(1 for r in rows if r[4]=='OK');rs.append([P(g['guia']),P(g['esp'].title()),P(g['emissao']),P(g['qtd']),P(len(rows)),P(ok),P(len(rows)-ok)])
t=Table(rs,colWidths=[75,110,65,62,60,40,60],hAlign='LEFT');t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,colors.grey),('BACKGROUND',(0,0),(-1,0),TEAL)]));el+=[t]
for g,rows in res:
    el+=[PageBreak(),Paragraph(f"Guia {g['guia']} - {g['esp'].title()} (emitida em {g['emissao']}, {g['qtd']} sessões autorizadas, {len(rows)} assinadas)",ss['Heading2'])]
    data=[[P(x,head) for x in ['#','Data assinada','Atendimento no sistema','Situação','Resultado','Observação']]]
    for i,dd,det,sit,rr,obs in rows: data.append([P(i),P(dd+'/2026'),P(det),P(sit),P('OK' if rr=='OK' else 'Inconsistente'),P(obs)])
    t=Table(data,colWidths=[18,62,140,68,76,176],repeatRows=1,hAlign='LEFT')
    st=[('GRID',(0,0),(-1,-1),.5,colors.grey),('BACKGROUND',(0,0),(-1,0),TEAL),('VALIGN',(0,0),(-1,-1),'TOP')]
    for j,r in enumerate(rows,1): st.append(('BACKGROUND',(0,j),(-1,j),GRN if r[4]=='OK' else RED))
    t.setStyle(TableStyle(st));el+=[t]
el+=[PageBreak(),Paragraph("Atendimentos realizados sem data assinada nas guias anexadas",ss['Heading2']),
 Paragraph("Sessões concluídas (ou da Força Tarefa) que não aparecem em nenhuma das guias anexadas. Podem pertencer a guias que não foram anexadas.",body),Spacer(1,6)]
if orf:
    data=[[P(x,head) for x in ['Data','Horário','Especialidade','Profissional','Situação']]]
    for r in orf: data.append([P(r['data']),P(f"{r['ini']}-{r['fim']}"),P(r['especialidade'].title()),P(r['profissional'].title()),P(r['status'].title())])
    t=Table(data,colWidths=[62,70,120,190,80],repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,colors.grey),('BACKGROUND',(0,0),(-1,0),TEAL),('VALIGN',(0,0),(-1,-1),'TOP')]));el+=[t]
else: el.append(Paragraph("Nenhum.",body))
el+=[PageBreak(),Paragraph(f"Evoluções dos atendimentos ({periodo})",ss['Title'])]
profs=[]
for r in sess:
    p=(r['profissional'],r['especialidade'])
    if p not in profs: profs.append(p)
for p,e in sorted(profs,key=lambda x:(x[1],x[0])):
    g=[r for r in sess if r['profissional']==p and r['especialidade']==e]
    el.append(Paragraph(f"{escape(p)} - {escape(e)}",ss['Heading2']))
    data=[[P(x,head) for x in ['Data','Horário','Situação','Evolução']]]
    for r in g:
        ev=Paragraph(escape(r['evolucao']).replace('\n','<br/>'),cell) if r['evolucao'] else Paragraph('Sem evolução registrada',vazio)
        data.append([P(r['data']),P(f"{r['ini']}-{r['fim']}"),P(r['status']),ev])
    t=Table(data,colWidths=[58,62,78,342],repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,colors.grey),('BACKGROUND',(0,0),(-1,0),TEAL),('VALIGN',(0,0),(-1,-1),'TOP')]));el+=[t,Spacer(1,10)]
d.build(el)
