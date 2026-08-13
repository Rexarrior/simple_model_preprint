# Brynjolfsson, Li и Raymond: field evidence о generative AI в customer support и границы переноса в M0-M4

## Назначение и главный вывод

Источник нужен для статьи о fixed-workload makespan ячейки «один разработчик - `P` кодовых ИИ-агентов» как крупномасштабное полевое свидетельство трёх вещей:

1. доступ к generative AI может повысить операционный throughput в реальной организации;
2. средний эффект скрывает сильную неоднородность по опыту, исходному skill и типу проблемы;
3. скорость, вероятность успешного разрешения, качество и customer experience являются разными outcomes и могут двигаться по-разному.

Главная граница переноса: `issues resolved per hour` не равно времени завершения фиксированной coding task. Это составной throughput outcome, зависящий от длительности обращения, числа одновременно обслуживаемых чатов и resolution rate. Поэтому опубликованные `15%` нельзя без дополнительных предпосылок обращать в `1/1.15` и подставлять как `k`. Работа также не варьирует число кодовых агентов, не задаёт фиксированный проектный workload и не измеряет makespan.

## Критический аудит версии

### Финальная журнальная публикация

**Полная ссылка:** Erik Brynjolfsson, Danielle Li, and Lindsey R. Raymond. “Generative AI at Work.” *The Quarterly Journal of Economics* 140(2), 889-942, 2025. DOI: [10.1093/qje/qjae044](https://doi.org/10.1093/qje/qjae044).

**Статус:** финальная peer-reviewed журнальная публикация, version of record; online publication 4 February 2025, print issue May 2025. Издательские метаданные указывают лицензию CC BY-NC 4.0.

**Финальные sample и headline result:** abstract version of record сообщает `5,172` customer-support agents и средний рост `issues resolved per hour` на `15%` (QJE p. 889). Там же указаны существенная неоднородность по работникам, улучшения speed и quality у менее опытных и менее skilled работников, малый выигрыш по speed и небольшое снижение quality у наиболее опытных и skilled, признаки learning и English fluency, максимальный выигрыш на moderately rare problems, улучшение вежливости клиентов и снижение запросов на перевод к менеджеру.

### Что находится в переданном PDF

Файл `/Users/rexarrior/work/articles/simple_model_full/literature/brynjolfsson2025.pdf` **не является финальной QJE-версией**, несмотря на имя файла. Это NBER Working Paper 31161, April 2023, revised November 2023:

- титульный лист прямо обозначает `NBER Working Paper 31161` и предупреждает, что NBER working papers не прошли peer review (локальный PDF с. 1);
- abstract сообщает `5,179` agents и `14%`, а не финальные `5,172` и `15%` (локальный PDF с. 2);
- файл содержит 67 PDF-страниц; основной текст имеет внутреннюю нумерацию 1-28 на PDF-страницах 3-30, затем идут references, figures, tables и appendix;
- SHA-256: `9af82b90f2a94f8757ace8c7b7ef0934b145a00f4156fc806f4fb8a33e1bddc2`.

Это содержательный, но не косметический конфликт версий. В финальной статье изменились как минимум sample, средний эффект и набор подчёркнутых механизмов: финальный abstract добавляет heterogeneity по rarity проблем и English fluency, отсутствующие в abstract и основном тексте локальной версии; напротив, retention является заметным результатом working paper, но не заявлен в финальном abstract.

### Правило доказательств в этом обзоре

- Ссылки вида **«локальный PDF с. X»** относятся только к NBER revision November 2023.
- Ссылка **«QJE p. 889»** относится к финальному abstract, проверенному по DOI/Crossref metadata version of record.
- Детальные оценки, standard errors и страницы финальной QJE-версии нельзя честно извлечь из переданного файла. Поэтому ниже не выдумывается финальный CI и не выдаются номера страниц working paper за журнальные страницы.
- Для аудита uncertainty приводятся точные estimates и SE из локальной working-paper версии с явной маркировкой. Их нельзя автоматически цитировать как финальные QJE numbers.

## Исследовательские вопросы

Работа исследует, как доступ к generative AI conversational assistant влияет на:

1. производительность customer-support agents;
2. компоненты производительности: handle time, chats per hour и resolution rate;
3. качество и customer experience;
4. распределение эффекта по исходному skill и tenure;
5. следование рекомендациям, learning и изменение коммуникации;
6. в working-paper версии - customer sentiment, managerial escalation и attrition.

Для нашей статьи наиболее важен не универсальный causal effect «ИИ вообще», а вопрос о гетерогенности эффекта: один и тот же инструмент может давать существенно разные outcomes для разных пользователей и проблем.

## Организационный контекст, инструмент и выборка

### Рабочая среда

Исследование проводится у Fortune 500 enterprise software company и её подрядчиков. Agents отвечают в чатах на технические вопросы американских small businesses; большинство работников находятся на Филиппинах, меньшая часть - в США и других странах. Чаты случайно назначаются agents, в среднем длятся около 40 минут и требуют диагностики технической проблемы, знания продукта и управления эмоционально сложным разговором (локальный PDF с. 11-12).

Случайное назначение чатов помогает против case selection между agents, но **не является случайным назначением AI treatment**.

### AI treatment и режим взаимодействия

Система объединяет GPT-family model с дополнительными customer-service-specific ML components и обучением на размеченных прошлых разговорах. Labels включают successful resolution, handle time и признак top performer. Во время чата инструмент предлагает:

- варианты ответа клиенту;
- ссылки на внутреннюю техническую документацию.

Это augmentative и интерактивный режим: рекомендации видит только agent, человек остаётся ответственным за ответ и может принять, изменить или проигнорировать suggestion. При недостатке training data система не предлагает ответ (локальный PDF с. 12-13).

Такой `r` ближе к интерактивному ассистированию одного работника, чем к автономному coding agent. Нельзя считать, что AI самостоятельно выполняет неделимую задачу, пока человек свободен.

### Sample

Финальная QJE-версия сообщает `5,172` customer-support agents (QJE p. 889).

Локальная working-paper версия содержит:

- `5,179` agents;
- `3,007,501` chats;
- `1,636` treated agents и около `1.18` млн chats в post-AI observations;
- `89%` agents вне США, преимущественно на Филиппинах;
- 25 locations и 133 teams в полной описательной выборке (локальный PDF с. 13-14, 53, Table 1).

Outcomes доступны на разных подвыборках. Handle time и chats per hour авторы восстанавливают из chat-level data для всех agents. Resolution rate и customer satisfaction получены от data firm лишь для части subcontracted workforce; поэтому и omnibus outcome `resolutions per hour` наблюдается на меньшей подвыборке (локальный PDF с. 14).

## Deployment и causal identification

### Staggered deployment

После первоначального семинедельного randomized pilot на 50 agents система постепенно разворачивалась на agent level; основная масса внедрения пришлась на November 2020 - February 2021. Pilot входит в общую выборку, но отдельно не анализируется из-за малого размера (локальный PDF с. 13).

Следовательно, основной результат не является estimate отдельного RCT. Он основан на observational staggered rollout, включающем маленький randomized pilot.

### Основная спецификация

Working paper оценивает difference-in-differences на agent-month panel:

```text
y_it = delta_t + alpha_i + beta * AI_it + gamma * X_it + epsilon_it,
```

где `AI_it` означает доступ agent `i` к рекомендациям в month `t`. Preferred specification включает year-month fixed effects, agent fixed effects и time-varying tenure; standard errors clustered at agent level (локальный PDF с. 15-16).

Для динамики treatment effects используется interaction-weighted event-study estimator Sun and Abraham. Авторы отдельно показывают robustness с estimators Callaway-Sant'Anna, Borusyak-Jaravel-Spiess и de Chaisemartin-D'Haultfoeuille, чтобы не опираться только на potentially biased two-way fixed effects при heterogeneous treatment timing (локальный PDF с. 15-16, 38-39, 60).

### Что нужно для причинной интерпретации

Event-study identification требует как минимум:

- parallel trends при отсутствии treatment;
- отсутствия anticipatory behavior;
- корректной обработки cohort- и event-time heterogeneity;
- отсутствия unobserved time-varying shocks, одновременно связанных со временем deployment и outcomes.

Pre-treatment event-study estimates выглядят близкими к нулю, а post-treatment effect возникает сразу и сохраняется (локальный PDF с. 16, 38-39). Это поддерживает, но не доказывает parallel trends. Сам staggered rollout после pilot не описан как случайный. В raw data eventual-treated agents уже до внедрения имеют более высокий `resolutions per hour`, chats per hour и resolution rate, чем never-treated; agent fixed effects убирают time-invariant differences, но не неизвестные time-varying selection factors (локальный PDF с. 14-16).

### Основные causal limitations

1. Основной deployment не рандомизирован; маленький pilot не анализируется отдельно.
2. Не дано институциональное правило очередности rollout, достаточное для доказательства exogeneity timing.
3. Treatment мог совпадать с team-, manager- или location-specific изменениями, не поглощёнными общей time FE.
4. Часть quality outcomes доступна только на неполной подвыборке subcontractors.
5. Adherence post-treatment endogenous: более полезные рекомендации и более подходящие agents могут одновременно повышать и adherence, и outcome.
6. Outages редки, кратки и не обязательно случайны; learning analysis прямо характеризуется авторами как noisy и suggestive.
7. Attrition model working paper не может использовать agent fixed effects и поэтому слабее main productivity design.
8. Одно предприятие, один класс customer-support work и относительно стабильный software product ограничивают external validity.

## Outcomes и точные результаты

### Primary outcome: resolutions per hour

`Resolutions per hour` (`RPH`, также описано как issues resolved per hour) - число успешно разрешённых chats на час работы agent. Это omnibus productivity measure, зависящее от:

- average handle time (`AHT`);
- chats handled per hour (`CPH`), включая несколько одновременных chats;
- resolution rate (`RR`) (локальный PDF с. 14).

**Финальный QJE result:** `+15%` в среднем при `n=5,172` agents (QJE p. 889). Финальный abstract не сообщает SE или CI.

**Непроверяемая по переданному PDF часть:** точный coefficient, SE и CI final QJE Table не могут быть установлены из NBER revision. Поэтому численный final-QJE uncertainty в этом обзоре намеренно не указан.

**Working-paper result для version audit:** preferred level specification даёт `+0.301` resolutions/hour, `SE=0.0498`, baseline mean `2.174`, то есть `13.8%`; `N=12,328` agent-month observations (локальный PDF с. 16, 54, Table 2). Обычная normal-approximation трансформация даёт 95% CI level coefficient примерно `[0.203, 0.399]`, или `[9.4%, 18.3%]` относительно указанного baseline mean. Это вычисление из опубликованных coefficient и SE, а не reported final-QJE CI.

Log specification working paper даёт `0.138`, `SE=0.0199`, `N=11,904` (локальный PDF с. 54, Table 2). Точное преобразование point estimate `exp(0.138)-1` равно примерно `14.8%`; normal 95% interval на log scale `[0.099, 0.177]` преобразуется примерно в `[10.4%, 19.4%]`. Этот result также относится только к working paper.

### Decomposition working-paper estimate

Preferred working-paper specification показывает (локальный PDF с. 16-17, 55, Table 3):

| Outcome | Estimate | SE | Baseline mean | Интерпретация |
|---|---:|---:|---:|---|
| Average handle time | `-3.750` min | `0.476` | `40.6` min | около `-9.2%`; быстрее отдельный chat |
| Chats per hour | `+0.366` | `0.0363` | `2.557` | около `+14.3%`; включает multitasking |
| Resolution rate | `+0.0128` | `0.00717` | `0.821` | `+1.28` percentage points; только `p<0.10` |
| Customer satisfaction, NPS | `-0.128` | `0.660` | `79.58` | экономически мало, статистически неотличимо от нуля |

Для resolution rate normal 95% CI по приведённым coefficient и SE примерно `[-0.0013, 0.0269]`, то есть включает ноль. Поэтому сильная часть среднего productivity result в working paper связана с handle time и chats per hour, а не с надёжно установленным средним улучшением resolution quality.

### Почему `RPH` не является `k`

Даже если обозначить throughput ratio как `1.15`, обратная величина `1/1.15≈0.87` стала бы time ratio только при строгих дополнительных условиях: фиксированный и однородный workload, одинаковый acceptance criterion, отсутствие очередей и concurrency changes, неизменные quality и completion probability. Исследование этим условиям не соответствует:

- поток customer issues динамический, а не fixed set;
- agents могут обслуживать несколько chats одновременно;
- RPH включает resolution rate;
- case mix неоднороден;
- outcome агрегирован на agent-month;
- нет coding-task baseline `Z_i X`.

Поэтому допустимая запись - «throughput вырос на 15% в данном customer-support process», но не `k=0.87` для coding tasks.

## Heterogeneity

### По исходному skill

Working paper строит pre-AI skill index из call efficiency, resolution rate и surveyed customer satisfaction за предыдущий quarter и делит agents на within-firm-month quintiles. Lowest-skill quintile получает `0.29` log point, или около `34%`, прироста RPH; highest-skill quintile не получает прироста RPH (локальный PDF с. 17-18, 40-41).

По decomposed outcomes lower-skill agents имеют наибольшие gains. Для highest-skill workers working paper показывает positive chats/hour, но нулевой effect на AHT и небольшие statistically significant declines в resolution rate и customer satisfaction. То есть ускорение и quality не обязаны совпадать по знаку (локальный PDF с. 18, 41).

Final QJE abstract сохраняет этот qualitative result: less skilled workers улучшают speed и quality, а highest skilled получают small speed gains и small quality declines (QJE p. 889).

### По tenure

Working paper делит agents по tenure на `<1`, `1-2`, `3-6`, `7-12`, `>12` months, контролируя initial skill. Agents с tenure менее месяца получают `0.38` log point, или около `46%`, прироста RPH; для tenure более года effect близок к нулю. У наиболее experienced работников также наблюдаются small negative quality effects (локальный PDF с. 18-19, 40, 42).

Experience curves показывают, что treated agents с двумя месяцами tenure достигают уровня untreated agents с более чем шестью месяцами tenure. Это descriptively согласуется с ускорением движения по experience curve, но само по себе не отделяет learning от непосредственного следования AI recommendations (локальный PDF с. 19, 43).

### По типу и редкости проблемы

Этот анализ относится к финальной версии и отсутствует в локальном working paper. Final abstract сообщает, что gains largest для **moderately rare problems**: у human agents меньше baseline experience, но AI system ещё имеет достаточно training data (QJE p. 889).

Финальный replication code группирует topics по overall frequency и отдельно по within-agent frequency и оценивает change in chat duration с agent, month, tenure и topic controls. Однако без final PDF/table нельзя надёжно назвать subgroup coefficients, uncertainty или более точные journal pages. Безопасный вывод - наличие немонотонной task heterogeneity, а не численная калибровка для конкретных coding-task classes.

## Adherence, learning и retention

### Adherence

Agents часто игнорируют suggestions. Working paper сообщает weighted mean adherence `38%`, IQR `23%-50%`; в обзорном абзаце того же раздела приведено округлённое `35%`. Adherence определяется как copy suggested text либо самостоятельный ввод очень похожего текста (локальный PDF с. 20).

Initial-adherence quintiles коррелируют с returns: примерно `10%` RPH gain в lowest quintile и около `25%` в highest. Авторы прямо предупреждают, что это может отражать selection или selection on gains, а не causal effect следования рекомендации. Adherence со временем растёт, особенно у initially low-adherence и senior workers (локальный PDF с. 20-21, 44-45).

Для M0-M4 это поддерживает dependence от фактического режима использования, но adherence rate не является ни `r`, ни `h`, ни долей autonomous time.

### Learning

Working paper использует software outages: во время редких сбоев treated workers временно не получают recommendations. После более длительной prior exposure agents выполняют chats быстрее даже во время outage; pattern сильнее у high-adherence agents. Авторы интерпретируют это как evidence of durable skill acquisition (локальный PDF с. 22-23, 46-47).

Доказательство **suggestive, не чисто causal**:

- outages rare и not necessarily random;
- post-adoption outage estimates noisy;
- сравниваются разные chats и периоды;
- high adherence endogenous;
- outage может затрагивать разные servers и login cohorts.

Final QJE abstract осторожно сохраняет формулировку «evidence that AI facilitates worker learning» и добавляет improvement in English fluency, particularly among international agents (QJE p. 889). Численный fluency effect по переданному PDF проверить нельзя.

### Retention / attrition

Retention присутствует в local working paper. Для agents с tenure менее шести месяцев AI access ассоциирован примерно с `10` percentage point decline in attrition при baseline `25%`, то есть примерно с `40%` relative reduction. По skill decline значим во всех группах без систематического gradient (локальный PDF с. 28).

Этот result слабее main productivity estimate: attrition случается один раз, поэтому specification не включает agent fixed effects; authors прямо предупреждают, что selective deployment к agents с высокой ожидаемой retention может завысить effect (локальный PDF с. 28).

Final QJE abstract retention не упоминает. Без final PDF этот working-paper result нельзя безусловно атрибутировать version of record.

## Quality и customer experience

Нужно различать четыре уровня outcomes:

1. **Resolution rate:** operational success обращения. В working paper средний gain мал и не проходит обычный 5% threshold, но lower-skill/new workers выигрывают больше, а top workers могут ухудшаться.
2. **NPS:** post-chat survey customer satisfaction. Средний working-paper effect около нуля, хотя subgroup effects различаются.
3. **Customer sentiment:** LLM-based sentiment score текста клиента от `-1` до `1`. Working paper даёт `+0.177`, `SE=0.0133`, baseline `0.141`, что authors описывают как примерно половину SD (локальный PDF с. 27, 56, Table 4).
4. **Manager requests:** доля chats, где customer просит manager/supervisor. Working paper сообщает примерно `25%` decline относительно baseline около `6%` (локальный PDF с. 27-28, 51).

Customer sentiment является model-scored textual outcome, а не direct satisfaction survey. Manager request - proxy customer confidence, не actual escalation. Финальный abstract формулирует более осторожно: customers are more polite and less likely to ask to speak to a manager (QJE p. 889).

## Полный mapping к M0-M4

| Поле модели | Статус | Что даёт источник | Граница переноса |
|---|---|---|---|
| `X`, baseline unit time | **отсутствует** | Есть baseline means customer-support outcomes | Нет универсальной единицы coding effort и no-AI duration одной фиксированной задачи |
| `Z_i` | **conceptual support for heterogeneity** | Effect зависит от skill, tenure и rarity/topic проблемы | Нет task complexity scale, сопоставимой с baseline time `Z_i X`; rarity не равна complexity |
| `k_i^(r)` | **не идентифицируется** | Field evidence показывает context-dependent AI effect | `issues/hour` - composite throughput, не ratio completion times fixed coding task; нельзя ставить `k=1/1.15` |
| `r` | **описан один близкий режим** | Real-time conversational suggestions, optional adherence, human remains responsible | Нет сравнения interactive/delegated/autonomous coding modes; режим не варьируется экспериментально |
| `N` / fixed workload | **отсутствует** | Наблюдается поток примерно 3 млн chats в working paper | Нет заранее фиксированного конечного набора задач с общим completion point |
| `W = X sum Z_i k_i` | **отсутствует** | RPH агрегирует service throughput | Нет AI-weighted total work фиксированного проекта; поток issues и case mix меняются |
| `P` | **не идентифицируется** | CPH учитывает возможность нескольких simultaneous chats | Это human multitasking, не число параллельных coding agents; agent count не варьируется |
| Неделимость / `M_N` (M1) | **отсутствует** | Отдельный chat дискретен как service case | Нет allocation неделимых jobs по `P` executors и longest-task bound |
| DAG / `L` (M2) | **отсутствует** | Внутри diagnosis есть последовательность действий | Precedence graph, critical path и project dependencies не заданы |
| `C(P)` (M3) | **отсутствует** | Инструмент встроен в production workflow | Нет scaling experiment по `P`, agent-agent integration, merge conflicts или coherency overhead |
| `h_i^(r)` | **conceptual only** | Человек читает, выбирает, редактирует и отправляет suggestions; adherence далеко не 100% | Нет двухканального хронометража human-active и AI-autonomous intervals; adherence не равна time share |
| `H = X sum Z_i h_i` | **отсутствует** | Работа остаётся human-in-the-loop | Нет fixed set tasks и суммы capacity-1 human intervals |
| `gamma(P)` | **отсутствует** | CPH отражает фактический multitasking chats | Не варьируется число AI streams и не измеряется switching penalty относительно `P` |
| Makespan | **отсутствует** | AHT - duration отдельного chat; RPH - throughput | Ни одна метрика не является временем завершения фиксированного набора связанных coding tasks |

Источник расположен **перед scheduling layer** M0-M4. Он помогает обосновать, почему параметры должны быть task-, user- и mode-specific и почему нельзя использовать одну productivity metric. Он не калибрует scheduling constraints или multi-agent scaling.

## Что источник поддерживает

1. Generative AI может давать measurable field productivity gain вне лаборатории: final abstract сообщает `+15% issues resolved per hour` у `5,172` agents (QJE p. 889).
2. Средний effect нельзя считать свойством инструмента: heterogeneity по skill, tenure и problem rarity велика.
3. Speed и quality нужно измерять раздельно: lower-skilled agents могут улучшать оба, тогда как highest-skilled получают небольшой speed gain вместе с небольшим quality decline.
4. Composite throughput раскладывается на handle time, concurrency/chats per hour и resolution probability; один headline percentage не раскрывает механизм.
5. Interaction mode имеет значение: agents обладают discretion и часто игнорируют recommendations.
6. Возможно durable learning, но outage evidence следует называть suggestive, а не окончательным доказательством human-capital accumulation.
7. Customer experience может улучшаться даже при малом среднем effect на NPS: sentiment, manager requests и resolution - разные constructs.
8. Problem frequency даёт немонотонную heterogeneity: maximum gain на moderately rare problems поддерживает task-specific calibration, но rarity нельзя отождествлять с `Z`.

## Что источник не позволяет утверждать

1. Что generative AI универсально повышает производительность на 15%.
2. Что `15% issues/hour` означает `15%` сокращение completion time или `k=0.85/0.87`.
3. Что customer-support result переносится на software development или autonomous coding agents.
4. Что работа оценивает эффект `P>1` agents, linear scaling или оптимальное число агентов.
5. Что simultaneous chats эквивалентны параллельным code-agent streams.
6. Что можно оценить `Z`, `W`, неделимость, DAG/`L`, `C(P)`, `h`, `H`, `gamma(P)` или makespan.
7. Что staggered rollout целиком рандомизирован: отдельно упомянут только pilot из 50 agents.
8. Что event-study absence of pretrends доказывает parallel trends и исключает time-varying selection.
9. Что adherence causally создаёт высокий return: adherence endogenous.
10. Что outages дают чистый natural experiment: они rare, noisy и not necessarily random.
11. Что retention effect является столь же надёжным, как main productivity effect; working-paper attrition model не включает agent FE.
12. Что final QJE uncertainty равна working-paper uncertainty: versions различаются.
13. Что все final-QJE subgroup estimates и pages можно восстановить из переданного NBER PDF.

## Отличие от M0-M4

| Измерение | Brynjolfsson, Li и Raymond | M0-M4 |
|---|---|---|
| Центральный вопрос | Field effect AI assistant на worker productivity и experience | Makespan fixed workload при одном developer и `P` coding agents |
| Топология | Один support agent, один real-time assistant, customer chat stream | Один developer как общий human resource, несколько параллельных agent streams |
| Workload | Поток неоднородных customer issues | Заранее заданный набор задач с `Z_i` и `W` |
| Primary outcome | Issues/resolutions per hour | Completion time / makespan и speedup |
| Outcome composition | AHT, CPH с multitasking, resolution rate | Task durations `Z_i k_i X`, allocation и resource-feasible schedule |
| Параллелизм | Agents могут вести несколько chats; число AI assistants не варьируется | Явный `P` executors и effective process parallelism |
| Dependencies | Не заданы как project graph | DAG и critical path `L` |
| Human work | Human chooses and edits suggestions, но time share не измерен | `h_i`, capacity-1 aggregate `H`, non-overlapping human intervals |
| Coordination | Не оценивается как функция scale | `C(P)` и `gamma(P)` разделяют integration и switching overhead |
| Identification | Staggered DiD/event study с observational rollout | Детерминированная модель, требующая внешней empirical calibration |
| Generalizability | Одна enterprise-software support environment | Параметры должны калиброваться для каждой task-tool-mode configuration |

## Проверенные claims для Related Work

1. Финальная QJE-версия анализирует staggered introduction generative AI assistant на данных `5,172` customer-support agents и сообщает средний рост issues resolved per hour на `15%`; это field throughput effect, не coding-task completion-time effect (QJE p. 889).
2. Final abstract подчёркивает substantial heterogeneity: less experienced/lower-skilled workers улучшают speed и quality, а most experienced/highest-skilled получают небольшие gains по speed и небольшие declines по quality (QJE p. 889).
3. В final version gains largest на moderately rare problems, где human baseline experience ограничен, но AI имеет достаточно training data. Это поддерживает task-specific effect, а не единый `k` (QJE p. 889).
4. Локальная working-paper decomposition показывает механизм headline throughput: shorter handle time и больше chats per hour при лишь небольшом и неопределённом на 5% уровне среднем improvement resolution rate; эти exact numbers нельзя выдавать за final QJE table (локальный PDF с. 16-17, 55).
5. Staggered rollout оценивается DiD и interaction-weighted event studies с agent/time/tenure controls, но основной rollout не заявлен как randomized; причинный вывод зависит от parallel trends и отсутствия time-varying selection (локальный PDF с. 13, 15-16, 38-39).
6. Outage analysis совместим с durable learning, но outages rare, noisy и nonrandom; корректна формулировка «suggestive evidence», а не установленная величина retention of skill (локальный PDF с. 22-23).
7. Исследование не варьирует `P`, не задаёт DAG и не разделяет human/AI time, поэтому не валидирует multi-agent makespan, `C(P)`, `h`, `H` или `gamma(P)`.

## Короткий вариант встраивания

> Brynjolfsson, Li и Raymond (2025) изучают staggered deployment generative AI assistant среди 5,172 customer-support agents и сообщают средний рост issues resolved per hour на 15%. Эффект существенно неоднороден: менее опытные и lower-skilled workers улучшают как speed, так и quality, тогда как наиболее experienced и skilled получают малый выигрыш по speed и небольшое ухудшение quality; максимальные gains наблюдаются на moderately rare problems. Для нашей модели это field evidence в пользу task-, user- и mode-specific эффекта, но не численная оценка `k`: issues/hour объединяет handle time, multitasking и resolution rate и не равно времени завершения фиксированной coding task. Исследование также не варьирует число агентов и не идентифицирует неделимость, DAG/`L`, `C(P)`, человеческую долю `h` или `gamma(P)`.

## Evidence pages и provenance

| Источник / страница | Раздел / объект | Опорное содержание |
|---|---|---|
| QJE p. 889, final abstract | Metadata; sample; headline findings | `5,172` agents; `+15% issues/hour`; heterogeneity по skill/experience; learning; English fluency; moderately rare problems; customer politeness и manager requests |
| Локальный PDF с. 1 | NBER cover | Working Paper 31161, April 2023 revised November 2023; not peer-reviewed warning |
| Локальный PDF с. 2 | Working-paper abstract | `5,179` agents; `+14%`; novice/low-skill `+34%`; sentiment, retention, learning claims working-paper version |
| Локальный PDF с. 11-12 | Setting and AI system | Fortune 500 software firm, geography, random chat assignment, 40-minute chats, AHT/RR/NPS, training data and suggestions |
| Локальный PDF с. 13 | Deployment | Seven-week randomized pilot with 50 agents; gradual agent-level rollout; bulk adoption November 2020-February 2021 |
| Локальный PDF с. 13-14 | Sample and outcomes | 3 million chats, 5,179 agents, 1,636 treated post-AI; unequal outcome availability; definition and decomposition RPH |
| Локальный PDF с. 15 | Empirical Strategy | DiD equation, agent/time/tenure FE, clustered SE, assumptions and heterogeneous-timing estimators |
| Локальный PDF с. 16-17 | Main Results | Working-paper `13.8%`; AHT/CPH/RR/NPS decomposition and interpretation |
| Локальный PDF с. 17-19 | Skill and tenure heterogeneity | Lowest-skill `34%`, newest `46%`, null/negative quality patterns at top, experience curves |
| Локальный PDF с. 20-21 | Adherence | Definition, mean/IQR, endogenous return gradient, convergence over time |
| Локальный PDF с. 22-23 | Learning | Outage design, noisy/nonrandom caveat, duration patterns by exposure and adherence |
| Локальный PDF с. 24-26 | Communication change | Embeddings, within-worker change, low/high-skill convergence; suggestive mechanism |
| Локальный PDF с. 26-28 | Experience of work | Sentiment design, manager requests, attrition estimates and stronger causal caveat |
| Локальный PDF с. 29-30 | Conclusion and limitations | Generalizability, long-run labor/skill/job-design unknowns, stable-product boundary |
| Локальный PDF с. 38-39 | Event-study figures | 95% CIs, pre/post dynamics for RPH and decomposed outcomes |
| Локальный PDF с. 40-43 | Heterogeneity figures | Skill, tenure and experience curves with confidence intervals |
| Локальный PDF с. 53 | Table 1 | Exact working-paper descriptive sample and outcome means |
| Локальный PDF с. 54 | Table 2 | Exact working-paper main coefficients, SE, observations and FE specifications |
| Локальный PDF с. 55 | Table 3 | Exact working-paper AHT, CPH, RR and NPS decomposition |
| Локальный PDF с. 56 | Table 4 | Exact working-paper customer and agent sentiment estimates |

## Итоговая оценка

Это сильный field source для тезиса, что эффект generative AI является свойством конкретной связки worker-task-process, а не постоянным коэффициентом инструмента. Большая operational sample, production deployment, decomposed outcomes и heterogeneity analyses существенно полезнее одного лабораторного average. Особенно важны расхождение speed и quality у top workers и немонотонность эффекта по rarity проблемы.

Для M0-M4 источник остаётся внешним evidence layer, а не parameter estimator. Его primary outcome - throughput динамического service process, не makespan фиксированного workload; число agents `P`, зависимости, интеграционный overhead и человеческое время не измерены. Кроме того, переданный PDF является старой NBER-версией. Поэтому в статье следует цитировать final QJE metadata и `15%`, а exact working-paper coefficients использовать только для методологического разбора либо после повторной сверки с настоящим QJE PDF. До получения version of record нельзя указывать final numerical uncertainty или переносить working-paper pages и tables как журнальные.
