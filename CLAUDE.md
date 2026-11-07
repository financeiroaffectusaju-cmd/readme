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

## Regras já decididas
- Reposição: mesmo profissional, no dia em que o paciente já vem, horário mais próximo; sem vaga, horários exclusivos de reagendamento, Jusci (manhãs, Psicologia) e Malu (tardes, Fono, menos terça); demais casos, turno extra.
- Turno extra só abre com pelo menos metade dos horários preenchidos (4 de 8), em blocos contínuos. Custo: R$ 40,00 por hora, R$ 28,00 para Psicopedagogia.
- Não usar horários de outros profissionais da mesma especialidade (decisão de 12/10).
- Márcia Carla (TO) só atende a partir de 20/10.
- Não desfazer trabalho já feito pela equipe de reagendamento.

## Instituto Affectus: agenda e custo dos médicos (decisão de 07/11/2026)
Estrutura separada da clínica (planilha `Custo_Terapias_Instituto_Affectus_16_v20.xlsx`, aba Médicos). Negociado com os médicos de cada especialidade:
- 1 dia de atendimento por mês por especialidade, das 8h às 12h e das 13h às 17h (8 h por dia).
- Consulta de 45 min (neuropediatra e psiquiatra infantil) e de 30 min (pediatra).

Capacidade de atendimento (consultas):
- Neuropediatra: 10 por dia e por mês, 120 por ano.
- Psiquiatra infantil: 10 por dia e por mês, 120 por ano.
- Pediatra: 16 por dia e por mês, 192 por ano (96 pacientes, consulta + retorno).
- Total: 36 por mês e 432 por ano, cerca de 23% da demanda de 1.848 consultas por ano (300 crianças, consulta + retorno em 6 meses, margem de 10%; psiquiatra 80% das crianças).

Custo (só das consultas que cabem na agenda): neuropediatra R$ 90.000 (R$ 750 por consulta), psiquiatra R$ 90.000 (R$ 750 por consulta), pediatra R$ 48.000 (R$ 500 por paciente, consulta + retorno). Total R$ 228.000 por ano (R$ 19.000 por mês), antes R$ 1.056.000 pela demanda. Custo anual total do Instituto: R$ 6.023.500; primeiro ano com investimento: R$ 7.278.433.
Para atender toda a demanda seriam necessários cerca de 5,5 dias por mês por médico.
