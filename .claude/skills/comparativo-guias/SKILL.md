---
name: comparativo-guias
description: Fluxo da Affectus para um paciente. Busca no sistema (affectusaju.com/sistema) as sessões e as evoluções do período, lê as guias Hapvida escaneadas e gera um PDF com o comparativo "data assinada na guia x atendimento no sistema" mais as evoluções por profissional. Chamado pela gestora de "Comparativo-guias" (ex.: "Comparativo-guias NOME DO PACIENTE" com as guias anexadas). Usar também quando ela pedir "mesmo processo" para um paciente, mandar guias escaneadas, ou pedir comparativo de guias e evoluções.
---

# Comparativo-guias: guias x atendimentos + evoluções (por paciente)

Nome do processo para a gestora: **Comparativo-guias**. Ao ser chamado, pedir o que faltar (paciente, guias, período) e seguir os passos abaixo.

Processo definido com a gestora em 27-28/10/2026. Um PDF por paciente. Só leitura: nunca salvar, concluir nem alterar nada no sistema.

## Entradas
- Nome do paciente.
- PDF/fotos das guias do paciente (Hapvida, "Guia de Serviço Profissional/SADT"). Podem vir giradas, de cabeça para baixo e escritas à mão.
- Período: o da planilha de agendamentos do mês, ou o que as guias cobrem (ex.: janeiro a maio). Confirmar com a gestora se for outro.
- Opcional: planilha de agendamentos (.xls que é HTML; `pandas.read_html(f, header=1)`), útil para saber quais profissionais atenderam o paciente no mês.

## Acesso
- O ambiente da sessão precisa liberar `affectusaju.com` (Network access do ambiente). Sem isso o proxy devolve 403 e nada funciona. A extensão do Chrome costuma não existir em sessão em nuvem; use o Chromium com Playwright.
- Login e senha NUNCA vão para arquivo nem para o repositório. Passar por variáveis de ambiente `LOGIN` e `SENHA` na hora de rodar. A gestora informa no chat; depois, lembrar que convém trocar a senha.
- Login: POST em `php/login.php` (campos `login`, `senha`); no Playwright, preencher `#login`, `#senha` e clicar `#logar`.

## Passo 1: ler as guias
1. Renderizar as páginas (`pdftoppm -r 200 -png`) e olhar cada uma. Girar quando preciso (PIL `rotate(90)`, `rotate(180)`); o texto da guia deve ficar legível.
2. De cada guia anotar: nº da guia, especialidade (campo 27), data de emissão (campo 7), quantidade autorizada (campo 29) e as datas assinadas do **campo 63** ("Data e Assinatura de Procedimentos em Série"), de 1 a 10.
3. Ampliar a faixa do campo 63 (render a 300 dpi, cortar em 4 partes e ampliar). Letra manuscrita erra fácil: marcar no PDF final que as datas foram lidas à mão e anotar as duvidosas no campo `nota` (ver abaixo).
4. Salvar em `guias.json`:
```json
[{"guia":"123456789","esp":"PSICOLOGIA","emissao":"15/01/2026","qtd":8,
  "datas":["13/01","13/01","20/01","20/01"],
  "nota":{"1":"Leitura manuscrita 10/03; confira se não é 07/03"}}]
```
`esp` deve ser igual à especialidade do profissional no sistema (PSICOLOGIA, FONOAUDIOLOGIA, TERAPEUTA OCUPACIONAL, MUSICOTERAPIA...). Uma entrada em `datas` por assinatura, repetindo a data quando assinada mais de uma vez.

## Passo 2: buscar sessões e evoluções no sistema
`scrape_sessoes.js` faz o roteiro da gestora para cada profissional da(s) especialidade(s): tela inicial (`painel.php?pag=agenda_profissional`), seleciona o profissional, lupa ao lado de Paciente, digita o nome em "Profissional/Fornecedores", Buscar, confere o nome, Selecionar, preenche Início e Término, Buscar. Depois, para cada sessão, abre o prontuário (`painel.php?pag=prontuario&id_atendimento=ID`, o mesmo destino do botão "Atender") e lê o campo Evolução (textarea `#exame_fisico`).

```bash
mkdir -p out
LOGIN=... SENHA=... PAC="NOME COMEÇO DO PACIENTE" PACRE="NOME COMPLETO DO PACIENTE" \
ESP="- (PSICOLOGIA|MUSICOTERAPIA)\s*$" TAG=paciente INICIO=2026-01-01 TERMINO=2026-05-31 \
NODE_PATH=$(npm root -g) node scrape_sessoes.js
```
- `PAC` é o texto digitado na busca; `PACRE` é a regex que filtra as linhas do paciente; `ESP` filtra os profissionais pela especialidade que aparece no fim do nome na lista (`NOME - ESPECIALIDADE`); inclua as especialidades das guias.
- A busca sem escolher profissional não traz tudo; por isso percorre os profissionais das especialidades.
- Conferir no log que "pacientes encontrados" tem só o paciente certo. Se houver homônimos, parar e perguntar.
- Roda em alguns minutos; em segundo plano com `nohup` e acompanhar o log (`FIM` no final). Saída: `out/TAG_sessoes_evol.json`.
- Nunca clicar em OK, Chamar na TV, Salvar e sair ou Concluir atendimento.


### Conferir se não faltou profissional (obrigatório)
A lista "Selecione o profissional" só traz profissionais ativos. Quem saiu da clínica não aparece e suas sessões escapam da varredura (caso real: Terapia Ocupacional da Clarissa em jan-mar, com a Juliana Profeta). Por isso, sempre cruzar com o **histórico do paciente**, que traz todas as sessões de todos os profissionais, com data, horário, situação, nº da guia e evolução:
1. Descobrir o id do paciente (célula `td.id` na busca do modal "Consultar Paciente").
2. `curl -c cj.txt -d "login=$LOGIN" -d "senha=$SENHA" https://affectusaju.com/sistema/php/login.php` e depois `python3 -I historico_paciente.py ID_DO_PACIENTE TAG` (usa o cookie `cj.txt` do diretório atual; grava `out/TAG_hist_ents.json` já filtrado em jan-mai; ajustar as datas no script se o período for outro).
3. Comparar a contagem do histórico com a da varredura. Se o histórico tiver mais sessões, completar com elas: buscar a evolução de cada id novo no prontuário (`painel.php?pag=prontuario&id_atendimento=ID`, `#exame_fisico`) e usar o conjunto completo no Passo 3. A evolução do histórico vem com entidades HTML e `|` no lugar das quebras; prefira o texto do prontuário. Para buscar a evolução de uma lista de ids: `LOGIN=... SENHA=... node evolucoes_por_id.js ids.json saida.json` (tenta 3 vezes por prontuário e não para se um falhar; ids que falham ficam com texto vazio e são listados no final; nesse caso use o texto da evolução que veio no histórico, decodificando as entidades HTML e removendo as tags. Aconteceu com as sessões de 02 a 13/01/2026 do Ian: o prontuário não abre, mas o histórico traz a evolução). Com mais de 150 sessões a busca leva uns 15 a 20 minutos; espere o arquivo de saída ter todos os ids antes de montar o PDF. O histórico traz também o **Nº da guia** de cada sessão (campo `guia`), útil para conferir a qual guia o sistema vinculou o atendimento.
4. Especialidades sem guia (ex.: Socialização) entram nas evoluções, mas não na lista "sem data assinada".
Anelly (81) e Jasminy (57) foram conferidas: a varredura já estava completa.

## Passo 3: comparar e gerar o PDF
```bash
WORKDIR=. python3 -I build_comparativo.py "NOME COMPLETO" out/TAG_sessoes_evol.json guias.json Paciente_comparativo_guias_evolucoes.pdf "janeiro a maio de 2026"
```
Regras do comparativo:
- Cada data assinada é conferida com as sessões **da mesma especialidade** (qualquer profissional) naquele dia.
- Contam como atendimento as situações **CONCLUIDO** e **FORÇA TAREFA** (sessões do programa Força Tarefa Hapvida; não têm evolução no prontuário).
- Duas assinaturas na mesma data exigem duas sessões nesse dia; a que sobrar é inconsistência.
- Situações FALTOU, CANCELADO, AGENDADO e CONFIRMADO não contam: se a data foi assinada e a sessão está assim, é inconsistência ("assinada, mas no sistema consta como ...").
- Sessões concluídas que não casam com nenhuma assinatura vão para a seção "Atendimentos realizados sem data assinada nas guias anexadas" (podem ser de guias que não foram anexadas).
- Sessões autorizadas e ainda não assinadas na guia aparecem só na tabela-resumo (Autorizadas x Assinadas); não são inconsistência.
- O PDF tem: resumo, uma página por guia (verde = OK, vermelho = inconsistente), sessões sem guia, e as evoluções por profissional em ordem cronológica (sessão sem texto aparece como "Sem evolução registrada").

## Entrega
- Enviar o PDF ao usuário e resumir: quantas inconsistências, quais guias, o que é leitura duvidosa de letra, sessões ainda "Confirmado" sem evolução.
- Nunca guardar guias, PDFs, evoluções ou JSON de pacientes no repositório (dados clínicos). Só os scripts e este roteiro ficam versionados.
- Dependências: node + `playwright` (já vem instalado no ambiente), python3 com `reportlab` e `pandas`, `poppler-utils` (`pdftoppm`).
