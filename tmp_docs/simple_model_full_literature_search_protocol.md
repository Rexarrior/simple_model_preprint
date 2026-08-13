# Поисковый протокол: ближайшие постановки для `simple_model_full`

Дата поиска: 2026-08-09. Поиск продолжает, а не заменяет корпус из 25 работ,
зафиксированный в `simple_model_full_evidence_matrix.md` на 2026-08-04.

## Вопросы и область поиска

Поиск был ограничен четырьмя вопросами:

1. какие scheduling-постановки ближе всего к чередованию исполнительных и
   повторных фаз единственного сервера;
2. какие эксперименты по supervisory control обосновывают конечную пропускную
   способность одного оператора с учётом очереди и переключения;
3. какие coding-agent системы действительно исполняют несколько ветвей
   конкурентно и что именно они измеряют;
4. существует ли работа, совместно калибрующая на программных задачах все входы
   M4 и календарный срок принятого результата.

## Источники поиска

- локальный корпус из 34 PDF и индивидуальные обзоры в
  `simple_model_full/literature_reviews/`;
- arXiv и страницы версий arXiv;
- официальные страницы и proceedings издателей/конференций: IEEE, INFORMS,
  Elsevier, Springer, NeurIPS и COLM;
- Crossref/DOI metadata;
- институциональные репозитории авторских рукописей (City Research Online и
  CiteSeerX) при недоступности издательского PDF.

Веб-поиск использовался для навигации к первичным и официальным версиям, но
результаты поиска, блоги и обзоры не использовались как доказательства claims.
Scopus и Web of Science в этой итерации не использовались; поэтому отрицательный
результат ограничен просмотренным корпусом и перечисленными каналами.

## Запросы

Запросы выполнялись на английском языке, с проверкой цитирующих и связанных
работ на страницах найденных первичных публикаций:

- `"parallel machine scheduling" "single server" loading unloading`;
- `scheduling common server repeated service operations machine blocking`;
- `reentrant parallel machines common server scheduling`;
- `"Scheduling reentrant jobs on parallel machines with a remote server"`;
- `multi-mode resource-constrained project scheduling original paper DOI`;
- `disjunctive graph scheduling shared resource critical path`;
- `"Predicting Controller Capacity" supervisory control multiple UAVs`;
- `human supervisory control multiple robots operator capacity queueing`;
- `interaction time neglect tolerance attention allocation switching cost`;
- `2025 2026 parallel coding agents repository multi-agent software engineering`;
- `"parallel" "coding agents" repository-level wall-clock`;
- `"Effective Strategies for Asynchronous Software Engineering Agents"`;
- `MAGIS multi-agent GitHub issue resolution`;
- `coding agent orchestrator auditor verifier rework benchmark runtime`.

## Критерии включения

Источник включался, только если он удовлетворял всем обязательным условиям:

- первичная публикация или официальная версия рукописи;
- меняет позиционирование статьи, закрывает один из четырёх вопросов или
  поддерживает конкретное проверяемое утверждение;
- для количественного результата доступны population, intervention,
  comparator, outcome, estimator/aggregation, правило включения и ограничения
  переноса;
- метрика названа точно: elapsed/runtime, active time, throughput, quality,
  success, comprehension и compute cost не смешиваются;
- версия и библиографические данные проверены по первичному каналу.

Архитектурная работа, измеряющая только качество, могла быть включена лишь для
описания ролей, циклов аудита или фактической конкурентности; она не
интерпретировалась как свидетельство ускорения.

## Критерии `optional` и исключения

`Optional` означает, что источник релевантен, но не добавляет различия поверх
уже включённой более близкой или более полной работы, либо его полный текст не
удалось проверить. Исключались вторичные обзоры для ключевых claims, gray
literature об инструментах, работы с другим значением «parallel coding», а также
источники без новой опоры для модели.

## Процедура проверки

Для каждого включённого PDF проверены титульные данные, версия, дизайн,
определения метрик, таблицы/рисунки с результатами, ограничения и выводы.
Постраничные карты находятся в `simple_model_full/literature_reviews/`.
Библиографические записи сверены с DOI/arXiv/proceedings metadata. Поиск завершён
2026-08-09; допустимая формулировка отрицательного результата — только «в
пределах просмотренного корпуса не найдена работа, одновременно объединяющая
перечисленные компоненты».
