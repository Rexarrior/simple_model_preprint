# Geng, Neubig (2026) — Effective Strategies for Asynchronous Software Engineering Agents

## Проверенная версия

- Jiayi Geng, Graham Neubig.
- arXiv:2603.21489v2, revised 2026-07-08; 22 PDF pages.
- На дату поиска работа указана как accepted paper COLM 2026; опубликованных
  proceedings ещё нет, поэтому в BibTeX сохранён статус препринта и версия.
- Локальный файл: `../literature/geng2026_caid.pdf`.

## Почему включён

Это ближайшая найденная программная постановка с фактической конкурентностью:
центральный manager строит dependency-aware plan, несколько engineer-agents
работают асинхронно в изолированных git worktrees, после чего ветки интегрируются
и тестируются. Работа позволяет отделить nominal agent count, реально
перекрывающиеся интервалы, DAG/delegation topology и integration overhead.

## Дизайн и количественные claims

- **Population:** задачи PaperBench и Commit0-Lite; в основных опытах три
  семейства моделей (Claude, MiniMax, GLM).
- **Intervention:** CAID с manager и несколькими engineer-agents; 2 инженера для
  PaperBench и 4 для Commit0-Lite в основном сравнении.
- **Comparator:** single-agent baseline той же модельной семьи и benchmark;
  отдельно ablation по 2/4/8 инженерам и стратегиям верификации.
- **Outcomes:** benchmark score/pass rate, wall-clock runtime в секундах и cost.
- **Estimator/aggregation:** средние значения по benchmark runs в таблицах
  статьи; отдельные trajectory plots не являются оценкой среднего эффекта.
- **Inclusion:** PaperBench и Commit0-Lite instances в заявленной конфигурации;
  fixed iteration budgets. Человек-оператор во время выполнения отсутствует.
- **Результат:** в Table 2 CAID повышает score для всех шести пар
  model--benchmark, но во всех шести парах увеличивает runtime и cost. Например,
  для Claude на PaperBench score меняется с 57.2 до 63.3, runtime — с 1803.5 до
  2080.4 s, cost — с 3.3 до 6.5; на Commit0-Lite — 53.1 до 59.1, 692.6 до
  1583.2 s и 1.9 до 8.1. Это улучшение качества, не makespan speedup.
- **Scaling:** 2/4/8-agent ablation немонотонна: Commit0-Lite достигает лучшего
  качества при 4 инженерах и ухудшается при 8; на PaperBench рост сверх 2 даёт
  мало score, тогда как runtime/cost продолжают расти.
- **Ограничения переноса:** нет человеческих фаз, no-AI counterfactual,
  task/mode-specific `k`, human-active time и принятия человеком; fixed budgets
  и две benchmark families не калибруют M4 для реального проекта.

## Отображение на M4

Поддерживает необходимость явных DAG, фактической конкурентности, изоляции,
merge/test integration и topology-dependent overhead. Не поддерживает тезис,
что больше агентов сокращают календарный срок. Manager является программным
агентом, а не общим человеческим ресурсом мощности 1; CAID не моделирует
локальное удержание потока в очереди к человеку.

## Постраничная карта PDF

- p. 1 — abstract, определения CAID и три SWE primitives; заявленные score gains.
- p. 2 — мотивация, Table 1 с типами workspace coordination, contributions.
- p. 3 — dependency-aware planning, manager/engineer roles, isolated worktrees.
- p. 4 — branch-and-merge, executable verification, benchmarks и setup.
- p. 5 — Table 2: score, runtime и cost для single-agent и CAID.
- p. 6 — workspace/verification ablations; начало анализа parallelism.
- p. 7 — Figure 3 (2/4/8 agents) и Figure 4 с реальными Gantt-like timelines.
- p. 8 — delegation/review ablations и quality--runtime trade-off; related work.
- p. 9 — related work, limitations: wall-clock substantially not reduced,
  coordination bottleneck и fixed budgets.
- p. 10 — дополнительные ограничения, conclusion и начало references.
- p. 11 — references.
- p. 12 — references.
- p. 13 — references и переход к appendix.
- p. 14 — manager system prompt.
- p. 15 — continuation of manager prompt and delegation protocol.
- p. 16 — engineer prompt and worktree constraints.
- p. 17 — review/integration prompt.
- p. 18 — additional prompt/configuration details.
- p. 19 — detailed Commit0-Lite result tables.
- p. 20 — additional Commit0-Lite/model-level results.
- p. 21 — detailed PaperBench results.
- p. 22 — remaining detailed results and appendix notes.

## Допустимый claim

CAID показывает, что repository-level агентные ветви могут выполняться
конкурентно, но полезное масштабирование зависит от декомпозиции и координации;
в опубликованных сравнениях улучшение benchmark score сопровождалось большим
runtime и cost. Это нельзя представлять как доказательство ускорения.
