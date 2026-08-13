# Canh et al. (2026): OSDAG, DAG-based online dispatch для heterogeneous multi-robot collaboration

## Назначение и границы обзора

Этот документ разбирает OSDAG применительно к модели M0-M4 для fixed-workload makespan звезды «один developer - `P` coding agents». Основной фокус: scheduling problem, DAG и resource model, online/offline assumptions, число и тип исполнителей, objective, алгоритм, теоретические гарантии, эксперименты и наличие человеческого ограничения внимания.

OSDAG релевантна прежде всего уровням M2 и частично M3: работа строит dependency DAG, измеряет makespan и показывает, что динамический запуск готовых задач может уменьшать простой исполнителей по сравнению с заранее зафиксированным последовательным порядком. Однако это робототехническая система без supervising developer. Она не задает no-AI baseline, не измеряет человеческие окна постановки и проверки и не дает численных `k`, `h`, `H`, `C(P)` или `gamma(P)`.

Локальный PDF содержит 6 страниц. Он был прочитан поэтапно: сначала титул и abstract, затем формальная постановка и Algorithm 1, после этого экспериментальные таблицы, real-world section и limitations. Номера ниже относятся к PDF-страницам локальной копии.

## Метаданные, версия и статус

**Точное название:** “OSDAG: Online Scheduling for Efficient Multi-Robot Collaboration”.

**Авторы в порядке титульной страницы PDF:** Thanh Nguyen Canh, Thang Tran Viet, Phuc Van Dinh, Xiem HoangVan, Nak Young Chong.

PDF отмечает Thanh Nguyen Canh и Thang Tran Viet как equal contributors. Xiem HoangVan и Nak Young Chong отмечены символом corresponding author (PDF с. 1).

**Аффилиации:**

- School of Information Science, Japan Advanced Institute of Science and Technology;
- University of Engineering and Technology, Vietnam National University;
- Department of Robotics, Hanyang University.

**Полная проверенная ссылка:** Thanh Nguyen Canh, Thang Tran Viet, Phuc Van Dinh, Xiem HoangVan, and Nak Young Chong. “OSDAG: Online Scheduling for Efficient Multi-Robot Collaboration.” arXiv:2606.15255v1 [cs.RO], 2026. DOI: [10.48550/arXiv.2606.15255](https://doi.org/10.48550/arXiv.2606.15255).

**Проверенная версия:** на первой странице локального PDF напечатано `arXiv:2606.15255v1 [cs.RO] 13 Jun 2026`. Submission history arXiv на дату проверки 4 августа 2026 года содержит только `v1`, поданную 13 июня 2026 года в 11:22:34 UTC.

**Статус:** arXiv preprint. В PDF нет названия принятой конференции или журнала, publisher DOI либо утверждения о прохождении peer review. Поэтому источник нельзя обозначать как accepted или peer-reviewed. arXiv указывает лицензию CC BY 4.0, но это лицензионный, а не публикационный статус.

**Локальная копия:** `/Users/rexarrior/work/articles/simple_model_full/literature/osdag2026.pdf`.

**SHA-256:** `6c2d3b464d58e15b82473324e92baa559d4521d579a0b9e5f58cef77c46427c5`.

### Что именно означает OSDAG

PDF не содержит отдельной фразы вида “OSDAG stands for ...” и не дает буквенной расшифровки аббревиатуры. Авторская формулировка на титуле имеет вид:

> OSDAG: Online Scheduling for Efficient Multi-Robot Collaboration

Метод далее последовательно описывается как сочетание **online scheduling** и **Directed Acyclic Graph (DAG)**. Поэтому безопасная содержательная расшифровка - «OSDAG, online scheduling over a DAG», а точное полное название следует цитировать по титулу. Не следует приписывать авторам отсутствующую в PDF буквенную формулу вроде “Online Scheduling Directed Acyclic Graph”.

## Исследовательский вопрос

Нумерованных RQ в PDF нет. Из abstract, problem statement и contributions восстанавливается следующий проектный вопрос:

> Как один раз преобразовать natural-language instruction в валидный dependency-annotated task graph для heterogeneous agents, а затем во время исполнения запускать готовые задачи так, чтобы соблюдать precedence и feasibility constraints, уменьшать простой и сокращать makespan без повторных LLM calls?

Работа одновременно решает три подзадачи:

1. Grounding: сопоставить инструкцию с доступными агентами, объектами, reachability и action capabilities.
2. Representation: представить полученные подзадачи и зависимости как DAG.
3. Dispatch: во время выполнения выдавать свободному агенту готовую заранее назначенную ему задачу.

Это design-and-evaluation paper. Она не формулирует статистические гипотезы, не доказывает approximation guarantee и не решает общий класс scheduling problems до оптимума.

## Постановка и модель

### Агенты, объекты и capabilities

Задана команда heterogeneous agents

```text
N = {N_1, ..., N_N}
```

и множество объектов

```text
O = {o_1, ..., o_M}.
```

Для агента `N_i` определены reachable set `S(N_i)` и executable action set `A(N_i)`. Геометрическая достижимость объекта задается евклидовым расстоянием и бинарной матрицей `R` (PDF с. 2, equations (1)-(2)).

### Task model

Каждая сгенерированная подзадача имеет вид (PDF с. 3, equation (4)):

```text
T_i = (mu_i, a_i, o_i, d_i, D_i),
```

где:

- `mu_i` - заранее назначенный агент;
- `a_i` - действие;
- `o_i` - целевой объект;
- `d_i` - destination или target state;
- `D_i` - множество prerequisite task IDs.

Для задачи вводятся start time `s_i`, execution duration `p_i` и completion time `c_i=s_i+p_i`. Заявленная цель - минимизация `C_max` при соблюдении precedence, reachability и action-feasibility constraints (PDF с. 3, equations (5)-(9)).

### Три стадии OSDAG

1. **LLM-driven task decomposition.** Gemini Flash вызывается один раз с instruction, описаниями агентов, reachable objects, actions и current object state. LLM должен вернуть структурированный список задач с назначениями и dependencies.
2. **Task graph formalization.** Каждая задача становится вершиной, prerequisite relation - дугой. Topological sort проверяет acyclicity; cyclic graph отвергается.
3. **Constraint-aware online scheduling.** Scheduler хранит completed set `C(t)`, running set `B(t)` и состояния агентов `Free/Busy`. Для свободного агента вычисляется ready set и выбирается задача с наименьшим индексом.

Если LLM output нарушает schema или feasibility constraints, plan отклоняется и генерируется заново с refined constraints (PDF с. 3). Число допустимых regeneration attempts и их влияние на reported reasoning time не специфицированы.

### Что DAG кодирует напрямую

Формально DAG `G=(V,E)` кодирует prerequisite relations: `(v_j,v_i)` означает, что `T_j` должна завершиться до старта `T_i`. Это прямое precedence model.

Работа также говорит, что DAG отражает resource constraints, например object handoff и shared-resource order. Однако reachability и manipulation-state feasibility проверяются не только ребрами DAG, а отдельным runtime predicate

```text
R(N_i, T_j, t) = R_hold(N_i, T_j, t) and R_reach(N_i, T_j).
```

Поэтому точнее различать:

- static precedence/resource ordering, закодированный ребрами;
- dynamic state feasibility, проверяемый scheduler во время dispatch.

### Важное ограничение task allocation

Несмотря на формулировки “allocates ready tasks to idle agents”, Algorithm 1 не выбирает исполнителя среди нескольких совместимых агентов. Ready set свободного агента содержит только задачи с уже фиксированным назначением:

```text
E_i(t) = {T_j | mu_j = N_i, ...}.
```

Следовательно, LLM выполняет assignment до старта execution, а online scheduler выполняет только **dispatch заранее назначенных задач**. Свободный Robot A не может взять готовую задачу Robot B, даже если capabilities это позволяют. Это существенно уже общей multi-robot task allocation problem.

## Online и offline assumptions

Название “online scheduling” требует точной квалификации.

**Что известно до исполнения:** весь набор задач, все назначения `mu_i`, весь DAG и capability context генерируются и валидируются до движения роботов.

**Что происходит online:** scheduler наблюдает фактические завершения, текущие `Free/Busy` states и manipulation state, после чего немедленно запускает новые ready tasks.

**Чего нет:**

- online arrival новых jobs;
- раскрытия новых precedence edges после старта;
- reassignment задачи другому совместимому агенту;
- replanning после execution failure;
- duration-aware или critical-path-aware priority;
- пересмотра DAG при изменении среды.

В терминах классической scheduling theory это ближе к dynamic/event-responsive list dispatch по заранее известному DAG, чем к online scheduling с неизвестным будущим input. Псевдокод при этом не чисто event-driven: он увеличивает время как `t <- t + Delta t`, то есть описывает polling loop, хотя narrative использует термин event-driven (PDF с. 3-4).

## Algorithm 1 и теоретический статус

### Правило dispatch

Algorithm 1 выполняет следующие действия (PDF с. 4):

1. Инициализирует completed и running sets.
2. Для каждого свободного агента вычисляет ready set.
3. Выбирает ready task с наименьшим индексом: `arg min j`.
4. Помещает ее в running set.
5. После completion освобождает агента и повторяет проверку.

Это fixed-priority list rule по task ID. Оно не использует `p_i`, remaining critical path, shortest processing time, longest processing time, slack или прогноз resource contention.

### Что доказано и не доказано

В работе нет теорем, лемм, approximation ratio, lower bounds, competitive ratio, complexity analysis или proof of optimality. Формула `min C_max` задает objective, но Algorithm 1 не доказан как решающий этот optimization problem.

Авторы прямо признают в conclusion, что current task-selection policy may not yield globally optimal schedules (PDF с. 5-6). Поэтому безопасная формулировка - «эвристика уменьшила makespan в отдельных сценариях», а не «алгоритм минимизирует makespan».

### Неполнота математической программы

Constraints (5)-(9) фиксируют objective, precedence и capability feasibility, но не выписывают явное disjunctive/capacity constraint, запрещающее пересечение двух задач одного агента. `Free/Busy` logic Algorithm 1 обеспечивает это операционно. Поэтому equations (5)-(9) сами по себе не являются полной mathematical programming formulation расписания.

## Связь с Graham list scheduling

OSDAG имеет семейное сходство с Graham-style list scheduling:

- есть конечный набор nonpreemptive tasks;
- есть precedence DAG;
- ready tasks запускаются при освобождении исполнителя;
- objective - makespan.

Однако стандартную гарантию Graham для `P|prec|C_max` нельзя переносить автоматически:

1. У Graham исполнители одинаковы, а ready task может быть выдан любому свободному processor.
2. В OSDAG agents heterogeneous, а `mu_i` заранее фиксирует единственного исполнителя задачи.
3. OSDAG проверяет manipulation-state и reachability constraints сверх обычного precedence DAG.
4. Global work-conserving property не гарантирована: агент может простаивать, когда ready tasks существуют, но назначены другим агентам.
5. Algorithm 1 не анализируется через total work `W`, critical path `L` или idle-time chain.

Поэтому OSDAG не дает альтернативу Graham bound и не подтверждает используемый в M2 коридор. Для M0-M4 это современный application example DAG dispatch, а не источник классической scheduling guarantee.

## Связь с RCPSP

Task graph, heterogeneous capabilities, shared-object state и makespan objective естественно соседствуют с RCPSP и multi-mode RCPSP:

- precedence relations соответствуют `prec`;
- `Free/Busy` agent capacity соответствует renewable resource capacity 1 для каждого агента;
- reachable/action sets ограничивают feasible modes или assignments;
- shared-object constraints могут быть заданы ресурсами или дополнительными precedence relations;
- objective соответствует `C_max`.

OSDAG не сопоставляет свою постановку с RCPSP, не использует стандартную RCPSP classification и не дает exact/approximation algorithms для такого класса. Если рассматривать каждого совместимого агента как mode, общий multi-mode formulation был бы шире OSDAG, поскольку OSDAG фиксирует `mu_i` до dispatch.

Следовательно, новизну источника следует искать не в DAG, makespan или capacity constraints как таковых, а в system integration: one-shot LLM decomposition, grounding и lightweight runtime dispatch для robot manipulation.

## Исполнители и человеческое внимание

### Simulation

В simulation workers - роботы. Human supervisor в execution loop отсутствует. LLM является pre-execution planner, а не capacity-1 human orchestrator.

### Real-world experiment

Real-world section содержит одного UF850 manipulator и человека, которому scheduler показывает текстовые команды. Здесь человек является **одним из heterogeneous task executors**, выполняющим физические pick/place actions параллельно с роботом (PDF с. 5).

Это не модель «один developer supervises `P` agents»:

- человек не ставит задачи LLM;
- не проверяет agent outputs;
- не обслуживает все роботные потоки как common server;
- не переключается между review contexts;
- его attention time не измеряется отдельно;
- нет общей очереди human verification.

Human attention в смысле M4 поэтому отсутствует. Наличие человека как физического worker не поддерживает `h`, `H` или `gamma(P)`.

## Эксперименты

### Simulation setup

Эксперименты выполнены в PyBullet на пяти tabletop-manipulation scenarios (PDF с. 4-5):

| Task | Содержание |
|---|---|
| 1 | Matching cubes to bowls, 2 agents |
| 2 | Matching cubes to bowls, 3 agents; проверка parallel execution |
| 3 | Cleaning table с implicit dependency, например открыть drawer до размещения object |
| 4 | Строго упорядоченная сортировка `apple -> banana -> cup` |
| 5 | Matching cubes to bowls с inter-agent handoff |

LLM backbone назван только как `Gemini Flash`; точный checkpoint/version в PDF не указан.

Baselines:

- RoCo, dialogue-based decentralized framework;
- TwoStep, hierarchical LLM-PDDL planner;
- ChatGPT-Prompts, flat-sequence generation.

PDF сообщает одинаковые task instructions и environment states для методов, но не утверждает явно, что все baselines используют тот же LLM checkpoint и одинаковый inference budget.

Metrics:

- Planning Success Rate (`SR`, %);
- Reasoning Time (`RT`, seconds);
- Makespan (`MS`, seconds);
- Success-weighted Step Efficiency (`SSE`).

`RT` и `MS` публикуются отдельно. End-to-end duration `RT+MS` как единый outcome не приводится.

### Полная Table 1

В каждой ячейке указан порядок `SR / SSE / RT / MS`. Результаты усреднены по 10 trials; `-` означает execution failure (PDF с. 4-5).

| Method | Task 1 | Task 2 | Task 3 | Task 4 | Task 5 |
|---|---|---|---|---|---|
| RoCo | `100 / 1.00 / 108.5 / 19.1` | `90 / 0.88 / 206.3 / 21.9` | `0 / 0 / 134.7 / -` | `100 / 1.00 / 64.1 / 22.7` | `100 / 1.00 / 94.8 / 41.6` |
| TwoStep | `90 / 0.90 / 15.2 / 19.1` | `70 / 0.66 / 14.3 / 22.0` | `0 / 0 / 14.8 / -` | `0 / 0 / 14.7 / -` | `90 / 1.00 / 15.0 / 41.6` |
| ChatGPT-Prompts | `100 / 0.50 / 8.2 / 33.9` | `90 / 0.36 / 8.9 / 35.9` | `90 / 0.51 / 8.3 / 48.3` | `100 / 1.00 / 10.3 / 22.7` | `100 / 1.00 / 9.2 / 41.6` |
| OSDAG | `100 / 1.00 / 9.1 / 19.1` | `90 / 0.88 / 14.0 / 22.5` | `80 / 0.80 / 13.4 / 26.1` | `100 / 1.00 / 12.8 / 15.2` | `100 / 1.00 / 10.5 / 26.0` |

### Точный смысл headline results

**“5-15x faster reasoning” относится к сравнению только с RoCo.** Отношения `RT_RoCo/RT_OSDAG` по пяти задачам приблизительно равны `11.9x`, `14.7x`, `10.1x`, `5.0x` и `9.0x`. OSDAG не является самым быстрым planner относительно всех baselines: ChatGPT-Prompts имеет меньшее `RT` во всех пяти задачах (`8.2-10.3 s` против `9.1-14.0 s`).

**“Up to 38% reduction in makespan” относится к Task 5:**

```text
(41.6 - 26.0) / 41.6 = 0.375,
```

то есть `37.5%`, округленно `38%`.

Для Task 4:

```text
(22.7 - 15.2) / 22.7 = 0.330,
```

то есть около `33%`.

Эффект не универсален. В Task 2 OSDAG имеет `MS=22.5 s`, что немного хуже RoCo (`21.9 s`) и TwoStep (`22.0 s`). В Task 1 его `MS=19.1 s` совпадает с RoCo и TwoStep. В Task 3 OSDAG быстрее единственного успешно исполнившего baseline ChatGPT-Prompts (`26.1` против `48.3 s`), но имеет меньший success rate (`80%` против `90%`).

### Ablation study

Table 2 удаляет embeddings, graph или online scheduling (PDF с. 5).

Главные результаты:

- `w/o Graph` дает `SR=0` во всех пяти scenarios;
- `w/o Online Schedule` не меняет makespan Tasks 1-3;
- в Task 4 отключение online scheduling увеличивает `MS` с `15.2` до `22.7 s`, на `49%` относительно OSDAG time;
- в Task 5 отключение online scheduling увеличивает `MS` с `26.0` до `41.6 s`, на `60%` относительно OSDAG time;
- `w/o Embedding` снижает Task 2 success rate с `90%` до `70%` и увеличивает reasoning time с `14.0` до `28.3 s`.

Ablation study подтверждает значение runtime dispatch только для двух из пяти tested scenarios. Для первых трех full OSDAG и `w/o Online Schedule` имеют одинаковый reported makespan.

### Real-world evidence

Real-world demonstration использует UF850 manipulator, Intel RealSense D435, parallel gripper, YOLOv11-seg и человека, получающего scheduled text instructions. Сценарий - совместная сортировка colored cubes по bowls (PDF с. 5-6).

Раздел дает qualitative figure и описание, но не сообщает:

- число trials;
- success rate;
- makespan;
- reasoning time;
- variance или failure count;
- сравнение с baseline.

Поэтому real-world section подтверждает feasibility demonstration, а не численный effect size.

## Неопределенность и ограничения доказательств

### Статистическая неопределенность

Основные simulation values усреднены по 10 trials. PDF не дает standard deviations, standard errors, confidence intervals, hypothesis tests или correction for repeated comparisons. Для `SR` один trial соответствует 10 percentage points, поэтому различия `80%`, `90%` и `100%` при таком `n` имеют существенную sampling uncertainty.

Не описаны power calculation, preregistration, random seeds, distribution task durations и правила агрегации `MS` при неуспешных trials. Поэтому точные средние можно цитировать как reported results, но нельзя объявлять статистически установленное превосходство.

### Признанные авторами ограничения

Conclusion перечисляет три ограничения (PDF с. 5-6):

1. Dependency edges генерирует LLM; ошибки reasoning могут расти с environmental complexity и agent count.
2. Current task-selection policy может не давать globally optimal schedules.
3. Replanning отсутствует; execution failure может каскадно нарушить весь plan.

### Дополнительные ограничения для M0-M4

1. Пять коротких manipulation scenarios не являются fixed software project.
2. Agent count не варьируется систематически при неизменном workload; Task 1 и Task 2 различаются одновременно по `P` и scenario.
3. `RT` и `MS` разделены, поэтому нет полного task duration, сопоставимого с `k`.
4. Нет no-AI или one-human baseline `Z_i X`.
5. Task assignments фиксирует LLM; scheduler не решает online reassignment.
6. Нет duration-aware scheduling и critical-path computation.
7. Нет теоретической lower/upper bound на makespan.
8. Нет throughput experiment или long-run arrival process.
9. Quality представлена short-horizon `SR/SSE`, а maintainability, verification и rework отсутствуют.
10. Real-world evidence qualitative.
11. Точный Gemini Flash checkpoint и inference settings не указаны.
12. Baseline compute/model parity полностью не документирована.
13. Нет supervising human resource и context switching.
14. Система не проверена на coding agents, shared repository, merge conflicts или software acceptance tests.

## Полный mapping `Z,k,r,W,P,L,C(P),h,H,gamma(P)`

Здесь **direct** означает математически близкий измеряемый объект, **conceptual** - сходный механизм без численной совместимости, **mismatch** - близкое название с другой семантикой, **absent** - объект не задан.

| Поле M0-M4 | Статус | Соответствие в OSDAG | Точная граница переноса |
|---|---|---|---|
| `X` | **absent** | Есть absolute seconds execution | Нет базовой единицы human work без AI |
| `Z_i` / `Z` | **absent** | Есть discrete manipulation subtasks и пять scenarios разной сложности | Нет нормированной сложности и no-AI duration `Z_i X` |
| `k_i^(r)` / `k` | **absent** | `RT` и `MS` различаются между системами | Нет ratio полного AI time к matched no-AI baseline; planning и execution time разделены |
| режим `r` | **conceptual** | One-shot LLM decomposition + DAG + online dispatch является system configuration | Это agent-system architecture, не режим developer-agent interaction; нет task-specific `rho(i)` |
| `W = X sum Z_i k_i` | **absent** | DAG содержит задачи с execution durations `p_i` | Сумма `sum p_i` не публикуется и не связывается с baseline или total work bound |
| `P` | **direct count, limited design** | `N` - число heterogeneous agents; Task 1 использует 2, Task 2 - 3 | Нет controlled scaling curve при одном workload; задачи fixed-assigned, агенты неодинаковы |
| M1 / неделимость | **direct structural** | Robot actions являются discrete, non-overlapping per agent в Algorithm 1 | Нет longest-job bound `M_N` и анализа allocation на identical workers |
| DAG | **direct** | `G=(V,E)` из task dependencies | Граф генерирует LLM; assignment также уже зафиксирован |
| `L` | **conceptual, численно absent** | Precedence chains ограничивают возможный параллелизм | Critical-path length не вычисляется, не публикуется и не используется priority rule |
| `C(P)` | **conceptual only** | Повторные LLM calls и dialogue history создают coordination/planning latency; one-shot design ее уменьшает | Нет функции overhead от `P`, total-work multiplier или controlled estimate при fixed workload |
| `a_i^(r)` | **absent** | Robot execution можно считать autonomous phase | Нет нормировки, paired human baseline или decomposition `k=a+h` |
| `h_i^(r)` / `h` | **absent** | В real-world demo человек сам выполняет scheduled manipulation tasks | Он worker, не supervisor; specification/review time не измеряется |
| `H = X sum Z_i h_i` | **absent** | Нет общей очереди human service intervals | Human executor не обслуживает все agents как capacity-1 common resource |
| `gamma(P)` | **absent** | Нет cognitive switching measurement | Agent/robot coordination latency не является human context-switch penalty |
| makespan | **direct** | `C_max=max_i c_i`, reported `MS` | Это execution makespan robot task graph, отдельно от LLM reasoning time и без no-AI speedup |
| throughput | **absent** | Каждый scenario завершается один раз | Нет потоковой нагрузки, arrivals или steady-state output rate |
| quality | **direct, но вне time objective M0-M4** | `SR` и `SSE` | Нельзя свести к duration без заданного acceptance/quality constraint |

### Mapping к уровням M0-M4

| Уровень | Что требует M0-M4 | Что дает OSDAG | Вердикт |
|---|---|---|---|
| M0 | Fixed work `W`, one-stream effect `k`, ideal `W/P` | Набор robot subtasks и execution times | Нет no-AI baseline, `W/P` или speedup identity |
| M1 | Indivisible tasks, assignment и longest-task bound | Discrete tasks и one-at-a-time execution per agent | Структурное соответствие без lower bound; assignment fixed by LLM |
| M2 | Precedence DAG и critical path `L` | Прямой DAG и ready-task dispatch; measured makespan | Наиболее близкий слой, но `L` не вычисляется и Graham guarantee отсутствует |
| M3 | `C(P)` для растущего coordination/integration overhead | One-shot LLM уменьшает planning latency; online dispatch уменьшает idle time | Поддерживает механизм overhead qualitatively, но не параметрическую функцию или shared-code integration |
| M4 | Один developer, `h`, capacity-1 `H`, verification windows, `gamma(P)` | Human supervisor отсутствует; real-world human является worker | M4 не поддерживается |

## Что источник поддерживает для нашей статьи

1. **DAG делает доступный параллелизм явным.** Ready branches можно запускать без ожидания unrelated tasks (PDF с. 2-4).
2. **Execution policy влияет на makespan даже при одном task graph.** Online-dispatch ablation уменьшает Tasks 4-5 с `22.7` до `15.2 s` и с `41.6` до `26.0 s` (PDF с. 5).
3. **Dependency omission может разрушить качество.** В tested scenarios `w/o Graph` дает `SR=0` во всех пяти задачах (PDF с. 5).
4. **Повторные LLM conversations могут доминировать planning latency.** OSDAG с одним call имеет в `5.0-14.7x` меньше reasoning time, чем RoCo, на пяти scenarios (PDF с. 4-5).
5. **Одного числа agents недостаточно.** В Task 2 три агента не дают OSDAG меньший makespan, чем RoCo/TwoStep; структура и policy важнее номинального count (PDF с. 5).
6. **Online dispatch не равен global optimization.** Авторы признают, что earliest-index policy может быть неоптимальной (PDF с. 5-6).
7. **Planning success и execution time нужно измерять раздельно.** Task 3 показывает trade-off: OSDAG быстрее ChatGPT-Prompts по `MS`, но имеет меньший `SR` (PDF с. 5).
8. **Dynamic recovery является отдельным слоем.** Статический DAG плюс online dispatch не устраняет cascading failures без replanning (PDF с. 6).

Пункты 1-4 являются прямым пересказом design/results. Пункты 5 и 7 - сравнительный синтез Table 1. Перенос на software agents остается аналогией.

## Что источник не позволяет утверждать

1. Что OSDAG расшифровывается авторами отдельной буквенной фразой, отличной от title; такой фразы в PDF нет.
2. Что работа peer-reviewed или accepted.
3. Что Algorithm 1 глобально минимизирует makespan.
4. Что дан approximation ratio или Graham-style bound.
5. Что scheduler online выбирает лучшего агента для каждой задачи; `mu_i` фиксирован заранее.
6. Что OSDAG соответствует общему formal online scheduling с неизвестными future jobs.
7. Что makespan уменьшается во всех задачах и относительно всех baselines.
8. Что `5-15x` относится ко всем baselines; это сравнение с RoCo.
9. Что `38%` является средним эффектом; это maximum для Task 5.
10. Что differences statistically significant; uncertainty intervals и tests не опубликованы.
11. Что `RT` входит в reported `MS` или что `RT+MS` анализируется как end-to-end time.
12. Что можно получить `k` из Table 1: нет no-AI denominator и fixed acceptance-adjusted total time.
13. Что agent count причинно определяет latency или makespan: `P` не варьируется при неизменном scenario.
14. Что task graph содержит duration-weighted critical path `L`; paper его не вычисляет.
15. Что dialogue latency или idle time являются функцией `C(P)` M0-M4.
16. Что human-robot demonstration моделирует human supervision нескольких agents.
17. Что источник оценивает `h`, `H` или `gamma(P)`.
18. Что результаты переносятся на coding agents, repository integration и code review.
19. Что real-world experiment количественно подтверждает simulation effect sizes.
20. Что отсутствие graph вообще всегда приводит к failure; это результат пяти конкретных manipulation scenarios.

## Отличие от M0-M4

| Измерение | OSDAG | M0-M4 |
|---|---|---|
| Центральный вопрос | Как one-shot LLM и online DAG dispatch координируют heterogeneous robots | Когда один developer с `P` coding agents сокращает fixed-workload makespan |
| Workload | Одна natural-language instruction, разложенная LLM на manipulation tasks | Заранее фиксированный набор software tasks с baseline complexities `Z_i` |
| Исполнители | Heterogeneous robots; в demo один robot и один human worker | `P` coding agents под контролем одного developer |
| Assignment | `mu_i` генерируется LLM до execution | Assignment/scheduling является частью анализируемой конфигурации |
| Online component | Runtime dispatch ready preassigned tasks по completion/state | Модель задает bounds и требует resource-feasible human-agent schedule |
| Длительности | Absolute robot execution `p_i`; reported `RT` и `MS` | `p_i=k_i^(r) Z_i X`, где one-stream time включает generation, verification и correction |
| DAG | LLM-generated prerequisite graph | Exogenous/project DAG с duration-weighted critical path `L` |
| Objective | Execution `C_max`, `SR`, `SSE`, отдельно `RT` | End-to-end fixed-workload makespan и speedup; quality через acceptance/rework time |
| Scheduling result | Earliest-index heuristic, no bound | Lower bounds M0-M4 и Graham-based sufficient criterion на M1-M2 |
| Coordination | LLM reasoning latency, idle time, object/resource state | Agent integration `C(P)` плюс human switching `gamma(P)` |
| Human | Отсутствует как supervisor; в demo выполняет физические tasks | Capacity-1 developer выполняет specification/review/correction intervals |
| Uncertainty | 10-trial means без intervals | Параметры допускают stochastic extension, но требуют внешней calibration |

OSDAG находится ближе всего к прикладному M2: она демонстрирует dependency-aware list dispatch и измеряет execution makespan. M0-M4 добавляет отсутствующий baseline and estimation layer (`Z,k,r`), fixed-workload bounds (`W,L`), growing agent integration overhead (`C(P)`) и общий human resource (`h,H,gamma(P)`).

## Проверенные claims для Related Work

1. Canh et al. предлагают OSDAG, где LLM один раз строит agent-assigned dependency DAG, после чего lightweight scheduler во время execution запускает готовые задачи у свободных заранее назначенных agents (PDF с. 1-4).
2. Формальная цель записана как минимизация `C_max` при precedence и capability constraints, но Algorithm 1 использует earliest-index dispatch и не сопровождается proof of optimality или approximation bound; conclusion прямо признает возможную global suboptimality (PDF с. 3-6).
3. В пяти PyBullet scenarios по 10 trials OSDAG имела reasoning time `9.1-14.0 s`; заявленный `5-15x` gain относится к RoCo, тогда как ChatGPT-Prompts была быстрее по `RT` во всех пяти задачах (PDF с. 4-5).
4. На Tasks 4-5 OSDAG уменьшила makespan с `22.7` до `15.2 s` и с `41.6` до `26.0 s` относительно reported baselines; в Task 2 ее `22.5 s` немного превышали `21.9/22.0 s` RoCo/TwoStep (PDF с. 5).
5. Ablation без dependency graph провалила все пять scenarios, а замена online dispatch последовательным per-agent execution увеличила makespan только в Tasks 4-5 (PDF с. 5).
6. Работа не моделирует human supervisory attention: real-world human является task executor рядом с одним manipulator, а не common reviewer для нескольких agents (PDF с. 5-6).
7. Source поддерживает application-level роль DAG и dynamic dispatch, но не калибрует `k`, не вычисляет critical path `L`, не задает `C(P)` и не подтверждает M4.

## Рекомендуемое место в статье

Источник лучше вставить в подраздел о современных LLM/multi-agent architectures после Kim et al. и перед переходом к Graham/RCPSP. Его роль - связать эмпирическую литературу multi-agent systems с классическим scheduling core:

- Kim et al. показывают task-architecture alignment преимущественно по success/accuracy;
- OSDAG прямо использует DAG, online dispatch и execution makespan;
- Graham и RCPSP дают классические формальные границы и resource model, которых у OSDAG нет.

Не использовать OSDAG как источник для human-attention subsection или как численную калибровку `k`, `C(P)` и `gamma(P)`.

### Короткий вариант встраивания

> Canh et al. (2026) предложили OSDAG для heterogeneous multi-robot collaboration: LLM один раз генерирует agent-assigned dependency DAG, после чего lightweight scheduler запускает готовые задачи у свободных назначенных исполнителей. В пяти PyBullet scenarios по 10 trials подход сократил reasoning time в `5-15x` относительно dialogue-based RoCo и уменьшил makespan до `38%` в наиболее выгодном сценарии; при этом в одной задаче его makespan был немного выше двух baselines, а uncertainty intervals не публиковались. Формально Algorithm 1 является earliest-index dispatch по заранее известному DAG и фиксированным assignments, не имеет approximation guarantee и, по признанию авторов, может быть глобально неоптимальным. Поэтому работа подтверждает прикладную ценность DAG и dynamic dispatch для M2, но не дает Graham-bound, RCPSP novelty, AI duration factor `k` или модель последовательного human attention `H`.

### Вариант для discussion о границе “online”

> Термин online требует различать planning и dispatch. В OSDAG весь task set, DAG и назначения agents формируются до execution; online является только реакция на completion и текущий resource state. Такая схема ближе к runtime list dispatch по заранее известному графу, чем к online scheduling с неизвестными future jobs, и не включает reassignment или replanning после failure.

### Предлагаемая BibTeX-запись

```bibtex
@misc{canh2026osdag,
  author        = {Canh, Thanh Nguyen and Viet, Thang Tran and Van Dinh, Phuc and HoangVan, Xiem and Chong, Nak Young},
  title         = {{OSDAG}: Online Scheduling for Efficient Multi-Robot Collaboration},
  year          = {2026},
  eprint        = {2606.15255},
  archiveprefix = {arXiv},
  primaryclass  = {cs.RO},
  doi           = {10.48550/arXiv.2606.15255},
  url           = {https://arxiv.org/abs/2606.15255},
  note          = {Version 1, submitted 13 June 2026}
}
```

## Таблица опорных страниц

| PDF-страница | Раздел / объект | Опорное содержание | Статус свидетельства |
|---:|---|---|---|
| 1 | Title; Abstract; Introduction | Точное название, авторы, arXiv v1/date; one-shot LLM; DAG; online scheduling; headline `5-15x` и `38%`; критика repeated inference/offline plan | Метаданные и claims авторов |
| 2 | Fig. 1; Contributions; Problem Statement | Три стадии OSDAG; contributions; heterogeneous agents, reachability, action sets, objects | Прямая system/problem formulation |
| 3 | Equations (3)-(17); Sections 2.2-2.4 | Task tuple с fixed `mu_i`; objective `min C_max`; validation; DAG; topological sort; completed/running sets; per-agent ready set | Прямая formalization и основа online/offline qualification |
| 4 | Algorithm 1; Experimental Setup; beginning of Results | Earliest-index dispatch; `Free/Busy`; `Delta t`; five scenarios; metrics; baselines; reported reasoning and makespan interpretation | Алгоритм и evaluation design |
| 5 | Tables 1-2; Ablation; Real-World; Conclusion | Полные numerical results; 10 trials; ablations; UF850+human demonstration; headline comparisons; lack of global optimality и replanning | Основная evidence page |
| 6 | Conclusion continuation; References | Ошибки dependency generation с ростом complexity/agent count; cascading failures; отсутствие recovery; publication context | Ограничения и статус corpus |

## Итоговая оценка релевантности

OSDAG является полезным современным источником для мостика между LLM-based multi-agent coordination и классической теорией расписаний. Работа прямо использует dependency DAG, ready-task dispatch и execution makespan и показывает на пяти небольших manipulation scenarios, что runtime dispatch может сокращать idle time и makespan относительно sequential pre-allocation.

Доказательная сила ограничена свежим arXiv v1, десятью trials на scenario без uncertainty intervals, отсутствием systematic agent-count scaling и количественного real-world comparison. Algorithm 1 не решает общий optimization problem: assignments фиксированы LLM заранее, priority равен task index, optimality и approximation bounds отсутствуют, а replanning не поддерживается.

Для M0-M4 источник дает прямую прикладную опору только DAG/makespan слою M2 и качественную мотивацию отделять planning overhead от execution. Он не является источником для no-AI effect `k`, total work `W`, critical-path bound `L`, coordination multiplier `C(P)` или human bottleneck `h,H,gamma(P)`. Корректное позиционирование: OSDAG демонстрирует специализированную робототехническую реализацию one-shot LLM decomposition и runtime DAG dispatch; M0-M4 ставит другой вопрос о fixed software workload, baseline speedup и capacity-1 developer, опираясь на классические Graham/RCPSP конструкции для формальных границ.
