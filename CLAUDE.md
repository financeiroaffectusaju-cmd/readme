# Contexto do Painel de Reagendamento v2 (Affectus)

Artefato: https://claude.ai/artifact/JmDzos4bmmNDP8og4mVjKJ (privado, da gestora).

## Documento mensal por paciente (decisão da gestora, 12/10/2026)
No fim de cada mês a gestora emite, para cada paciente, um documento com tudo o que foi reagendado no mês:
- datas das reposições (data da falta e data da reposição);
- especialidades;
- profissionais que atenderam o paciente;
- campo de assinatura do responsável pelo paciente.

Ao ser pedida a gerar esse documento, montar um por paciente a partir da coleção `sessoes` do banco do painel (campos `pac`, `dataOrig`, `data`, `ini`, `fim`, `esp`, `prof`, `status`), considerando só as sessões do mês e fora de "Sem retorno". Entregar em Word ou PDF, um por paciente.

## Relatório de biometria
Pacientes atendidos sem coleta de biometria (limite de 4 coletas por dia) ficam na aba Biometria, com histórico por paciente. O relatório do mês é anexado às guias.

## Fontes de dados e equipe (decisão da gestora, 22/10/2026)
- A agenda dos profissionais (horários dos próximos dias) está no Google Drive da gestora. Usar o conector do Drive para buscá-la; não pedir a exportação de novo. Planilha: "AGENDA AFFECTUS - OFICIAL" (Google Sheets, id `1xPxozKD544q8FoR24_RSArWUyflxrgDo4HmwJu4i_xY`, atualizada em 21/10). Há ainda "HORÁRIOS DAS SALAS" (id `1wh3RvIWBgWP08kj46WGZVHc7CJZNUu_mgfKTRtQRVbo`).
- As faltas de cada dia vêm em arquivo `agendamentos_-_<data>.xls` (na prática um HTML com tabela; colunas Data, Profissional, Especialidade, Paciente, Biometria, Inicio, Fim, Sessões, Guia, Situação...). Falta = Situação "FALTOU". Entram na coleção `sessoes` como origem "Falta DD/MM", id `fDDMM-NNNN`.
- Equipe de reagendamento: Marcela, Lara, Mylena e Renata (nova, em aprendizado). Cada paciente fica com um responsável só. Renata recebe cerca de 10% dos pacientes sem responsável; o restante é dividido igualmente entre as outras três.
- Feriado de 12/10: as sessões "Feriado 12/10" ficam guardadas no banco e fora do painel. Não trabalhar nelas (nem preencher responsável) até a gestora pedir.
- A Renata deve receber faltas visíveis no painel, nunca sessões do feriado.
- Nunca excluir nem sobrescrever o que já foi feito: só criar registros novos e preencher `responsavel` onde estiver vazio. Gravar sempre com `if_version`.

## Regras já decididas
- Reposição: mesmo profissional, no dia em que o paciente já vem, horário mais próximo; sem vaga, horários exclusivos de reagendamento, Jusci (manhãs, Psicologia) e Malu (tardes, Fono, menos terça); demais casos, turno extra.
- Turno extra só abre com pelo menos metade dos horários preenchidos (4 de 8), em blocos contínuos. Custo: R$ 40,00 por hora, R$ 28,00 para Psicopedagogia.
- Não usar horários de outros profissionais da mesma especialidade (decisão de 12/10).
- Márcia Carla (TO) só atende a partir de 20/10.
- Não desfazer trabalho já feito pela equipe de reagendamento.
