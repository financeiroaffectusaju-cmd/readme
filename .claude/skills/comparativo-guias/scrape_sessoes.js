const { chromium } = require('playwright');
const fs=require('fs');
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({viewport:{width:1500,height:1100}}); const p = await ctx.newPage();
  p.on('dialog', d=>d.accept().catch(()=>{}));
  await p.goto('https://affectusaju.com/sistema/index.php');
  await p.fill('#login', process.env.LOGIN); await p.fill('#senha', process.env.SENHA);
  await Promise.all([p.waitForURL(/painel\.php/), p.click('#logar')]);
  await p.goto('https://affectusaju.com/sistema/painel.php?pag=agenda_profissional');
  const opts = (await p.$$eval('#idProfBusca option', o => o.map(x => [x.value, x.textContent.trim()]))).filter(o=>o[0] && new RegExp(process.env.ESP,'i').test(o[1]));
  console.log('profissionais a varrer:', opts.length);
  await p.click('tbody.filtro .buscar_paciente');
  await p.fill('#buscarPaciente #associado',process.env.PAC);
  await p.click('#btnBuscarAssociadosModal');
  await p.waitForSelector('#buscarPaciente .selecionarResponsavel');
  console.log('pacientes encontrados:', JSON.stringify(await p.$$eval('#buscarPaciente .retornoAssociados td.nome', e=>e.map(x=>x.textContent.trim()))));
  await p.click('#buscarPaciente .selecionarResponsavel');
  await p.waitForTimeout(1200);
  await p.fill('tbody.filtro input.inicio',process.env.INICIO||'2026-01-01');
  await p.fill('tbody.filtro input.termino',process.env.TERMINO||'2026-05-31');
  const out=[];
  for (const [id,label] of opts) {
    await p.selectOption('#idProfBusca',id);
    await p.click('tbody.filtro .consultar_agendamento_prof');
    await p.waitForTimeout(2500);
    const rows = await p.$$eval('tr.aff-row', trs=>trs.map(tr=>{const c=[...tr.querySelectorAll('td')].map(t=>t.innerText.trim().replace(/\s+/g,' ')); return {id:tr.dataset.idAtendimento,idProf:(tr.querySelector('.idProf')||{}).value,paciente:c[1],proc:c[2],data:c[4],sessao:c[5],ini:c[6],fim:c[7],status:c[8]};}));
    const mine = rows.filter(r=>new RegExp(process.env.PACRE,'i').test(r.paciente||'') && r.idProf===id);
    if (mine.length) console.log(label, mine.length);
    for (const r of mine){ r.profissional=label.replace(/\s*-\s*[^-]*$/,'').trim(); r.especialidade=label.split(' - ').pop().trim(); out.push(r);}
    fs.writeFileSync(`out/${process.env.TAG}_sessoes.json`, JSON.stringify(out,null,1));
  }
  console.log('total sessões:', out.length);
  for (const [i,r] of out.entries()) {
    await p.goto('https://affectusaju.com/sistema/painel.php?pag=prontuario&id_atendimento='+r.id);
    await p.waitForSelector('#exame_fisico',{state:'attached'});
    await p.waitForTimeout(500);
    r.evolucao = await p.evaluate(()=>{const v=document.getElementById('exame_fisico').value; const d=new DOMParser().parseFromString(v,'text/html'); return (d.body.innerText||d.body.textContent||'').trim();});
    if (i%10==0) fs.writeFileSync(`out/${process.env.TAG}_sessoes_evol.json`, JSON.stringify(out,null,1));
  }
  fs.writeFileSync(`out/${process.env.TAG}_sessoes_evol.json`, JSON.stringify(out,null,1));
  console.log('FIM');
  await b.close();
})().catch(e=>{console.error('ERRO',e.message);process.exit(1)});
