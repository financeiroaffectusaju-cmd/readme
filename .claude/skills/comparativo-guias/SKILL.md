---
name: comparativo-guias
description: Fluxo da Affectus para um paciente. Busca no sistema (affectusaju.com/sistema) as sessões e as evoluções do período, lê as guias Hapvida escaneadas e gera um PDF com o comparativo "data assinada na guia x atendimento no sistema" mais as evoluções por profissional. Usar quando a gestora pedir "mesmo processo" para um paciente, mandar guias escaneadas, ou pedir comparativo de guias e evoluções.
---

# Comparativo de guias x atendimentos + evoluções (por paciente)

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
