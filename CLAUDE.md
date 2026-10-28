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

## Comparativo de guias x atendimentos + evoluções (por paciente)
Quando a gestora pedir "o mesmo processo" para um paciente, ou mandar guias Hapvida escaneadas, seguir o roteiro em `.claude/skills/comparativo-guias/SKILL.md` (scripts na mesma pasta). Resultado: um PDF por paciente com as datas assinadas nas guias conferidas com as sessões do sistema (inconsistências) e as evoluções por profissional. Só leitura no sistema; senha nunca vai para arquivo nem repositório; dados de pacientes não são versionados.

## Regras já decididas
- Reposição: mesmo profissional, no dia em que o paciente já vem, horário mais próximo; sem vaga, horários exclusivos de reagendamento, Jusci (manhãs, Psicologia) e Malu (tardes, Fono, menos terça); demais casos, turno extra.
- Turno extra só abre com pelo menos metade dos horários preenchidos (4 de 8), em blocos contínuos. Custo: R$ 40,00 por hora, R$ 28,00 para Psicopedagogia.
- Não usar horários de outros profissionais da mesma especialidade (decisão de 12/10).
- Márcia Carla (TO) só atende a partir de 20/10.
- Não desfazer trabalho já feito pela equipe de reagendamento.
