# Pinedo (2008): учебниковый контекст для fixed-workload makespan M0--M4

## Назначение и границы обзора

Этот документ разбирает один источник применительно к статье о makespan фиксированного набора связанных задач в конфигурации «один разработчик -- `P` кодовых ИИ-агентов». Pinedo используется как учебниковый источник стандартной теории расписаний, а не как эмпирическое или теоретическое исследование ИИ.

Проверена локальная копия `/Users/rexarrior/work/articles/simple_model_full/literature/pinedo2008.pdf`, 662 PDF-страницы. Это именно **третье издание 2008 года**. Сначала были просмотрены титульные страницы, оглавление и предметный индекс, после чего выборочно прочитаны разделы о нотации, одинаковых параллельных машинах, `C_max`, precedence constraints, critical path, LPT/LIST, deterministic/stochastic models и упоминаниях resource-constrained scheduling. PDF целиком не извлекался. В локальном файле печатная страница 1 главы 1 продублирована на PDF-страницах 15 и 16, поэтому единого постоянного смещения пагинации нет; ниже всегда указаны оба номера.

Разведение эпистемических статусов строгое:

- **direct**: тот же математический объект или результат непосредственно присутствует в scheduling-постановке источника;
- **analogy**: сходна структурная роль, но семантика M0--M4 или требуемая параметризация добавляется извне;
- **absent**: механизм в собственной модели источника отсутствует.

## Библиография и статус

**Проверенная ссылка:** Michael L. Pinedo. *Scheduling: Theory, Algorithms, and Systems*. Third Edition. Springer Science+Business Media, LLC, 2008. ISBN `978-0-387-78934-7`; e-ISBN `978-0-387-78935-4`; DOI: [10.1007/978-0-387-78935-4](https://doi.org/10.1007/978-0-387-78935-4) (PDF 1--2; титульный лист и оборот титула).

**Статус:** научный учебник/монография по теории и практике расписаний. Это не журнальная статья и не первичное эмпирическое исследование. Локальный PDF не описывает процедуру внешнего рецензирования, поэтому отдельное утверждение о peer review не делается.

**Редакция:** предисловие прямо озаглавлено `Preface to the Third Edition` и датировано `Spring 2008`; оно сообщает о добавлении, среди прочего, online scheduling в главу о параллельных машинах (PDF 6--7 / печ. pp. ix--x). Метаданные шестого издания 2022 года, включая другой DOI и ISBN, к этой копии не относятся и здесь не используются.

## Вопрос и вклад источника

### Вопрос

Pinedo определяет scheduling как распределение ресурсов между задачами во времени с целью оптимизации одного или нескольких критериев. Ресурсами могут быть машины, экипажи или вычислительные устройства, а задачами -- производственные операции, этапы проекта или исполнения программ; одним из возможных критериев прямо названо время завершения последней задачи (PDF 15--16 / печ. p. 1).

Книга в целом систематизирует deterministic и stochastic machine scheduling, алгоритмы, оценки сложности и практические scheduling systems. Для M0--M4 релевантен более узкий учебниковый вклад:

1. стандартная трёхпольная нотация `alpha | beta | gamma`;
2. определение identical parallel machines `P_m`, precedence constraints `prec` и makespan `C_max`;
3. классические постановки `P_m || C_max`, `P_m | prec | C_max` и `P_infinity | prec | C_max`;
4. critical-path reasoning, LPT и list-based scheduling;
5. явное различие deterministic и stochastic models.

Источник не ставит вопрос об ускорении относительно baseline одного разработчика и не исследует человеко-агентную ячейку.

## Постановка и метод

### Учебниковая постановка

В deterministic framework число работ `n` и машин `m` конечно; работе `j` приписываются processing time `p_ij` или `p_j`, release date `r_j`, due date `d_j` и weight `w_j` (PDF 27--28 / печ. pp. 13--14). Scheduling problem записывается как

```text
alpha | beta | gamma,
```

где `alpha` задаёт machine environment, `beta` -- характеристики обработки и ограничения, а `gamma` -- минимизируемый objective (PDF 28 / печ. p. 14).

Для identical parallel machines обозначение `P_m` означает `m` одинаковых машин; каждая работа требует одну операцию и может выполняться на любой допустимой машине (PDF 28 / печ. p. 14). В главе 5 базовая nonpreemptive постановка `P_m || C_max` интерпретируется как балансировка нагрузки между параллельными машинами; решение включает назначение работ машинам, а при makespan objective порядок независимых работ внутри одной машины значения не имеет (PDF 123--124 / печ. pp. 111--112).

### Fixed workload и известность данных

В детерминированной части задано конечное множество работ с известными параметрами. Глава 5 дополнительно называет такую постановку offline scheduling: processing times, release dates и due dates известны заранее и могут учитываться при оптимизации (PDF 124, 150--151 / печ. pp. 112, 138--139). Это совместимо с fixed-workload instance M0--M4.

Однако Pinedo не определяет fixed-workload **сравнение конфигураций** относительно baseline без ИИ. Из книги следует, как оптимизировать расписание заданных `p_j`; из неё не следует, как значения `p_j` меняются при переходе от человека к ИИ, от одного режима к другому или от одного `P` к другому.

### Метод книги

Это синтетическое теоретико-учебное изложение. Используются классификация задач, конструктивные алгоритмы, proofs of optimality, complexity results, worst-case/competitive ratios и численные примеры. Эмпирической выборки разработчиков, агентов или проектов нет.

## Релевантные определения и результаты

### 1. Makespan `C_max`

**Direct.** Completion time работы обозначается `C_j`. Makespan определяется как

```text
C_max = max(C_1, ..., C_n),
```

то есть время завершения последней работы; его минимизация обычно способствует хорошей загрузке машин (PDF 32 / печ. p. 18). Это тот же тип objective, что makespan в M0--M4.

Книга при этом не отождествляет makespan с effort. Сумма processing times задаёт работу системы, но срок определяется расписанием, machine capacity и ограничениями.

### 2. Identical parallel machines и неделимость

**Direct для M1 после задания длительностей.** `P_m || C_max` состоит из `n` работ на `m` одинаковых параллельных машинах без указанного `prmp`, то есть без разрешённых прерываний. В терминах M1 нужно внешне положить

```text
m = P,
p_i = Z_i k_i^(r) X.
```

После этой подстановки scheduling core совпадает: неделимые работы назначаются одинаковым исполнителям, а objective равен `C_max`. Но разложение `p_i` на `Z_i`, `k_i^(r)` и `X` принадлежит M0--M4, а не Pinedo.

Постановка уже вычислительно нетривиальна: `P_2 || C_max` названа NP-hard в ordinary sense через эквивалентность PARTITION (PDF 124 / печ. p. 112).

### 3. Workload bounds и граница M1

**Direct на уровне scheduling quantities, с оговоркой о достижимости.** В доказательстве LPT guarantee используется стандартная нижняя граница оптимума

```text
C_max(OPT) >= (sum_j p_j) / m
```

(PDF 125 / печ. p. 113). Самая длинная работа также не может завершиться быстрее собственного `p_1`, если `p_1 >= ... >= p_n`. В разделе с разрешёнными прерываниями эти две границы объединены в Lemma 5.2.2:

```text
C_max >= max{p_1, (sum_j p_j)/m},
```

и для `P_m | prmp | C_max` последующий алгоритм достигает этой величины (PDF 136 / печ. p. 124).

Для nonpreemptive M1 то же выражение остаётся нижней границей, но равенство в общем случае не гарантировано. Поэтому при `p_i = Z_i k_i^(r) X`, `W = sum_i p_i` и `m=P` источник поддерживает смысл

```text
B_1 = max{W/P, max_i p_i}
```

как lower bound, но не формулу точного makespan. Точное равенство `T=W/P` уровня M0 является идеализацией делимости M0, а не результатом Pinedo для `P_m || C_max`.

### 4. Precedence constraints и стандартная нотация M2

**Direct.** Entry `prec` в поле `beta` означает, что одна или несколько работ должны завершиться до начала другой; отдельно определены chains, intrees и outtrees (PDF 30 / печ. p. 16). Следовательно, после задания длительностей уровень M2 естественно относится к классу

```text
P_m | prec | C_max,
```

с `m=P`.

При неограниченном числе параллельных ресурсов книга записывает project scheduling problem как `P_infinity | prec | C_max`: нужно минимизировать полное время проекта, а классическими методами названы CPM и PERT (PDF 35 / печ. p. 21). Algorithm 5.1.3 запускает каждую работу сразу после завершения всех её предшественников и является оптимальным для этой unlimited-machine постановки (PDF 127 / печ. p. 115). Critical jobs определяются совпадением earliest и latest possible start times; они образуют critical path (PDF 127--129 / печ. pp. 115--117).

Для конечного `m`, `2 <= m < n`, общая задача `P_m | prec | C_max` названа strongly NP-hard (PDF 129 / печ. p. 117). Это поддерживает тезис M2, что `max{W/P,L}` является лишь lower bound, а построение оптимального расписания нетривиально.

Комбинированная формула

```text
T >= max{W/P, L}
```

в таком обозначении на проверенных страницах не напечатана. Её ветви являются стандартными capacity и critical-path bounds, но объединение и AI-adjusted weights `Z_i k_i^(r) X` вносит M0--M4.

### 5. LPT и list scheduling

**Direct, но только при соблюдении разных областей применимости.** Для независимых работ `P_m || C_max` LPT назначает в момент 0 `m` самых длинных работ, а затем при освобождении машины запускает самую длинную из ещё не начатых (PDF 124 / печ. p. 112). Theorem 5.1.1 даёт

```text
C_max(LPT) / C_max(OPT) <= 4/3 - 1/(3m)
```

(PDF 125 / печ. p. 113). Это approximation guarantee относительно оптимального makespan, а не относительно lower bound `max{sum p_j/m, p_1}` и не относительно baseline без ИИ.

Для произвольного статического priority list без precedence constraints книга приводит более слабую worst-case границу

```text
C_max(LIST) / C_max(OPT) <= 2 - 1/m
```

(PDF 126 / печ. p. 114). Отдельно в online section алгоритм `LIST` назначает следующую предъявленную работу каждой освободившейся машине и имеет competitive ratio `2-1/m` (Theorem 5.6.1; PDF 151--152 / печ. pp. 139--140). Совпадение констант не делает offline worst-case guarantee и online competitive result одним утверждением.

При precedence constraints Pinedo рассматривает critical-path и largest-number-of-successors priority rules, а также специальные tree cases (PDF 129--132 / печ. pp. 117--120). На проверенных страницах книга не формулирует используемую в M2 аддитивную гарантию Graham

```text
C_LS <= W/P + (1 - 1/P)L.
```

Поэтому Pinedo (2008) подходит для учебникового контекста list scheduling и LPT, но прямой первичный источник точной precedence-aware границы должен оставаться Graham (1966).

### 6. Deterministic и stochastic scheduling

**Direct как классификационное различие.** В deterministic part предполагается конечный набор работ, а глава 5 в основном использует offline data, известные заранее (PDF 22, 124 / печ. pp. 7, 112). В stochastic part distributions processing times, release dates и due dates считаются известными в момент 0, но их фактические realizations становятся известны только при завершении обработки или наступлении события; случайные величины обозначаются заглавными буквами, например `X_ij` (PDF 251--252 / печ. pp. 243--244).

Книга также рассматривает expected makespan на stochastic parallel machines, но результаты зависят от класса distributions и policies. Например, для двух машин и exponentially distributed processing times LEPT минимизирует expected makespan только в классе nonpreemptive static list policies (PDF 326 / печ. p. 321). Это показывает, что переход от детерминированных `k_i` к случайным величинам нельзя свести к механической замене на средние без проверки условий.

Текущая M0--M4 является deterministic model с замечанием о возможном стохастическом расширении. Pinedo поддерживает необходимость такого разведения, но не доказывает конкретный критерий M0 в ожиданиях для AI-derived `k_i`.

### 7. Resource constraints: присутствуют только на границе охвата

На печатной странице 21 книга прямо перечисляет `personnel scheduling` и `resource constrained scheduling` среди scheduling features, не охваченных изложенным framework (PDF 35 / печ. p. 21). В обзорных комментариях также указан отдельный труд *Scheduling under Resource Constraints*, но собственная reusable-capacity модель RCPSP в релевантных главах книги не развита (PDF 24 / печ. p. 9; PDF 619 / references p. 626).

Следовательно, Pinedo (2008) нельзя использовать как прямое основание для утверждения, что человеческое внимание является renewable resource capacity 1, или для feasibility constraint, запрещающего перекрытие human intervals. Для этого нужны источники по RCPSP или parallel machines with a common/single server. В Pinedo прямыми остаются `P_m`, `prec` и `C_max`; общий человеческий ресурс M4 отсутствует.

## Mapping к параметрам M0--M4

| Параметр статьи | Статус | Соответствие у Pinedo (2008) | Граница переноса |
|---|---|---|---|
| `Z` / `Z_i` | **absent** | Есть processing time `p_i`, но нет нормированной baseline complexity и единицы `X` | `Z_i X` задаётся вне scheduling model; `p_i` уже является длительностью |
| `k` / `k_i^(r)` | **absent** | Длительности могут различаться между работами | Нет коэффициента изменения времени из-за ИИ, однопоточной калибровки и сравнения с baseline без ИИ |
| `r` | **absent** | В книге `r_j` означает release date, а не режим | Нет interactive/delegated/autonomous mode и task-specific назначения режимов |
| `P` | **direct** | `m` в environment `P_m`, целое число identical parallel machines | Соответствие действует после абстрагирования агентов как одинаковых исполнителей; вещественный effective `P` M0 книгой не задаётся |
| `W` | **direct** на scheduling level | `sum_j p_j`, total processing requirement, и capacity bound `sum_j p_j/m` | Равенство `W=X sum Z_i k_i^(r)` и AI-семантика составляющих отсутствуют; `W/P` обычно lower bound, не точный makespan |
| `L` | **direct** | Длина critical path в precedence project определяет unlimited-machine project duration и lower bound для finite machines | AI-adjusted node weights задаются M0--M4; символ `L` в книге также может использоваться для иных величин, поэтому нужен контекст |
| `C(P)` | **absent** | Есть setup times и иные фиксированные ограничения отдельных scheduling models | Нет глобального agent-agent integration multiplier, зависящего от числа параллельных агентов |
| `h` / `h_i` | **absent** | Отдельной human share processing time нет | Нельзя выводить разложение `k_i=a_i+h_i` из machine processing time |
| `H` | **absent** | Нет суммы последовательных human intervals | Книга не задаёт capacity-1 human resource в рассматриваемой постановке |
| `gamma(P)` | **absent** | Нет cognitive context-switching penalty | Online decisions, preemptions и machine setups не эквивалентны переключению внимания разработчика |
| makespan | **direct** | `C_max=max_j C_j`, центральный objective глав 4--8 и 12 | Нет speedup `T_h/T_ai` и baseline одного разработчика без ИИ |

## Что источник поддерживает

1. **Стандартное позиционирование M1.** После внешнего задания `p_i=Z_i k_i^(r)X` независимые неделимые задачи на `P` одинаковых агентах имеют ядро `P_m || C_max` при `m=P` (PDF 28, 124 / печ. pp. 14, 112).
2. **Стандартное позиционирование M2.** DAG constraints соответствуют `prec`, а objective -- `C_max`; critical path является прямым scheduling object, а finite-machine problem существенно сложнее unlimited-machine project scheduling (PDF 30, 127--129 / печ. pp. 16, 115--117).
3. **Различие work и makespan.** `sum p_j/m` является capacity lower bound; неделимость и зависимости могут сделать срок больше. Поэтому `W/P` нельзя автоматически считать достижимым (PDF 125, 136 / печ. pp. 113, 124).
4. **Алгоритмический контекст.** LPT имеет гарантию `4/3-1/(3P)` относительно оптимума для независимых deterministic jobs; arbitrary list и online LIST имеют отдельные bounds (PDF 124--126, 151--152 / печ. pp. 112--114, 139--140).
5. **Необходимость разделять deterministic и stochastic claims.** Известные длительности, известные distributions и фактические realizations образуют разные постановки и требуют разных policies/results (PDF 251--252, 326 / печ. pp. 243--244, 321).

## Что источник не позволяет утверждать

- Что Pinedo (2008) исследует кодовых ИИ-агентов, разработчиков или режимы человеко-агентного взаимодействия.
- Что книга определяет или эмпирически валидирует `Z_i`, `k_i^(r)`, `h_i`, `C(P)` либо `gamma(P)`.
- Что `T=W/P` является точным makespan для nonpreemptive `P_m || C_max`; это capacity lower bound, а точность требует дополнительной идеализации или специальной preemptive постановки.
- Что lower bound `max{W/P,L}` всегда достижим на конечном числе исполнителей.
- Что LPT guarantee `4/3-1/(3P)` применима к задачам с precedence constraints, shared human resource, coordination overhead или stochastic durations.
- Что online LIST theorem является доказательством offline precedence-aware bound Graham.
- Что общий последовательный человеческий ресурс отсутствует во всей scheduling literature. Книга лишь не развивает его в проверенной machine-scheduling постановке и сама указывает resource-constrained scheduling как отдельный класс.
- Что stochastic treatment книги обосновывает замену каждого AI-specific `k_i` только его средним без анализа distributions, information structure и policy class.
- Что источник даёт speedup относительно последовательного baseline без ИИ или оптимальное число агентов.

## Отличие от M0--M4

| Измерение | Pinedo (2008) | M0--M4 |
|---|---|---|
| Исследовательский вопрос | Как классифицировать и решать scheduling problems при заданных jobs, resources, constraints и objectives | Когда fixed workload одного разработчика выполняется быстрее с `P>1` кодовыми ИИ-агентами |
| Длительность работы | Primitive `p_j` или random variable `X_j` | `p_i=Z_i k_i^(r)X`, где AI effect зависит от задачи и режима |
| Baseline | Не требуется для `C_max` optimization | Последовательное время без ИИ `T_h=X sum Z_i` |
| M0 | Capacity expression `sum p_j/m` служит lower bound | `W/P` постулируется точным при идеальной делимости |
| M1 | `P_m || C_max`, nonpreemptive independent jobs | Та же scheduling core после AI-specific parameterization |
| M2 | `P_m | prec | C_max`; `P_infinity | prec | C_max`, CPM/PERT и critical path | DAG с весами `Z_i k_i^(r)X`, lower bound `max{W/P,L}` и speedup criterion |
| M3 | Нет общего endogenous multiplier от числа исполнителей | `C(P)W/P` моделирует agent-agent integration overhead |
| M4 | Capacity-1 human resource в релевантной постановке не задан | `h_i`, `H`, `gamma(P)H` и непересекающиеся human intervals |
| Алгоритмический результат | Optimality, complexity и approximation/competitive guarantees для конкретных scheduling classes | Нижние границы и критерии ускорения полной человеко-агентной конфигурации |
| Стохастика | Отдельные random processing times, distributions и policy classes | Пока deterministic core; stochastic `k_i` только намечен как расширение |

M1--M2 не являются новыми классами scheduling problems: их ядро стандартно после того, как длительности уже заданы. Отличительный объект M0--M4 возникает раньше и позже scheduling core. Раньше -- через построение длительности из baseline complexity, AI effect и режима. Позже -- через добавление topology-specific `C(P)`, человеческой доли, capacity-1 attention и switching penalty, а также через сравнение с baseline без ИИ.

## Проверенные тезисы для синтеза Related Work

1. **Прямой результат:** Pinedo определяет `C_max`, identical parallel machines `P_m` и precedence entry `prec`; поэтому M1 и M2 после задания `p_i=Z_i k_i^(r)X` относятся к стандартным классам `P_m || C_max` и `P_m | prec | C_max` (PDF 28, 30, 32 / печ. pp. 14, 16, 18).
2. **Прямой результат с ограниченной областью:** для независимых deterministic jobs LPT удовлетворяет `C_max(LPT)/C_max(OPT) <= 4/3-1/(3m)`, тогда как arbitrary list и online LIST имеют отдельную границу `2-1/m`; эти результаты нельзя переносить на M3--M4 (PDF 124--126, 151--152 / печ. pp. 112--114, 139--140).
3. **Структурный синтез:** `sum p_j/m` и critical path дают две классические причины, по которым makespan ограничен снизу. После внешней AI-параметризации они становятся ветвями `W/P` и `L`, но формула M0--M4 и её speedup interpretation не являются цитатой из учебника.
4. **Граница вклада:** Pinedo поддерживает scheduling language M1--M2, но не механизмы M3--M4. Новизну статьи следует связывать не с `C_max`, DAG или LPT, а с совместной связью baseline `Z`, task/mode-specific `k` и `r`, AI-adjusted workload, agent overhead и последовательного человеческого ресурса в fixed-workload сравнении.

## Короткое встраивание в Related Work

> В стандартной нотации теории расписаний makespan определяется как `C_max=max_j C_j`, а `P_m` обозначает `m` одинаковых параллельных машин; precedence constraints кодируются entry `prec` (Pinedo, 2008, PDF 28, 30, 32 / pp. 14, 16, 18). Поэтому после задания длительностей `p_i=Z_i k_i^(r)X` уровни M1 и M2 имеют классическое ядро `P_m || C_max` и `P_m | prec | C_max` при `m=P`. Capacity bound `sum_i p_i/P` и critical path ограничивают достижимый makespan, а для независимых работ LPT имеет гарантию `4/3-1/(3P)` относительно оптимума (PDF 124--129 / pp. 112--117). Это прямой scheduling-контекст, но не модель человеко-агентной производительности: baseline complexity, AI-specific duration factor и режим, `C(P)`, человеческая доля `h`, суммарное время `H` и switching penalty `gamma(P)` в источнике отсутствуют.

## Таблица опорных страниц

| Содержание | PDF-страницы | Печатные страницы | Статус свидетельства |
|---|---:|---:|---|
| Третье издание, 2008; ISBN, e-ISBN и DOI | 1--2 | Титул/оборот титула | Библиографические данные локальной копии |
| `Preface to the Third Edition` | 6--7 | ix--x | Прямое подтверждение редакции; не 2022 |
| Scheduling как allocation of resources to tasks over time | 15--16 | 1 | Определение предмета; p. 1 продублирована в PDF |
| Framework `alpha | beta | gamma`; identical machines `P_m` | 27--28 | 13--14 | Стандартная deterministic notation |
| Precedence constraints `prec` | 30 | 16 | Прямое определение ограничения |
| Makespan `C_max=max(C_1,...,C_n)` | 32 | 18 | Прямое определение objective |
| `P_infinity | prec | C_max`, CPM/PERT; упоминание resource-constrained scheduling вне framework | 35 | 21 | Project/critical-path context и граница охвата ресурсов |
| `P_m || C_max`, LPT definition и NP-hardness `P_2 || C_max` | 124 | 112 | M1 и алгоритмический контекст |
| LPT guarantee `4/3-1/(3m)` и workload lower bound | 125 | 113 | Theorem 5.1.1 и его proof |
| Arbitrary offline list bound `2-1/m` | 126 | 114 | Worst-case result без precedence constraints |
| `P_infinity | prec | C_max`, optimal project algorithm | 127 | 115 | Unlimited-resource project scheduling |
| Critical path и slack | 128--129 | 116--117 | Прямой critical-path construction |
| Strong NP-hardness `P_m | prec | C_max` при `2<=m<n` | 129 | 117 | Complexity finite-machine M2 |
| Exact `max{p_1,sum p_j/m}` для preemptive identical machines | 136 | 124 | Lemma 5.2.2; не exact result для nonpreemptive M1 |
| Online LIST и competitive ratio `2-1/m` | 151--152 | 139--140 | Theorem 5.6.1; не offline precedence result |
| Stochastic framework: distributions known, realizations revealed later | 251--252 | 243--244 | Deterministic/stochastic distinction |
| LEPT и expected makespan для специального stochastic case | 326 | 321 | Theorem 12.1.2; distribution- и policy-specific result |

## Итоговая оценка источника

Pinedo (2008) является сильным учебниковым якорем для языка и границ классической scheduling части статьи. Он прямо подтверждает `P_m`, `prec`, `C_max`, critical path, workload lower bounds, LPT/list scheduling и разделение deterministic/stochastic models. Его доказательная сила заканчивается там, где длительности должны быть выведены из процесса применения ИИ и где появляется один разработчик как особый ресурс. Поэтому корректная роль источника -- показать, что M1--M2 опираются на стандартное scheduling core, одновременно ясно отделив собственные механизмы M0, M3 и M4 от результатов учебника.
