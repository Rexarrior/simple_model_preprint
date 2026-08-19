# Bousetouane (2026): governance readiness AI-агентов, а не производительность или multi-agent scaling

## Назначение и главный вывод

Этот документ разбирает Bousetouane (2026) применительно к модели M0-M4 для
fixed-workload makespan звезды «один developer - `P` coding agents».

Фактический источник - не обзор production deployments и не исследование
производительности разработки. Это работа одного автора, которая:

1. вводит ProofAgent Index (PAI), составной индекс готовности AI-агента к
   production release;
2. реализует индекс в авторском ProofAgent Harness;
3. проверяет внутреннюю различительную способность индекса на adversarial trap
   evaluations в доменах healthcare и finance.

Главная граница переноса: paper оценивает, ранжирует ли PAI риск провала на
других traps того же harness. Он не наблюдает реальные production deployments,
software tasks, developers, принятый код, completion time, human effort,
rework или project makespan. Число одновременно работающих агентов не
варьируется. Поэтому источник не калибрует `k`, `h`, `H`, `P`, `C(P)` или
`gamma(P)` и не даёт evidence о multi-agent scaling.

**Рекомендация:** исключить из основного корпуса Related Work текущей статьи как
периферийный источник. При отдельном обсуждении quality/readiness constraints
его можно упомянуть одной оговорочной фразой: capability benchmark не заменяет
production release gate. Использовать его как доказательство ускорения,
надёжности в production или преимуществ нескольких coding agents нельзя.

Локальный PDF содержит 24 страницы. Основной текст занимает PDF-страницы 1-21,
references - 22-24. Напечатанная нумерация совпадает с номерами PDF. Все ссылки
на страницы ниже относятся к локальной копии.

## Библиография, версия и статус

**Точное название:** “Stop Shipping AI Agents on Faith: Capability Is Not
Production Readiness”.

**Автор:** Fouad Bousetouane.

**Аффилиации на титуле:** ProofAgent.ai и The University of Chicago, USA (PDF
с. 1).

**Полная рабочая ссылка:** Fouad Bousetouane. “Stop Shipping AI Agents on Faith:
Capability Is Not Production Readiness.” arXiv:2607.27677v1 [cs.MA], 2026.
DOI: [10.48550/arXiv.2607.27677](https://doi.org/10.48550/arXiv.2607.27677).

**Проверенная версия:** `arXiv:2607.27677v1`, подана 30 июля 2026 года в
04:44:47 UTC. Primary category - `cs.MA`, secondary category - `cs.AI`. На 4
августа 2026 года submission history содержит только v1. На первой странице PDF
напечатано `arXiv:2607.27677v1 [cs.MA] 30 Jul 2026`.

**Статус:** arXiv preprint. В PDF и записи arXiv нет peer-reviewed venue,
сведений о принятии или издательской версии. Источник нельзя называть
рецензируемым или принятым к публикации.

**Лицензия arXiv:** CC BY 4.0.

**Конфликт интересов:** автор сообщает об аффилиации с ProofAI LLC и
ProofAgent.ai, которые разрабатывают описанные ProofAgent Harness и ProofAgent
Index (PDF с. 21). Это не опровергает результаты, но усиливает необходимость
независимой внешней валидации.

**Локальная копия:**
`shipping_faith2026.pdf`, SHA-256
`34c92f7faeefa6e03338788ad45376c3a8fd55337a83647fd8158c567e2f55a9`.

Предлагаемая BibTeX-запись, если источник всё же понадобится в discussion:

```bibtex
@misc{bousetouane2026shipping,
  author        = {Bousetouane, Fouad},
  title         = {Stop Shipping {AI} Agents on Faith: Capability Is Not Production Readiness},
  year          = {2026},
  eprint        = {2607.27677},
  archiveprefix = {arXiv},
  primaryclass  = {cs.MA},
  doi           = {10.48550/arXiv.2607.27677},
  url           = {https://arxiv.org/abs/2607.27677},
  note          = {Version 1, submitted 30 July 2026}
}
```

## Фактический тип работы и исследовательский вопрос

### Тип работы

Наиболее точная классификация:

- method/index proposal;
- prototype implementation report;
- controlled adversarial benchmark validation внутри авторского evaluation
  harness.

Это не:

- systematic или scoping review;
- field study production deployments;
- observational production telemetry study;
- randomized developer productivity experiment;
- software engineering benchmark;
- исследование управления одним человеком несколькими агентами;
- исследование multi-agent architecture scaling.

Раздел 2 называется Related Work, но наличие такого раздела не превращает paper
в обзор. Его основной вклад - новый индекс и собственная validation study.

### Явный RQ

Центральный вопрос empirical section сформулирован прямо (PDF с. 10):

> Соответствуют ли более низкие PAI scores более высокому риску провала на
> unseen ProofAgent Harness traps?

Дополнительные evaluation goals (Table 1, PDF с. 10):

1. ранжирует ли PAI unseen failure risk;
2. снижает ли context engineering defect rate;
3. связан ли capability tier с failure risk;
4. достаточно ли capability для readiness;
5. сохраняется ли signal в healthcare и finance;
6. остаётся ли PAI decomposable и auditable.

Таким образом, фактический estimand - различительная способность индекса внутри
trap-based evaluation environment. Это не эффект внедрения агента на
производительность, качество реального продукта или частоту production
incidents.

## Что именно измеряет PAI

PAI объединяет четыре оси на шкале 0-100 (PDF с. 7-9):

| Ось | Содержание по paper |
|---|---|
| Evaluation `E` | Task success, hallucination resistance, safety, instruction following, manipulation resistance, tool use |
| Context `Q` | Role clarity, instructions, grounding, memory, tool schemas, guardrails, injection hardening, token efficiency |
| Compliance `C` | Наличие evidence соответствия применимым controls; отсутствующее evidence не считается выполнением |
| Governance `G` | Ownership, scope, approval, monitoring, incident response, rollback, evidence retention, lifecycle control |

Raw score - weighted geometric mean осей. В эксперименте применяются равные
веса. Отдельный admissibility gate ограничивает итоговый score при hard block;
missing mandatory evidence также блокирует положительный release verdict (PDF
с. 8-9).

Hard blocks включают prohibited use, critical safety failure, недостаточную
hallucination resistance, tool-use breach, critical technical finding, missing
compliance evidence, unresolved governance finding и недостаточный capability
для risk tier. Итоговые bands: `Blocked`, `Not ready`, `Ready with caveats`,
`Ready` (PDF с. 9).

Это полезная release-governance конструкция, но она не является временной или
ресурсной моделью. Ни одна ось не измеряет elapsed accepted-work time,
developer effort или concurrency.

## Empirical design

### Конфигурационная сетка

Validation пересекает три фактора (PDF с. 10-11):

- domain: healthcare, finance;
- capability tier: weak, mid, strong;
- context condition: B0, B5.

Получаются `2 x 3 x 2 = 12` configurations.

Capability tiers заданы разными backbone models:

| Tier | Model |
|---|---|
| Weak | `amazon/meta.llama3-8b-instruct-v1:0` |
| Mid | `scaleway/llama-3.3-70b-instruct` |
| Strong | `databricks/databricks-llama-4-maverick` |

Это ordinal model-class factor, а не одинаковая система с одним независимо
изменённым параметром. Переход tier одновременно меняет размер, поколение и
архитектуру backbone.

Контекст также изменяется пакетом. B0 объединяет weak instructions, grounding,
tool-schema constraints, guardrails и incomplete governance profile. B5
объединяет stronger instructions, grounding, tool structure, guardrails и
governance evidence. Поэтому эффект B0 против B5 нельзя разложить на причинные
эффекты отдельных компонентов context engineering.

Evaluated agents вызывались через Eden AI EU endpoint. Scoring выполнял
ProofAgent Harness: primary harness LLM - local `gemma-3-27b-it`, fallback -
`scaleway/qwen3-235b-a22b-instruct-2507`; использованы три scoring personas с
Debate consensus и majority rule для compliance checks (PDF с. 11).

### Held-out configuration study

Для каждой из 12 configurations создавались два непересекающихся trap packs
(PDF с. 12):

- development pack: 25 turns, по которым вычислялись `E,Q,C,G` и PAI;
- held-out exam pack: 10 других turns, по которым configuration получала
  `PASS` или `FAIL`.

Итого: `12 x (25 + 10) = 420` turns. Единица анализа для AUC - configuration,
не turn. Из 12 configurations восемь получили `FAIL`, четыре - `PASS` (PDF
с. 12-13).

`FAIL` означал, что exam pack содержал release-blocking failure или превышал
failure tolerance для deployment risk tier. Это отделяет конкретные development
и exam traps, но predictor и outcome остаются внутри одной авторской ontology,
harness и семейства failure rules. Поэтому AUC проверяет internal held-out
consistency, а не external criterion validity против production outcomes.

### 10,000-turn validation

Вторая часть содержит (PDF с. 15):

- 10,000 evaluated turns;
- 1,000 multi-turn sessions;
- те же 12 configurations;
- два domain labels, три capability tiers и два context conditions;
- 4,179 turns с одним назначенным primary defect type.

Paper прямо предупреждает, что reported rates являются **trap-conditional** и
не должны интерпретироваться как ожидаемые production failure rates (PDF с.
15). Следовательно, авторское выражение “deployment scale” относится к объёму
harness evaluation, а не к фактическому production deployment.

## Основные результаты

### Held-out ranking

На 12 configuration-level observations PAI получил `AUC = 0.98`; были восемь
failed и четыре passing configurations, а highest-scoring FAIL и lowest-scoring
PASS образовали одну tied boundary pair (PDF с. 12-14).

Ablation на тех же 12 outcomes (PDF с. 14-15):

| Predictor | Held-out AUC |
|---|---:|
| `E` only | 0.80 |
| `Q` only | 0.88 |
| Geometric mean `E,Q` | 0.94 |
| Arithmetic mean `E,Q,C,G` | 0.94 |
| PAI without hard-block cap | 0.97 |
| PAI with hard-block cap | 0.98 |

Разница `0.97 -> 0.98` от hard-block cap получена на крайне малой выборке из 12
configurations и без interval estimate. Её нельзя представлять как устойчивое
доказательство превосходства конкретной aggregation rule.

### Trap-conditional defect rates

По 10,000 turns общий defect rate равен `4,179 / 10,000 = 41.79%` (PDF с. 15).

**Context contrast** (PDF с. 16):

| Context | Turns | Defects | Defect rate |
|---|---:|---:|---:|
| B0 | 5,000 | 3,287 | 65.74% |
| B5 | 5,000 | 892 | 17.84% |

Reported difference: `47.90` percentage points и `72.9%` relative reduction.

**Capability contrast** (PDF с. 16):

| Capability | Turns | Defects | Defect rate |
|---|---:|---:|---:|
| Weak | 3,334 | 2,510 | 75.28% |
| Mid | 3,334 | 839 | 25.16% |
| Strong | 3,332 | 830 | 24.91% |

Главное снижение наблюдается между weak и mid; aggregate rates mid и strong
почти совпадают.

**Совместный context-capability contrast** (PDF с. 16-17):

| Capability | Context | Turns | Defects | Defect rate |
|---|---|---:|---:|---:|
| Weak | B0 | 1,667 | 1,641 | 98.44% |
| Weak | B5 | 1,667 | 869 | 52.13% |
| Mid | B0 | 1,667 | 830 | 49.79% |
| Mid | B5 | 1,667 | 9 | 0.54% |
| Strong | B0 | 1,666 | 816 | 48.98% |
| Strong | B5 | 1,666 | 14 | 0.84% |

**Domain contrast** (PDF с. 17): finance `41.64%` (`2,083/5,002`) и healthcare
`41.94%` (`2,096/4,998`).

**Primary defect types** (PDF с. 17):

| Type | Count | Share of defects |
|---|---:|---:|
| Safety | 1,385 | 33.14% |
| Tool use | 1,381 | 33.05% |
| Hallucination resistance | 1,314 | 31.44% |
| Phantom tool call claimed | 99 | 2.37% |

Каждому defective turn назначен один primary type, поэтому counts взаимно
исключаются и суммируются в 4,179.

## Неопределённость и measurement gaps

### Что paper сообщает

Paper даёт точечные counts, percentages, PAI values и AUC. Для AUC автор
отмечает одну tied boundary pair и малое число 12 configurations (PDF с.
12-14). Также указано, что trap rates нельзя переносить на production (PDF с.
15).

### Что не сообщается

В PDF отсутствуют:

- confidence intervals для AUC и defect rates;
- repeated runs или distribution результатов по seeds;
- hypothesis tests или uncertainty для context/capability contrasts;
- cluster-aware analysis, учитывающий вложенность turns в 1,000 sessions и 12
  configurations;
- power calculation или preregistration;
- sensitivity analysis к PAI weights, thresholds и hard-block rules, кроме
  ограниченной ablation;
- inter-rater или test-retest reliability scoring personas;
- human adjudication benchmark для LLM-judge verdicts;
- фактическая fallback invocation rate, хотя автор прямо пишет, что её следует
  сообщать из run artifacts (PDF с. 11, 18);
- полные run artifacts и data package, позволяющие независимо восстановить все
  420 и 10,000 outcomes непосредственно из paper;
- внешний validation set из другой организации, другого harness или реальных
  incidents;
- longitudinal drift evaluation после смены model, context или policy.

Большое число turns не превращает 10,000 observations в 10,000 независимых
production cases. Turn-level point estimates описывают конкретное распределение
adversarial traps и конкретный scoring pipeline.

### Construct-validity gap

Development и exam packs не пересекаются по конкретным traps, что уменьшает
прямую утечку test items. Однако PAI predictor и held-out PASS/FAIL outcome
созданы одним ProofAgent Harness, используют родственные failure constructs и
release rules. Поэтому `AUC=0.98` подтверждает переносимость внутри собственной
measurement system, но не показывает, что PAI предсказывает:

- production incidents;
- developer acceptance;
- escaped defects;
- correctness или maintainability software artifacts;
- regulatory audit outcomes;
- user harm;
- time, cost или business value deployment.

## Production deployment evidence

### Что есть

- Open-source harness реализует CLI evaluation workflow, JSON/Markdown reports,
  governance profile и release-review artifacts (PDF с. 18-20).
- Run можно связать с agent version, context package, domain knowledge,
  governance profile и environment metadata (PDF с. 19-21).
- PAI формализует fail-closed release decision и сохраняет decomposed evidence
  вместо одного capability score (PDF с. 7-9, 20-21).

### Чего нет

- ни одного описанного реального production deployment;
- числа организаций, release decisions, пользователей или deployed agents;
- pre/post-deployment comparison;
- incident, rollback, audit или monitoring outcomes после release;
- production traffic, latency, uptime или task-success telemetry;
- evidence, что PAI gate уменьшил реальные failures;
- comparison released vs blocked agents в поле.

Следовательно, paper даёт **production-readiness framework**, но не
**production deployment evidence**. Реализованный CLI подтверждает наличие
prototype/tooling, а не external effectiveness release process.

## Benchmarks против реальной работы

Фактический benchmark - adversarial multi-turn trap evaluation в двух
регулируемых domain settings. Domain labels повышают содержательную
правдоподобность scenarios, но не делают turns реальными healthcare или finance
transactions.

Для сопоставимости с реальной работой отсутствуют:

- sampling frame production tasks;
- task identity и естественное распределение task types;
- fixed workload и одинаковые acceptance criteria;
- no-agent или alternative-workflow comparator;
- реальные human users и domain professionals;
- downstream consequences agent actions;
- обычная, не adversarial task frequency;
- time/cost/quality trade-off.

Trap-conditional defect rate полезен для stress testing, но его denominator -
число специально сформированных evaluation turns, а не число рабочих задач.

## Acceptance, quality и reliability

### Acceptance

В paper `PASS/FAIL` означает соответствие held-out trap pack release policy, а
readiness bands означают решение governance gate. Это не developer acceptance
agent-generated code и не принятие законченной software task.

### Quality

Ось `E` включает task success и несколько safety/reliability metrics. Однако
paper не измеряет:

- functional correctness code artifact;
- тестовое покрытие;
- maintainability, security или performance кода;
- соответствие software specification;
- качество интеграции нескольких changes;
- одинаковый quality gate при сравнении completion time.

Поэтому PAI нельзя использовать как quality adjustment для `k`. Его можно
рассматривать только как пример отдельного release constraint.

### Reliability

Reported reliability - частота defect labels на traps и configuration-level
held-out ranking. Нет repeated-trial reliability одной и той же task,
production failure rate, mean time between failures или стабильности по версиям.

### Human review и rework

Governance axis включает approval, monitoring, incident response, rollback и
human oversight как policy concepts. Reports предназначены для human release
review (PDF с. 7-9, 19-21). Но empirical study не измеряет:

- время человека на review;
- число review iterations;
- acceptance/rejection agent output человеком;
- исправление defects и повторный запуск;
- rework duration;
- очередь нескольких агентов к одному reviewer;
- context-switching reviewer между agent streams.

`human_oversight` в governance profile - metadata/policy field, а не
хронометраж человеческого ресурса. Его нельзя интерпретировать как `h` или `H`.

## Полное mapping к `Z,k,r,W,P,L,C(P),h,H,gamma(P)`

Здесь **direct contextual support** означает близкий наблюдаемый construct без
численной совместимости с M0-M4; **mechanism only** - мотивирующий механизм;
**absent** - параметр не измеряется.

| Поле M0-M4 | Статус | Ближайший объект Bousetouane | Точная граница |
|---|---|---|---|
| `X` | **absent** | Нет общей baseline unit времени | Evaluation scores и defect labels не являются временем ручной работы |
| `Z_i` / `Z` | **absent** | Trap/domain labels и capability-context grid | Нет software task difficulty относительно no-AI baseline, story points или effort scale |
| `k_i^(r)` / `k` | **absent** | Defect rates при B0/B5 и capability tiers | Нет duration ratio, no-AI denominator, fixed task и quality-adjusted completion time |
| режим `r` | **mechanism only** | B0/B5 context packages и разные backbone tiers | Это bundles operating context и model capability, а не сравнение interactive/delegated/autonomous coding workflows |
| `W = X sum Z_i k_i` | **absent** | 420 и 10,000 evaluation turns | Число traps не является фиксированным объёмом software work |
| `P` | **absent** | 12 configurations, 1,000 sessions и три scoring personas | Ни configurations, ни sessions, ни evaluator personas не являются числом concurrent coding agents у одного developer; `P` не варьируется |
| `L` / DAG | **absent** | Multi-turn scenarios | Нет task precedence graph, duration weights или critical path project work |
| `C(P)` | **absent** | Tool-use defects и governance overhead | Нет agent-agent integration cost и dose-response по concurrent agent count |
| `a_i^(r)` | **absent** | Agent выполняет evaluation turns | Agent-active time отдельно не измеряется |
| `h_i^(r)` / `h` | **mechanism only** | Human oversight, approval и release review как required controls | Policy presence не является active human time share; specification/review/correction intervals не записаны |
| `H = X sum Z_i h_i` | **absent** | Governance metadata и reports | Нет набора jobs и capacity-1 service intervals одного reviewer |
| `gamma(P)` | **absent** | Нет близкого measured construct | Переключение человека между concurrent agent contexts не изучается |
| Makespan | **absent** | Число turns/sessions и release report | Нет start/finish fixed workload, elapsed duration или accepted project completion |
| Quality/readiness constraint | **direct contextual support** | PAI bands, hard blocks, held-out trap outcomes | Это отдельный admissibility construct; он не встроен в time objective и не валидирован production outcomes |

### Mapping к уровням M0-M4

| Уровень | Что требует M0-M4 | Что даёт источник | Вердикт |
|---|---|---|---|
| M0 | Fixed `W`, one-stream time factor `k`, ideal `W/P` | Readiness score и adversarial defect rate | Не калибрует работу, время или speedup |
| M1 | Неделимые jobs и longest-job duration | Отдельные turns | Turn не определён как software job и не имеет elapsed weight |
| M2 | Precedence DAG и critical path `L` | Multi-turn interaction sequence | Нет project DAG или makespan bound |
| M3 | Дополнительный integration overhead как функция `P` | Tool-use defects | Нет нескольких worker agents и зависимости overhead от `P` |
| M4 | Один developer, `k=a+h`, capacity-1 `H`, verification windows, `gamma(P)` | Governance требует oversight/review conceptually | Human activity и concurrency не измеряются |

## Изучается ли concurrency или multi-agent scaling

Нет. Несмотря на primary category `cs.MA`, empirical design не варьирует число
worker agents и не сравнивает centralized, decentralized, independent или
communicating agent architectures.

Не являются `P`:

- три capability tiers - это три класса backbone model;
- 12 configurations - это factorial cells;
- 1,000 sessions - это evaluation units;
- три scoring personas - это jury внутри harness;
- 10,000 turns - это объём evaluation events.

Paper не сообщает simultaneous execution, fan-out одного человека, agent-agent
communication, shared artifacts, merge conflicts, queueing к reviewer или
scaling curve. Поэтому источник не поддерживает `P`, `C(P)`, finite optimal
parallelism или потолок по `H`.

## Что источник поддерживает для текущей статьи

1. **Capability score не равен production readiness.** Release decision может
   требовать отдельного context, compliance и governance evidence, а также hard
   blocks (PDF с. 7-9, 21).
2. **Evaluation должна сохранять decomposed evidence.** Один aggregate score
   может скрывать unsafe tool behavior или missing mandatory controls (PDF с.
   8-9, 13-15).
3. **Operating context влияет на adversarial reliability.** В конкретном
   ProofAgent trap setup B5 имел существенно меньший defect rate, чем bundled
   B0 condition (PDF с. 15-17). Это context-specific benchmark result, не
   production effect size.
4. **Capability и context нельзя отождествлять.** В harness validation mid/strong
   agents при B0 были хуже mid agent при B5 по trap-conditional defect rate
   (PDF с. 16-18).
5. **Adversarial benchmark rates нельзя переносить на production base rates.**
   Эту границу автор фиксирует прямо (PDF с. 15).
6. **Time objective нуждается в заданном acceptance standard.** Это вывод для
   позиционирования M0-M4: makespan имеет смысл сравнивать только для outputs,
   прошедших заранее определённый quality/readiness gate. Сам paper временной
   модели не даёт.

## Что источник не позволяет утверждать

1. Что PAI валидирован на production deployments.
2. Что `AUC=0.98` предсказывает production incidents или business outcomes.
3. Что 10,000 turns являются 10,000 реальными healthcare/finance tasks.
4. Что B5 уменьшает production failure rate на `72.9%`.
5. Что stronger context причинно даёт весь observed contrast: B0/B5 меняют
   несколько компонентов одним пакетом.
6. Что hard-block cap устойчиво превосходит uncapped PAI: разница AUC `0.01`
   получена на 12 configurations без interval estimate.
7. Что PAI надёжнее независимой human review или внешнего audit.
8. Что LLM judging согласуется с экспертами: human adjudication study нет.
9. Что readiness score измеряет code quality, developer productivity или
   accepted software output.
10. Что observed defect означает rework и имеет измеренную стоимость во времени.
11. Что governance evidence сокращает makespan или human effort.
12. Что `human_oversight` field даёт численное `h`.
13. Что source измеряет один developer - несколько agents.
14. Что три scoring personas являются multi-agent worker system.
15. Что source оценивает `P`, `L`, `C(P)`, `H`, `gamma(P)` или optimal
    concurrency.
16. Что результаты относятся к coding agents: validation domains - healthcare и
    finance, а software-development task set не описан.
17. Что source peer-reviewed; проверенный статус - arXiv v1.

## Отличие от M0-M4

| Измерение | Bousetouane (2026) | M0-M4 |
|---|---|---|
| Центральный вопрос | Ранжирует ли PAI риск провала на unseen harness traps и достаточно ли evidence для release | Когда один developer с `P` coding agents сокращает fixed-workload makespan |
| Тип результата | Governance readiness index и internal held-out validation | Детерминированная time/scheduling model |
| Unit of analysis | Configuration и adversarial turn | Software task `i`, fixed task set и project completion |
| Population | 12 model-context-domain configurations | One-developer star с externally calibrated parameters |
| Workload | Harness trap packs | Заданный объём `Z_i`, `W` и optional DAG |
| Baseline | B0/B5 и capability tiers | Последовательная no-AI работа `T_h = X sum Z_i` |
| Outcome | PAI, PASS/FAIL, trap-conditional defect rate | Elapsed accepted-work makespan и speedup |
| Acceptance | Governance policy и hard blocks | Output считается завершённым после включённых в duration verification/rework |
| Human role | Oversight, approval и review как policy requirements | Timed specification, verification и correction как `h_i`; общий `H` |
| Parallelism | Не изучается | Explicit `P` concurrent coding agents |
| Dependencies | Multi-turn scenario, без project DAG | Precedence DAG и critical path `L` |
| Overhead | Не временной; readiness controls | `C(P)` и `gamma(P)` как time penalties |
| External validity | Adversarial healthcare/finance harness | Требует калибровки на software tasks и workflows |

Источник находится не рядом со scheduling layer M0-M4, а на ортогональной оси
release governance. Полезный синтез состоит не в переносе результатов в
коэффициенты модели, а в уточнении границы objective: минимизация makespan не
должна позволять обход обязательного acceptance/readiness constraint.

## Рекомендация по включению

### Вердикт

**Исключить из основного Related Work.** Причины:

- нет software-development population или coding tasks;
- нет time/effort/makespan outcome;
- нет реальных production deployments;
- нет human review timing и rework;
- нет concurrency или multi-agent scaling;
- связь с M0-M4 ограничена общей оговоркой о quality/readiness gate;
- работа является self-authored validation собственного коммерчески связанного
  framework и пока имеет статус arXiv v1.

В ограниченный корпус на 20-25 источников paper уступает более прямым работам о
developer productivity, production coding-agent telemetry, human-agent
interaction, shared-server scheduling и multi-agent scaling.

### Когда допустимо оставить

Источник можно сохранить как optional discussion citation, если в статье
появится отдельный абзац о том, что текущая модель:

- оптимизирует только elapsed time;
- предполагает фиксированный acceptance standard;
- не моделирует production governance, compliance и safety как отдельные
  objectives;
- в будущем может быть расширена constrained optimization: минимизировать
  makespan при обязательном quality/readiness gate.

Он не нужен для доказательства формул M0-M4.

## Проверенные claims и возможное встраивание

### Безопасные claims

1. Bousetouane (2026) предлагает PAI, который объединяет Evaluation, Context,
   Compliance и Governance посредством geometric aggregation и hard-block
   release gate (PDF с. 7-9).
2. В авторской held-out trap validation использованы 12 configurations; PAI,
   рассчитанный по 25 development turns на configuration, ранжировал PASS/FAIL
   на десяти других turns с reported `AUC=0.98`, восемью FAIL, четырьмя PASS и
   одной tied boundary pair (PDF с. 10-14).
3. В отдельной 10,000-turn adversarial validation B0 и B5 получили defect rates
   `65.74%` и `17.84%`, но paper прямо запрещает трактовать эти
   trap-conditional rates как production failure rates (PDF с. 15-18).
4. Source рассматривает release readiness, а не developer productivity:
   elapsed task time, accepted code, human effort и fixed workload не
   измеряются.
5. Concurrency не варьируется; capability tiers, sessions и scoring personas не
   являются числом coding agents `P`.

### Claims, которых следует избегать

- «PAI доказанно снижает production failures».
- «На 10,000 production tasks сильный context снизил ошибки на 72.9%».
- «Production-ready agents работают быстрее».
- «Governance уменьшает rework или human review time».
- «AUC 0.98 подтверждён на независимых организациях».
- «Исследование показывает benefit multi-agent systems».
- «Три agent personas обеспечили надёжный multi-agent consensus» без оговорки,
  что это LLM scoring jury, а human reliability не проверена.
- «Работа калибрует `k`, `h`, `C(P)` или `gamma(P)`».

### Встраивание только при расширении discussion

Не рекомендуется вставлять этот текст в текущий core Related Work. Если нужен
короткий limitation paragraph, допустима следующая формулировка:

> Временная эффективность не исчерпывает production readiness. Bousetouane
> (2026) предлагает отдельный release index, объединяющий behavioral evaluation,
> context, compliance и governance evidence с hard-block conditions. Его
> validation выполнена на adversarial ProofAgent Harness traps, а не на
> production deployments, поэтому reported defect rates не калибруют
> производительность или надёжность coding agents. Для настоящей модели этот
> источник задаёт только внешнюю границу применимости: makespan следует
> оптимизировать при фиксированном acceptance/readiness standard, а не вместо
> него.

### Более короткая оговорка для limitations

> M0-M4 моделирует время при заданном стандарте приёмки и не заменяет отдельную
> проверку production readiness, включающую safety, compliance и governance.

Для этой общей фразы ссылка на Bousetouane optional: claim нормативный и может
быть лучше поддержан независимыми стандартами или peer-reviewed evaluation
literature, чем self-validation PAI.

## Таблица доказательных страниц

| PDF-страница | Раздел / объект | Опорное содержание | Статус evidence |
|---:|---|---|---|
| 1 | Title; Abstract | Exact title, author, affiliations, arXiv v1, заявленный PAI и headline validation | Metadata и author summary |
| 2 | Contents | Структура: related work, PAI, empirical validation, implementation, conclusion | Навигация |
| 3-4 | Introduction | Capability vs readiness, intended contribution, 10,000-turn claim | Авторская framing, не production evidence |
| 7 | Compliance/governance; PAI; dimensions | Определения readiness и осей `E,Q,C,G` | Прямое описание метода |
| 8 | Aggregation and admissibility | Weighted geometric mean, epsilon floor, cap и final score | Формальная спецификация PAI |
| 9 | Hard blocks; bands; interpretation | Fail-closed logic, release bands, граница «high PAI не значит never fail» | Прямое описание gate |
| 10 | Evaluation goal; Table 1; setup | Явный RQ, шесть goals, 12-configuration grid | Главный источник фактического RQ/design |
| 11 | Tables 2-5 | 420 turns, 10,000 turns, 1,000 sessions, backbone и harness models, B0/B5 | Sample и instrumentation |
| 12 | Held-out strategy; AUC definition | 25 development + 10 exam turns на configuration; PASS/FAIL rule; unit=configuration | Internal held-out design |
| 13-14 | Tables 7-8; configuration values | 12 configurations, 8 FAIL, 4 PASS, AUC 0.98, tied boundary, exact PAI values | Primary result, без CI |
| 14-15 | Ablation; Table 9; large validation setup | AUC 0.80-0.98; 10,000 turns, 4,179 defects; trap-conditional warning | Internal comparison; production перенос запрещён |
| 16 | Tables 11-13 | Context, capability и joint defect rates | Exact point estimates, без uncertainty |
| 17 | Tables 14-15 | Domain rates и mutually exclusive primary defect counts | Exact descriptive results |
| 18 | Interpretation; implementation | Авторские выводы, caveat про fallback artifacts, open-source harness | Interpretation и prototype evidence |
| 19-20 | CLI, mapping, governance profile, reports | Run inputs, evidence bundle, human release-review artifact | Operational tooling, не field deployment |
| 21 | Conclusion; Conflict of Interest | Итоговый claim и affiliation с ProofAI LLC/ProofAgent.ai | Авторский вывод и обязательная COI оговорка |

## Итоговая оценка источника

Источник подтверждает узкий и полезный тезис: behavioral capability benchmark
не является полным production release decision. Однако его empirical evidence
ограничено внутренним adversarial harness validation, где predictor и outcome
принадлежат одной measurement system. Реальных deployments, developers,
software tasks, elapsed time, quality-adjusted acceptance, human review effort и
multi-agent concurrency нет.

Для статьи о fixed-workload makespan звезды «один developer - `P` coding
agents» это ортогональный governance source. Он не поддерживает формальную
иерархию M0-M4 и не закрывает ни один основной evidence gap по `k`, `P`, `L`,
`C(P)`, `h`, `H` или `gamma(P)`. Лучшее решение - исключить его из core
Related Work и при необходимости оставить только одну limitation citation о
том, что time optimization предполагает внешний acceptance/readiness gate.
