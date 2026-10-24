# Atendimentos médicos: cálculos salvos (24/10/2026)

Base para atualizar a aba "Médicos" da planilha de custos (Custo_Terapias_Instituto_Affectus_10.xlsx), que ainda está com as premissas antigas (consulta de 30 min, 16 consultas por dia, 1 dia por mês por médico).

## Premissas definidas pela gestora
- Horário dos médicos: 8h às 12h e 13h às 17h (8 h por dia). Pagamento por hora disponível.
- Consulta de 45 min (pode chegar a 1 h, conforme o paciente). Cabem 5 por turno e 10 por dia (225 de 240 min no turno).
- Fluxo: 1 consulta para cada paciente, nos 6 primeiros meses, e 1 reavaliação (retorno) até 6 meses depois.
- Margem de 10% sobre as consultas de cada fase, para pacientes que precisarem de reavaliação a mais.
- Horas de atendimento = consultas × 0,75 h. Dias de médico = consultas ÷ 10.
- Valor da hora: neuropediatra e psiquiatra infantil R$ 750,00; pediatra R$ 500,00.
- Base: 300 crianças.

## Cenário A: os 3 médicos atendem as 300 crianças (900 consultas por fase)
| | Sem 10% | Com 10% |
|---|---|---|
| Consultas no ciclo de 12 meses | 1.800 | 1.980 |
| Consultas por mês | 150 | 165 |
| Horas de atendimento por mês | 112,5 h | 123,75 h |
| Horas no ciclo | 1.350 h | 1.485 h |
| Por médico, por mês | 50 consultas, 37,5 h, 5 dias | 55 consultas, 41,25 h, 5,5 dias (6 fechados) |

## Neuropediatra: 100% das crianças (300)
| | Sem 10% | Com 10% |
|---|---|---|
| Primeiras consultas + reavaliações | 300 + 300 = 600 | 330 + 330 = 660 |
| Consultas por mês | 50 | 55 |
| Horas de atendimento por mês | 37,5 h | 41,25 h |
| Horas no ciclo | 450 h | 495 h |
| Dias por mês | 5 | 5,5 (6 fechados) |
| Horas disponíveis por mês | 40 h | 44 h (48 h com 6 dias) |
| Custo por mês (R$ 750,00 por hora) | R$ 30.000,00 | R$ 33.000,00 (R$ 36.000,00 com 6 dias) |

## Psiquiatra infantil: 80% das crianças (240), mesmo fluxo do neuropediatra
| | Sem 10% | Com 10% |
|---|---|---|
| Primeiras consultas + retornos | 240 + 240 = 480 | 264 + 264 = 528 |
| Consultas por mês | 40 | 44 |
| Horas de atendimento por mês | 30 h | 33 h |
| Horas no ciclo | 360 h | 396 h |
| Dias por mês | 4 | 4,4 (5 fechados) |
| Horas disponíveis por mês | 32 h | 35,2 h (40 h com 5 dias) |
| Custo por mês (R$ 750,00 por hora) | R$ 24.000,00 | R$ 26.400,00 (R$ 30.000,00 com 5 dias) |

## Se tudo (1ª consulta e reavaliação) tivesse de caber em 6 meses
A carga dobra: neuropediatra 100 consultas por mês (75 h; 110 e 82,5 h com a margem); psiquiatra infantil 80 consultas por mês (60 h; 88 e 66 h com a margem).

## Pendências
- Pediatra: fluxo e percentual de crianças ainda não definidos.
- Atualizar a aba "Médicos" e o "Resumo Geral" da planilha com estes números.
