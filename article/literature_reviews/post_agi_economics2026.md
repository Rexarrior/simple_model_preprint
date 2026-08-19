# Ruan (2026): Flourishing Value Theory для post-AGI economics

## Назначение и итоговая оценка

Этот документ разбирает локальный PDF применительно к модели M0--M4 для
fixed-workload makespan звезды «один developer -- `P` coding agents».

Источник является не моделью производительности, расписаний или масштабирования
агентов, а нормативно-концептуальной теорией экономической ценности в сценариях
post-AGI. Его основной вопрос: что считать ценностью, если продуктивный интеллект
становится изобильным, а output, price, profit и human labor перестают быть
достаточными показателями общественного результата. Автор предлагает
Flourishing Value Theory (FVT), где первичным объектом оценки служит
контрфактический, распределительно чувствительный вклад в устойчивые возможности
людей и сообществ процветать в социальных и планетарных ограничениях.

Для M0--M4 работа полезна только как **нормативная граница objective**. Она
поддерживает предупреждение, что сокращение makespan и человеческого времени не
равно улучшению welfare, agency, meaningful work или справедливому распределению
выгод. Она не задаёт fixed workload, software tasks, one-human-many-agents
topology, production/scheduling function, временные коэффициенты или
количественную scaling evidence. Поэтому источник рекомендуется **не включать в
ядро текущего Related Work**. Возможна одна краткая ссылка в Discussion или
limitations, если статья явно обсуждает, что её objective ограничен временем
завершения при заданном acceptance standard.

Локальный PDF содержит 35 страниц: основной текст и conclusion занимают
страницы 1--30, references -- 31--35. Номера ниже относятся к PDF-страницам.

## Метаданные, версия и статус

**Точное название arXiv:** “A New Theory of Value for Post-AGI Economics”.

**Подзаголовок на обложке PDF:** “From Scarcity and Exchange to Flourishing
Capacity”. Подзаголовок не входит в title поля arXiv.

**Автор:** Keyun Ruan. На титульной странице указаны Human Flourishing Program,
Harvard University и адрес `keyun@fas.harvard.edu` (PDF 1).

**Проверенная ссылка:** Keyun Ruan. “A New Theory of Value for Post-AGI
Economics.” arXiv:2608.01432v1 [cs.AI], 2026.
[https://arxiv.org/abs/2608.01432v1](https://arxiv.org/abs/2608.01432v1).
DOI: [10.48550/arXiv.2608.01432](https://doi.org/10.48550/arXiv.2608.01432).

**Версия:** `arXiv:2608.01432v1`, подана 2 августа 2026 года в 18:26:33 UTC.
Основная категория -- `cs.AI`, дополнительная -- `econ.GN`. На дату проверки
4 августа 2026 года submission history содержит только `v1`.

**Статус:** arXiv preprint. Обложка использует labels `Preprint` и `Research
Article`, но arXiv не сообщает journal reference, принятие в журнал или
конференцию. Поэтому работу нельзя называть peer-reviewed или опубликованной
рецензируемой статьёй. Фактический тип по содержанию -- integrative conceptual
article: нормативная теория ценности, narrative/integrative synthesis и
иллюстративное application, без собственной эмпирической выборки и без
формальной экономико-математической модели.

**Проверка локальной копии:** SHA-256 файла
`post_agi_economics2026.pdf` равен
`2d1db13c2426e291dee2d257a9a6e24700ef847c70aa8b76be735075661d1fce` и
совпадает с SHA-256 ответа `https://arxiv.org/pdf/2608.01432v1`. Обзор относится
именно к arXiv v1, а не к документу, идентифицированному по имени файла.

### Предлагаемая BibTeX-запись

```bibtex
@misc{ruan2026postagi,
  author        = {Ruan, Keyun},
  title         = {A New Theory of Value for Post-{AGI} Economics},
  year          = {2026},
  eprint        = {2608.01432},
  archiveprefix = {arXiv},
  primaryclass  = {cs.AI},
  doi           = {10.48550/arXiv.2608.01432},
  url           = {https://arxiv.org/abs/2608.01432v1},
  note          = {Version 1, submitted 2 August 2026}
}
```

## Исследовательский вопрос и предмет

Явного нумерованного RQ нет. Из introduction, definition и conclusion основной
вопрос восстанавливается так:

> Что должно считаться экономической ценностью в сценарии, где AGI существенно
> снижает дефицит продуктивного интеллекта, автоматизирует значительную долю
> когнитивного труда и усиливает расхождение между labor, price, preference,
> output и устойчивым человеческим и общественным благополучием?

Вспомогательные вопросы работы:

1. Почему labor input, market price, revealed preference, profit и GDP
   становятся неполными value measures при масштабируемой автоматизации?
2. Как определить flourishing value, сохранив multidimensionality, agency,
   distribution, ecological constraints и downside risk?
3. Когда допустимо агрегировать многомерный value profile в decision score?
4. Как применять FVT к work-replacing AI, business governance, national
   accounting и AI policy?

Это не RQ о том, при каком `P` сокращается makespan, и не вопрос о
производительности coding agents.

## Метод и фактический тип аргумента

### Заявленный метод

Автор прямо называет подход **integrative conceptual method**. Работа
сопоставляет theories of value и welfare с capability approach, human
flourishing, ecological limits, automation, transformative AI, AI agents,
preference formation и measurement (PDF 4).

Обзор economics of AI заявлен как comprehensive по крупным research programmes
и field-shaping contributions, но selective по узким applications и
unpublished cases (PDF 4--5). Не сообщены:

- bibliographic databases и search strings;
- дата и временной диапазон поиска;
- inclusion/exclusion criteria;
- число найденных, screened и excluded источников;
- независимый screening или data extraction;
- quality appraisal, risk of bias или certainty grading;
- protocol registration или review flow.

Следовательно, формулировку abstract о `structured review` следует понимать как
структурированную автором интегративную карту литературы, а не systematic review,
scoping review с воспроизводимым поиском или meta-analysis.

### Тип аргумента

Аргумент имеет четыре слоя:

1. **Диагноз:** AGI может разделить production и human labor, price и social
   value, preference satisfaction и autonomous well-being, output и flourishing
   (PDF 3--4).
2. **Нормативное определение:** value определяется через контрфактический вклад
   в устойчивые capabilities to flourish (PDF 13--14).
3. **Процедурная архитектура:** primary output должен быть многомерным value
   profile; contextual scalar допустим только после явного выбора population,
   weights, horizon, distribution, agency floors, ecological limits и risk
   tolerance (PDF 14--18).
4. **Applications:** семь propositions, два иллюстративных пути замещения труда,
   criteria для firms, governments, national accounts и AI governance
   (PDF 20--29).

Автор специально оставляет framework **conceptual and procedural rather than
equation-based**. Formalisation и empirical calibration названы последующими
задачами (PDF 4--5).

## Предпосылки об automation, substitution и complementarity

### Post-AGI как scenario class

`Post-AGI` не является прогнозом даты. Это класс сценариев, где достаточно
общие и автономные AI systems способны выполнять, координировать или улучшать
значительную долю экономически ценного cognitive work, возможно вместе с
robotics и scientific discovery. Для аргумента достаточно, чтобы дефицит
productive intelligence снизился настолько, что destabilise labor income,
marginal-cost pricing или текущие output/welfare measures (PDF 4--5).

### Substitution

Работа допускает широкое замещение человеческих cognitive и physical tasks,
частичное отделение output от human labor и снижение labor share. Однако это
scenario assumption, опирающийся на cited automation literature, а не
собственная оценённая substitution elasticity или task model (PDF 3, 6,
10--11).

Замещение не трактуется как автоматическое уничтожение ценности человеческой
деятельности. Care, friendship, citizenship, parenting, contemplation,
artistic practice и moral judgment могут оставаться ценными независимо от
market demand на труд (PDF 10--11).

### Complementarity и institution dependence

Автор подчёркивает complementarities между AI и data, human capital,
organizational processes, ownership, market access, scientific experimentation
и institutional design. Поэтому одна и та же technical capability может дать
противоположные value profiles при разных ownership, access, governance и
transition arrangements (PDF 7--8, 21).

Это концептуально согласуется с тезисом M0--M4, что результат принадлежит полной
workflow configuration, а не инструменту отдельно. Но FVT сравнивает
общественные outcomes институциональных режимов, тогда как M0--M4 сравнивает
elapsed makespan конфигураций `sigma=(P,r)`.

## Production functions, bottlenecks и workload

### Собственной production function нет

Статья пересказывает growth и task-based literature: effects зависят от
substitutability, bottlenecks, task coverage, diffusion, organizational
reorganisation и production function for ideas (PDF 6). Она также обсуждает
AI-assisted scientific search и experimental capacity как complement (PDF 8).

Но FVT не задаёт:

- функцию выпуска `Y=F(K,L,AI)`;
- task assignment между labor и AI;
- elasticity of substitution;
- law of motion для capital или ideas;
- budget/resource constraint с оценёнными параметрами;
- scheduling или queueing model;
- функцию production time от числа agents.

Термин `post-AGI value frontier` обозначает множество feasible states,
максимизирующих flourishing при resource, rights, agency, risk и planetary
constraints. Это нормативная Pareto-like boundary, а не production frontier
для makespan или agent scaling (PDF 18--19).

### Bottlenecks

Ключевой тезис состоит не в исчезновении scarcity, а в её миграции. Energy,
land, minerals, compute infrastructure, ecological capacity, trusted
institutions, human attention, care, legitimacy и positional goods остаются
ограниченными (PDF 3). При cognitive abundance ценность зависит от способности
институтов преобразовать capability в широко доступное flourishing без новых
bottlenecks, dependency и rent extraction (PDF 19).

`Human attention` здесь только один пункт в списке residual scarcities. Статья
не моделирует внимание как capacity-1 server, не выделяет specification/review
intervals и не показывает, что verification bandwidth ограничивает completion
time. Поэтому этот фрагмент нельзя использовать как формальный источник M4.

### Fixed против scalable workload

Работа предполагает, что cognitive capability может стать abundant and
scalable, а marginal replication cost некоторых informational goods приблизится
к нулю (PDF 2--3, 20). Однако она не различает fixed-workload speedup и
scaled-workload throughput в смысле Amdahl/Gustafson, не фиксирует объём задач и
не варьирует `P`.

Следовательно, `scalable intelligence` в FVT не является scaled-workload model.
Источник не показывает, растёт ли workload вместе с числом agents и как это
влияет на makespan.

## Основные результаты и количественная evidence

### Flourishing Value Theory

FVT определяет value как контрфактический, distribution-sensitive вклад
системы, института, asset или intervention в durable capabilities людей и
сообществ to flourish within social and planetary constraints (PDF 13).

Определение включает семь commitments: counterfactuality,
multidimensionality, capabilities, agency, distribution, dynamic/regenerative
effects и constraints на компенсацию критических потерь (PDF 13--14). Далее
автор задаёт двенадцать элементов complete value theory: value object,
value-bearing community, baseline, dimensions, system boundary, measurement,
aggregation, distribution, time/option value, risk/constraints,
creation-versus-capture и legitimate decision rule (PDF 14--15).

### Seven propositions

Семь propositions являются выводами концептуального аргумента, а не
статистически проверенными гипотезами (PDF 20--22):

1. Cognitive abundance увеличивает divergence между price и value.
2. Automation отделяет human worth от market productivity.
3. Preference-shaping AI ослабляет welfare interpretation revealed preference.
4. Flourishing value технологии зависит от surrounding institutions.
5. Некоторые flourishing dimensions non-fungible ниже thresholds.
6. Work-replacing AI создаёт positive value только при flourishing replacement
   institutions.
7. Regenerative и option-creating assets недооцениваются static accounts.

### Worked application

На PDF 22--23 сравниваются две фирмы с **технически одинаковыми** agentic AI
systems. В обоих сценариях AI по предположению снижает human hours per unit of
output на 50% и повышает operating profit. Pathway A концентрирует выгоды,
ослабляет agency и интенсифицирует оставшуюся работу; Pathway B сочетает AI с
income protection, worker participation, shorter hours, human authority,
broader ownership и ecological constraints.

Число `50%` является условием мысленного примера. Нет dataset, sample,
estimation procedure, comparator observations или uncertainty. Его нельзя
цитировать как empirical effect AI и нельзя подставлять как `k=0.5`.

### Собственная quantitative evidence

Собственной количественной evidence нет:

- нет участников, firms, projects, tasks или agent runs;
- нет fitted parameters, effect sizes, standard errors или confidence
  intervals;
- нет simulation, calibration, sensitivity analysis или validation FVT;
- нет численного value profile или RoF calculation;
- нет controlled comparison fixed/scaled workload;
- нет agent-count scaling curve.

Численные результаты cited studies на PDF 6--9 принадлежат первичным источникам,
а не Ruan. Для claims об employment, productivity, labor demand или growth
следует проверять и цитировать эти первичные работы.

## Human constraint и работа

FVT рассматривает work шире paid task execution. Работа может давать income,
routine, esteem, community, skill development, interdependence и meaning, но
также stress, hierarchy, danger и loss of time. Поэтому корректное сравнение
automation -- не `jobs` против `no jobs`, а полные social states и институты,
замещающие полезные функции work (PDF 21--23).

Это важно для интерпретации M4: меньшее `h` увеличивает только верхнюю границу
time speedup при заданных требованиях. Из FVT не следует, что вся человеческая
доля -- waste. Human authority, participation, appeal, learning и meaningful
roles могут быть constraints или самостоятельными outcomes (PDF 21--25).

При этом работа не измеряет:

- время specification, prompting, review, correction или approval;
- долю active human time внутри task duration;
- intervention frequency;
- очередь результатов нескольких agents;
- overlap human и agent phases;
- context switches и recovery duration;
- предельное число agents на одного человека.

Поэтому FVT поддерживает **необходимость не смешивать time efficiency и social
value**, но не человеческий bottleneck `H` как scheduling result.

## Ограничения работы

### Ограничения, прямо обсуждаемые автором

Section 9 перечисляет шесть групп возражений и ограничений (PDF 29--30):

1. Риск paternalism при substantive account of flourishing.
2. Невозможность устранить ethical judgment при сравнении multidimensional
   values; иногда допустим только partial ordering.
3. Goodharting и proxy failure даже при mixed methods и audit safeguards.
4. Сохранение material scarcities после AGI.
5. Неопределённый moral status потенциально sentient AI systems.
6. Political capture weights, indicators и thresholds.

### Дополнительные ограничения доказательной силы

1. FVT не формализована и не откалибрована; это прямо отложено на future work.
2. Integrative review не имеет воспроизводимого search/screening protocol.
3. Не показано, что двенадцать элементов necessary and jointly sufficient в
   формальном или эмпирическом смысле.
4. Seven propositions не проверены на данных и не имеют falsification tests.
5. Worked application является illustrative contrast с предположенным 50%
   reduction, а не case study.
6. RoF и Flourishing Metrics ссылаются на отдельную рукопись, заявленную как
   submitted for publication; текущий PDF не валидирует их measurement
   properties.
7. Выбор dimensions, weights, floors и affected populations остаётся
   контекстным и политическим; universal scalar намеренно отвергается.
8. Перенос от prospective post-AGI scenario к современным coding agents требует
   отдельной аргументации.
9. Работа не исследует software engineering, coding quality, code review,
   repository dependencies или maintainability.
10. Статус свежего arXiv v1 усиливает необходимость осторожной формулировки.

## Полное mapping к `Z,k,r,W,P,L,C(P),h,H,gamma(P)`

Здесь **conceptual** означает сходный аргумент без операциональной или численной
совместимости; **absent** -- объект не задан.

| Поле M0--M4 | Статус | Ближайший объект FVT | Точная граница переноса |
|---|---|---|---|
| `X` | **absent** | Human labor и resources обсуждаются как экономические inputs | Нет базовой единицы no-AI task duration |
| `Z_i` / `Z` | **absent** | Task exposure и различия occupations пересказываются в review | Нет software jobs, complexity scale или baseline effort `Z_i X` |
| `k_i^(r)` / `k` | **absent** | AI может повышать task performance или замещать labor; эффекты task-, institution- и horizon-dependent | Нет matched one-stream AI/no-AI elapsed time и коэффициент не вычисляется |
| режим `r` | **conceptual** | Unit of evaluation -- AI-plus-institution system; outcomes зависят от ownership, governance и transition design | Это широкий institutional regime, не operational mode developer-agent interaction и не `rho(i)` |
| `W = X sum Z_i k_i` | **absent** | Output и productive capability обсуждаются концептуально | Нет fixed task set, additive durations или total work |
| `P` | **absent** | Productive intelligence может стать abundant and scalable | Нет числа concurrent agents, topology, controlled variation или effective parallelism |
| M1 / неделимость | **absent** | Отдельные tasks и occupations упоминаются в cited literature | Нет nonpreemptive jobs, longest-task bound или allocation |
| DAG / `L` | **absent** | Institutions convert capability into outcomes; innovation может иметь complementary stages | Нет precedence graph, duration-weighted paths или critical path |
| `C(P)` | **absent** | Organizational redesign, complementary assets и externalities влияют на value | Нет overhead, возникающего именно с ростом concurrent `P`, и нет multiplier work |
| `a_i^(r)` | **absent** | Autonomous systems выполняют cognitive work | Agent-only elapsed intervals не выделены и не нормированы |
| `h_i^(r)` / `h` | **conceptual boundary only** | Human authority, participation, agency, meaningful work и oversight должны сохраняться | Это normative roles/outcomes, не доля active human task time |
| `H = X sum Z_i h_i` | **absent** | Human attention названа residual scarcity | Нет суммы service intervals, capacity-1 developer или feasible schedule |
| `gamma(P)` | **absent** | Attention scarcity и work intensity упоминаются qualitatively | Нет context switching, agent count, recovery time или functional form |
| Makespan | **absent** | Снижение required human hours используется в мысленном примере | Нет project completion objective, fixed acceptance gate или baseline speedup |
| Throughput / scalable workload | **absent** | Обсуждаются scalable cognition, output и growth regimes | Нет arrival process, workload scaling rule или steady-state throughput |
| Welfare / flourishing | **direct central outcome** | Multidimensional Flourishing Value Profile с distribution, agency, thresholds и risk | Это самостоятельный outcome, который текущая M0--M4 сознательно не оптимизирует |

### Mapping по уровням M0--M4

| Уровень | Возможная связь | Что источник не даёт |
|---|---|---|
| M0 | Напоминает, что productivity/output -- partial signal, а task effects зависят от context | Нет `W/P`, fixed work, `k` или speedup identity |
| M1 | Не рассматривается | Нет indivisible software jobs и allocation |
| M2 | Не рассматривается | Нет DAG, precedence или `L` |
| M3 | Institutional/organizational complements могут влиять на outcomes | Нет integration overhead как функции `P` и нет `C(P)` |
| M4 | Human attention остаётся scarce; agency и meaningful human roles могут быть constraints | Нет time split `a+h`, common-server schedule, `H` или `gamma(P)` |

FVT находится **за пределами scheduling layer**. Она задаёт более широкий
evaluation boundary, внутри которого makespan является лишь одним
instrumental metric. M0--M4, напротив, намеренно решает узкий fixed-time
objective и требует внешней калибровки временных параметров.

## Что источник поддерживает для нашей статьи

1. **Productivity не равна value.** Output, price, profit и labor input являются
   частичными signals и могут расходиться с distribution, agency и durable
   welfare (PDF 2--4, 18, 26--27).
2. **Эффект AI institution-dependent.** Одна technical capability может давать
   противоположные outcomes при разных ownership, governance, access и
   workforce-transition arrangements (PDF 21--23).
3. **Automation следует оценивать по полному переходу.** Уменьшение human hours
   недостаточно без учёта income, health, time use, agency, relationships,
   meaning, skills, ownership и ecological costs (PDF 21--23, 28--29).
4. **Residual scarcities сохраняются.** Даже при abundance productive
   intelligence ограничениями могут оставаться compute, energy, attention,
   care, legitimacy, institutions и ecological capacity (PDF 3, 19, 30).
5. **Человеческое участие не всегда pure overhead.** Authority, participation,
   appeal, learning, dignity и meaningful roles могут быть самостоятельными
   требованиями к хорошему deployment (PDF 21--25).
6. **Primary outcome может требовать vector representation.** Aggregate score
   способен скрыть severe minority harm и threshold violations (PDF 12,
   16--18).

Пункты 1--6 поддерживают framing и limitations. Они не подтверждают формулы или
численные параметры M0--M4.

## Что источник не позволяет утверждать

1. Что работа peer-reviewed, accepted или имеет journal publication.
2. Что это systematic review или exhaustive reproducible review economics of
   AI.
3. Что FVT является оценённой эконометрической, general-equilibrium,
   production-function или scheduling model.
4. Что seven propositions эмпирически подтверждены.
5. Что 50% reduction human hours в worked application является наблюдаемым
   effect size.
6. Что AGI обязательно наступит или устранит scarcity; post-AGI задан как
   scenario class.
7. Что human labor будет полностью заменён или что wages/labor share обязательно
   упадут при любых institutional settings.
8. Что productive intelligence является единственным bottleneck.
9. Что human attention -- единственный последовательный resource или главный
   verification bottleneck.
10. Что источник исследует одного developer с несколькими coding agents.
11. Что `P>1` ускоряет work, имеет diminishing returns или finite optimum.
12. Что `scalable intelligence` соответствует scaled-workload theorem.
13. Что можно получить `Z`, `k`, `W`, `P`, `L`, `C(P)`, `h`, `H` или
    `gamma(P)` из FVT.
14. Что institutional dependence FVT численно валидирует режим `r` M0--M4.
15. Что work-replacement pathways задают resource-feasible schedules.
16. Что cited empirical studies становятся собственной quantitative evidence
    автора.
17. Что FVT или RoF уже прошли empirical validation.
18. Что уменьшение `h` всегда повышает net value: source прямо мотивирует
    agency, participation и meaningful work как самостоятельные outcomes.

## Отличие от M0--M4

| Измерение | Ruan / FVT | M0--M4 |
|---|---|---|
| Центральный вопрос | Что считать value при abundant productive intelligence | Когда `P>1` coding agents сокращают fixed-workload makespan |
| Тип работы | Integrative conceptual и normative theory | Детерминированная formal scheduling/scalability model |
| Объект | AI-plus-institution system и societal outcomes | Одна ячейка «developer -- `P` coding agents» |
| Workload | Не фиксирован и не формализован | Заданный набор software tasks с `Z_i` и baseline `X` |
| Automation | Prospective broad task/labor substitution | Task- и mode-specific observed duration factor `k_i^(r)` |
| Parallelism | Abundant/scalable intelligence как macro scenario | Явное число/effective parallelism `P` |
| Dependencies | Institutional conversion pathways | Formal DAG и critical path `L` |
| Human role | Welfare bearer, participant, authority и носитель meaningful activity | Capacity-1 resource со временем `h_i`, суммой `H` и switching penalty |
| Outcome | Multidimensional flourishing profile, distribution, agency, risk | Makespan и speedup относительно sequential no-AI baseline |
| Aggregation | Contextual и constrained; universal scalar отвергается | Scalar completion time при заданном acceptance standard |
| Evidence | Conceptual synthesis и illustrative application | Formal bounds; empirical values должны приходить из внешней calibration |

Работы не конкурируют и не являются близкими формальными предшественниками.
FVT спрашивает, **стоит ли полученный социальный результат производить**, а
M0--M4 -- **сколько времени займёт фиксированный принятый объём работы** при
данной workflow architecture.

## Рекомендация о включении

### Решение для текущего Related Work: исключить

Источник следует исключить из основного Related Work по четырём причинам:

1. Нет прямого предметного соответствия software engineering или coding agents.
2. Нет formal or empirical link к fixed workload, makespan, `P`, scheduling,
   DAG или shared human verification resource.
3. Собственных quantitative findings нет; 50% -- illustrative assumption.
4. Текущий обзор уже требует более близких источников по empirical coding
   productivity, multi-agent scaling, Graham/RCPSP/common-server scheduling и
   human supervisory attention.

Искусственное сопоставление с M0--M4 создало бы ложное впечатление, что FVT
поддерживает `H`, `gamma(P)` или scaling law. Это не так.

### Когда включение станет оправданным

Одна ссылка оправдана в Discussion/limitations, если статья явно добавит хотя
бы один из следующих вопросов:

- почему makespan -- не полная мера developer productivity или deployment
  value;
- почему уменьшение human involvement может конфликтовать с agency,
  understanding, accountability или meaningful work;
- почему одинаковое техническое ускорение даёт разные outcomes при разных
  ownership и transition institutions;
- как перейти от time-only objective к multi-objective evaluation.

В таком месте FVT должна использоваться как normative framework, не как
empirical или mathematical evidence.

## Проверенные claims

Если источник всё же цитируется, безопасны следующие 2--4 claims.

1. Ruan предлагает Flourishing Value Theory, определяющую value как
   counterfactual и distribution-sensitive вклад в durable capabilities людей
   и сообществ to flourish within social and planetary constraints (PDF
   13--15).
2. В FVT price, output и profit остаются полезными, но частичными signals; primary
   object -- multidimensional value profile, а scalar aggregation допускается
   только контекстно и при явных agency, distribution, risk и planetary
   constraints (PDF 16--19).
3. Proposition 4 и worked application утверждают, что одна technical AI
   capability может иметь противоположные value profiles при разных ownership,
   governance и workforce-transition arrangements; пример является
   иллюстративным, не эмпирическим (PDF 21--23).
4. Замещение труда следует оценивать не только по jobs, output или human
   hours, но и по income, agency, relationships, meaning, skills, ownership и
   ecological effects; статья не измеряет эти outcomes на данных (PDF 21--23,
   28--29).

## Короткий вариант встраивания

Для текущего Related Work вставка **не рекомендуется**. Если нужен один абзац в
Discussion/limitations, безопасен следующий вариант:

> Наша модель оптимизирует время завершения фиксированного объёма работ при
> заданном стандарте приёмки и потому не является полной моделью ценности
> внедрения. Ruan (2026) в концептуальной Flourishing Value Theory подчёркивает,
> что одинаковая техническая способность AI может давать противоположные
> общественные результаты при разных ownership, governance и workforce-transition
> arrangements, а сокращение human hours не описывает изменения agency,
> security, relationships и meaningful work. Этот framework не моделирует
> coding agents, parallelism или makespan и не калибрует параметры M0--M4; он
> задаёт внешнюю нормативную границу нашей time-only objective.

## Таблица опорных страниц

| PDF | Раздел / объект | Опорное содержание | Статус свидетельства |
|---:|---|---|---|
| 1 | Cover | Title, subtitle, один автор, affiliation, labels `Preprint` и `Research Article` | Прямые metadata PDF |
| 2--4 | Abstract; Introduction | FVT summary; four separations labor/price/preferences/output; nine contributions; post-AGI value problem | Авторская постановка |
| 4--5 | Conceptual Method and Scope | Integrative conceptual method; selective review; post-AGI как scenario class; framework procedural, не equation-based; formalisation/calibration future work | Прямое описание метода и scope |
| 5--6 | Economics of AI; Growth | GPT/automation literature; effects зависят от substitutability, bottlenecks, production function for ideas, diffusion и reorganisation | Narrative synthesis cited literature |
| 6--8 | Tasks, labor, firms, innovation | Heterogeneous labor evidence; task exposure не равна adoption/job loss; bounded productivity studies; organizational complements | Secondary synthesis, не собственные findings |
| 8--10 | Distribution, data, agents, welfare | Ownership, market power, AI agents, consumer surplus и residual value-theory gap | Secondary synthesis и авторская gap claim |
| 10--13 | Inherited value theories | Decoupling labor/output; price/value divergence; endogenous preferences; limits aggregation/GDP | Концептуальный аргумент |
| 13--15 | FVT definition and architecture | Definition, seven commitments, twelve elements complete value theory | Собственная нормативная framework |
| 15--18 | Societal value; profile; aggregation; risk; floors | AI-plus-institution system; value profile; contextual aggregation; non-compensation; distinction price/output/profit/value | Собственная framework |
| 18--20 | Value frontier; three shifts | Normative frontier; governed abundance; residual bottlenecks; transformation и positive-sum framing | Концептуальный вывод |
| 20--22 | Seven propositions | Price-value divergence, labor/human worth, preference shaping, institution dependence, thresholds, work replacement, regenerative assets | Conceptual propositions, не tested results |
| 22--23 | Worked application | Два institutional pathways; assumed 50% reduction human hours; dimensions transition; longitudinal evaluation argument | Мысленный пример, не empirical evidence |
| 23--25 | Firms and flourishing business | Viability/additionality/flourishing/constraints gates; human complementarity, workforce transition, agency, shared gains | Prescriptive institutional criteria |
| 25--28 | Governments, GDP, governance, markets | National capability accounts; distribution; risk; reversible deployment; limits market/output signals | Policy architecture |
| 28--29 | Empirical Research Agenda | Causal deployments, longitudinal outcomes, work replacement beyond wages, aggregation/risk/governance experiments | Future research, не выполненная evidence |
| 29--30 | Objections and Limitations; Conclusion | Paternalism, comparison, Goodhart, residual scarcity, artificial welfare, political capture; conversion as central problem | Признанные limitations и conclusion |
| 31--35 | References | Corpus economics, welfare, flourishing и AI literature | Secondary pointers; primary claims требуют проверки первоисточников |

## Итог

Ruan предлагает свежую нормативную теорию того, что должно считаться value в
prospective post-AGI economy. Её сильная сторона для нашей статьи -- ясное
разделение technical productivity и broader social outcome: одинаковое
снижение human hours может сопровождаться разными последствиями для security,
agency, meaning, distribution и ecology.

Однако источник периферийно релевантен текущему исследовательскому вопросу. Он
не изучает coding agents, fixed workload, makespan, task decomposition,
parallelism или human verification bandwidth; не содержит собственной
production function, dataset или effect size. Полный mapping к M0--M4 почти
целиком отсутствует, а сходство ограничено общим тезисом о
configuration/institution dependence и напоминанием, что time objective неполна.

Рекомендация: **не включать в ядро Related Work; при необходимости цитировать
один раз в Discussion/limitations как normative boundary, с явной оговоркой о
концептуальном статусе arXiv v1 и отсутствии quantitative validation.**
