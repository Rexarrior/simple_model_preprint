# Akinrele et al. (2026): taxonomy когнитивных пробелов generative и agentic AI

## Назначение и границы обзора

Этот документ разбирает локальный PDF применительно к модели M0-M4 для
fixed-workload makespan звезды «один разработчик - `P` coding agents».

Главная терминологическая граница: работа изучает не когнитивные пробелы
разработчиков и не потерю понимания кода при использовании AI. Под *cognitive
capability gaps* авторы понимают недостающие или фрагментарные способности
самих generative и agentic AI систем: устойчивое состояние и память,
долговременные цели, самоконтроль, взаимодействие со средой и адаптивное
обучение. Это taxonomy-driven narrative survey и концептуальная архитектурная
работа, а не эксперимент с людьми, coding agents или параллельным расписанием.

Источник полезен для M0-M4 как описание механизмов, из-за которых автономный
агент может требовать дополнительного контекста, проверки, вмешательства и
повторной работы. Эти механизмы могут влиять на mode-specific `k_i^(r)` и
человеческую долю `h_i^(r)`, но работа не измеряет время и не калибрует ни один
параметр модели. В частности, она не исследует одного человека с несколькими
одновременно работающими агентами и не даёт evidence для `gamma(P)`.

Локальный файл содержит 15 PDF-страниц; номера ниже относятся к этой локальной
копии и совпадают с видимой нумерацией документа.

## Библиография, версия и статус

**Название:** “A Taxonomy of Cognitive Capability Gaps in Generative and
Agentic AI”.

**Авторы:** Taye Akinrele, Sindhuja Penchala, Noorbakhsh Amiri Golilarz, Sudip
Mittal, Shahram Rahimi. Все авторы на титульной странице аффилированы с
Department of Computer Science, The University of Alabama, Tuscaloosa, USA
(PDF 1).

**Проверенная ссылка:** Taye Akinrele, Sindhuja Penchala, Noorbakhsh Amiri
Golilarz, Sudip Mittal, and Shahram Rahimi. “A Taxonomy of Cognitive Capability
Gaps in Generative and Agentic AI.” arXiv:2608.02553v1 [cs.AI], 2026.
[https://arxiv.org/abs/2608.02553v1](https://arxiv.org/abs/2608.02553v1).
DOI resolver: [10.48550/arXiv.2608.02553](https://doi.org/10.48550/arXiv.2608.02553).

**Версия:** `arXiv:2608.02553v1`, подана 3 августа 2026 года в основной
категории `cs.AI`. На момент проверки 4 августа 2026 года submission history
содержит только `v1`. arXiv указывает `15 pages, 4 figures`.

**Статус:** arXiv preprint. На arXiv и в PDF нет сведений о принятии в журнал
или конференцию. Источник нельзя называть peer-reviewed или опубликованной
рецензируемой статьёй. Страница arXiv помечает arXiv-issued DOI через DataCite
как ожидающий регистрации; устойчивым идентификатором версии остаётся
`arXiv:2608.02553v1`.

**Проверка первичного PDF:** SHA-256 локального файла
`cognitive_gaps2026.pdf` равен
`91e4fe12b00f2049bc07f882004491c40c4dfb24d1b94793edbbe4be062f2bcb` и
совпадает с SHA-256 ответа `https://arxiv.org/pdf/2608.02553v1`. Следовательно,
обзор относится именно к первичному PDF arXiv v1, а не к файлу, определённому
по локальному имени.

### Предлагаемая BibTeX-запись

```bibtex
@misc{akinrele2026cognitive,
  author        = {Akinrele, Taye and Penchala, Sindhuja and Amiri Golilarz, Noorbakhsh and Mittal, Sudip and Rahimi, Shahram},
  title         = {A Taxonomy of Cognitive Capability Gaps in Generative and Agentic {AI}},
  year          = {2026},
  eprint        = {2608.02553},
  archiveprefix = {arXiv},
  primaryclass  = {cs.AI},
  doi           = {10.48550/arXiv.2608.02553},
  url           = {https://arxiv.org/abs/2608.02553v1},
  note          = {arXiv:2608.02553v1, submitted 3 August 2026}
}
```

## Фактический объект и смысл cognitive gaps

Объект работы - современная литература о generative AI, agentic AI и
предлагаемом авторами следующем уровне, *Cognitive AI*. Авторы противопоставляют
короткогоризонтное генерирование или выполнение задачи устойчивому поведению,
для которого система должна хранить и пересматривать состояние, поддерживать
цели, контролировать собственное рассуждение, учитывать среду и учиться после
развёртывания (PDF 1-4).

Термин *gap* обозначает разрыв между этим желаемым набором когнитивных
способностей и фактическими свойствами нынешних систем. Он не обозначает:

- пробелы в знаниях или навыках разработчика;
- разрыв общего контекста между человеком и агентом;
- ухудшение понимания человеком сгенерированного кода;
- context-switch cost при обслуживании нескольких агентов;
- разницу производительности между AI и no-AI workflow.

Пять верхнеуровневых групп gap (PDF 4-8):

1. **Persistent State Modeling:** persistent memory, state revision, latent
   state modeling.
2. **Goal-Directed Autonomy:** goal formulation, planning and adaptation, goal
   persistence.
3. **Self-Monitoring and Control:** metacognitive monitoring, uncertainty/OOD
   detection, abstention and control decisions.
4. **Environment Interaction:** world modeling, tool-augmented reasoning,
   environment feedback loops.
5. **Learning and Adaptation:** policy adaptation, continual learning, safe
   knowledge updates.

## Исследовательский вопрос

Нумерованного research question в PDF нет. Из abstract, introduction,
contributions и Section III основной вопрос корректно восстанавливается так:

> Какие повторяющиеся когнитивные ограничения современных generative и
> agentic AI препятствуют устойчивому, адаптивному и саморегулируемому
> поведению на длинном горизонте, как организовать эти ограничения в единую
> taxonomy и какие архитектурные и оценочные направления следуют из неё?

Вспомогательные вопросы работы:

1. Какие недостатки повторяются в литературе о памяти, целях, метакогниции,
   grounding, tool use и continual learning?
2. Какие существующие подходы частично закрывают каждый недостаток и что
   остаётся нерешённым?
3. Как связать пять групп в концептуальной Adaptive Cognitive Intelligence
   Architecture (ACIA)?
4. Почему task-level benchmarks недостаточны и какие longitudinal cognitive
   properties следует оценивать?

Это не вопрос о том, при каком `P` сокращается makespan, и не вопрос о
производительности coding agents.

## Дизайн обзора, corpus и метод

### Заявленный метод

Авторы прямо называют метод **narrative synthesis**. Литература организована не
по model family или application domain, а по cognitive capabilities и
operational behavior. Заявленный охват включает cognitive architectures,
foundation models, agentic AI, memory systems, reasoning/planning,
metacognition, environment interaction, world modeling и continual learning
(PDF 3-4).

Пять измерений, по словам авторов, «emerged across the surveyed literature».
Далее для каждого измерения описываются objective, representative approaches и
остающийся gap; результат сведён в taxonomy Table II (PDF 4-8).

### Corpus и sample

Эмпирической выборки людей, задач, моделей, agent runs или production systems
нет. Библиография содержит 106 нумерованных источников `[1]-[106]`, но сама
статья не определяет эти 106 позиций как формально отобранную review sample.

Не сообщены:

- библиографические базы и поисковые системы;
- search strings и дата поиска;
- временной диапазон публикаций;
- inclusion/exclusion criteria;
- число найденных, удалённых как дубли, screened и excluded работ;
- процедура независимого screening или data extraction;
- оценка качества, risk of bias или strength of evidence;
- protocol registration, PRISMA flow или systematic-review checklist.

В списке литературы смешаны peer-reviewed статьи, обзоры, arXiv и Authorea
preprints. Статус источников не используется для взвешивания выводов. Поэтому
работу следует называть narrative taxonomy-driven survey, а не systematic
review, scoping review с воспроизводимым поиском или meta-analysis.

## Основные результаты taxonomy

| Измерение | Сформулированный gap | Значение для надёжности | Evidence в PDF |
|---|---|---|---:|
| Persistent State Modeling | Память остаётся преимущественно внешней; belief updates плохо распространяются; persistent latent state между взаимодействиями отсутствует | Система теряет или повторно запрашивает контекст, противоречиво пересматривает состояние и плохо поддерживает long-horizon task | 4-5, Table II на 8 |
| Goal-Directed Autonomy | Цели в основном задаются извне; planning хрупок и дорог; сохраняется goal drift | Автономное выполнение короткой инструкции не доказывает устойчивого следования цели | 5-6, Table II на 8 |
| Self-Monitoring and Control | Self-correction хрупка; confidence плохо калибрована; abstention не переносится устойчиво между доменами | Fluent output нельзя принимать как надёжный сигнал корректности; нужны внешняя verification и control gates | 6-7, Table II на 8 |
| Environment Interaction | World models нестабильны; tool use слабо связан с reasoning; feedback может закреплять ошибку | Tool access сам по себе не обеспечивает правильный выбор инструмента, обновление состояния и recovery после failure | 7, Table II на 8 |
| Learning and Adaptation | Policy adaptation локальна; continual learning страдает forgetting; repeated knowledge edits нарушают global coherence | Поведение после обновлений и накопленного опыта может деградировать, даже если локальная правка выглядит успешной | 8-9, Table II на 8 |

Это результаты авторского синтеза, а не пять независимо оценённых effect sizes.
В работе нет количественного ранжирования gaps, prevalence, confidence intervals
или оценки того, какой gap чаще приводит к production failure.

## ACIA и evaluation outputs

### Adaptive Cognitive Intelligence Architecture

Авторы предлагают концептуальную ACIA - closed-loop архитектуру из Perception
and Attention, Memory, Reasoning and Planning, Metacognition, Action и Learning
and Adaptation. Компоненты связывают восприятие среды, хранение состояния,
планирование, самоконтроль, действие и feedback-driven update (PDF 9-10).

ACIA является recommended conceptual architecture. В PDF нет реализации,
алгоритма orchestration, репозитория, benchmark run, ablation, baseline или
сравнения ACIA с существующими агентами. Фраза о координации с другими агентами
находится в описании Action component, но не задаёт multi-agent protocol,
топологию или concurrency experiment (PDF 9).

### Cognition-centric evaluation

Авторы утверждают, что output accuracy и short-horizon task success не
покрывают memory persistence, goal drift, belief consistency, uncertainty,
grounding и safe adaptation. Предлагается longitudinal evaluation в dynamic
environments (PDF 10-12).

Table IV вводит три иллюстративные метрики (PDF 11):

- Cognitive Persistence Index `CPI = f(T_ret, P_mem, R_mem)`;
- Cognitive Adaptation Rate `CAR = f(A_succ, A_opp)`;
- Cognitive Consistency Score через долю contradictions в reasoning episodes.

Авторы оставляют `f(.)` application-dependent. Метрики не операционализированы
полностью, не применены к sample и не имеют evidence по reliability, validity
или sensitivity. Их нельзя цитировать как validated measures.

## Human oversight, understanding, trust и context

### Human oversight

Статья утверждает, что из-за ограничений памяти, самоконтроля, grounding и
адаптации нынешние системы остаются зависимыми от external supervision и human
intervention (PDF 2). Table I называет need for human oversight одним из
ограничений Agentic AI (PDF 4), а future-directions section требует сочетать
растущую автономность с interpretability, controllability, alignment и human
oversight (PDF 12).

Это **narrative claim**, а не измеренный human-in-the-loop outcome. Не указаны
число reviewers, review time, intervention rate, escalation policy, качество
после вмешательства или стоимость контроля.

### Understanding

Основное употребление understanding относится к способности AI понимать язык,
контекст или среду и поддерживать coherent world/state representation. Работа
не измеряет, понимает ли разработчик код, написанный агентом, и не исследует
mental model человека. Для claims о human code comprehension этот источник не
подходит.

### Trust

Trust упоминается как одна из нерешённых проблем Cognitive AI наряду с safety,
alignment и integration (Table I, PDF 4). Trust не определён как construct, не
измеряется анкетой или поведением и не связан с calibrated reliance. Источник
не позволяет утверждать, что пользователи больше или меньше доверяют агентам.

### Context

Context в работе - прежде всего machine-side information state:

- finite context windows и stateless interactions вытесняют прошлую информацию
  (PDF 4-5);
- внешняя память улучшает retrieval, но не равна устойчивому внутреннему
  cognitive state (PDF 5);
- Perception and Attention должна приоритизировать релевантную информацию, а
  Memory - сохранять и пересматривать contextual knowledge (PDF 9-10);
- single-context benchmarks могут не обнаруживать потери persistent state
  (PDF 11).

Это не human context-switching между agent windows. Нельзя превращать memory
degradation модели в численный штраф `gamma(P)` разработчика.

## Production implications

Для production agent systems из survey обоснованно следуют требования к
дизайну и измерениям, но не оценка производительности:

1. Нужно хранить версионированное task/repository state и проверять, что новый
   context действительно обновляет прежние beliefs, а не только добавляется в
   prompt (PDF 4-5, 9-11).
2. Goal completion следует проверять на длинной последовательности действий;
   прохождение одного short task не исключает goal drift (PDF 5-6, 11).
3. Self-check агента нельзя считать достаточным acceptance gate: confidence и
   self-correction остаются нестабильными, поэтому нужны external tests,
   verification и escalation rules (PDF 6-7, 9-12).
4. Tool call должен обновлять internal task state и уметь запускать replanning
   после failure; простое наличие search, API или interpreter недостаточно
   (PDF 7, 9-10).
5. Feedback loops требуют контроля, потому что могут усиливать bias и ошибки,
   а repeated updates - нарушать global consistency (PDF 7-9).
6. Production evaluation должна включать retention, contradiction, goal drift,
   adaptation и recovery на длинном горизонте, а не только pass rate первого
   ответа (PDF 10-12).

Для coding workflow перевод в M0-M4 является дополнительной гипотезой: каждый
failure памяти, planning, monitoring или tool integration может увеличить
prompt reconstruction, review, debugging и rework, то есть наблюдаемые `k` и
`h`. Сама статья не проверяет этот временной канал и не показывает, насколько
он велик.

## Outcomes и неопределённость

### Фактические outcomes работы

Работа производит четыре типа результата:

1. пятичастную taxonomy cognitive gaps;
2. narrative synthesis representative approaches и остающихся limitations;
3. conceptual ACIA;
4. proposal cognition-centric longitudinal evaluation.

Она не производит empirical outcomes по времени, throughput, cost, quality,
success coding tasks, human comprehension или concurrent-agent scaling.

### Неопределённость и доказательная сила

- Нет effect sizes, standard errors, confidence intervals или meta-analytic
  estimates.
- Нет формальной оценки certainty для каждого taxonomy claim.
- Нет воспроизводимого search и screening process, поэтому неизвестна coverage
  bias литературы.
- Нет quality weighting mixed corpus; preprints и peer-reviewed работы входят в
  синтез без разных evidence grades.
- Не показано, что пять dimensions являются исчерпывающими, взаимно
  независимыми или устойчивыми при альтернативном кодировании.
- ACIA не реализована и не валидирована.
- Иллюстративные metrics оставляют агрегирующую функцию неопределённой и не
  проверены на данных.
- Многие выводы относятся к Cognitive AI вообще, а не к software engineering,
  поэтому domain transfer требует отдельного исследования.

Следовательно, безопасный evidentiary статус - **современная концептуальная
карта проблем и research agenda**, а не количественное доказательство эффекта.

## Связь с `r`, `h` и `gamma(P)`

### Режим `r`

Источник даёт косвенные признаки, которыми можно дополнить описание режима:
способ хранения состояния, степень автономии, planning/replanning policy,
self-monitoring, uncertainty-based abstention, tool-use policy и human
escalation. Эти свойства правдоподобно различают interactive, delegated и
autonomous workflows.

Однако статья не задаёт `r` как experimental condition, не сравнивает режимы
на одинаковых coding tasks и не оценивает `k_i^(r)` или `h_i^(r)`. Это feature
schema для будущей калибровки, а не готовая taxonomy режимов M0-M4.

### Человеческая доля `h` и сумма `H`

Прямая связь ограничена утверждением о сохраняющейся зависимости от human
oversight/intervention (PDF 2, 4, 12). Из этого можно мотивировать включение в
`h` времени на:

- повторную передачу потерянного контекста;
- проверку goal consistency и ограничения drift;
- внешнюю верификацию вместо доверия self-correction;
- решение об abstention, retry или escalation;
- проверку tool outputs и recovery после failure;
- контроль knowledge/policy updates.

Но review не хронометрирует эти действия, не нормирует их на `Z_i X` и не
показывает, что все интервалы обслуживает один developer. Численные `h_i` и
`H` отсутствуют.

### Штраф `gamma(P)`

Связи нет. Survey обсуждает потерю **агентного** state/context на длинном
горизонте, а не восстановление человеческого mental context при переключении
между `P` concurrent streams. Число потоков не варьируется, switch events не
собираются, recovery time не измеряется. Источник не поддерживает
монотонность, линейность или даже наличие отдельного `gamma(P)`.

## Исследует ли работа concurrency

Нет. Слово *agentic* в объекте обзора означает systems с planning, tool use и
autonomous task execution; оно не означает одновременно запущенную группу
агентов.

ACIA включает other agents в среду и упоминает coordinating with other agents
как возможную функцию Action component (PDF 9-10), но работа не задаёт:

- число агентов или `P`;
- one-human-many-agents topology;
- independent, centralized, decentralized или star architecture;
- одновременные tasks, branches или shared artifacts;
- developer attention queue;
- agent-agent communication или merge/integration cost;
- scheduling, throughput или makespan outcome.

Следовательно, источник не является ни single-agent workflow study в
эмпирическом смысле, ни concurrency study. Это survey общих capability gaps
agentic systems с преимущественно long-horizon, но не parallel, постановкой.

## Полное mapping к `Z,k,r,W,P,L,C(P),h,H,gamma(P)`

| Поле M0-M4 | Статус | Ближайший объект Akinrele et al. | Точная граница |
|---|---|---|---|
| `Z_i` / `Z` | **absent** | Упоминаются task complexity, open-ended и long-horizon tasks | Нет no-AI complexity scale, общей единицы `X` или набора software jobs |
| `k_i^(r)` / `k` | **conceptual mechanism only** | Memory loss, brittle planning, weak self-correction и tool failures могут создавать retries/rework | Нет elapsed duration, no-AI denominator, coding task или mode comparison; coefficient не вычисляется |
| режим `r` | **conceptual feature support** | Уровень autonomy, planning, memory, metacognition, abstention, tool policy и human escalation | Не задана operational taxonomy human-agent workflows и нет experimental assignment |
| `W = X sum Z_i k_i` | **absent** | Survey агрегирует литературу, а не work | Нет fixed workload и суммируемых task durations |
| `P` | **absent** | ACIA допускает interaction/coordination с other agents | Число concurrent agents не определено и не варьируется; topology отсутствует |
| `L` / DAG | **absent** | Long-horizon reasoning и multi-step planning | Long horizon не является precedence DAG; нет vertex weights или critical path |
| `C(P)` | **absent** | Adaptive planning может иметь computational overhead; tool integration может быть хрупкой | Overhead не зависит от числа parallel agents и не является agent-agent integration multiplier |
| `h_i^(r)` / `h` | **indirect conceptual support** | External supervision, human intervention, oversight, verification и control | Human time не измерено, не разделено с agent time и не нормировано на baseline |
| `H = X sum Z_i h_i` | **absent** | Общая потребность в human oversight | Нет fixed job set, суммы human intervals, capacity-1 developer или resource-feasible schedule |
| `gamma(P)` | **absent** | Machine context loss и attention prioritization | Это не human context switching; нет `P`, switch count, recovery duration или functional form |
| Makespan | **absent** | Task success и long-term behavior обсуждаются как evaluation targets | Нет project completion time, baseline speedup или scheduling objective |

### Mapping по уровням M0-M4

| Уровень | Возможная связь | Что источник не даёт |
|---|---|---|
| M0 | Capability failures могут изменить one-stream duration, а значит внешний `k` | Нет timing, fixed work, делимости или `W/P` |
| M1 | Long-horizon task может требовать декомпозиции | Нет неделимых jobs, machine assignment или longest-job bound |
| M2 | Goal-directed planning подразумевает последовательности действий | Нет project DAG и critical path `L` |
| M3 | Planning и adaptation могут быть computationally expensive | Нет overhead, возникающего именно при росте concurrent `P`, и нет `C(P)` |
| M4 | Сохраняющаяся external supervision мотивирует human verification resource | Нет human intervals, единственного developer, non-overlap constraint, `H` или `gamma(P)` |

Источник расположен **до estimation и scheduling layers** M0-M4: он описывает
reliability properties, которые могут стать predictors будущих `k` и `h`, но
не преобразует их во время и не строит расписание.

## Что источник поддерживает для M0-M4

1. Short-horizon task execution не гарантирует надёжность на длинном горизонте:
   нужны persistent state, goal maintenance, self-monitoring и feedback-grounded
   adaptation (PDF 1-8, 11-12).
2. Внешняя память и повторное добавление context не эквивалентны устойчивому
   internal state; state revision должна сохранять coherence (PDF 4-5, 8-9).
3. Planning quality, adaptability и efficiency образуют trade-off; более
   адаптивные reasoning procedures могут добавлять computational overhead
   (PDF 5-6).
4. Fluent reasoning и declared confidence недостаточны для acceptance:
   self-correction и uncertainty estimation остаются хрупкими (PDF 6-7).
5. Tool availability не равна integrated tool reasoning: агенту нужно выбрать
   момент вызова, обновить reasoning по результату и replanning после failure
   (PDF 7).
6. Feedback и online adaptation могут усиливать ошибки, а repeated knowledge
   updates - нарушать global consistency (PDF 7-9).
7. Current agentic systems продолжают требовать external supervision и human
   oversight; для M0-M4 это мотивирует наличие человеческих verification и
   control intervals внутри `h` (PDF 2, 4, 12).
8. Оценка production agents должна включать longitudinal persistence,
   consistency, goal drift и adaptation, а не только output accuracy или
   single-task success (PDF 10-12).

Пункты 7-8 поддерживают необходимость измерять human oversight и downstream
reliability, но не численную модель их стоимости.

## Что источник не позволяет утверждать

1. Что работа peer-reviewed, accepted или опубликована вне arXiv.
2. Что review систематический, исчерпывающий или воспроизводимый.
3. Что 106 references являются формально screened corpus с известным risk of
   bias.
4. Что taxonomy состоит из статистически выявленных latent factors или что
   пять dimensions независимы и исчерпывающи.
5. Что ACIA реализована, превосходит существующие architectures или прошла
   empirical validation.
6. Что CPI, CAR и CCS являются validated metrics; их `f(.)` оставлена
   неопределённой и ни одна метрика не применена к данным.
7. Что source измеряет human understanding, code ownership, trust, reliance или
   review effectiveness.
8. Что потребность в human oversight имеет известную частоту, длительность или
   causal effect на quality.
9. Что agent memory/context gap равен human context-switch cost.
10. Что long-horizon task равна project DAG или что goal persistence задаёт
    critical path `L`.
11. Что computational overhead adaptive planning является `C(P)`.
12. Что можно получить `k`, `h` или `H` из qualitative taxonomy.
13. Что работа исследует `P>1`, multi-agent fan-out, one-human-many-agents
    supervision, concurrency или diminishing returns.
14. Что упоминание coordination with other agents валидирует multi-agent
    architecture или scaling law.
15. Что источник поддерживает форму `gamma(P)=1+delta(P-1)` или любой другой
    штраф переключения человека.
16. Что cognitive gaps сами по себе доказывают замедление или ускорение coding
    work: time outcome отсутствует.
17. Что findings из cited primary papers становятся собственными empirical
    results этого survey.

## Отличие от M0-M4

| Измерение | Akinrele et al. (2026) | M0-M4 |
|---|---|---|
| Центральный вопрос | Какие cognitive capabilities отсутствуют у generative/agentic AI и как организовать research agenda | Когда `P>1` coding agents сокращают fixed-workload makespan |
| Тип работы | Narrative taxonomy-driven survey плюс conceptual architecture | Formal scheduling/scalability model с внешней empirical calibration |
| Объект | Когнитивные свойства AI systems на long horizon | Одна human-agent cell и фиксированный набор software tasks |
| Топология | Не фиксирована; environment может включать users, tools и agents | Звезда «один developer - `P` agents» |
| Outcome | Taxonomy, ACIA, evaluation proposal | Makespan и speedup относительно sequential no-AI baseline |
| Время | Не измеряется | Центральный outcome; `k`, `W`, bounds M0-M4 |
| Human role | External supervision, oversight и evaluation упомянуты концептуально | Human work измеряется как `h_i`, суммируется в capacity-1 `H` |
| Context | Persistent machine state, memory и context windows | Task context влияет на `k/h`; human switching выделяется в `gamma(P)` |
| Dependencies | Long-horizon goals и plans | Formal DAG и critical path `L` |
| Parallelism | Не исследуется | Явные `P`, `C(P)`, resource-feasible schedules и finite optimum |
| Uncertainty | Предмет self-monitoring и future evaluation; без review-level certainty grading | `k` может быть stochastic input; core использует deterministic bounds |

Модели дополняют друг друга только через будущий measurement layer. Taxonomy
может подсказать, какие capability и telemetry features объясняют observed
`k_i^(r)` и `h_i^(r)`. M0-M4 затем использует эти time parameters для
fixed-workload schedule. Ни одна работа не подменяет другую.

## Проверенные claims для Related Work

### Безопасные claims

1. Akinrele et al. (2026) предлагают narrative taxonomy пяти cognitive
   capability gaps generative и agentic AI: persistent state, goal-directed
   autonomy, self-monitoring/control, environment interaction и
   learning/adaptation (PDF 1, 3-8).
2. Survey связывает long-horizon unreliability с externalized memory, unstable
   belief revision, goal drift, fragile self-correction, poorly calibrated
   uncertainty, weak tool integration и unsafe continual updates (PDF 4-9).
3. Авторы предлагают conceptual ACIA из perception/attention, memory,
   reasoning/planning, metacognition, action и learning/adaptation; реализация и
   validation не представлены (PDF 9-10).
4. Работа призывает оценивать agents longitudinally по memory retention,
   adaptation, consistency и goal stability, поскольку short-task benchmarks
   не обнаруживают часть long-horizon failures (PDF 10-12).
5. Источник отмечает сохраняющуюся зависимость current systems от external
   supervision и human oversight, но не измеряет intervention time или effect
   (PDF 2, 4, 12).
6. Для M0-M4 перечисленные gaps являются возможными drivers `k` и `h`, но
   source не рассматривает coding workload, no-AI baseline, concurrent agents,
   human switching или makespan.

### Claims, которых следует избегать

- «Akinrele et al. экспериментально доказали пять cognitive gaps».
- «Это systematic review 106 исследований».
- «ACIA повышает надёжность или производительность agents».
- «CPI/CAR/CCS - валидированные метрики».
- «Работа измеряет доверие или понимание разработчика».
- «Survey показывает стоимость human oversight».
- «Memory context loss агента оценивает `gamma(P)` человека».
- «Long-horizon planning моделирует `L` или project critical path».
- «Adaptive planning overhead подтверждает `C(P)`».
- «Работа исследует multi-agent concurrency или оптимальное `P`».
- «Cognitive gaps дают численный `k` или `h`».

## Предлагаемое место в статье

Источник лучше использовать не в подразделе multi-agent scaling, а в конце
подраздела о human-AI interaction/reliability или в synthesis and limitations.
Его роль - показать, почему снижение first-pass task time недостаточно для
долгогоризонтной оценки и какие agent-side failures могут переносить работу в
human verification/rework.

### Короткий вариант встраивания

> Akinrele et al. (2026) в narrative survey организуют ограничения generative
> и agentic AI по пяти группам: persistent state, goal-directed autonomy,
> self-monitoring and control, environment interaction и learning and
> adaptation. Авторы подчёркивают externalized memory, goal drift, хрупкую
> self-correction, слабую calibration uncertainty, неполную интеграцию tool
> feedback и нестабильность repeated updates, а потому предлагают дополнять
> task-level benchmarks longitudinal evaluation памяти, адаптации и
> consistency. Для нашей модели эти ограничения являются возможными
> источниками mode-specific verification и rework внутри `k_i^(r)` и
> `h_i^(r)`. Однако работа представляет собой arXiv v1 narrative survey без
> воспроизводимого search protocol или собственной empirical sample; она не
> измеряет время, не исследует coding workflow и не варьирует число
> concurrent agents, поэтому не калибрует `k`, `h`, `C(P)` или `gamma(P)`.

### Вариант для discussion M4

> Потребность в человеческой проверке определяется не только качеством
> единичной генерации. Таксономия Akinrele et al. указывает на long-horizon
> failure channels - потерю persistent state, goal drift, слабую
> self-correction, некалиброванную uncertainty и ошибки интеграции tool
> feedback, - которые могут возвращать работу человеку даже после автономного
> выполнения. В M4 такие последствия должны попадать в измеренное `h`, если
> они вызывают восстановление контекста, verification или rework. Сам survey,
> однако, не хронометрирует вмешательства и не исследует переключение между
> несколькими агентами, поэтому не задаёт ни `H`, ни `gamma(P)`.

## Таблица доказательных страниц

| PDF | Раздел / объект | Опорное содержание | Статус свидетельства |
|---:|---|---|---|
| 1 | Title; Abstract; Introduction | Точные title/authors/arXiv id; taxonomy-driven survey; пять dimensions; distinction task performance vs cognition | Прямые metadata и author summary |
| 1-2 | Introduction; Fig. 1 | Persistent memory, goal maintenance, self-monitoring, grounding и adaptation; dependence on external supervision/human intervention | Авторская постановка, опирающаяся на citations |
| 3-4 | Background; Survey Methodology | Narrative synthesis; охват literature domains; пять dimensions emerged; нет systematic search details | Прямое описание метода и его границы |
| 4-5 | Persistent State Modeling | External memory, context-window loss, inconsistent state revision, no persistent latent state | Narrative synthesis representative work |
| 5-6 | Goal-Directed Autonomy | Externally specified goals, planning/adaptation overhead, goal drift | Narrative synthesis representative work |
| 6-7 | Self-Monitoring and Control | Fragile verification/self-correction, prompt-sensitive uncertainty, abstention limitations | Narrative synthesis representative work |
| 7 | Environment Interaction | Weak world models, loosely integrated tool use, feedback loops that can reinforce errors | Narrative synthesis representative work |
| 8-9 | Learning and Adaptation; Table II | Local policy adaptation, catastrophic forgetting, inconsistent repeated knowledge updates; summary taxonomy | Narrative synthesis and author table |
| 9-10 | ACIA; Fig. 4; Table III | Conceptual closed-loop architecture; components and mapping; mention of coordination with agents | Conceptual proposal, not implementation |
| 10-11 | Evaluation Strategies | Limits output/task benchmarks; need long-horizon evaluation; human evaluation and LLM-as-judge discussed | Methodological synthesis |
| 11 | Table IV | Illustrative CPI, CAR, CCS; `f(.)` application-dependent | Unvalidated metric proposal |
| 11-12 | Future Directions | Persistent state, metacognitive control, continual learning, cognition-centric evaluation, safety/transparency/human oversight | Research agenda |
| 12 | Conclusion | Restatement of taxonomy, ACIA and evaluation contribution | Author conclusion, no new data |
| 12-15 | References `[1]-[106]` | Mixed bibliography underlying narrative synthesis | Secondary pointers; primary claims require source-level verification |

## Итоговая оценка источника

Akinrele et al. дают компактную современную карту agent-side reliability gaps,
которые first-pass productivity studies могут не увидеть. Для M0-M4 особенно
полезны persistent state, goal drift, self-monitoring, uncertainty, tool
feedback и safe adaptation как candidate drivers дополнительной verification
и rework. Источник также поддерживает важное ограничение measurement design:
single-task success недостаточен для long-horizon production deployment.

Доказательная сила ограничена статусом arXiv v1 и narrative method без
воспроизводимого поиска, формальной sample и certainty grading. Taxonomy, ACIA
и cognition-centric metrics являются conceptual outputs; собственного
эксперимента нет. Работа не исследует разработчиков, human code understanding,
fixed workload, elapsed time или concurrency. Поэтому её корректная роль в
статье - reliability/contextual source для интерпретации `r` и состава
потенциального `h`, но не доказательство multi-agent speedup, `P`, `C(P)`, `H`
или `gamma(P)`.
