# Chakhlevitch, Glass (2009) — Reentrant Jobs on Parallel Machines with a Remote Server

## Проверенная версия

- Konstantin Chakhlevitch, Celia A. Glass.
- Published: *Computers & Operations Research* 36(9), 2580--2589 (2009),
  DOI `10.1016/j.cor.2008.11.007`.
- Локальный PDF — открытая Statistical Research Paper No. 30 (2008), 39 pages,
  из City Research Online; нумерация ниже относится к этой author/report version.
- Локальный файл: `../literature/chakhlevitch2009_reentrant.pdf`.

## Почему включён

Это ближайшая найденная reentrant-постановка: job инициализируется и выполняет
первую фазу на одной из parallel primary machines, проходит среднюю фазу на
единственном remote server и возвращается на ту же primary machine для final
processing. Важно, что server **не удерживает** primary machine; следовательно,
модель близка чередованием, но не локальной блокировкой M4.

## Постановка и результаты

- **Jobs/resources:** independent jobs; alternative primary machines и один
  remote server.
- **Route:** initialization/setup and main processing on assigned primary
  machine, remote-server operation, then return to the same primary machine.
- **Capacity/blocking:** remote server capacity 1; primary machine can process
  another job while assigned job is at server.
- **Outcome:** deterministic makespan; paper studies complexity, lower bounds,
  heuristics and laboratory-motivated instance data.
- **Ограничения переноса:** одна reentry, predetermined route, independent jobs,
  no human queue semantics or task-DAG, no task/mode-specific `k`, integration
  overhead or software acceptance; laboratory process не coding evidence.

## Постраничная карта локального PDF

- p. 1 — City repository cover and citation to 2008 report version.
- p. 2 — report title, authors and institutional metadata.
- p. 3 — report/disclaimer front matter.
- p. 4 — abstract and three-stage reentrant problem summary.
- p. 5 — laboratory motivation and scheduling context.
- p. 6 — related models and contributions.
- p. 7 — process route and remote-server interpretation.
- p. 8 — formal feasible schedule, makespan and notation.
- p. 9 — computational complexity and relation to chain-reentrant shop.
- p. 10 — reentrant structure and primary-machine assignment.
- p. 11 — structural properties.
- p. 12 — lower-bound development.
- p. 13 — lower-bound/proposition continuation.
- p. 14 — heuristic construction.
- p. 15 — sequencing/assignment procedure.
- p. 16 — heuristic variants.
- p. 17 — algorithmic details.
- p. 18 — additional properties and algorithm transition.
- p. 19 — computational experiment and instance design.
- p. 20 — synthetic results.
- p. 21 — synthetic results continuation.
- p. 22 — comparative heuristic results.
- p. 23 — sensitivity/results table.
- p. 24 — synthetic results discussion.
- p. 25 — laboratory-derived data and throughput/makespan comparison.
- p. 26 — practical savings/results discussion and conclusions.
- p. 27 — references.
- p. 28 — appendix algorithm/pseudocode.
- p. 29 — appendix proof/details.
- p. 30 — appendix proof/details.
- p. 31 — appendix tables/algorithm continuation.
- p. 32 — appendix ending.
- p. 33 — City Statistical Research Papers series back matter.
- p. 34 — report-series catalogue.
- p. 35 — report-series catalogue.
- p. 36 — report-series catalogue.
- p. 37 — report-series catalogue.
- p. 38 — report-series catalogue.
- p. 39 — final report-series back matter.

## Допустимый claim

Чередование primary executor--single server--same executor уже имеет близкий
формальный аналог. В найденной модели серверная фаза освобождает primary machine;
поэтому local slot hold M4 не следует приписывать этой работе и нельзя считать
само reentry software-specific новизной.
