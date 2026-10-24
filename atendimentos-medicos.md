# Atendimentos médicos: cálculos salvos (24/10/2026)

Base para atualizar a aba "Médicos" da planilha de custos (Custo_Terapias_Instituto_Affectus_10.xlsx), que ainda está com as premissas antigas (consulta de 30 min, 16 consultas por dia, 1 dia por mês por médico).

## Premissas definidas pela gestora
- Horário dos médicos: 8h às 12h e 13h às 17h (8 h por dia). Pagamento por hora disponível.
- Consulta de 45 min (pode chegar a 1 h, conforme o paciente). Cabem 5 por turno e 10 por dia (225 de 240 min no turno).
- Fluxo: 1 consulta para cada paciente, nos 6 primeiros meses, e 1 reavaliação (retorno) até 6 meses depois.
- Margem de 10% sobre as consultas de cada fase, para pacientes que precisarem de reavaliação a mais.
- Horas de atendimento = consultas × 0,75 h.
- Quantidade de dias de cada médico na clínica: EM ABERTO, a negociar com os médicos. Não calcular dias, horas disponíveis nem custo até a definição (referência: 10 consultas por dia).
- Valor da hora (já informado): neuropediatra e psiquiatra infantil R$ 750,00; pediatra R$ 500,00.
- Base: 300 crianças.

## Cenário A (anterior): os 3 médicos atendem as 300 crianças (900 consultas por fase)
| | Sem 10% | Com 10% |
|---|---|---|
| Consultas no ciclo de 12 meses | 1.800 | 1.980 |
| Consultas por mês | 150 | 165 |
| Horas de atendimento por mês | 112,5 h | 123,75 h |
| Horas no ciclo | 1.350 h | 1.485 h |
| Por médico, por mês | 50 consultas, 37,5 h | 55 consultas, 41,25 h |

## Neuropediatra: 100% das crianças (300)
| | Sem 10% | Com 10% |
|---|---|---|
| Primeiras consultas + reavaliações | 300 + 300 = 600 | 330 + 330 = 660 |
| Consultas por mês | 50 | 55 |
| Horas de atendimento por mês | 37,5 h | 41,25 h |
| Horas no ciclo | 450 h | 495 h |

## Psiquiatra infantil: 80% das crianças (240), mesmo fluxo do neuropediatra
| | Sem 10% | Com 10% |
|---|---|---|
| Primeiras consultas + retornos | 240 + 240 = 480 | 264 + 264 = 528 |
| Consultas por mês | 40 | 44 |
| Horas de atendimento por mês | 30 h | 33 h |
| Horas no ciclo | 360 h | 396 h |

## Pediatra: 100% das crianças (300), mesmo fluxo do neuropediatra
| | Sem 10% | Com 10% |
|---|---|---|
| Primeiras consultas + retornos | 300 + 300 = 600 | 330 + 330 = 660 |
| Consultas por mês | 50 | 55 |
| Horas de atendimento por mês | 37,5 h | 41,25 h |
| Horas no ciclo | 450 h | 495 h |

Consulta de 45 min. Valor da hora já informado: R$ 500,00 (custo só depois de definidos os dias).

## Resumo atual dos 3 médicos (neuropediatra 300, psiquiatra infantil 240, pediatra 300)
| | Sem 10% | Com 10% |
|---|---|---|
| Consultas no ciclo de 12 meses | 1.680 | 1.848 |
| Consultas por mês | 140 | 154 |
| Horas de atendimento por mês | 105 h | 115,5 h |
| Horas no ciclo | 1.260 h | 1.386 h |

## Se tudo (1ª consulta e reavaliação) tivesse de caber em 6 meses
A carga dobra: neuropediatra e pediatra 100 consultas por mês cada (75 h; 110 e 82,5 h com a margem); psiquiatra infantil 80 consultas por mês (60 h; 88 e 66 h com a margem).

## Pendências
- Dias na clínica de cada médico (e, a partir deles, horas disponíveis e custo): a negociar.
- Atualizar a aba "Médicos" e o "Resumo Geral" da planilha com estes números.

## Pagamento por consulta (definido em 24/10/2026)
- Neuropediatra e psiquiatra infantil: R$ 750,00 por consulta (consultas e retornos).
- Pediatra: R$ 500,00 por consulta + retorno (lido como valor por paciente; confirmar com a gestora).
- Custo por ano, com 10%: neuropediatra 660 × R$ 750,00 = R$ 495.000,00; psiquiatra infantil 528 × R$ 750,00 = R$ 396.000,00; pediatra 330 × R$ 500,00 = R$ 165.000,00; total R$ 1.056.000,00 (R$ 88.000,00 por mês).
- Sem 10%: R$ 450.000,00 + R$ 360.000,00 + R$ 150.000,00 = R$ 960.000,00 (R$ 80.000,00 por mês).
- Se o pediatra cobrar R$ 500,00 por consulta e por retorno: 660 × R$ 500,00 = R$ 330.000,00 e total com 10% de R$ 1.221.000,00.
- Planilha: Custo_Terapias_Instituto_Affectus_13.xlsx (aba Médicos, chave B32 para o pediatra).
