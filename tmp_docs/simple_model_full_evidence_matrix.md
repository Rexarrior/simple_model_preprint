# Evidence matrix: `simple_model_full`

Дата синтеза: 2026-08-09.

## Статус

Матрица продолжена после постраничного анализа исходных 34 и пяти новых PDF. Канонические
подробности, версии и опорные страницы находятся в
`simple_model_full/literature_reviews/`. В основной корпус Related Work отобраны
30 работ; различия между elapsed time, active time, throughput, success,
quality и comprehension сохранены явно.

## Основной корпус

| Тема | Источник | Дизайн / outcome | Что поддерживает | Граница утверждения |
|---|---|---|---|---|
| AI productivity | Peng et al. (2023) | RCT; elapsed time среди completers | Контекстный `k<1` при `P=1` | Одна задача; complete-case; не multi-agent scaling |
| AI productivity | Becker et al. (2025) | Issue-level field RCT; active implementation time | Контекстный `k>1`; зависимость от задачи и пользователя | Не calendar makespan; смешанный набор early-2025 tools |
| AI productivity | Brynjolfsson et al. (2025) | Field rollout; issues/hour | Гетерогенность эффекта по опыту и типу работы | Throughput customer support нельзя переводить в software `k` |
| Human--AI interaction | Vaithilingam et al. (2022) | Within-subjects; time, success, usability | Состав `h`: understanding, validation, repair, debugging | Нет численного `h`; comparator -- IntelliSense; `P=1` |
| Human--AI interaction | Barke et al. (2023) | Qualitative/grounded theory; interaction modes | Режим `r` меняется между acceleration и exploration | Нет control и duration ratio |
| Agentic coding | Balepur et al. (2026) | Randomized agent vs constrained chatbot; time, accuracy, comprehension | Режим меняет одновременно completion и понимание | Нет no-AI arm, exact `k` и concurrent agents |
| Production telemetry | Liu et al. (2026) | 13.5M sessions; calls, tools, latency | Sequential chains, retries, shallow internal concurrency | Session не равна задаче; нет acceptance, quality и counterfactual |
| Measurement | METR (2026) | Gray literature; redesign of productivity study | Selection effects и concurrent-agent bias | Не peer-reviewed effect estimate |
| Effort estimation | Boehm, Abts, Chulani (2000) | Narrative survey | Таксономия внешних estimators для `\hat{k}` | Не scheduling и не LLM evidence |
| Effort estimation | Jørgensen (2007) | Review of expert/model comparisons | Нет универсально лучшего estimator; нужна local calibration | Не доказывает превосходство expert или model |
| Effort estimation | Jørgensen, Shepperd (2007) | Systematic evidence map; 304 journal papers | Ограничения historical validation и uncertainty reporting | 304 papers не равны независимым studies; не meta-analysis |
| Scalability | Amdahl (1967) | Fixed-workload scaling argument | Структурная аналогия потолка `1/\bar h_w` | Не human-attention model |
| Scalability | Gunther (2008) | Analytical preprint; USL | Рабочая форма `C(P)` с contention/coherency | Не эмпирическая валидация coding agents |
| Software coordination | Brooks (1995) | Book; human software teams | Интеграционные издержки и conceptual integrity | `P(P-1)/2` нельзя переносить на agent star буквально |
| Multi-agent systems | Kim et al. (2025; v3 2026) | 260 benchmark configurations; success/accuracy | Decomposability, sequentiality, topology-dependent overhead | Нет elapsed makespan и human supervisor; agent count confounded |
| Coding-agent orchestration | Tao et al. (2024), MAGIS | SWE-bench; resolved ratio, role/QA ablations | Manager--Developer--QA и автоматический audit--rework cycle | Role count не равен concurrency; success не является speedup; нет human time |
| Concurrent coding agents | Geng, Neubig (2026; v2), CAID | PaperBench/Commit0-Lite; score, runtime, cost; 2/4/8 agents | Actual concurrent worktrees, dependency plan, merge/test overhead; nominal count $\ne$ useful parallelism | Score рос вместе с runtime/cost; нет человека, no-AI `k` и accepted-result calibration |
| Scheduling | Graham (1966) | List scheduling with precedence | Bound для M1--M2 при фиксированном priority list | Нет `C(P)` и common human resource |
| Scheduling | Graham (1969) | LPT for independent jobs | Tight approximation relative to `T*` | Не относительно `B_1`; не DAG/M3/M4 |
| Scheduling | Pinedo (2008), 3rd ed. | Textbook | Makespan и parallel-machine notation | Не использовать metadata 6th ed. 2022 |
| Scheduling | Brucker et al. (1999) | RCPSP review | DAG, modes и renewable resource capacity 1 | Не AI-specific `k`, `h` или `gamma` |
| Common server | Hall et al. (2000) | Parallel machines with common server | Ближайший формальный аналог shared sequential service | Server setup не равен полному human review/rework cycle |
| Common server | Kravchenko, Werner (1997) | Parallel machines with single server | Второй аналог shared capacity-1 resource | Нет DAG, LLM semantics и switching cost |
| Repeated common server | Elidrissi et al. (2023; arXiv v1) | Two machines; server loading and no-delay unloading; makespan | Service--executor--service и machine hold при недоступной выгрузке уже стандартны | Независимые jobs; нет rework loop, DAG, `k`, software calibration; препринт |
| Reentrant shared server | Chakhlevitch, Glass (2009) | Primary machine--remote server--same primary machine; makespan | Ближайший формальный аналог чередования executor--service--executor | Одна reentry; primary machine во время server phase освобождается; не software tasks |
| HRI | Olsen, Wood (2004) | Fan-out model and experiments | Ограниченный полезный fan-out; autonomous vs interaction time | Robot fan-out не калибрует число coding agents |
| HRI | Crandall et al. (2005) | Formal/empirical multitasking model | Capacity-1 attention и feasibility intervention windows | Steady-state robot cycles, не fixed project makespan |
| HRI | Crandall et al. (2011) | State-dependent attention allocation | Policy- and state-dependent service/switching | Не функция `gamma(P)` и не coding data |
| HRI | Cummings, Mitchell (2008) | 12-person UAV simulation; interaction/queue/SA wait and predicted capacity | Capacity-1 queue, reorientation and finite useful fan-out | Capacity model, small UAV context; 36--67% reduction нельзя переносить на coding agents |
| Cognition | Salvucci, Taatgen (2008) | Threaded cognition | Интерференция на отдельных последовательных cognitive resources | Не вся human activity serial; нет long coding calibration |

## Синтез по уровням M0--M4

| Уровень | Ближайшая литература | Корректное позиционирование |
|---|---|---|
| M0 | AI productivity; effort estimation | `k` является task/tool/user/mode/outcome-specific входом; до проекта нужен внешний `\hat{k}` |
| M1 | Graham (1969), Pinedo | Неделимость, longest job и LPT стандартны; новизны здесь нет |
| M2 | Graham (1966), RCPSP | DAG, critical path и makespan стандартны; AI-специфика только в длительностях и baseline |
| M3 | Gunther, Brooks, Kim et al., CAID | `C(P)` -- topology-dependent гипотеза; actual concurrency и integration можно наблюдать, но форму и параметры надо калибровать |
| M4 | RCPSP, loading/unloading and reentrant server models, HRI, MAGIS/CAID | Capacity-1 service, reentry, fan-out, DAG и audit loops известны по отдельности; вклад -- их software-specific совместное отображение, а не отдельный механизм |

## Решения по спорным местам модели

1. Вклад формулируется как software-specific synthesis, а не как изобретение
   makespan, DAG, общего ресурса или multi-agent scaling.
2. `C(P)` и `gamma(P)` являются калибруемыми гипотезами. Конечный оптимум по
   `P` требует растущего штрафа (`beta>0` или `delta H>0`), а не следует
   безусловно.
3. M4 зафиксирована как фазовая модель с локальной блокировкой: начатая задача
   удерживает назначенного агента до приёмки, включая очередь к человеку;
   остальные агенты продолжают работу независимо. Переиспользование
   заблокированного потока и запуск дополнительного приоритетного потока сверх
   `P` исключены из области статьи. Поэтому при `C=gamma=1` ветвь `W/P`
   сохраняется как нижняя граница, но фактическое время может быть больше из-за
   эндогенного ожидания `Q(pi)`.
4. `C(P)` применяется только к автономной агентной работе `A`, а `gamma(P)` --
   только к человеческим фазам `H`; скорректированные веса используются и в
   суммарной работе, и при вычислении критического пути.
5. Граница Graham относится к list scheduling в `P|prec|Cmax`; отсутствие
   common resource относится к этой постановке, а не ко всей scheduling
   literature.
6. Численные AI outcomes не смешиваются: elapsed time, active time,
   throughput, quality, success и comprehension остаются разными величинами.
7. CAID является ближайшей фактически конкурентной coding-agent системой, но
   её рост score при большем runtime/cost не интерпретируется как speedup.
8. Loading/unloading и reentrant server models исключают novelty claims для
   повторного сервиса, возврата на тот же executor и отдельных вариантов slot
   hold; отличие M4 находится в software mapping и совместной калибровке.

## Не включены в основной корпус

| Источник | Решение | Причина |
|---|---|---|
| Gustafson (1988) | optional | Scaled workload/throughput, тогда как статья фиксирует workload и makespan |
| Noy, Zhang (2023) | optional | Полезный внешний knowledge-work benchmark, но не software-specific |
| Vaccaro et al. (2024) | optional | Quality/complementarity meta-analysis, не time/makespan |
| OSDAG (2026) | optional | Полезный DAG-dispatch example, но не formal foundation и без human loop |
| Sander et al. (2026) | optional | Agent roles в основном последовательны; nominal count не равен `P` |
| Jiang et al. (2015) | optional | Loading/unloading аналог релевантен, но проверен только abstract; Elidrissi et al. доступен полностью и покрывает нужное структурное различие |
| Talbot (1982) | optional | Первичная multi-mode RCPSP работа, но полный текст в этой итерации недоступен; mode properties уже покрыты Brucker et al. |
| Balas (1969) | optional | Исторический disjunctive-graph первоисточник; полный текст недоступен, стандартность механизма проверена по Pinedo |
| MASAI / HyperAgent | optional | Repository roles и testing полезны, но не добавляют actual-concurrency/human-time evidence поверх MAGIS и CAID |
| Bryant, Kirkham (1983) | excluded from body | Локальный файл ошибочно назван `boehm1981.pdf`; это вторичный review essay |
| ACEM | excluded | Недатированная непроверенная рукопись без эмпирической валидации |
| Cognitive gaps (2026) | excluded | Narrative taxonomy без coding productivity data |
| Post-AGI economics (2026) | excluded | Нормативная периферия относительно fixed-workload model |
| Shipping on faith (2026) | excluded | Production-readiness governance, не scaling или human attention |

## Итоговое позиционирование

Предшествующие работы по отдельности моделируют effort, parallel-machine
scheduling, repeated shared service, operator attention или agent coordination.
В пределах корпуса, просмотренного по протоколу от 2026-08-09, не найдена
работа, совместно калибрующая на software tasks task/mode-specific `k`, agent и
human intervals, DAG, actual concurrency, repeated human service, local slot
hold, integration/switching overhead и accepted-result calendar makespan.
Статья объединяет эти величины в одной фазовой постановке и задаёт протокол их
оценки, но её текущие синтетические эксперименты сами не закрывают эмпирический
пробел.
