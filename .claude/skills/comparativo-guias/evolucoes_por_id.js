const { chromium } = require('playwright');
const fs=require('fs');
(async () => {
  const ids=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
  const b = await chromium.launch(); const p = await b.newPage();
  p.on('dialog', d=>d.accept().catch(()=>{}));
  await p.goto('https://affectusaju.com/sistema/index.php');
  await p.fill('#login', process.env.LOGIN); await p.fill('#senha', process.env.SENHA);
  await Promise.all([p.waitForURL(/painel\.php/), p.click('#logar')]);
  const out={}, falhas=[];
  for (const id of ids){
    let ok=false;
    for (let t=0;t<3&&!ok;t++){
      try{
        await p.goto('https://affectusaju.com/sistema/painel.php?pag=prontuario&id_atendimento='+id,{timeout:45000});
        await p.waitForSelector('#exame_fisico',{state:'attached',timeout:20000}); await p.waitForTimeout(400);
        out[id]=await p.evaluate(()=>{const v=document.getElementById('exame_fisico').value; const d=new DOMParser().parseFromString(v,'text/html'); return (d.body.innerText||d.body.textContent||'').trim();});
        ok=true;
      }catch(e){ if(t==2){ out[id]=''; falhas.push(id);} }
    }
    fs.writeFileSync(process.argv[3],JSON.stringify(out,null,1));
  }
  console.log('ok',Object.keys(out).length,'falhas',JSON.stringify(falhas));
  await b.close();
})();
