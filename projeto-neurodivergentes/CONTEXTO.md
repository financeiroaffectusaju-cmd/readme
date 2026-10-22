# Instituto Affectus: contexto do projeto (atualizado em 22/10/2026)

Projeto de atendimento a crianças neurodivergentes. Estrutura **separada** da clínica atual: as regras e os profissionais da agenda de reagendamento (CLAUDE.md na raiz) não se aplicam aqui.

## Status
- A apresentação de volume de atendimentos foi enviada ao chefe em 22/10/2026. **Aguardando o parecer dele.**
- Próxima etapa, depois da validação: **orçamentos** (turnos por profissional, custo por especialidade, remuneração por turno).
- Projeto ainda em elaboração; o ano de referência é julho/2026 a junho/2027 (parâmetro de cálculo).

## Como trabalhar com a gestora
- Em caso de dúvida, **perguntar** antes de seguir; não presumir.
- Registrar fielmente o que ela decide; sugestões ficam separadas das decisões.
- Não desfazer o que já foi decidido.

## Onde está tudo
- Artefato **Instituto Affectus** (consolida tudo): https://claude.ai/artifact/F99g5HYE8i2J4cHdk5BE76 (privado; fonte em `instituto-affectus.html`).
- Apresentação para o chefe (9 slides): https://claude.ai/artifact/8cY11Hpabpw9N24Pc1svV9 (privada; fonte em `ferramentas/apresentacao/project/`).
- Planilha completa: `agenda-atendimentos.xlsx` (páginas HTML equivalentes em `agenda-atendimentos.html`).
- Resumo do volume (dia, semana, mês, ano): `resumo-volume-atendimentos.xlsx`.
- Scripts que geram a grade, as planilhas e as páginas: `ferramentas/` (precisam de `ortools` e `openpyxl`; os caminhos de saída estão escritos no topo de cada script).

## Decisões da gestora

### Funcionamento e plano adotado
- Segunda a sexta, 7h às 19h, almoço 12h às 13h. 246 dias de atendimento em jul/2026 a jun/2027 (feriados nacionais, Carnaval, Corpus Christi, 8/7, 8/12, 17/3 e 24/6 descontados; o São João está em aberto e há uma chave na aba Calendário).
- **Plano adotado (22/10/2026): Opção 2.** 300 crianças, 16 sessões de terapia de 30 min por mês, em 1 visita de 2 h por semana, sempre no mesmo dia, horário e sala (8 h de terapia por mês). Cenário de 100% de ocupação (sem vaga reservada para reposição).
- Cada criança faz 3 ou 4 especialidades, sempre com pelo menos 2 entre Psicologia, Terapia Ocupacional e Fonoaudiologia. Horários seguidos. Crianças fora desse formato serão tratadas caso a caso.
- Reposição: livre, sem horário fixo reservado. A vaga de quem falta no dia pode repor outra criança do mesmo pacote.
- Remuneração dos profissionais **por turno** (manhã 7h às 12h, tarde 13h às 19h).

### Salas e profissionais
- Fonoaudiologia, Terapia Ocupacional, Psicopedagogia, Psicomotricidade: 1 sala cada, 2 profissionais por sala, cada um com 1 criança.
- Psicologia: 1 sala dividida, 2 profissionais, cada um com seu paciente.
- Musicoterapia: 1 sala, 1 profissional, individual.
- Terapia alimentar: 1 sala, 1 nutricionista, 2 pacientes por vez.
- Médicos (neuropediatra, psiquiatra infantil, pediatra): 1 dia por mês cada (disponibilidade deles), consultas de 30 min, 8h às 12h e 13h às 17h.
- Odontologia: 2 dentistas, 1 por dia em todos os dias de atendimento (podem ser profissionais diferentes por dia), consultas de 40 min, primeira consulta e retorno em 4 a 5 meses.
- Xadrez: 1 sala, profissional próprio, 1 por turno. Capoeira: 1 sala, 1 profissional por turno.
- Psicóloga dos pais: 1 sala, 1 psicóloga exclusiva, sessões de 30 min, 1 sessão a cada 2 visitas, alternando individual e grupo (grupos de 8).
- Oficinas profissionalizantes: 1 sala para todas, **turmas fixas**; mães: confeitaria e panificação, artesanato e personalizados, estética básica; pais: elétrica e instalações básicas, informática e manutenção de celulares, barbearia. Funcionamento a definir.
- Xadrez e capoeira são extras (aulas de 1 h, antes ou depois da visita, alternando a cada visita).

## Números (300 crianças, 246 dias)
| | Dia | Semana | Mês | Ano |
|---|---|---|---|---|
| Sessões de terapia de 30 min | 240 | 1.200 | 4.920 | 59.040 |
| Visitas de 2 h | 60 | 300 | 1.230 | 14.760 |
| Consultas médicas | 16 por dia médico | 11,7 | 48 | 576 |
| Consultas odontológicas | 3,7 | 18,3 | 75 | 900 |
| Xadrez / capoeira / oficinas (crianças ou pais) | 30 cada | 150 | 615 | 7.380 |
| Psicóloga dos pais (individual / em grupo) | 15 / 15 | 75 / 75 | 308 / 308 | 3.690 / 3.690 |
| **Total de atendimentos e participações** | **366** | **1.830** | **7.503** | **90.036** |

- Sessões por especialidade por dia (pacotes-modelo): Psicologia 42, TO 39, Fono 39, Psicomotricidade 39, Psicopedagogia 33, Terapia alimentar 30, Musicoterapia 18.
- Grade: 60 blocos de visita por dia, provados por solver; mais de 62 não foram provados nem descartados. A grade nominal está na aba Semanal 16 sessões (C001 a C300).
- Turnos por ano: 7.944 (terapias, psicóloga dos pais, dentista, capoeira, xadrez e médicos), na aba Equipe e turnos.
- Crianças de segunda e sexta fazem 48 visitas por ano; as de terça a quinta, 50 (feriados).

## Plano médico
Rodízio dos dias da semana: o dia de cada médico muda a cada mês; cada dia médico atende só crianças que já vêm naquele dia, com a consulta antes ou depois da visita. Todas as 300 crianças têm pelo menos 1 consulta no 1º ano; o ciclo com os 3 médicos fecha em cerca de 20 meses (15 com consultas de 20 min; 10 com 15 min). Detalhes nas abas Médicos e Agenda médica.

## Opções avaliadas e descartadas
- Opção 1: 24 sessões por mês, 3 visitas a cada 2 semanas (2 h): 200 crianças (180 com 10% de reposição).
- Referência: 24 sessões por mês, 1 visita semanal de 3 h: 190 crianças (170 com reposição). Sem grade nominal.
- Os tetos teóricos calculados antes da grade (225 e 202 crianças) não foram obtidos na grade real.

## Em aberto
- Parecer do chefe sobre os números.
- São João (24/06/2027), 8/12 (conferir decreto) e funcionamento das oficinas.
- Origem dos pacientes; perfil da demanda por especialidade (vem da triagem; os pacotes da grade são ilustrativos).
- Remuneração por turno e orçamentos (só depois da validação).
