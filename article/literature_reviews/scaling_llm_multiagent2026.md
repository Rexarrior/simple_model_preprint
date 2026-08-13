# Sander et al. (2026): архитектурное масштабирование последовательной LLM-MAS и границы переноса на M0-M4

## Назначение и границы обзора

Этот документ разбирает Sander et al. применительно к модели M0-M4 для
fixed-workload makespan звезды «один разработчик - `P` coding agents». Источник
релевантен как свежий эксперимент по масштабированию LLM-driven multi-agent
system: он одновременно рассматривает число специализированных агентов,
сложность workflow, feedback loops, success, token cost, execution time,
timeouts и run-to-run consistency на задачах terminal/system engineering.

Главная граница переноса принципиальна. Экспериментальная архитектура является
**автономным последовательным agent-agent workflow**: в каждый момент активен
один агент, который после завершения передаёт summary следующему. Число
агентных ролей растёт от 1 до 7, но это не означает одновременное исполнение
1, 3, 5 или 7 потоков. Человек может теоретически добавить сообщение в общий
chat, однако в экспериментальном execution loop human supervisor отсутствует.
Поэтому работа информирует прежде всего M2-M3 и гипотезу о конечном полезном
масштабе архитектуры, но не измеряет параллелизм `P` в смысле M0-M4 и не
валидирует M4.

Локальный PDF содержит 8 страниц; основной текст занимает PDF-страницы 1-7,
references начинаются на странице 7 и продолжаются на странице 8. Номера ниже
относятся к PDF-страницам локальной копии.

## Библиография, версия и статус

**Точное название:** “Scaling LLM-Driven Multi-Agent Systems: Design Principles
and Architectural Scalability Analysis”.

**Авторы:** Linus Sander, Fengjunjie Pan, Vahid Zolfaghari, Andre Schamschurko,
Nenad Petrovic, Alois Knoll. Linus Sander и Fengjunjie Pan указаны как авторы с
равным вкладом (PDF 1).

**Аффилиация:** Robotics, Artificial Intelligence and Real-Time Systems, School
of Computation, Information and Technology, Technical University of Munich
(PDF 1).

**Полная ссылка:** Linus Sander, Fengjunjie Pan, Vahid Zolfaghari, Andre
Schamschurko, Nenad Petrovic, and Alois Knoll. “Scaling LLM-Driven Multi-Agent
Systems: Design Principles and Architectural Scalability Analysis.”
arXiv:2607.27942v1 [cs.MA], 2026. DOI:
[10.48550/arXiv.2607.27942](https://doi.org/10.48550/arXiv.2607.27942).

**Проверенная версия:** `arXiv:2607.27942v1 [cs.MA]`, подана 30 июля 2026 года
в 09:50:04 UTC. На дату проверки arXiv показывает только v1. Идентификатор и
дата также напечатаны на первой странице PDF.

**Статус:** arXiv preprint. В PDF и arXiv-записи не указаны journal/conference
venue, принятие или peer review. Поэтому источник нельзя обозначать как
рецензируемую или принятую публикацию. ArXiv показывает DOI как arXiv-issued
DOI с pending registration.

**Локальная копия:**
`simple_model_full/literature/scaling_llm_multiagent2026.pdf`, SHA-256
`d67a50ab014245c05b78c09d90c17aec55a8988111c8fc76b633d63a3a11c157`.

Предлагаемая будущая запись для `references.bib`:

```bibtex
@misc{sander2026scaling,
  author        = {Sander, Linus and Pan, Fengjunjie and Zolfaghari, Vahid and Schamschurko, Andre and Petrovic, Nenad and Knoll, Alois},
  title         = {Scaling {LLM}-Driven Multi-Agent Systems: Design Principles and Architectural Scalability Analysis},
  year          = {2026},
  eprint        = {2607.27942},
  archiveprefix = {arXiv},
  primaryclass  = {cs.MA},
  doi           = {10.48550/arXiv.2607.27942},
  url           = {https://arxiv.org/abs/2607.27942},
  note          = {Version 1, submitted 30 July 2026}
}
```

## Исследовательский вопрос

Нумерованных RQ в PDF нет. Из abstract, introduction, contributions и
experimental design следует основной вопрос:

> Как accuracy, cost, execution time, consistency и использование feedback
> loops меняются при последовательном наращивании сложности одной
> principle-guided LLM-MAS architecture, и зависит ли полезность такого
> масштабирования от capability базовой LLM?

Работа также решает проектную задачу: вывести из prior work четыре принципа
масштабируемой архитектуры и проверить построенный по ним reference workflow на
tool-rich terminal tasks (PDF 1-4).

Это controlled benchmark comparison заранее заданных configurations, но не
чистый dose-response experiment по agent count. В каждом шаге одновременно
меняются число ролей, decomposition, минимальная длина workflow и число
доступных feedback loops.

## Что именно масштабируется

### Архитектурные принципы

Авторы формулируют четыре принципа (PDF 1-3):

1. **Simplicity:** добавлять архитектурную сложность постепенно и только при
   эмпирически установленной необходимости.
2. **Elastic feedback:** агенты сами решают, нужен ли дополнительный feedback
   cycle; универсальное заранее заданное число циклов не предполагается.
3. **Sequential workflow with optional loops:** основной workflow
   последовательный, а циклы возвращают управление на предыдущие стадии.
4. **Summary-based communication:** следующий агент получает не полный trace
   рассуждений, а natural-language summary; accumulated group chat растёт
   линейно по числу выполненных шагов.

### Топология

Reference architecture задаётся directed workflow graph
`G_w=(A,E,s,T)`, где `A` - agent roles, `E` - разрешённые переходы, `s` - start
agent, `T` - terminal agents. Каждый non-terminal agent имеет successor, каждый
non-start agent достижим, а out-degree ограничена тремя. Активный агент сам
выбирает successor через тег в итоговом summary; parser добавляет summary в
общий chat и запускает следующего агента (PDF 3).

Это graph of control flow, допускающий циклы, а не DAG неделимых project jobs.
Shared group chat является общей памятью summaries. Следующий агент получает
весь накопленный chat и работает в том же environment (PDF 3).

### Четыре configurations

| Configuration | Agent roles | Feedback loops | Workflow |
|---|---:|---:|---|
| Singleton | 1 | 0 | Один agent решает task end-to-end |
| MAS-S | 3 | 1 | Solver -> Tester -> Summarizer; Tester может вернуть задачу Solver |
| MAS-M | 5 | 3 | Explorer, Solver, Tester, Approver, Summarizer; Approver может вернуть к Solver/Tester |
| MAS-L | 7 | 5 | Добавлены Sub-Task Planner/Solver и более сложный refinement loop с Tester, Refiner и Approver |

Каждый scaling step добавляет одновременно два agent roles и два loops. В
MAS-L также сильнее декомпозируется solving phase (PDF 4). Поэтому contrast
`1 -> 3 -> 5 -> 7` нельзя приписать одному agent count.

## Метод

### Benchmark и задачи

Все configurations проверяются на Terminal-Bench 2.0, который содержит более
80 end-to-end terminal/system-engineering tasks в изолированных Docker
environments с автоматическими success criteria. В results фактический набор
назван набором из 89 unique tasks. Задачи включают OS operations, server
management и software-engineering challenges, требуют multi-turn interaction,
исследования незнакомого environment, выполнения tools и исправления решения
по обратной связи (PDF 3, 5).

Агентам доступны четыре tools (PDF 3-4):

- Shell: одна Bash-команда в non-persistent environment;
- Terminal: persistent `tmux`, ввод keystrokes и окно `128 x 16`;
- Python: определение и выполнение полного Python script;
- Search: DuckDuckGoSearch через LangChain, top 4 results.

Это автономные benchmark tasks. Они не образуют один software project с общей
датой завершения, распределением jobs между параллельными executors и
человеческой приёмкой.

### Модели

Methods называют три модели одной family (PDF 4):

- GPT-5-nano;
- GPT-5-mini;
- GPT-5.3-Codex.

Полный scaling grid из четырёх configurations выполнен для GPT-5-nano и
GPT-5-mini. GPT-5.3-Codex проверен только в MAS-M как отдельная
state-of-the-art/leaderboard reference: пять runs, mean accuracy `0.715`
(PDF 5). Поэтому abstract и conclusion корректно говорят о двух LLMs в
основном scalability analysis, хотя methods перечисляет три используемые
модели.

Точные immutable model snapshot IDs, temperature, reasoning effort и прочие
inference parameters в PDF не приведены. Приписывать результат всей GPT-5
family или конкретным production endpoints нельзя.

### Prompts

Роли реализованы только system prompts. Prompts создавались итеративно через
drafting, LLM-assisted refinement и manual local Docker runs на простых test
scripts; авторы стремились оставить их простыми и domain-general (PDF 4).
Полный protocol prompt tuning, число итераций и независимый validation set в
PDF не описаны.

### Runs и budgets

Для каждой пары configuration x GPT-5-mini/GPT-5-nano выполнено от трёх до
пяти Terminal-Bench runs. MAS-M для обеих моделей запускался пять раз для
leaderboard submission; MAS-M/GPT-5.3-Codex также запускался пять раз (PDF 5).

Matched token, call, monetary или wall-clock budget между configurations не
задан. Более сложные systems делают больше calls и потребляют больше tokens до
завершения или terminal-bench timeout. Точное значение timeout, hardware,
parallel execution policy и абсолютные token/time budgets PDF не сообщает.

### Outcomes

1. **Accuracy:** доля trials с полным task success; Terminal-Bench reward равен
   нулю, если не прошёл хотя бы один unit test.
2. **Test-weighted accuracy:** средняя доля пройденных tests, допускающая
   partial success.
3. **Cost proxies:** LLM calls, prompt tokens, completion tokens и overall
   execution time. В итоговой таблице cost trend основан только на average
   completion tokens.
4. **Consistency:** среди tasks, решённых хотя бы в одном run, доля решённых во
   всех runs данной configuration.
5. **Loop utilization:** фактическое использование доступных feedback edges.
6. **AgentTimeout errors:** число прерываний за превышение task timeout.

Денежная стоимость не опубликована. Execution time измеряется, но численные
latency values в results не приведены (PDF 5-6).

## Точные результаты

### Binary task accuracy, completion-token cost trend и consistency

Table I сообщает следующие агрегаты (PDF 6):

| Model | System | Accuracy | Stepwise accuracy delta | Reported cost trend | Consistency |
|---|---|---:|---:|---:|---:|
| GPT-5-mini | Singleton | `0.296` | - | baseline | `42%` |
| GPT-5-mini | MAS-S | `0.341` | `+15.2%` | `+1x` | `46%` |
| GPT-5-mini | MAS-M | `0.348` | `+2.2%` | `+1.4x` | `36%` |
| GPT-5-mini | MAS-L | `0.315` | `-9.7%` | `+3.2x` | `46%` |
| GPT-5-nano | Singleton | `0.097` | - | baseline | `11%` |
| GPT-5-nano | MAS-S | `0.090` | `-7.7%` | `+1.1x` | `11%` |
| GPT-5-nano | MAS-M | `0.105` | `+16.7%` | `+1.6x` | `5%` |
| GPT-5-nano | MAS-L | `0.105` | `+0.0%` | `+3.4x` | `5%` |

Три уточнения обязательны:

1. `Acc. delta` является **пошаговым** относительным изменением от предыдущей
   configuration, а не всегда изменением относительно Singleton.
2. Это изменение success rate, а не времени. `+15.2%` нельзя назвать
   `15.2% faster` или преобразовать в `k`.
3. Table caption определяет cost trend через average completion tokens, но не
   приводит absolute token counts и не раскрывает достаточно строго смысл
   знака `+` в обозначениях вида `+1x`. Поэтому безопасно цитировать сами
   labels, не разворачивая `+1x` в самостоятельно вычисленный total multiplier.

Для GPT-5-mini peak binary accuracy достигается в MAS-M с 5 roles/3 loops, а
MAS-L падает ниже MAS-S. Для GPT-5-nano монотонного scaling gain нет: итоговые
значения остаются около `0.09-0.105`, несмотря на рост cost trend (PDF 5-6).

### Test-weighted accuracy

При partial-credit outcome картина для GPT-5-mini сохраняется, но первый gain
уменьшается с `15.2%` до `3.0%` (PDF 5):

| GPT-5-mini configuration | Mean | SD |
|---|---:|---:|
| Singleton | `0.514` | `0.014` |
| MAS-S | `0.530` | `0.037` |
| MAS-M | `0.543` | `0.024` |
| MAS-L | `0.518` | `0.013` |

Для GPT-5-nano опубликованы:

- Singleton: `0.328 +/- 0.072`;
- peak MAS-M: `0.351 +/- 0.029`;
- MAS-L: `0.320 +/- 0.114`.

Точное test-weighted значение MAS-S для GPT-5-nano в тексте не напечатано.

Различие binary и test-weighted effects показывает зависимость вывода от
acceptance rule: apparent gain значительно больше при all-tests-pass outcome,
чем при средней доле пройденных tests. Для M0-M4 это аргумент в пользу
фиксированного quality gate при измерении duration, но не численная калибровка
времени.

### Cost, latency и timeouts

Авторы сообщают, что LLM calls, completion tokens и execution time монотонно
растут от Singleton к MAS-L и в целом растут приблизительно линейно с
architectural complexity (PDF 5-6). Однако:

- absolute calls/tokens/time не опубликованы;
- prompt-token trend отдельно не показан;
- dollar cost отсутствует;
- нет cost-normalized confidence intervals;
- не построена fitted scaling law, slope или `R^2`;
- архитектурная сложность не разложена на count, roles, loops и path length.

AgentTimeout errors резко растут (PDF 5-6):

| Model | Singleton mean | MAS-L mean |
|---|---:|---:|
| GPT-5-mini | `3.33` | `50.00` |
| GPT-5-nano | `1.00` | `37.67` |

PDF называет эти значения means числа AgentTimeout errors, но не даёт для них
SD/CI и не вполне явно фиксирует aggregation unit. Авторы связывают падение
MAS-L прежде всего с более длинным minimum execution path и timeout exposure.
Поэтому результат показывает latency/timeout cost усложнения, а не выигрыш от
параллельного выполнения.

### Run-to-run consistency

Для GPT-5-mini число unique tasks, решённых хотя бы один раз, выросло с `38` у
Singleton до `47` у MAS-M, затем снизилось до `39` у MAS-L. Число tasks, впервые
решённых на новом scaling level, уменьшалось: `8` у MAS-S, `6` у MAS-M, `2` у
MAS-L. Менее половины решённых tasks воспроизводились во всех runs каждой
configuration (PDF 5, 7).

Для GPT-5-nano Singleton и MAS-S решили во всех runs по две tasks, MAS-M и
MAS-L - по одной. Большинство successes возникали только в одном из трёх runs;
число newly solved tasks составляло `8`, `1`, `3` для MAS-S, MAS-M и MAS-L
соответственно (PDF 5).

Table I даёт consistency `42/46/36/46%` для GPT-5-mini и `11/11/5/5%` для
GPT-5-nano (PDF 6). Сравнение требует осторожности: metric определяется как
success во **всех** runs, а MAS-M запускался пять раз, тогда как полный design
использует от трёх до пяти runs. Разная строгость события «успех во всех runs»
частично confounds consistency percentages. Работа не строит per-task success
probability или reliability-adjusted estimator.

### Использование feedback loops

Доступность loop не означает его фактическое использование (PDF 6):

- в MAS-S `120/167` (`71.9%`) GPT-5-mini trials и `92/180` (`51.1%`)
  GPT-5-nano trials не использовали loop;
- в MAS-M без loops прошли `180/257` (`70.0%`) GPT-5-mini trials и `74/164`
  (`45.1%`) GPT-5-nano trials;
- два Approver-based loops MAS-M были задействованы лишь в `19` mini и `14`
  nano task runs;
- в MAS-L почти все trials использовали хотя бы один loop, преимущественно
  SubTaskSolver-SubTaskPlanner;
- Refiner-Tester loop сработал `17` раз для mini и `20` раз для nano;
- Approver loops срабатывали один-два раза на model, а Approver-Tester ни разу
  не сработал для GPT-5-nano.

Это поддерживает task-adaptive feedback как идею, но не показывает, что loop
causally улучшает task: loop activation выбирает сам agent и потому зависит от
сложности и неудачного хода run.

## Scaling law, saturation и capability moderator

Работа обнаруживает **peak at intermediate architectural complexity**, но не
оценивает математический scaling law. Для GPT-5-mini binary и test-weighted
accuracy максимальны в MAS-M, после чего падают в MAS-L; cost и timeout растут.
Для GPT-5-nano accuracy почти не улучшается, хотя loops и communication
используются и cost растёт (PDF 5-7).

Авторы формулируют это как minimum base-model capability prerequisite. Строго
по данным установлен только contrast двух full-grid model tiers:

- GPT-5-mini получает ограниченный peak-then-decline gain;
- GPT-5-nano не показывает устойчивого gain;
- GPT-5.3-Codex проверен только в MAS-M, поэтому не даёт третью scaling curve.

Численный threshold capability не определён, capability не измерена внешней
continuous scale, interaction `model capability x agent count` не оценена. В
тексте нет regression, hypothesis test или confidence interval для moderator.
Следовательно, безопасный claim - «польза масштабирования различалась между
двумя model tiers», а не «существует универсальный порог capability».

Насыщение также нельзя приписать одному `P`: MAS-L одновременно имеет больше
roles, loops, summaries, minimum stages, opportunities error propagation и
timeout exposure.

## Sequentiality и decomposability как moderators

### Что работа показывает

1. Архитектура намеренно последовательна: shortest path должен обслуживать
   простые tasks, loops - более сложные (PDF 2-3).
2. MAS-L декомпозирует solving phase на Planner и Solver, но это увеличивает
   minimum execution path и timeout exposure (PDF 4, 6).
3. Дополнительные feedback branches часто не используются, особенно более
   сильной GPT-5-mini (PDF 6).
4. Авторы интерпретируют peak как баланс дополнительной specialization и
   verification против communication, error propagation и latency (PDF 6-7).

### Чего работа не проверяет

- tasks не размечены по independent/decomposable/sequential structure;
- нет task-level decomposition score;
- нет interaction между task structure и configuration;
- нет precedence DAG jobs и duration-weighted critical path;
- не сравниваются parallel и sequential topology при одинаковых roles;
- не рандомизируется decomposition одной и той же task;
- не показано, для каких именно Terminal-Bench task classes MAS-M помогает.

Поэтому источник поддерживает лишь общий mechanism claim: архитектурная
декомпозиция имеет издержки и конечный полезный уровень. Он не даёт прямого
эмпирического moderator effect для нашего `L`.

## Статистическая неопределённость

1. Для test-weighted accuracy приведены mean и SD across runs; для headline
   binary accuracy Table I не приводит SD или CI (PDF 5-6).
2. Confidence intervals, `p`-values, preregistered hypotheses и power analysis
   отсутствуют.
3. Tasks повторяются между runs и configurations, но paired/hierarchical model
   на task level не построена.
4. Stepwise percentages являются descriptive ratios агрегированных accuracy,
   а не causal effect estimates с uncertainty.
5. Consistency metric зависит от числа runs, которое различается между
   configurations.
6. Timeout means приведены без variance и точного aggregation description.
7. Claim «approximately linear cost growth» не подкреплён fitted model.
8. Claim о capability threshold основан на двух полных curves и не содержит
   численной границы.

Таким образом, работа даёт полезные descriptive scaling traces, но не точный
статистический закон насыщения.

## Человеческая роль

Human feedback упоминается только как возможная функция shared group chat:
сообщение пользователя может быть добавлено в историю и станет доступно
следующим агентам (PDF 3). В actual benchmark procedure не сообщаются human
interventions, review, approvals или corrections.

В частности, не измерены:

- developer active time;
- task specification time;
- human review/rework;
- очереди результатов на приёмку;
- non-overlapping human intervals;
- context switching между concurrent tasks;
- maximum human fan-out;
- human acceptance beyond automated Terminal-Bench tests.

Tester и Approver являются LLM agents. Их нельзя трактовать как developer или
как численную оценку человеческой доли `h`.

## Полный mapping `Z,k,r,W,P,L,C(P),h,H,gamma(P)`

Здесь **direct** означает близкий измеряемый объект, **conceptual** - полезный
механизм без численной совместимости, **mismatch** - похожее название с другой
физической семантикой, **absent** - объект не измеряется.

| Поле M0-M4 | Статус | Ближайший объект у Sander et al. | Точная граница переноса |
|---|---|---|---|
| `Z_i` / `Z` | **conceptual** | 89 Terminal-Bench tasks различаются по сложности и числу tests | Нет no-AI baseline duration `Z_i X`, единой complexity scale или project weights |
| `k_i^(r)` / `k` | **absent для M0-M4** | Есть accuracy и качественный рост execution time относительно autonomous Singleton | Нет human no-AI denominator, absolute time results и fixed-quality duration ratio; success delta не равен `k` |
| режим `r` | **conceptual, semantic mismatch** | Singleton/MAS-S/MAS-M/MAS-L задают разные autonomous agent-agent workflows | `r` M0-M4 задаёт способ human-agent выполнения task; здесь human mode отсутствует и roles/loops меняются вместе |
| `W = X sum Z_i k_i` | **absent** | Один и тот же benchmark corpus повторяется для configurations | Corpus не планируется как единый fixed workload с общей completion boundary; token sum не равна duration work |
| `P` | **nominal count, mismatch** | Число agent roles равно `1,3,5,7` | Агенты активируются последовательно; effective concurrent parallelism не меняется как `P`; count confounded с loops/roles/path length |
| `L` / M2 | **conceptual, mismatch** | Directed workflow имеет shortest path и optional cycles; MAS-L имеет более длинный minimum path | Это control-flow graph agents, не precedence DAG project jobs; weighted critical-path duration не вычисляется |
| `C(P)` / M3 | **conceptual support** | Calls, completion tokens, execution time и timeouts растут с architectural complexity; summaries/loops создают communication work | Нет чистой функции от concurrent `P`, elapsed multiplier, fitted law или separation count from topology; shared-code merge cost отдельно не измерен |
| `h_i^(r)` / `h` | **absent** | Human может теоретически написать в group chat; Tester/Approver выполняют verification | Human не участвует в experimental runs; LLM review не является human-active interval |
| `H = X sum Z_i h_i` | **absent** | Нет близкого measured resource | Не наблюдаются task-level human intervals и capacity-1 developer |
| `gamma(P)` | **absent** | Agent context растёт через accumulated summaries | Это agent-side context/communication, не human switching penalty между concurrent streams |
| Makespan | **absent как project outcome** | Overall execution time отдельного benchmark trial измерялось, но не опубликовано численно | Нет fixed set jobs, parallel schedule, project finish и human resource feasibility |

### Mapping к уровням M0-M4

| Уровень | Что требует M0-M4 | Что даёт источник | Вердикт |
|---|---|---|---|
| M0 | Fixed duration work `W`, concurrent `P`, `W/P` | Один benchmark corpus и autonomous configurations с 1-7 roles | Не валидирует `W/P`: workflow последовательный и duration ratio не опубликован |
| M1 | Неделимые jobs, assignment по executors, longest-job bound | Discrete benchmark tasks | Tasks являются независимыми trials, а не jobs одного schedule; allocation отсутствует |
| M2 | Precedence DAG и critical path `L` | Directed agent control workflow с loops и растущим minimum path | Поддерживает механизм sequential latency, но graph и `L` имеют другой смысл |
| M3 | Scale-dependent integration multiplier `C(P)` | Рост calls/tokens/time/timeouts, peak-then-decline accuracy | Сильная концептуальная опора coordination overhead, но без идентификации функции `C(P)` |
| M4 | Один developer, `k=a+h`, `H`, verification windows и `gamma(P)` | Human execution resource отсутствует | Не поддерживает M4 количественно и не является one-human-many-agents experiment |

## Что источник поддерживает для нашей статьи

1. **Agent count сам по себе недостаточен.** Результат зависит от capability и
   полного workflow; больше ролей и loops не дают монотонного gain (PDF 5-7).
2. **Полезный архитектурный масштаб конечен.** Для GPT-5-mini peak возникает в
   MAS-M, после чего MAS-L теряет accuracy при большем token/time cost и числе
   timeouts (PDF 5-6).
3. **Coordination overhead наблюдаем.** LLM calls, completion tokens и
   execution time растут с complexity, а timeout failures увеличиваются до
   mean `50.00`/`37.67` в MAS-L (PDF 5-6).
4. **Base-model capability модерирует benefit.** GPT-5-mini показывает
   ограниченный peak, GPT-5-nano - почти плоскую accuracy curve при растущем
   cost (PDF 5-7).
5. **Дополнительная decomposition может удлинить последовательный путь.** В
   MAS-L Planner/Solver split добавляет minimum stages и timeout exposure
   (PDF 4, 6).
6. **Feedback должен быть elastic.** Многие доступные loops фактически не
   используются; фиксированное добавление cycles не равно полезной работе
   (PDF 2, 6).
7. **Mean success недостаточен.** Consistency остаётся ниже 50% во всех
   configurations, несмотря на более высокую mean accuracy части systems
   (PDF 5-7).
8. **Acceptance rule меняет apparent effect.** Первый mini gain равен `15.2%`
   по all-tests-pass accuracy и только `3.0%` по test-weighted accuracy
   (PDF 5).
9. **Summary communication ограничивает рост shared context конструктивно.**
   Один summary на sequential step даёт линейный рост group-chat history, хотя
   его фактическая экономия против full traces отдельно не ablated (PDF 3).

Пункты 2-5 поддерживают qualitative форму M3 и идею конечного optimum, но не
калибруют `C(P)` и не являются доказательством формулы M4.

## Что источник не позволяет утверждать

1. Что 3, 5 или 7 agents дают соответствующий concurrent parallelism.
2. Что MAS-M уменьшает execution time или makespan: paper говорит о росте
   execution time и не печатает exact latency values.
3. Что GPT-5-mini agents ускорили работу на `15.2%`: это изменение success rate.
4. Что completion-token labels `+1x...+3.4x` являются speedup или elapsed-time
   multiplier.
5. Что найден scaling law: fitted functional form и uncertainty отсутствуют.
6. Что optimum равен пяти agents вообще; это peak одной confounded architecture
   на одном benchmark и двух full-grid model tiers.
7. Что существует численно установленный minimum capability threshold.
8. Что agent count causal: вместе с count меняются роли, loops, decomposition и
   minimum path.
9. Что sequential/decomposable task structure является оценённым moderator:
   task-level interaction analysis отсутствует.
10. Что directed workflow graph равен project precedence DAG или что его
    shortest/minimum path равен нашему critical path `L`.
11. Что reported cost trend даёт `C(P)`: nominal role count не является нашим
    concurrent `P`, а elapsed multiplier не оценён.
12. Что Tester/Approver заменяют человеческую верификацию или измеряют `h`.
13. Что human feedback channel означает human-in-the-loop evaluation.
14. Что можно оценить `H`, intervention windows, fan-out или `gamma(P)`.
15. Что более высокая mean accuracy означает production reliability: менее
    половины solved tasks воспроизводились во всех runs.
16. Что consistency percentages полностью сопоставимы при разном числе runs.
17. Что результат обобщается на repository-scale coding, long-horizon project
    work, shared code branches, merge conflicts или maintainability.
18. Что GPT-5.3-Codex подтверждает ту же scaling curve: проверена только MAS-M.
19. Что источник peer-reviewed или accepted.

## Отличие от M0-M4

| Измерение | Sander et al. | M0-M4 |
|---|---|---|
| Центральный вопрос | Как сложность автономной sequential MAS меняет accuracy, cost и reliability | Когда один developer с concurrent coding agents сокращает fixed-workload makespan |
| Топология | Agent-to-agent directed control workflow, shared summary chat, optional loops | Star topology: один capacity-1 human и `P` agent executors |
| Исполнение | Один active agent за шаг, последующая передача control | До `P` agent tasks могут выполняться одновременно |
| Scaling axis | `1/3/5/7` roles вместе с `0/1/3/5` loops и новой decomposition | Explicit effective parallelism `P` при отдельно заданных task durations и overhead |
| Workload | 89 independent benchmark tasks, повторяемых по configurations | Один fixed set project jobs с общей completion boundary |
| Outcome | Success, partial-test success, token/call/time proxies, consistency | Elapsed project makespan и speedup относительно sequential human baseline |
| Dependencies | Workflow между agent roles, допускающий cycles | Precedence DAG между jobs и duration-weighted critical path `L` |
| Coordination | Summaries, loops, extra calls/tokens, error propagation и timeouts | Agent integration `C(P)` плюс human switching `gamma(P)H` |
| Human | Не участвует в runs; может опционально писать в chat | Specification, review и correction формируют `h_i` и общий `H` |
| Quality gate | Docker tests; all-or-nothing и test-weighted outcomes | Acceptance/rework должны входить в calibrated task duration |
| Uncertainty | Repeated runs, descriptive means/SD, consistency | Коэффициенты могут быть stochastic; требуется duration uncertainty/calibration |

Источник находится рядом с M2-M3, но не с M4. Он показывает, что больше
agentic stages и feedback opportunities могут повысить success только до
промежуточной точки, после чего token/time/timeout costs доминируют. M0-M4
решает другой вопрос: можно ли сократить elapsed completion time фиксированного
software workload за счёт **одновременных** agent streams при одном
последовательном human resource.

## Проверенные claims для Related Work

### Безопасные claims

1. Sander et al. построили summary-based directed LLM-MAS с последовательным
   workflow и optional loops и сравнили configurations с 1, 3, 5 и 7 agent
   roles на 89 Terminal-Bench tasks (PDF 3-5).
2. В полном scaling grid GPT-5-mini binary accuracy менялась
   `0.296 -> 0.341 -> 0.348 -> 0.315`, а GPT-5-nano -
   `0.097 -> 0.090 -> 0.105 -> 0.105`; stepwise deltas составляли
   `+15.2%, +2.2%, -9.7%` и `-7.7%, +16.7%, 0.0%` соответственно
   (PDF 5-6).
3. Table I одновременно показывает рост completion-token cost trend до
   `+3.2x/+3.4x` в MAS-L и consistency не выше `46%` для mini и `11%` для nano
   (PDF 6).
4. Test-weighted gain Singleton -> MAS-S для GPT-5-mini составил только `3.0%`,
   хотя all-tests-pass gain был `15.2%`, что показывает sensitivity к метрике
   success (PDF 5).
5. Mean AgentTimeout errors вырос от `3.33` до `50.00` для GPT-5-mini и от
   `1.00` до `37.67` для GPT-5-nano между Singleton и MAS-L; авторы связывают
   падение MAS-L с более длинным minimum path и timeout exposure (PDF 5-6).
6. Масштабирование не улучшило run-to-run consistency: менее половины solved
   tasks воспроизводились во всех runs каждой configuration (PDF 5-7).
7. Данные поддерживают capability-dependent, peak-then-decline pattern, но не
   чистый agent-count law: count, roles, loops и decomposition изменяются вместе,
   а execution остаётся последовательным.
8. Human supervisor в benchmark runs отсутствует, поэтому источник не
   подтверждает M4 и не оценивает `h`, `H` или `gamma(P)`.

### Claims, которых следует избегать

- «Семь агентов работают параллельно медленнее пяти».
- «Пять агентов ускоряют software engineering на 17%».
- «Авторы нашли оптимальное число coding agents `P=5`».
- «`C(P)` растёт линейно с коэффициентом из Table I».
- «Архитектура подтверждает critical-path bound M2».
- «GPT-5 должна превышать установленный capability threshold».
- «Human feedback входит в эксперимент».
- «Consistency равна вероятности success production task».

## Предлагаемое место в статье

Источник лучше вставить в подраздел **scalability laws and coordination
overhead** сразу после Kim et al. Он даёт более узкий software/system-engineering
пример с явным ростом calls/tokens/timeouts и peak at intermediate complexity.
Затем нужно провести границу: обе работы изучают autonomous LLM coordination,
тогда как M4 относится к human-supervised concurrent coding streams.

### Короткий вариант встраивания

> Sander et al. (2026) исследовали архитектурное масштабирование автономной
> LLM-MAS на 89 Terminal-Bench tasks, последовательно увеличивая workflow от
> одного agent до configurations с 3, 5 и 7 специализированными roles и
> optional feedback loops. Для GPT-5-mini binary success достиг максимума при
> пяти roles (`0.348` против `0.296` у Singleton), затем снизился до `0.315` при
> семи roles; для GPT-5-nano устойчивого роста не наблюдалось (`0.097-0.105`).
> При этом completion-token cost trend, execution time и число timeouts росли,
> а consistency solved tasks оставалась ниже 50%. Результат поддерживает
> capability-dependent diminishing returns и необходимость учитывать
> coordination overhead, но не является экспериментом по параллелизму: agents
> активируются последовательно, а count одновременно меняется с ролями,
> decomposition и числом loops. Человек в execution loop отсутствует, поэтому
> работа не калибрует `P`, `C(P)` или M4 для звезды «developer - coding agents».

### Вариант для discussion/limitations

> Agent count нельзя использовать как proxy эффективного параллелизма без
> описания control flow. В Sander et al. nominal scale растёт от 1 до 7 agents,
> однако execution остаётся последовательным: дополнительные роли удлиняют
> minimum path, увеличивают token consumption и резко повышают timeout exposure.
> Для нашей модели это пример различия между числом доступных исполнителей и
> фактически реализованным `P`; benefit должен оцениваться по resource-feasible
> schedule и elapsed makespan, а не по числу agent identities.

## Таблица доказательных страниц

| PDF-страница | Раздел / объект | Опорное содержание | Статус свидетельства |
|---:|---|---|---|
| 1 | Title; Abstract; Introduction | Exact title/authors/version; four principles; four configurations; two-model scaling claim; capability, cost, peak и consistency summary | Прямые metadata и author claims |
| 2 | Related Work; Design Principles P1-P3 | Bounded architecture-dependent gains; simplicity; elastic feedback; sequential workflow with optional loops | Conceptual basis |
| 3 | P4; Reference Architecture; Benchmark | Summary-only communication; shared accumulated chat; optional human message; directed workflow constraints; agent-selected successor; Terminal-Bench and tools | Прямая architecture specification |
| 4 | Tools; Prompts; Models; Configurations | Four tools; iterative prompt development; GPT-5-nano/mini/5.3-Codex; exact 1/3/5/7 roles and 0/1/3/5 loops; role decomposition | Прямой methods evidence |
| 5 | Metrics; Procedure; Accuracy; Consistency; Costs | Outcome definitions; 3-5 runs; MAS-M five runs; test-weighted means/SD; Codex `0.715`; unique/consistent tasks; monotonic calls/tokens/time; beginning timeout counts | Прямые methods и results |
| 6 | Figure 3; Loop utilization; Table I; Discussion | Exact binary accuracy, stepwise deltas, cost trends, consistency; loop denominators; timeout continuation; capability prerequisite; peak MAS-M and reasons | Главная quantitative evidence page |
| 7 | Figure 4; Discussion; Conclusion | Consistency below 50%; error reinforcement; practical guidelines; conclusion and scope | Interpretation and author conclusions |
| 7-8 | References | Prior literature cited by the source | Secondary pointers; не evidence собственных results |

## Итоговая оценка релевантности

Источник полезен как компактная современная эмпирика того, что architectural
scaling LLM-MAS имеет конечную отдачу: дополнительная specialization и
verification могут повысить success у более сильной base model, но одновременно
увеличивают calls, tokens, execution time, timeout risk и opportunities for
error propagation. Особенно ценны exact contrast GPT-5-mini/GPT-5-nano,
peak MAS-M, различие binary/test-weighted accuracy и consistency ниже 50%.

Доказательная сила для M0-M4 ограничена topology mismatch. В source нет
concurrent agent execution, fixed project makespan, human no-AI baseline,
developer review time или capacity-1 human bottleneck. Кроме того, count
полностью смешан с roles, loops и decomposition, а exact latency/cost budgets и
inferential uncertainty не опубликованы. Поэтому работу следует использовать
для качественного обоснования `C(P)`-подобного overhead, finite optimum и
различия nominal agent count/effective parallelism, но не как калибровку
`P`, `k`, `L`, `h`, `H` или `gamma(P)` и не как evidence M4.
