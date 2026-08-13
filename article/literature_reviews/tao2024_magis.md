# Tao et al. (2024) — MAGIS: LLM-Based Multi-Agent Framework for GitHub Issue Resolution

## Проверенная версия

- Wei Tao, Yucheng Zhou, Yanlin Wang, Wenqiang Zhang, Hongyu Zhang, Yu Cheng.
- NeurIPS 2024, volume 37; DOI `10.52202/079017-1647`; 31 PDF pages.
- Локальный файл: `../literature/tao2024_magis.pdf`.

## Почему включён

MAGIS — первичная repository-level coding-agent работа с ролями Manager,
Repository Custodian, Developer и QA. Она показывает цикл планирование--код--QA
--доработка, но оценивает прежде всего resolved ratio. Поэтому источник полезен
для архитектурного аналога повторных фаз и одновременно задаёт границу: agent
count/roles и success нельзя считать фактической конкурентностью или speedup.

## Дизайн и количественные claims

- **Population:** GitHub issues из SWE-bench, охватывающие 12 Python repositories.
- **Intervention:** MAGIS с четырьмя типами агентов и repository-aware memory.
- **Comparators:** прямое применение GPT-3.5, GPT-4 и Claude-2; отдельные
  ablations QA и hints.
- **Primary outcome:** доля issues, для которых generated patch проходит
  benchmark tests; дополнительно code-change statistics и descriptive runtime.
- **Estimator/aggregation:** resolved count / включённые SWE-bench issues;
  runtime на p. 19 описателен и не получен из рандомизированного одинакового
  time-budget comparison с Devin.
- **Результат:** MAGIS resolves 13.94% и даёт примерно восьмикратную долю против
  direct GPT-4 в эксперименте авторов. QA ablation меняет resolved ratio, а
  case study показывает до трёх developer attempts после QA comments.
- **Inclusion:** заявленный SWE-bench subset и execution environment статьи;
  человек не обслуживает запросы агентов в ходе runs.
- **Ограничения переноса:** Python/12 repositories, prompt/model dependence,
  primary outcome — quality/success; нет human-active time, no-AI baseline,
  фиксированного `P` реальных одновременных ветвей или календарного срока
  принятого человеком результата.

## Отображение на M4

Роли QA и Developer дают software-specific аналог `execution--audit--rework`,
но обе роли автоматизированы. Работа не устанавливает общий человеческий ресурс,
очередь, локальную блокировку или makespan effect; четыре роли не равны четырём
параллельным слотам.

## Постраничная карта PDF

- p. 1 — abstract, четыре роли и 13.94% resolved ratio.
- p. 2 — repository-level issue-resolution motivation and contributions.
- p. 3 — empirical analysis of direct-LLM failure factors.
- p. 4 — task complexity/context analysis and framework motivation.
- p. 5 — MAGIS workflow and Manager/Custodian/Developer/QA roles.
- p. 6 — repository memory, planning and developer procedure.
- p. 7 — QA review and iterative revision algorithms.
- p. 8 — experimental setup, SWE-bench, models and metrics.
- p. 9 — main resolved-ratio results and comparison table.
- p. 10 — QA/hint ablations and interpretation.
- p. 11 — threats/related discussion and start of references.
- p. 12 — references.
- p. 13 — references.
- p. 14 — references.
- p. 15 — references and appendix transition.
- p. 16 — appendix metrics and issue characteristics.
- p. 17 — additional figures/tables for issue and code statistics.
- p. 18 — supplementary result breakdowns.
- p. 19 — descriptive processing times and code-change statistics; not a
  controlled speedup estimator.
- p. 20 — qualitative interface/output example.
- p. 21 — additional execution screenshots/examples.
- p. 22 — case study: one developer accepted immediately, another revised after
  two QA rounds and accepted on the third attempt.
- p. 23 — enlarged workflow/interaction figure.
- p. 24 — supplementary screenshot/example.
- p. 25 — detailed related work and limitations (Python repositories, prompts).
- p. 26 — NeurIPS paper checklist.
- p. 27 — NeurIPS paper checklist continuation.
- p. 28 — NeurIPS paper checklist continuation.
- p. 29 — NeurIPS paper checklist continuation.
- p. 30 — NeurIPS paper checklist continuation.
- p. 31 — final checklist/appendix material.

## Допустимый claim

MAGIS демонстрирует автоматизированные роли планирования, разработки, QA и
повторной доработки на SWE-bench. Его рост resolved ratio является результатом
по качеству/успешности и не доказывает сокращение makespan или человеческого
времени.
