# Liu et al. (2026): production telemetry GitHub Copilot и граница между agent workload и developer productivity

## Назначение и главный вывод

Этот документ разбирает Liu et al. применительно к модели M0--M4 для
fixed-workload makespan звезды «один разработчик - `P` coding agents».
Источник важен как крупномасштабное описание того, как production coding agent
чередует LLM calls и tools, насколько его внутреннее исполнение последовательно,
где возникают retry loops, как распределены session/turn durations и насколько
неоднородны наблюдаемые workflows и пользователи.

Главная граница переноса: это **observational systems telemetry study**, а не
исследование developer productivity. Авторы наблюдают client-side structural
events GitHub Copilot coding agent, но не содержимое prompts, исходный код,
семантику и границы software tasks, acceptance результата, качество или no-AI
counterfactual. Поэтому session duration, token volume, LLM parallelism и tool
failure нельзя превращать в `k`, fixed-workload makespan или causal effect на
производительность разработчика.

Локальный PDF содержит 20 страниц. Основной текст и выводы занимают PDF-страницы
1--19, references продолжаются на страницах 19--20. Напечатанная нумерация
совпадает с номерами PDF. Все ссылки на страницы ниже относятся к локальной
копии.

## Библиография, версия и статус

### Точное название и расхождение записей

В источнике есть небольшое, но библиографически значимое расхождение:

- **канонический title в записи arXiv:** “Agentic Coding in the Wild:
  Characterizing GitHub Copilot **Traces** at Production Scale”;
- **title на титульной странице PDF:** “Agentic Coding in the Wild:
  Characterizing GitHub Copilot at Production Scale” (PDF с. 1).

Слово `Traces` присутствует в metadata arXiv, но отсутствует на видимом титуле
локального PDF и в HTML-rendered title исходного TeX. Для библиографической
записи безопаснее использовать title arXiv с `Traces`, одновременно сохраняя в
source note это расхождение.

### Авторы и аффилиации

**Авторы:** Banruo Liu, Haoran Qiu, Íñigo Goiri, Rodrigo Fonseca, Ricardo
Bianchini, Esha Choukse.

На титуле указаны UIUC для Banruo Liu, Microsoft Azure Research для Haoran Qiu,
Íñigo Goiri, Rodrigo Fonseca и Esha Choukse, Microsoft Azure для Ricardo
Bianchini. Сноска сообщает, что работа Banruo Liu выполнена во время internship
в Microsoft Azure Research (PDF с. 1).

### arXiv и статус

**Полная рабочая ссылка:** Banruo Liu, Haoran Qiu, Íñigo Goiri, Rodrigo Fonseca,
Ricardo Bianchini, and Esha Choukse. “Agentic Coding in the Wild:
Characterizing GitHub Copilot Traces at Production Scale.” arXiv:2608.00101v1
[cs.AI], 2026. DOI:
[10.48550/arXiv.2608.00101](https://doi.org/10.48550/arXiv.2608.00101).

**Проверенная версия:** `arXiv:2608.00101v1`, подана 30 июля 2026 года в
20:51:51 UTC. Primary category - `cs.AI`, secondary category - `cs.LG`. На 4
августа 2026 года submission history содержит только v1. На первой странице PDF
напечатано `arXiv:2608.00101v1 [cs.AI] 30 Jul 2026`.

**Статус:** arXiv preprint. В PDF и записи arXiv не указаны peer-reviewed venue,
acceptance или издательская версия. Источник нельзя называть рецензируемой или
принятой публикацией.

**Лицензия arXiv:** CC BY-NC-SA 4.0.

**Локальная копия:**
`agentic_coding_wild2026.pdf`, SHA-256
`01b4a5e0674e385807635629baf1d6c8399cacb4a049103f07eabd4dd266f782`.

Предлагаемая BibTeX-запись:

```bibtex
@misc{liu2026agenticcoding,
  author        = {Liu, Banruo and Qiu, Haoran and Goiri, {\'I}{\~n}igo and Fonseca, Rodrigo and Bianchini, Ricardo and Choukse, Esha},
  title         = {Agentic Coding in the Wild: Characterizing {GitHub Copilot} Traces at Production Scale},
  year          = {2026},
  eprint        = {2608.00101},
  archiveprefix = {arXiv},
  primaryclass  = {cs.AI},
  doi           = {10.48550/arXiv.2608.00101},
  url           = {https://arxiv.org/abs/2608.00101},
  note          = {Version 1, submitted 30 July 2026}
}
```

## Фактический предмет и исследовательские вопросы

### Предмет

Работа характеризует **нагрузку на serving infrastructure**, создаваемую
GitHub Copilot coding agent. Центральные объекты - LLM inference, tool execution,
KV-cache lifecycle, context compaction, client-observed latency, resource idle
periods и различия resource footprint между типами использования.

Это не исследование:

- времени выполнения заранее определённых software issues;
- числа принятых изменений или pull requests;
- качества, correctness или maintainability кода;
- производительности разработчика относительно no-AI baseline;
- project makespan одного fixed workload;
- causal effect одного или нескольких coding agents.

### RQ

Нумерованных research questions в PDF нет. Из abstract, introduction,
contributions и структуры анализа следуют четыре фактических вопроса:

1. Чем production coding-agent workload структурно отличается от chat/completion
   workload на уровне sessions, turns, LLM calls и tool calls?
2. Как session structure, turn boundaries, model switches и context compaction
   влияют на KV-cache reuse и client-observed execution latency?
3. Как tool mix, failures, retries и ограниченный runtime parallelism формируют
   resource demand и tail latency?
4. Насколько неоднородны user/workflow patterns и можно ли по turn-level signals
   предсказывать длинные idle periods для resource reclamation?

Тип доказательства для первых трёх вопросов - descriptive observational analysis
production telemetry. Для четвёртого есть отдельная out-of-time predictive
evaluation idle-time model. Ни одна часть не является randomized productivity
experiment.

## Dataset, provenance и privacy

### Источник и период

Данные получены из anonymized client-side telemetry GitHub Copilot coding agent
в Visual Studio и VS Code за первую неделю июня 2026 года. Traces происходят из
нескольких регионов США и покрывают не более трёх часовых поясов (PDF с. 3).

Авторы пишут, что анализируют sampled subset anonymized traces, кроме расчёта
некоторых aggregate metrics. Sampling fraction, полный sampling frame, правила
включения sessions/users, weighting и handling missing telemetry не раскрыты.
Подпись Figure 1 называет показанный subset uniformly sampled, но этого
недостаточно для полного selection audit (PDF с. 3--4).

### Объём корпуса

Table 3 сообщает (PDF с. 3):

| Единица | Объём |
|---|---:|
| Sessions | `13.5M` |
| User turns | `95.1M` |
| Anonymized users | `3.2M` |
| Models | `27+` |
| Tools | `45+` |
| LLM calls | `760.5M` |
| Tool calls | `774.7M` |
| Prompt tokens | `44.9T` |
| Completion tokens | `39.3B` |

Abstract и introduction округляют corpus до `13M sessions`, `761M LLM calls`,
`775M tool invocations` и `95T tokens` (PDF с. 1). Последнее число не
согласуется непосредственно с Table 3: `44.9T prompt + 39.3B completion` даёт
около `44.94T`, а не `95T`. PDF не объясняет, относится ли `95T` к иной
population, включает ли дополнительный token accounting или является ошибкой.
Поэтому claim `95T tokens` следует цитировать только как число abstract с явной
оговоркой; для прозрачной decomposition безопаснее использовать Table 3.

### Какие поля собирались

Для каждого LLM call и tool invocation telemetry содержит (PDF с. 3):

- timestamps и durations;
- input/output token counts, без reasoning tokens;
- model name;
- tool name;
- success/failure status.

Anonymized identifiers user, subscription, machine, IDE instance и session
позволяют связывать события между telemetry tables и реконструировать workflow
structure, включая overlap calls и потенциально concurrent sessions per user.

### Что не собиралось

Авторы прямо сообщают, что не собирали (PDF с. 3, 19):

- prompt text;
- file content и source code;
- model outputs;
- tool arguments;
- user-identifiable information;
- task success или code-quality signals.

Это сильное privacy ограничение одновременно задаёт главную measurement
границу: невозможно установить, какую software task решал user, был ли output
принят, что происходило во время межturnового gap и соответствуют ли две
sessions одному task или разным задачам.

### Confidentiality и воспроизводимость

Models в результатах частично анонимизированы как `Model A`, `B` и т.д. Авторы
также не дают server-side GPU utilization, queue depth, batch size и memory
pressure, объясняя это риском раскрытия model/serving confidentiality. В
conclusion заявлен план выпустить sanitized traces, но на момент v1 это future
release, а не доступный reproducibility artifact (PDF с. 7, 19).

## Фактическая единица анализа

Telemetry имеет трёхуровневую иерархию (PDF с. 3):

1. **Session** - lifetime одной coding-agent session.
2. **User turn** - один user prompt и вся последующая autonomous response chain
   агента до возврата управления пользователю.
3. **Step** - один LLM invocation или tool call внутри turn.

Канонический turn:

```text
User prompt -> LLM -> [LLM | tools -> LLM]* -> final response
```

Каждый turn начинается ровно с одного user-initiated LLM call; последующие calls
внутри turn являются auto-continued агентом. Последний step turn всегда LLM
call.

**Фактическая статистическая единица не равна software task.** Paper агрегирует
метрики на call, tool batch, turn, session и anonymized-user levels. Нет task ID,
issue ID, repository-level work item, fixed acceptance criterion или однозначной
границы «задача завершена». Один task может занимать несколько turns/sessions,
а один turn может быть вопросом, exploration, edit, build/retry или частью более
длинной работы. Поэтому слова `task` и `completion` в narrative нельзя
интерпретировать как M0--M4 job и accepted completion.

## Descriptive telemetry: основные результаты

### Sessions и turns

Session distributions сильно right-skewed (PDF с. 4--5):

| Metric per session | Median | P90 | Mean |
|---|---:|---:|---:|
| User turns | `3` | `15` | `6.1` |
| LLM calls | `15` | `100.5` | `40.6` |
| Tool calls | `13` | `111.4` | `43.6` |
| Session duration | `4.2 min` | `177.8 min` | `62.6 min` |

Mean-to-median ratio session duration равен `14.9x`. Это показывает heavy tail
agent usage, но session duration включает user gaps и не является task
completion time.

В Table 4 turn-level medians (`4.5` LLM calls, `4` tools, `227.6K` prompt
tokens, `1.9K` completion tokens) расходятся с соседним текстом (`3` LLM calls,
`3` tools, `160.2K` prompt tokens, `265` completion tokens). Причина различия в
PDF не объяснена. Для точных turn medians лучше ссылаться на конкретную Table 4
или Figure 4, а не объединять обе серии как одну оценку (PDF с. 4--5).

### Автономный loop и human touchpoints

После user message агент выполняет в среднем `6.6` LLM calls до возврата
управления. Авторы относят около `87%` LLM calls к agent-initiated и `13%` к
user-initiated (PDF с. 5--6).

Это прямое evidence автономных multi-step loops, но не оценка доли времени
человека. Число calls не взвешено по duration; user prompt может требовать
долгой specification, а inter-turn gap может содержать review, manual coding,
другую работу, meeting или abandonment.

### Внутренняя concurrency и sequentiality

LLM execution внутри turns преимущественно последовательна (PDF с. 6):

- `36.7%` turns строго sequential;
- `63.3%` имеют хотя бы некоторый overlap LLM calls;
- степень concurrency остаётся малой: median `1.15`, P90 `1.4`;
- overlap обычно возникает в середине turn при независимых subtasks или
  background sub-agents;
- начало и конец turn остаются последовательными, потому что downstream step
  ждёт результаты upstream branches.

Tool execution также в основном последовательна (PDF с. 13--14):

- `93%` tool batches содержат один invocation;
- только `7%` batches запускают несколько tools параллельно;
- среди parallel batches median width равна `2`, а `87.5%` содержат не более
  трёх tools;
- parallelism сосредоточен в read/search operations;
- write, build и terminal operations почти всегда serial из-за shared state и
  side effects.

Это важное descriptive evidence ограниченного internal parallelism и
dependency structure. Но measured concurrency - overlap calls/tools **внутри
одной agent session**, а не число независимых coding agents `P`, которыми
управляет один developer.

### Workflow archetypes и retries

Clustering turns по tool composition, LLM depth, tokens и execution properties
даёт шесть archetypes (PDF с. 6--7):

| Archetype | Share | Median LLM calls | Краткое описание авторов |
|---|---:|---:|---|
| Deep-loop read | `30.5%` | `9` | повторное чтение/search |
| LLM-only | `20.2%` | `1` | reasoning без tools |
| Multi-cycle edit | `19.0%` | `5` | read/edit/build loop |
| Multi-cycle other | `13.2%` | `4` | read-heavy refinement |
| Deep-loop with failures | `9.1%` | `36` | retry/debug loops |
| Deep-loop run | `8.1%` | `7` | terminal-heavy workflow |

Deep-loop with failures имеет `34` tool batches и примерно в четыре раза больше
LLM calls, чем median workflow. Наблюдаемые failed builds, missing dependencies
и unexpected results вызывают autonomous diagnosis/retry loops с растущим
context. Авторы суммируют это как amplification compute до `4x` (PDF с. 1,
6--7).

`4x` относится к resource demand/compute proxy retry workflow, не к dollar cost,
developer effort или fixed-quality completion time.

### Tools и failure metrics

Tool mix концентрирован (PDF с. 12--14):

- `get_file` - `35.0%` invocations;
- `run_command` - `17.0%`;
- string replacement - `9.8%`;
- top 11 tools дают более `90%` invocations;
- median tool duration - `166 ms`, mean - `16.7 s`, P90 - `4.4 s`, P99 -
  `79 s`.

Read/search tools быстры и почти всегда успешны; build, terminal и mutation
tools образуют latency tail. Для `run_command_in_terminal` failed invocation на
P95 длится в `48x` дольше successful invocation. Failed builds также добавляют
примерно в `7--8x` больше prompt tokens на median из-за diagnostics (PDF с. 13).

Tool success/failure - infrastructure event, а не task success. Failure может
быть полезным observation в нормальном debugging loop и не означает провал
software task.

### Tokens, compaction и infrastructure time

Median LLM call имеет `68K` prompt tokens, `63K` cached tokens и `247`
completion tokens; median input/output ratio превышает `275:1`. Conversation
history даёт `48%` input tokens, function/tool-call messages - `28%`, system
prompt - `14%`, repository instructions и прочий context - `10%` (PDF с. 7--8).

Context compaction (PDF с. 10--12):

- встречается в `7.8%` sessions;
- эти sessions дают `44.2%` total tokens, `37.1%` LLM calls и `38.9%` tool calls;
- median compaction занимает около `22%` turn duration;
- median prompt-token drop равен `72.8%`;
- median cache-hit-rate drop равен `66.1%`.

Это полезные признаки one-stream agent cost и long-session instability. Они не
являются `C(P)`, поскольку не оценены как дополнительный эффект роста числа
concurrent coding agents.

### User and workflow heterogeneity

По per-user medians авторы выделяют пять user archetypes (PDF с. 15--16):

| User type | Share | Sessions | Turns | Tools/turn | Tokens/turn |
|---|---:|---:|---:|---:|---:|
| Readers | `41.7%` | `2` | `6` | `4.8` | `203K` |
| Coders | `30.4%` | `5` | `50` | `6.2` | `417K` |
| Terminal users | `11.0%` | `2` | `7` | `4.0` | `213K` |
| Deep-loop users | `9.2%` | `2` | `6` | `20.0` | `1.1M` |
| Chat-only users | `7.6%` | `1` | `2` | `0` | `23K` |

Разница `23K` против `1.1M` даёт примерно `50x` range token consumption per
turn. Эта taxonomy описывает observed tool/resource behavior, а не skill,
developer productivity или causal response to AI. Интерпретации вроде
«refactor» или «exploring unfamiliar codebase» выводятся авторами из tool mix;
content telemetry для прямой проверки не собиралась.

### User idle и human intervention

Для multi-turn sessions median доля lifetime, классифицированная как user idle,
равна `80.1%`; LLM и tool execution дают medians `13.7%` и `2.0%`. Для
single-turn sessions с LLM и tools median LLM share равна `87.7%` (PDF с. 8).

Отдельно inter-turn user idle gap имеет median `1,512 s`, или `25.2 min`, с
tail более суток. Resource-specific cross-turn gaps короче: median container
idle `243 s`, KV-cache idle `172 s`; intra-turn medians равны `5.8 s` и `1.2 s`
(PDF с. 16--17).

Термин `user idle` означает отсутствие следующего telemetry event от user, а не
доказанную бездеятельность разработчика. Paper не видит, читает ли разработчик
результат, проверяет diff, редактирует код вручную, работает в другой session
или вообще оставил IDE. Эти интервалы нельзя считать ни `h`, ни свободным окном
для другого coding agent без дополнительного activity logging.

## Predictive component и uncertainty

### Idle-time predictor

Авторы обучают LightGBM quantile regressors на turn-level features: `150K`
sessions из одной недели для training и `50K` sessions следующей недели для
evaluation. Модель формирует survival curve idle duration, а не один point
forecast. Для binary outcome `idle > 60 s` reported ROC-AUC равен `0.73` против
`0.58` у heuristic previous-gap baseline; доля total idle time, захваченная
prediction policy, остаётся `86--90%` на разных cutoffs (PDF с. 17--18).

Это out-of-time predictive validation infrastructure signal, но не validation
developer behavior, task success или productivity. Paper не сообщает
randomized deployment, который показал бы фактическое снижение cost/latency без
regression от cache eviction или cold starts.

### Статистическая неопределённость descriptive findings

Для большинства headline telemetry metrics paper даёт medians, percentiles,
means и CDFs, но не confidence intervals, sampling weights или cluster-aware
uncertainty по users/sessions. Огромный event count уменьшает sampling noise для
наблюдаемой telemetry population, но не устраняет:

- непрозрачность sampled subset;
- зависимость миллионов events внутри одних users/sessions;
- selection into GitHub Copilot agent usage;
- отсутствие task content и quality;
- ограничение США и одной недели;
- изменение product/models/tools со временем.

Авторы пишут, что patterns наблюдались стабильно с января по июнь 2026 года, но
не публикуют полный longitudinal design или drift estimates и считают tracking
future work (PDF с. 19).

## Descriptive telemetry не равно productivity effect

| Наблюдаемая метрика | Что она действительно измеряет | Почему это не productivity effect |
|---|---|---|
| Session duration | lifetime client-side session, включая inter-turn gaps | Session не равна fixed task; нет acceptance и baseline |
| Turn duration | время prompt-to-final-response одного conversation turn | Turn может быть вопросом или частью task; quality неизвестна |
| LLM/tool calls | internal execution depth и serving load | Больше calls может означать сложность, retries или более полную проверку |
| Token consumption | inference/context resource volume | Tokens не равны elapsed developer time, quality или accepted work |
| Tool success/failure | status отдельного invocation | Failed build может быть нормальным debugging signal; task outcome неизвестен |
| `87%` agent-initiated calls | происхождение calls внутри turn | Не доля автономного времени и не снижение human effort на 87% |
| LLM concurrency `1.15/1.4` | overlap LLM calls внутри turn | Не число coding agents у одного developer и не project parallelism `P` |
| User idle gap | отсутствие user telemetry между turns | Может включать review, manual coding, другую работу или abandonment |
| `4x` retry amplification | compute/call growth failure-heavy workflow | Не `4x` dollar cost, developer time или makespan |
| `50x` tokens across archetypes | heterogeneity resource footprint | Не `50x` difference productivity или skill |

Чтобы оценить productivity, понадобились бы как минимум task identity и scope,
no-AI или alternative-mode comparator, common acceptance/quality gate,
start/finish boundaries, human/agent activity split и handling simultaneous
tasks. В текущей telemetry этих полей нет.

## Selection bias и causal limits

1. **Adoption selection.** Наблюдаются только пользователи GitHub Copilot coding
   agent в Visual Studio/VS Code, уже выбравшие product и конкретный workflow.
2. **Task selection.** Пользователи сами решают, какие задачи отдавать agent и
   когда запускать session; semantics задач не видна.
3. **No comparator.** Нет AI-disallowed, chat-only randomized arm или matched
   no-AI task durations. Chat-only users - поведенческий cluster, не control.
4. **No intervention.** Tool mix, concurrency, model switches, retries и
   compaction не назначаются случайно; они endogenous сложности и состояния
   workflow.
5. **Conditioning on active usage.** Session-level distributions не описывают
   задачи, которые разработчик не стал выполнять с agent, abandoned до session
   или решил вручную.
6. **Unknown sampling.** Не раскрыты sampling rate, weighting и event loss.
7. **Geography/time.** Только US regions, одна неделя июня 2026 года и максимум
   три time zones.
8. **Product drift.** Models, tools и autonomy policies быстро меняются; авторы
   прямо называют workload evolving.
9. **No demographics/context.** Нет опыта developer, repository maturity,
   language, task type, team process или quality bar.
10. **Client-side only.** Нет server queues, GPU load и полной end-to-end
    infrastructure path.
11. **No quality/success.** Авторы прямо признают невозможность связать resource
    efficiency с task completion quality.
12. **No causal productivity estimand.** Нельзя установить, сколько времени или
    effort тот же workload занял бы без agent либо при другом `P`.

Следовательно, causal формулировки допустимы только на уровне детерминированной
структуры protocol, например «после user prompt auto-continuation создаёт
последовательность calls». Формулировки «agent ускоряет developer» или
«parallelism повышает productivity» данными не идентифицируются.

## Полное mapping к `Z,k,r,W,P,L,C(P),h,H,gamma(P)`

Здесь **direct descriptive** означает близко измеряемый объект, но не обязательно
совместимый коэффициент; **mechanism only** - наблюдение возможного механизма;
**mismatch** - похожая метрика с другой физической семантикой; **absent** -
объект не измеряется.

| Параметр M0--M4 | Статус | Ближайший объект Liu et al. | Точная граница |
|---|---|---|---|
| `X` | **absent** | Нет общей baseline time unit | Не наблюдается ручное no-AI выполнение единицы работы |
| `Z_i` / `Z` | **mechanism only** | Heavy tails, workflow/user archetypes, различия tool mix | Нет task identity, baseline difficulty `Z_i X`, story points или content |
| `k_i^(r)` / `k` | **absent** | Turn/session durations и retry/resource metrics | Нет no-AI denominator, fixed task boundary и common quality gate; session ratio не вычисляется |
| режим `r` | **partial direct descriptive** | GitHub Copilot coding-agent protocol; user turn, auto-continuation, manual/auto model switch, tool workflow | Один product содержит неоднородные user strategies; mode не назначен task-level и не сравнивается причинно |
| `W = X sum Z_i k_i` | **absent** | Aggregate tokens, calls и session time | Serving volume не является суммой durations fixed software workload |
| `P` | **mismatch / mechanism only** | Intra-turn LLM concurrency, background sub-agents, parallel tool batches, linkable concurrent sessions | Не измерено число одновременно делегированных coding tasks/agents на developer; `P` не варьируется как treatment |
| `L` | **conceptual support** | Tight sequential LLM-tool chains, inverted-U concurrency, serial write/build operations, straggler joins | Нет precedence DAG software jobs, duration-weighted critical path или common project finish |
| `C(P)` | **mechanism only** | Shared-state serialization, KV contention, retries, model switches, compaction, long-tail tools | Effects не оценены относительно `P`; большинство существует уже внутри одной session и должно входить в one-stream `k` |
| `h_i^(r)` / `h` | **состав частично виден, численно absent** | User prompt запускает turn; следующий turn требует нового user event; possible review gap | Calls не равны time; prompt/review/manual coding не разделены; `87%` autonomy не даёт `h=0.13` |
| `H = X sum Z_i h_i` | **absent** | Inter-turn user gaps и anonymized user linkage | Gap не является active human service; fixed workload и non-overlapping human intervals отсутствуют |
| `gamma(P)` | **absent** | Можно было бы реконструировать concurrent sessions, но published distribution/switch costs нет | Inter-turn idle и cache loss не являются human context-switch recovery; зависимости от agent count нет |
| Makespan | **absent** | Session/turn wall-clock durations | Нет software-task completion boundary, fixed workload, accepted output и resource-feasible project schedule |

### Mapping к уровням M0--M4

| Уровень | Что требует M0--M4 | Что даёт источник | Вердикт |
|---|---|---|---|
| M0 | Fixed work `W`, one-stream time factor `k`, ideal `W/P` | Production distributions calls, tools, tokens и turn/session latency | Полезен для feature design и stochastic tails, но не калибрует `W`, `k` или speedup |
| M1 | Неделимые software jobs и longest-job duration | Turns/sessions дискретны, но не являются установленными jobs | Нет assignment tasks по agents и `M_N` |
| M2 | Precedence DAG и critical path `L` | Прямо наблюдается последовательная dependency chain LLM-tool-LLM и shallow forks | Поддерживает mechanism sequentiality, но не software DAG или quantitative `L` |
| M3 | Дополнительный integration overhead как функция `P` | Retry, shared-state serialization, cache/compaction и tool-tail mechanisms | One-session overhead богат, но dose-response `C(P)` не оценён |
| M4 | Один developer, `k=a+h`, capacity-1 `H`, verification windows и `gamma(P)` | User инициирует turns; inter-turn gaps видны только как отсутствие events | Не измерены active human work, review, simultaneous agent streams и switching penalty |

### Что telemetry может дать будущей калибровке

При расширенном instrumentation source предлагает полезную feature schema:

- session/turn/task identifiers и timestamps;
- LLM/tool call durations и overlap;
- model/tool/version;
- failures, retries и compaction;
- context/token growth;
- concurrent session/agent count;
- user prompt, review, correction и acceptance events;
- task success и quality gate.

Первые шесть групп уже частично видны в paper. Последние три необходимы, чтобы
перейти от serving workload к `k`, `h`, `H` и makespan. Без них даже точная
infrastructure telemetry не идентифицирует developer productivity.

## Что источник поддерживает для M0--M4

1. **Agentic workload имеет session/turn structure.** Один user prompt запускает
   длинную auto-continued LLM-tool chain; request-level независимая модель
   нагрузки недостаточна (PDF с. 1--3, 5--7).
2. **Автономность не устраняет последовательность.** Несмотря на некоторый
   overlap, LLM concurrency мала, а start/end и state-changing operations
   serial, что поддерживает необходимость учитывать dependencies, а не только
   nominal worker count (PDF с. 6, 13--14).
3. **Task/workflow effects должны быть heterogeneous.** Session durations,
   calls, tools и tokens имеют heavy tails; workflow archetypes различаются на
   порядок по execution depth (PDF с. 4--7).
4. **Failures создают endogenous rework loops.** Build/tool failures вызывают
   дополнительные reasoning, diagnostics, retries и growing context; такой
   workload должен входить в task/mode-specific duration distribution, а не
   считаться единичной генерацией (PDF с. 6--7, 12--14).
5. **Tool class и shared state ограничивают parallelism.** Reads можно batch'ить,
   а writes/builds/terminal operations обычно сериализуются (PDF с. 13--14).
6. **Long sessions несут state-management overhead.** Model switches и context
   compaction создают cache cold starts и latency, особенно в resource-heavy
   sessions (PDF с. 9--12).
7. **Пользовательская неоднородность велика.** Пять behavioral archetypes имеют
   примерно `50x` range token demand; uniform average скрывает различия режима и
   workload (PDF с. 15--16).
8. **Turn boundary является наблюдаемым human-agent handoff point.** Он отделяет
   автономный loop от следующего user input, но содержание human activity между
   turns требует дополнительного logging (PDF с. 3, 9, 16--18).
9. **Session time нельзя автоматически считать active task time.** В multi-turn
   sessions user gaps доминируют lifetime, а их смысл не наблюдается (PDF с. 8,
   16--17).
10. **Quality-aware measurement отсутствует даже в крупной telemetry.** Авторы
    прямо требуют joint resource/task-success analysis как future work (PDF
    с. 19).

## Что источник не позволяет утверждать

1. Что GitHub Copilot coding agent ускоряет или замедляет разработчиков.
2. Что `13.5M sessions` означают `13.5M completed software tasks`.
3. Что session duration является task completion time или makespan.
4. Что `87%` agent-initiated calls означает `87%` автономного времени,
   `h=0.13` или сокращение human effort на 87%.
5. Что median/P90 LLM concurrency равны числу coding agents `P`.
6. Что overlap sub-agents показывает benefit от multiple-agent supervision.
7. Что paper измеряет concurrent-agent count per developer; identifiers лишь
   позволяют потенциальную reconstruction, но published `P` distribution нет.
8. Что tool failure равен провалу task или defect результата.
9. Что `4x compute` retry loops означают `4x` developer time, dollar cost или
   makespan.
10. Что `95T tokens` можно без оговорки совместить с Table 3; accounting в PDF
    не согласован.
11. Что user archetypes являются типами skill/productivity или стабильными
    causal traits пользователя.
12. Что weekend sessions доказанно содержат более амбициозные задачи: это
    авторская интерпретация без content data.
13. Что user idle является свободным временем developer. Он может включать
    review, thought, manual work, другую session или abandonment.
14. Что LLM-dominated active execution означает LLM-dominated developer
    workflow: human work вне telemetry не наблюдается.
15. Что cache hit, compaction или model-switch percentages являются `C(P)`.
16. Что internal sequential chain численно валидирует критический путь `L`
    software project.
17. Что можно вычислить `k`, `h`, `H`, `gamma(P)` или optimal `P`.
18. Что source сравнивает fixed workload при разных configurations.
19. Что результат generalizes за пределы US GitHub Copilot/VS/VS Code snapshot
    июня 2026 года.
20. Что source peer-reviewed; проверенная запись - arXiv v1.

## Отличие от M0--M4

| Измерение | Liu et al. (2026) | M0--M4 |
|---|---|---|
| Центральный вопрос | Как production coding-agent workload нагружает LLM/tool serving infrastructure | Когда один developer с `P` coding agents сокращает fixed-workload makespan |
| Единица анализа | LLM/tool call, batch, turn, session, anonymized user | Software task `i`, fixed task set и project completion boundary |
| Population | Self-selected GitHub Copilot agent users в US regions | Абстрактная one-developer star с externally calibrated parameters |
| Workload | Наблюдаемая product telemetry без task content | Заданный объём `Z_i`, `W` и optional DAG |
| Baseline | Нет no-AI counterfactual | Последовательная no-AI работа `T_h=X sum Z_i` |
| Outcome | Calls, tokens, latency, cache, tool status, resource idle | Elapsed accepted-work makespan и speedup |
| Quality | Отсутствует | Не отдельная цель, но verification/rework должны входить во время |
| Параллелизм | Overlap LLM calls и tool batches внутри sessions | `P` concurrent coding agents/tasks под одним developer |
| Dependencies | Step-level LLM-tool chain | Task-level precedence DAG и critical path `L` |
| Human role | User prompt на turn boundary; остальная activity невидима | Specification, review, correction как `h_i`; общий capacity-1 `H` |
| Overhead | Retry, cache, compaction, model switch, tool latency | One-stream costs в `k`; только рост при `P>1` в `C(P)`/`gamma(P)` |
| Causal design | Descriptive telemetry; idle predictor out-of-time | Formal model, требующая внешней causal/observational calibration `k,h` |

Liu et al. находятся **до estimation и scheduling layers** M0--M4. Они дают
production evidence для формы agent service process и candidate telemetry
features, особенно для serial dependencies, retries и heavy tails. M0--M4
добавляет отсутствующие сущности: fixed software workload, no-AI baseline,
task/mode-specific elapsed coefficient, explicit agent count, DAG, accepted
completion и один последовательно обслуживающий human resource.

## Проверенные claims для Related Work

### Безопасные claims

1. Liu et al. анализируют sampled client-side telemetry GitHub Copilot coding
   agent из Visual Studio и VS Code за одну неделю июня 2026 года: Table 3
   сообщает `13.5M` sessions, `95.1M` turns, `3.2M` anonymized users, `760.5M`
   LLM calls и `774.7M` tool calls (PDF с. 3).
2. Каждый user turn начинается user prompt и разворачивается в autonomous
   LLM-tool chain; около `87%` LLM calls классифицированы как agent-initiated
   (PDF с. 3, 5--6).
3. Internal LLM parallelism shallow: `36.7%` turns strictly sequential, а при
   наличии overlap median concurrency `1.15`, P90 `1.4`; start/end turns
   остаются serial из-за dependencies (PDF с. 6).
4. Tool batches также преимущественно serial: `93%` содержат один invocation;
   parallel batches обычно состоят из 2--3 read operations, а state-changing
   tools почти не parallelized (PDF с. 13--14).
5. Failure-heavy workflows образуют autonomous retry loops: `Deep-loop with
   failures` составляет `9.1%` turns и имеет median `36` LLM calls и `34` tool
   batches; authors оценивают compute amplification до `4x` (PDF с. 1, 6--7).
6. Production usage сильно heterogeneous: user archetypes дают от `23K` до
   `1.1M` tokens per turn, примерно `50x` range (PDF с. 15--16).
7. В multi-turn sessions inter-turn gaps занимают большую часть session
   lifetime, но telemetry не раскрывает human activity внутри gap; source не
   содержит task quality/success signals (PDF с. 8, 16--17, 19).
8. Работа характеризует serving workload, а не productivity: task identity,
   no-AI comparator, accepted completion и quality отсутствуют, поэтому её
   duration/token results не дают `k` или makespan effect.

### Claims, которых следует избегать

- «На production data coding agents повысили производительность разработчиков».
- «GitHub Copilot автономно выполняет 87% работы».
- «Реальный developer эффективно управляет `P=1.15` agents».
- «63% задач выполняются параллельно».
- «Tool failures увеличивают срок разработки в четыре раза».
- «Median coding task занимает 4.2 минуты».
- «25 минут user idle - это свободное время для второго агента».
- «Deep-loop users в 50 раз продуктивнее/дороже других».
- «Работа оценивает `C(P)` или подтверждает M4».
- «Corpus содержит 95T tokens по Table 3» без оговорки о несогласованном
  accounting.

## Предлагаемое место в статье

Источник лучше вставить в подраздел о **production agentic workflows и
measurement limits** после работ о one-agent interaction/review и рядом с METR
2026, но до multi-agent scaling Kim et al. Он выполняет переход:

1. controlled productivity studies дают context-specific effect на time/quality;
2. production telemetry показывает внутреннюю структуру autonomous workflow,
   retries, shallow parallelism и heterogeneity;
3. однако telemetry без task/quality/human labels не даёт productivity effect;
4. M0--M4 требует объединить task-level calibration с explicit scheduling и
   human-resource accounting.

Не использовать источник как эмпирическую калибровку `k`, `h`, `C(P)` или как
доказательство выгоды multiple agents.

### Короткий вариант встраивания

> Liu et al. (2026) описали client-side production telemetry GitHub Copilot
> coding agent: 13.5 млн sessions, 95.1 млн user turns, 760.5 млн LLM calls и
> 774.7 млн tool calls от 3.2 млн anonymized users за одну неделю. После user
> prompt агент самостоятельно продолжал loop, так что 87% LLM calls были
> agent-initiated, однако internal parallelism оставался малым: 36.7% turns были
> строго последовательны, а median concurrency при overlap составляла 1.15.
> Tool execution также было преимущественно serial, особенно для write/build
> operations, а failures порождали длинные retry loops. Эти данные подтверждают
> неоднородность и dependency-constrained характер production agent workloads,
> но не измеряют developer productivity: session/turn не привязаны к fixed
> software tasks, prompt/code content и quality signals не собирались, no-AI
> comparator отсутствовал. Поэтому telemetry не даёт `k`, human share `h` или
> scaling effect по числу agents `P`.

### Вариант для discussion/measurement

> Production agent telemetry нельзя отождествлять с task productivity. В Liu et
> al. inter-turn user gaps доминировали lifetime multi-turn sessions, однако
> отсутствие user events не показывает, был ли разработчик свободен: он мог
> review'ить diff, редактировать код вручную, работать в другой session или
> оставить задачу. Для калибровки M4 нужны связанные task identifiers,
> acceptance outcomes и двухканальный хронометраж active human и autonomous
> agent intervals; одних LLM/tool timestamps недостаточно.

## Таблица доказательных страниц

| PDF-страница | Раздел / объект | Опорное содержание | Статус evidence |
|---:|---|---|---|
| 1 | Title; Abstract; Introduction; Table 1 | Title PDF без `Traces`, authors, arXiv v1, headline corpus, 87% autonomy, failures, 50x heterogeneity, systems target | Прямой metadata/author summary; `95T` расходится с Table 3 |
| 2 | Introduction; Background; Table 2 | Contributions, session-aware serving, coding-agent loop, sequential dependencies, distinction from chat | Авторская framing и system implications |
| 3 | Dataset and Methodology; Table 3 | VS/VS Code, first week June 2026, US regions, sampled anonymized client telemetry, excluded content, exact hierarchy и corpus counts | Главный прямой источник provenance/privacy/unit of analysis |
| 4--5 | Time series; Session-level overview; Table 4; Figure 4 | Session/turn means, medians, P90, heavy tails, weekday/weekend pattern | Descriptive telemetry; turn medians internally differ between table/text |
| 5--6 | Execution structure; Figures 6--7 | 1:1 LLM-tool coupling, 87% auto-continuation, strict/semi-overlap turns, median/P90 concurrency, inverted-U pattern | Direct call-level overlap, не coding-agent count `P` |
| 6--7 | Workflow archetypes; Table 5; Figure 8 | Six turn clusters, deep-loop failures, retry mechanisms, 4x compute claim | Descriptive clustering и trace illustration |
| 7--9 | LLM footprints; Figures 9--13 | Model/token distributions, prompt composition, LLM/tool/user time shares, KV cache | Infrastructure metrics, не productivity |
| 9--10 | Turn boundaries; model switches; Table 6 | Cache degradation, user gaps, model switching, compaction prevalence | Session mechanics; model identities confidential |
| 10--12 | Context compaction; Figures 17--20 | Trigger heterogeneity, 22% median turn overhead, token/cache drops, concentration in heavy sessions | One-session systems overhead |
| 12--13 | Tool statistics; Figures 21--25 | Tool mix, durations, success/failure, failed build context, 48x P95 terminal failure | Tool-event status, не task success |
| 13--14 | Runtime parallelism; Figures 26--28 | 93% single-tool batches, shallow read parallelism, serial side effects, overlap and critical-path tool tails | Direct internal tool concurrency |
| 15--16 | Users; Table 7; Figures 29--31 | Five user archetypes, shares, sessions/turns/tools/tokens, resource concentration, 50x range | Behavioral/resource clustering, не user productivity |
| 16--17 | Idleness; Table 8; Figure 32 | Definitions container/KV/user idle, intra/cross-turn distributions, 25.2-minute user gap | Event-gap telemetry; human activity unobserved |
| 17--18 | Idle predictor; Figure 33; multiplexing | 150K/50K temporal split, LightGBM quantiles, AUC 0.73, 86--90% captured idle, systems use | Predictive infrastructure component, не causal deployment/productivity |
| 18 | Related work | Positioning against production workload studies, benchmarks and smaller coding-agent traces | Secondary positioning |
| 19 | Limitations; Conclusion | No quality signals, client-side only, confidentiality, evolving workload, planned sanitized traces | Прямые ограничения и status artifacts |
| 19--20 | References | Corpus cited by paper | Secondary leads; external claims require primary-source checks |

## Итоговая оценка релевантности

Источник высоко релевантен как production evidence **внутренней структуры
agentic execution**. Он показывает, что coding-agent workload состоит не из
независимых запросов, а из session-bound sequential chains с короткими forks,
stateful tools, failures, retries, compaction и heavy-tailed resource demand.
Для M0--M4 это укрепляет мотивацию task-specific/stochastic `k`, ограниченного
parallelism, dependency term `L` и строгого разделения one-stream overhead от
дополнительных costs при `P>1`.

Доказательная сила для главного вопроса нашей статьи ограничена объектом
наблюдения. В source нет software-task unit, fixed workload, no-AI baseline,
acceptance/quality, полного human activity или assigned concurrent-agent count.
Он не оценивает `k`, `h`, `H`, `C(P)`, `gamma(P)` и makespan. Корректное место в
Related Work - не среди productivity effect sizes, а в отдельном переходе от
production telemetry к требованиям калибровки: крупный trace corpus описывает,
как работает agent infrastructure, но для ответа «ускоряет ли один developer
fixed workload с `P` agents» нужен другой measurement design.
