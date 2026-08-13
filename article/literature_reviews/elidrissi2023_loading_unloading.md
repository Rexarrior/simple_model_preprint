# Elidrissi et al. (2023) — Parallel Machines with a Loading/Unloading Server

## Проверенная версия

- Abdelhak Elidrissi, Rachid Benmansour, Keramat Hasani, Frank Werner.
- *Scheduling on parallel machines with a common server in charge of loading
  and unloading operations*, arXiv:2306.16669v1, submitted 2023-06-29;
  40 PDF pages. Peer-reviewed venue на дату поиска не найден.
- Локальный файл: `../literature/elidrissi2023_loading_unloading.pdf`.

## Почему включён

В отличие от setup-only common-server models, каждая работа обращается к одному
серверу и до, и после параллельной машинной фазы. Это ближайший формальный аналог
цепочки `human specification--agent work--human review`; no-delay unloading
также создаёт форму локального удержания машины. Однако повторный rework-цикл,
DAG и software-specific inputs отсутствуют.

## Постановка и результаты

- **Jobs/resources:** jobs на двух identical parallel machines; один server
  выполняет loading и unloading каждого job.
- **Constraints:** no delay между loading и processing и между processing и
  unloading; server capacity 1, каждая machine обрабатывает не более одного job.
- **Outcome:** deterministic makespan `C_max`; notation
  `P2,S1|s_j,t_j|C_max`.
- **Methods:** две MILP formulations, valid inequalities, lower bound,
  polynomial special cases и GVNS; computational instances оценивают solution
  quality/runtime алгоритмов, не человеческую производительность.
- **Главное структурное следствие:** из-за немедленной выгрузки завершившая
  processing работа удерживает machine до доступности server. Это частичный
  аналог slot hold в M4.
- **Ограничения переноса:** две машины, независимые jobs, по одной loading и
  unloading фазе, известные durations, нет return-to-machine rework, human
  switching, `k`, раздельной эмпирической калибровки `a/h` или software tasks.

## Постраничная карта PDF

- p. 1 — abstract, notation, no-delay loading/processing/unloading and makespan.
- p. 2 — introduction and setup-only common-server context.
- p. 3 — related loading/unloading and server scheduling literature.
- p. 4 — literature classification and problem gap.
- p. 5 — contributions, formal problem statement and notation.
- p. 6 — sequencing notation and dummy jobs.
- p. 7 — completion-time MILP variables and objective.
- p. 8 — machine and server non-overlap constraints.
- p. 9 — no-delay loading/processing/unloading constraints.
- p. 10 — time-indexed formulation.
- p. 11 — total idle-time equivalence.
- p. 12 — lower-bound construction.
- p. 13 — lower-bound proof/properties.
- p. 14 — polynomial special cases and structural properties.
- p. 15 — GVNS overview and initial solution.
- p. 16 — neighborhoods and local search.
- p. 17 — perturbation/stopping mechanisms.
- p. 18 — algorithmic details/pseudocode.
- p. 19 — computational design and instance generation.
- p. 20 — calibration of algorithm parameters.
- p. 21 — MILP comparison results.
- p. 22 — computational results continuation.
- p. 23 — lower-bound and optimality-gap results.
- p. 24 — GVNS performance tables.
- p. 25 — GVNS comparison continuation.
- p. 26 — sensitivity/instance-size results.
- p. 27 — runtime and gap results.
- p. 28 — additional computational table.
- p. 29 — additional computational table.
- p. 30 — results discussion.
- p. 31 — conclusions and limitations/future work.
- p. 32 — references.
- p. 33 — references.
- p. 34 — references.
- p. 35 — references.
- p. 36 — appendix computational tables.
- p. 37 — appendix computational tables.
- p. 38 — appendix computational tables.
- p. 39 — appendix computational tables.
- p. 40 — final appendix table.

## Допустимый claim

Повторное обращение к capacity-1 server до и после машинной обработки и
удержание машины при no-delay unloading уже являются известными scheduling
механизмами. M4 отличается не этими механизмами сами по себе, а их объединением
с DAG, task/mode-specific `k`, несколькими human--agent cycles, integration
overhead и software acceptance semantics.
