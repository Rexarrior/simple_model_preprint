# Screening log: продолжение поиска для `simple_model_full`

Дата решения: 2026-08-09. `Include` означает включение в Related Work,
evidence matrix, BibTeX и постраничный обзор. `Optional` сохраняет источник как
кандидата, но не расширяет основной корпус.

| Кандидат | Решение | Основание |
|---|---|---|
| Elidrissi et al. (2023), *Scheduling on parallel machines with a common server in charge of loading and unloading operations*, arXiv:2306.16669v1 | include | Формальная цепочка server--machine--server и no-delay unloading ближе setup-only моделей; позволяет точно отделить повторный сервис и удержание машины от software-specific M4. |
| Chakhlevitch & Glass (2009), *Scheduling reentrant jobs on parallel machines with a remote server* | include | Ближайшая найденная reentrant-цепочка primary machine--remote server--same primary machine; важно, что машина во время удалённого сервиса освобождается. |
| Cummings & Mitchell (2008), *Predicting Controller Capacity in Supervisory Control of Multiple UAVs* | include | Экспериментально добавляет queueing, situation-awareness wait и cognitive reorientation к fan-out; прямо ограничивает перенос результата контекстом UAV. |
| Geng & Neubig (2026), *Effective Strategies for Asynchronous Software Engineering Agents*, arXiv:2603.21489v2, accepted COLM 2026 | include | Реальная конкурентность в worktrees, dependency graph, merge/review и 2/4/8-agent ablation; wall-clock и cost растут, поэтому качество нельзя назвать ускорением. |
| Tao et al. (2024), *MAGIS*, NeurIPS 2024 | include | Первичная repository-level система с Manager/Custodian/Developer/QA и циклами audit--rework; outcome в основном resolved ratio, не makespan. |
| Jiang et al. (2015), *Single-server parallel-machine scheduling with loading and unloading times* | optional | Исторически важная loading/unloading модель, но проверен только abstract; включённая работа Elidrissi et al. даёт полный текст и более широкий сопоставительный контекст. |
| Talbot (1982), *Resource-Constrained Project Scheduling with Time-Resource Tradeoffs* | optional | Первичная ранняя multi-mode RCPSP; полный текст недоступен в этой итерации, а необходимые свойства modes уже проверены в имеющемся корпусе Brucker et al. |
| Balas (1969), *Machine Sequencing via Disjunctive Graphs* | optional | Исторический первоисточник disjunctive graph; полный текст недоступен, а стандартность механизма подтверждается локально проверенной книгой Pinedo. |
| Sander et al. (2026), multi-agent software framework | optional | Роли преимущественно выполняются последовательно; nominal agent count не задаёт конкурентность `P`. Уже отражено в старом screening. |
| OSDAG (2026) | optional | Полезен как DAG-dispatch example, но относится к робототехнике, не содержит человеческой очереди и не является формальным основанием M4. |
| MASAI | optional | Repository-level roles и тестирование релевантны архитектуре, но нет новой проверяемой оценки одновременного исполнения и human-active time поверх MAGIS/CAID. |
| HyperAgent | optional | Полезен для специализации ролей, но outcomes не идентифицируют makespan или эффект фактической конкурентности. |
| AgentForge (2026 preprint) | exclude | Более поздний непроверенный препринт не добавляет необходимого различия поверх CAID и MAGIS. |
| ParaCodex и работы о parallel code generation | exclude | «Параллельность» относится к генерируемой программе/ядру, а не к конкурентным coding-agent потокам. |
| Обзоры multi-agent orchestration 2025--2026 | exclude | Использованы только для навигации; ключевые claims проверены по первичным MAGIS, CAID и Kim et al. |
| OpenHands/другие блоги об orchestrators | exclude | Gray literature о быстро меняющихся инструментах; не используется для научных claims. |

Итог: пять новых источников включены, семь сохранены как optional и четыре
группы результатов исключены. Решение ограничивает расширение корпуса работами,
которые меняют ближайший аналог, метрику или границу переноса.
