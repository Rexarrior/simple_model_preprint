# Becker et al. (2025): контекстный пример `k > 1` у опытных разработчиков в знакомых репозиториях

## Назначение и границы обзора

Этот документ разбирает один источник применительно к модели M0-M4 для fixed-workload makespan ячейки «один разработчик - `P` кодовых ИИ-агентов». Работа важна как редкий причинный пример, в котором разрешение использовать ИИ соответствует увеличению времени выполнения: в изученной конфигурации контекстная оценка равна примерно `k = 1.19`, а не `k < 1`.

Главная граница переноса: Becker et al. изучают опытных open-source разработчиков, выполняющих реальные задачи в крупных зрелых репозиториях, с которыми они знакомы в среднем пять лет. Это не универсальная оценка влияния ИИ на программирование. Treatment разрешал разные инструменты и режимы, результат относится к frontier февраля-июня 2025 года, а основной outcome является self-reported **active implementation time** отдельной задачи, включая активную доработку после review, но исключая календарное ожидание review. Исследование не варьирует число одновременно работающих агентов и не измеряет project makespan.

Локальный PDF содержит 51 страницу. Основной текст занимает PDF-страницы 1-12; приложения A-B начинаются на странице 17, factor analysis C - на странице 18, empirical strategy D - на странице 28, дополнительные анализы E - на странице 31, описание инструментов F - на странице 35, рекрутинг, инструкции и статистика G - на страницах 37-51. Номера ниже относятся к PDF-страницам локальной копии.

## Библиография, статус и версия

**Полная ссылка:** Joel Becker, Nate Rush, Beth Barnes, and David Rein. “Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.” arXiv:2507.09089v2 [cs.AI], 2025. DOI: [10.48550/arXiv.2507.09089](https://doi.org/10.48550/arXiv.2507.09089).

**Имена авторов:** на титульной странице указано `Beth Barnes`; metadata arXiv раскрывает это имя как `Elizabeth Barnes`.

**Проверенная версия:** на первой странице указано `arXiv:2507.09089v2 [cs.AI] 25 Jul 2025` (PDF с. 1). Metadata arXiv также указывает v2 как текущую версию, 51 страницу, 8 таблиц и 22 рисунка. Локальная копия: `/Users/rexarrior/work/articles/simple_model_full/literature/becker2025.pdf`, SHA-256 `3e18d9e097a3163dbae662e8b7c68ace0510be433891994b136ae7730beab25c`.

**Статус:** препринт arXiv. В PDF не указано рецензируемое журнальное или конференционное издание, поэтому по проверенной версии источник нельзя обозначать как peer-reviewed.

**Институциональный контекст:** все авторы аффилированы с Model Evaluation & Threat Research (METR). Исследование оплачивает разработчикам участие и предоставляет Cursor Pro; отдельное заявление о конфликте интересов или финансировании в проверенном PDF не найдено.

## Исследовательские вопросы и тип доказательства

Основной причинный вопрос: как разрешение использовать доступные в начале 2025 года генеративные AI tools меняет время выполнения реальных repository issues опытными разработчиками, хорошо знакомыми со своими проектами (PDF с. 1-5).

Работа также рассматривает три вспомогательных вопроса:

1. Насколько ожидания разработчиков до задачи, их post hoc оценки и прогнозы внешних экспертов совпадают с измеренным эффектом.
2. Как меняется распределение времени между coding, search, prompting, ожиданием и review AI output.
3. Какие свойства разработчиков, задач, репозиториев, инструментов и экспериментального дизайна могут объяснять наблюдаемое замедление.

Тип доказательства - field randomized controlled trial с рандомизацией на уровне issue и повторными наблюдениями внутри разработчика. Причинная интерпретация сильнее, чем у survey или корреляционного field study, но population не выбрана случайно, treatment неоднороден, а основной outcome сообщается самими участниками.

## Pre-registration и заранее заданный дизайн

PDF не сообщает preregistration, зарегистрированный protocol, публичный prospective analysis plan или заранее проведённый power calculation. Поэтому нельзя называть исследование preregistered или утверждать, что primary specification и все анализы были зафиксированы до просмотра данных.

Что действительно было задано до treatment assignment:

1. Разработчик формировал список реальных задач и давал для каждой прогноз времени с ИИ и без ИИ.
2. Scope issue задавался до рандомизации, что ограничивает возможность создавать больше или меньше задач в зависимости от treatment.
3. После назначения разработчик должен был довести issue до pull request, пройти обычный процесс review и отдельно записать initial и post-review implementation time (PDF с. 5-7, 37-42).

Слово `a priori` в статье относится к перечню потенциальных факторов замедления, а не к preregistration. Авторы прямо называют factor analysis speculative/suggestive и предупреждают, что исследование не имеет мощности для множественных subset comparisons (PDF с. 2, 10-11, 18-28).

Randomization procedure менялась по ходу исследования: первые 25 завершённых issues распределялись block-randomization scheme, которую затем отменили из-за малых issue lists, после чего использовали simulated fair coin flip. Исключение первых 25 issues даёт сходное замедление 20%, но изменение процедуры является частью фактического дизайна, а не заранее неизменным protocol (PDF с. 5, 33).

## Разработчики и репозитории

### Рекрутинг

Разработчиков искали через профессиональные сети, ML-сообщества и GitHub profiles активных contributors к популярным репозиториям. Кандидат должен был иметь как минимум год профессионального опыта, как минимум шесть месяцев активно поддерживать выбранный repository, а repository обычно должен был иметь не менее 500 stars и 3,000 строк кода. Из 51 заполнившего initial interest survey отобрали около 20 подходящих участников; трёх позднее исключили из сбора данных: у двух репозитории приостановили разработку, у одного выявили систематическое нарушение treatment. Итоговый анализ включает 16 разработчиков (PDF с. 37-38, 45).

Участники были опытными software engineers, обычно с более чем десятилетием общего опыта. В среднем каждый работал со своим repository пять лет, что составляло 59% его возраста, и имел около 1,500 commits в нём. 93% ранее использовали web LLMs, 50% - GitHub Copilot, 44% - Cursor. Следовательно, это не выборка AI-naive новичков, но и не выборка исключительно expert Cursor users (PDF с. 2, 4, 23-24, 45-46).

Участникам платили `$150` за час, а не за число закрытых issues. Это снижало стимул искусственно дробить задачи или жертвовать quality ради count, но оплата по времени не создаёт прямого финансового стимула минимизировать duration каждого issue (PDF с. 4, 37).

### Репозитории

Исследование охватывает 14 крупных зрелых open-source repositories. В среднем они имели около 23,000 stars, 1.1 млн строк кода, 4,900 forks, 20,000 commits, 710 contributors и возраст около десяти лет. Среди раскрытых проектов присутствуют `stdlib-js`, `ghc`, `scikit-learn`, `transformers`, `hypothesis`, `jsdom` и другие; часть названий анонимизирована (PDF с. 4, 45-46).

Авторы характеризуют проекты как имеющие высокий quality bar. Это содержательная часть setting: опытный maintainer обладает tacit repository context, а accepted change должен соответствовать стилю, документации, тестам и неявным требованиям проекта, которые не сводятся к прохождению одного видимого test suite (PDF с. 4, 12, 19-20).

## Задачи и их отбор

Разработчики сами предоставляли списки полезных для своих repositories issues: bug fixes, features, refactoring и другие обычные work items. Issues могли существовать до исследования или создаваться во время него; примерно половина не была формально заведена в публичном tracker и велась отдельно для эксперимента. Ключевое условие состояло не в дате создания, а в фиксации issue и forecast **до** random assignment (PDF с. 5, 20-22, 37-42).

Задачи занимали от минут до часов, в среднем около двух часов active implementation time. Участников просили выбирать issues максимум примерно на два часа или разбивать более крупные работы. В exit interviews они называли их обычной работой, но находящейся на коротком краю нормального распределения: более крупные design discussions, review чужих PR и другие виды contribution не представлены (PDF с. 2, 5, 20-21).

Это одновременно сильная и ограничивающая черта:

1. **Сильная:** treatment не может увеличить число issues после назначения; сравнивается время заранее заданных work items.
2. **Ограничивающая:** workload не является фиксированным проектом с общей границей завершения; это выбранная разработчиками выборка сравнительно коротких issues.
3. **Ограничивающая:** разбиение задач до `<=2` часов меняет гранулярность и может удалять длинные зависимости, интеграционные фазы и архитектурную работу.
4. **Ограничивающая:** разработчики выбирали порядок после randomization и иногда работали над несколькими issues одновременно, поэтому issue-level active time не задаёт последовательное project schedule (PDF с. 5, 22).

## Рандомизация, treatment и compliance

### Рандомизация

После фиксации issue list и двух forecasts каждая задача назначалась в `AI-allowed` или `AI-disallowed`. Основная процедура - simulated fair coin flip; первые 25 issues использовали раннюю block scheme. В завершённой выборке 136 issues оказались AI-allowed и 110 AI-disallowed. Отклонение от 50/50 не было статистически различимо (`p=0.10`), а ex ante forecasts времени были сходны между arms (`p=0.28` и `p=0.56` для no-AI и AI forecasts; PDF с. 5, 8, 31, 33).

Алгоритм генерации coin flips, allocation concealment и момент раскрытия назначения описаны не настолько подробно, чтобы провести полный риск-of-bias audit. Blinding невозможно: разработчики знали, разрешён ли им AI, и исследователи могли видеть recordings.

### AI-allowed

В AI-allowed arm разрешались любые AI tools и модели, включая решение не использовать ИИ, если участник считал его бесполезным. METR предоставляла Cursor Pro, проводила 30-минутное обучение Cursor Agent и периодически давала советы по prompting. Cursor Agent мог искать и менять файлы, запускать shell commands, задавать вопросы и итеративно отлаживать программу без постоянного ввода пользователя (PDF с. 6, 37, 42).

В 44 валидных размеченных AI-allowed recordings использование моделей распределялось так:

| Модель | Доля issues в размеченной подвыборке |
|---|---:|
| Claude 3.7 Sonnet thinking | 25% |
| Claude 3.7 Sonnet | 34% |
| Claude 3.5 Sonnet | 23% |
| GPT-4o | 11% |
| Gemini 2.5 Pro | 3% |
| o1 | 2% |

Большинство issues выполнялось в феврале-марте 2025 года. Точная версия Cursor client, даты backend updates, model checkpoints и sampling parameters не зафиксированы. Cursor Agent/Composer и Cursor Chat использовались соответственно примерно в 55% и 48% AI-allowed issues; категории могли пересекаться. AI autocomplete применялся в большинстве AI-allowed issues (PDF с. 6, 25, 28, 36).

### AI-disallowed и отклонения от назначения

В AI-disallowed arm запрещались generative AI и LLM-based tab completion; обычный search оставался разрешён. По recordings авторы нашли три случая AI use среди 54 размеченных AI-disallowed issues, то есть около 6%, как минимум один случай был случайным. В AI-allowed arm в 16.4% из 44 валидных recordings участник не prompt'ил модель, хотя autocomplete мог использоваться. Это означает, что primary estimate является **intent-to-allow**, а не per-protocol effect фактического использования конкретного AI mode (PDF с. 5, 26).

## Outcome и учёт времени

### Primary outcome

Primary outcome - total implementation time issue:

1. `initial implementation time`: активное время от начала работы до PR, готового к review;
2. `post-review implementation time`: активное время на изменения после первого review, включая исправления и merge conflicts.

Календарное ожидание reviewer не учитывалось. Например, три дня ожидания и 20 минут исправлений давали 20 минут post-review time. Поэтому термин `completion time` в paper не равен elapsed calendar duration от старта issue до merge. Участники self-report'или обе компоненты после задачи; для issues без завершённого review post-review time импутировался средним по treatment arm (PDF с. 5-7, 27, 40-42).

Основной outcome включает 246 завершённых initial implementations: 136 AI-allowed и 110 AI-disallowed. Из 259 randomized valid issues 13 не были завершены, 6 AI-allowed и 7 AI-disallowed. Ещё 24 issues были сознательно сняты по причинам вроде высокой сложности, утраты актуальности или выполнения другим maintainer; авторы проверяли, что причины не связаны с assignment (PDF с. 8, 26-27).

### Screen-recording validation

Авторы вручную разметили 128 recordings общей длительностью 143 часа с разрешением около 10 секунд. После исключения cheating, broken recordings и расхождения более 20% между video и self-report осталось 74 recordings и 84 часа. Более короткие recordings размечались раньше, а небольшие post-review changes часто не записывались, поэтому activity sample не является случайным (PDF с. 8, 45-49).

На общей подвыборке video-based duration дал 25% slowdown, а self-reported time для той же подвыборки - 24%, что снижает опасение о крупной differential reporting bias. Однако screen recordings не заменяют objective timestamps для всей выборки (PDF с. 27).

### Activity outcomes

При AI-allowed разработчики тратили меньшую долю времени на непосредственное coding и search, но добавляли prompting, ожидание и review AI output. В 44 валидных AI-allowed recordings средние доли составляли примерно 8% на prompting, 4% на ожидание generation и 9% на review/cleaning output. Эти категории объясняют механизм издержек, но не дают `h`: остальная активная работа человека также входит в человеческий ресурс (PDF с. 8-10, 20, 25, 33-34).

## Оценивание эффекта и точный смысл 19%

Авторы определяют относительное изменение времени как

\[
S = \frac{E[T\mid AI\ allowed]}{E[T\mid AI\ disallowed]} - 1.
\]

Primary specification - OLS log-linear regression

\[
\log T_i = \alpha + \beta AI_i + \delta \log \widehat{T}^{NoAI}_i + \varepsilon_i,
\]

где no-AI forecast получен до assignment и используется как proxy сложности issue. Reported effect преобразуется как `S = exp(beta) - 1`. По умолчанию 95% confidence interval строится с HC3 standard errors и затем преобразуется с log scale (PDF с. 6-7, 28-30).

Основной результат:

\[
\widehat{S}=+0.19, \qquad 95\%\ CI=[+0.01,+0.39].
\]

То есть разрешение использовать ИИ связано с **19% увеличением regression-adjusted mean implementation time**, а primary 95% CI соответствует увеличению от 1% до 39%. На языке M0-M4:

\[
\widehat{k}_{\text{experienced OSS, early-2025, intent-to-allow}}
=1+\widehat{S}
=1.19,
\qquad 95\%\ CI\approx[1.01,1.39].
\]

Это не «снижение скорости на 19%». Если механически определить rate как `1/T`, reciprocal point ratio равен `1/1.19≈0.84`, то есть примерно на 16% ниже. Для статьи безопаснее использовать формулировку «время увеличилось на 19%» или `k≈1.19` (PDF с. 1-2, 6, 28-30).

Raw ratio средних времён давал более сильное увеличение примерно на 34%. Regression снижает оценку до 19%, потому что AI-allowed issues случайно оказались немного сложнее по ex ante no-AI forecasts; различие forecast difficulty при этом само по себе статистически незначимо (PDF с. 8-9, 31).

## Неопределённость и robustness

1. **Primary uncertainty:** HC3 95% CI `[1%,39%]` на шкале изменения времени исключает ноль лишь с небольшим запасом (PDF с. 2, 28-30).
2. **Зависимость внутри developer:** treatment назначался issue-level, но observations повторяются у 16 разработчиков. Developer-clustered, CR2 и CR3 intervals дают сходные point estimate и границы около нуля; two-stage bootstrap по developers, затем issues даёт заметно более широкий interval, пересекающий ноль. Следовательно, вывод о направлении устойчив по point estimates, но формальная значимость чувствительнее к способу учёта малой developer-level sample (PDF с. 28-29).
3. **Randomization scheme:** исключение первых 25 block-randomized issues даёт 20% slowdown (PDF с. 33).
4. **Outcome imputation:** экстремальные варианты post-review imputation дают 14% и 23% slowdown; point estimate не исчезает (PDF с. 27).
5. **Self-report validation:** video duration и self-report на одной подвыборке дают 25% и 24% slowdown (PDF с. 27).
6. **Alternative estimators:** ratio of means и regressions с другими covariates сохраняют положительный point estimate, хотя intervals различаются и некоторые включают ноль (PDF с. 27-30).
7. **Dropout:** 13 randomized valid issues не завершены почти симметрично между arms; subset analyses без dropout также дают slowdown. Отдельные subgroup estimates имеют широкие intervals и не должны использоваться как подтверждённые causal mechanisms (PDF с. 26).
8. **Multiple comparisons:** factor analysis содержит много post hoc/subset comparisons без дизайна, обеспечивающего мощность для них. Авторы сами называют эту часть suggestive (PDF с. 10, 18-28).

## Ожидания против измеренного эффекта

| Источник оценки | Ожидаемое изменение времени | Сопоставимый `k` |
|---|---:|---:|
| Developers до randomization | 24% быстрее | `0.76` |
| Developers post hoc | 20% быстрее | `0.80` |
| 34 economics experts | 39% быстрее | `0.61` |
| 54 ML experts | 38% быстрее | `0.62` |
| Измеренный primary effect | 19% медленнее | `1.19`, 95% CI `[1.01,1.39]` |

Developers достаточно хорошо прогнозировали относительную сложность issues: корреляция forecast с observed time равнялась `0.64` в AI-allowed и `0.59` в AI-disallowed arm. Ошибка относилась именно к знаку и величине AI effect. Даже после участия разработчики оценивали ускорение, хотя measured estimate показывал замедление (PDF с. 7-9, 34).

Для M0-M4 это поддерживает требование калибровать `k` по наблюдаемому времени, а не по self-report, adoption или экспертному forecast. Одновременно post hoc miscalibration помогает объяснить, почему участники продолжали использовать AI, хотя могли отказаться от него в AI-allowed arm (PDF с. 18).

## Качество и review outcomes

Задача считалась доведённой до результата, когда разработчик был удовлетворён implementation, открыл PR и прошёл обычный repository review. Total time включает активные исправления после review; это лучше, чем outcome до первого code generation, потому что часть rework возвращается в измеренное время (PDF с. 5-7, 35-36, 40-42).

Однако quality не измерена независимой стандартизированной шкалой:

1. AI-allowed и AI-disallowed PR проходили разные repository-specific review processes.
2. Авторы называют PR quality качественно сходным между conditions, но не публикуют blinded defect audit.
3. Mean post-review implementation time составлял 15 минут для AI-allowed и 9 минут для AI-disallowed; различие названо статистически незначимым, без точного `p` или CI (PDF с. 23).
4. Около 12% post-review times отсутствовали к концу study и были импутированы (PDF с. 27).
5. Не измерены долгосрочные defects, maintainability, security, operational incidents или lifecycle cost после merge.

Следовательно, источник поддерживает claim, что основной time effect не объясняется очевидным падением initial PR quality по доступным данным. Он не доказывает quality equivalence и не превращает implementation time в полноценную quality-adjusted productivity metric.

## Возможные механизмы замедления

Factor analysis выделяет пять факторов, которые авторы считают вероятно способствующими результату:

1. переоценка полезности AI самими разработчиками;
2. высокая familiarity разработчиков с repositories и типами задач;
3. размер и сложность зрелых repositories;
4. низкая reliability AI generations;
5. неявный repository context, которым владеет maintainer, но не модель.

Особенно релевантны для `k` и `h` наблюдения о reliability: принималось менее 44% предложенных строк Cursor; 75% разработчиков сообщали, что читают каждую строку принятого AI code; 56% обычно вносили крупные изменения; все сообщали о необходимости хотя бы какой-то modification; в размеченной подвыборке около 9% времени уходило на review/cleaning AI output (PDF с. 19-20).

Эти данные дают правдоподобный механизм `k>1`: генерация может уменьшать typing/search, но добавлять prompting, waiting, review, cleanup, rejected trajectories и возврат к ручной реализации. Factor analysis не идентифицирует причинный вклад каждого механизма отдельно, поэтому нельзя разложить 19% по компонентам или считать перечисленные факторы mediator estimates.

## Появляются ли concurrent agents

Нет, concurrent-agent supervision не является treatment и не измеряется как отдельный фактор.

1. Cursor Agent способен автономно выполнять многошаговую работу внутри issue, но study не назначает `P` и не сравнивает один агент с несколькими.
2. Разработчикам разрешалось работать над несколькими issues одновременно, однако paper не сообщает число параллельных agent instances, overlap intervals или schedule каждого issue (PDF с. 5).
3. В Appendix C авторы упоминают sampling many agent trajectories in parallel с LLM judge только как гипотетическую более сильную elicitation strategy и прямо говорят, что их данные не дают evidence о ней (PDF с. 25).
4. Activity labels описывают один текущий экранный workflow: prompt, generation wait, reading, acceptance/rejection и cleanup. Они не размечают переключение между несколькими agent streams как экспериментально заданный `P` (PDF с. 45-49).

Поэтому источник следует использовать как контекстную task-level калибровку до multi-agent scheduling layer, а не как наблюдение отрицательного или положительного масштабирования по `P`.

## Ограничения и внешняя применимость

### Ограничения, признанные авторами

1. Setting специфичен: опытные maintainers, знакомые repositories, крупные зрелые codebases и высокие quality standards. Результат совместим с ускорением новичков, unfamiliar-codebase work и greenfield projects (PDF с. 3, 12).
2. Более надёжные, быстрые или лучше elicited systems могут дать другой эффект даже в том же setting (PDF с. 12, 25).
3. Tasks находятся на коротком краю реальной работы и не включают весь спектр contribution, design и review activities (PDF с. 20-21).
4. Sampling bias recruitment нельзя исключить: разработчики, сильно зависящие от AI, могли отказаться участвовать из-за AI-disallowed arm (PDF с. 22).
5. Completion order выбирался после treatment assignment, что допускает bias по энергии, приоритету или моменту выполнения (PDF с. 22).
6. Эксперимент не blinded и мог стимулировать overuse AI у части участников (PDF с. 20-21).

### Дополнительные ограничения для переноса в M0-M4

1. **Нет preregistration.** Primary analysis и distinction primary/exploratory нельзя проверить по prospective registry.
2. **Малая cluster sample.** 246 issues не устраняют неопределённость от 16 non-random developers; two-stage developer bootstrap шире primary HC3 interval.
3. **Неоднородный treatment.** `AI-allowed` смешивает Cursor Agent, chat, autocomplete, web interfaces, разные модели и решение не использовать AI.
4. **Версия быстро устаревает.** Это snapshot февраля-июня 2025 года, преимущественно февраля-марта; нельзя переносить point estimate на поздние модели.
5. **Active time не makespan.** Календарное ожидание review исключено; overlapping issues не образуют измеренный end-to-end schedule.
6. **Self-report.** Основной time outcome не строится из автоматических start/finish timestamps, хотя video subset даёт сходный результат.
7. **Task selection и granularity.** Developers выбирали полезные issues и дробили длинные работы, поэтому sample не является случайным fixed workload реального проекта.
8. **Incomplete outcomes.** Часть randomized issues не завершена или снята; time-to-event/censoring model не используется.
9. **Quality equivalence не установлена.** Обычный PR process повышает realism, но не является общей blinded quality metric.
10. **Нет двухканального полного хронометража.** Screen labels полезны, но не размечают для всех задач все human и autonomous intervals в форме `a_i+h_i`.
11. **Нет multi-agent variation.** `P`, overlap agents, integration conflicts и switching между агентными потоками не задавались и не оценивались.

## Mapping ко всем параметрам M0-M4

Здесь **contextual** означает допустимый эмпирический input при сохранении setting; **mechanism only** означает наблюдение механизма без идентификации параметра; **absent** означает, что источник не измеряет объект.

| Параметр M0-M4 | Статус | Что можно сопоставить | Точная граница |
|---|---|---|---|
| `X`, baseline unit time | **contextual, неотделимый от `Z_i`** | No-AI forecast до randomization служит proxy baseline duration/difficulty; AI-disallowed arm задаёт counterfactual distribution | Нет единой базовой единицы `X`, paired no-AI time для каждого issue или калиброванной шкалы story points |
| `Z_i` / `Z` | **partial proxy** | `No-AI forecast_i` входит в regression как proxy сложности | Forecast не равен объективному `Z_i X`; errors и developer-specific scale не моделируются отдельно |
| `k_i^(r)` | **contextual group average** | Primary ratio соответствует `k≈1.19`, 95% CI `[1.01,1.39]`, для experienced OSS / early-2025 / intent-to-allow | Это adjusted average treatment effect, а не индивидуальный task ratio; смешаны tools, modes, non-use и developers |
| `r`, режим | **описан, но treatment неоднороден** | Cursor Agent/Composer, chat, autocomplete и web LLM; predominantly Claude 3.5/3.7 Sonnet | Нельзя приписать `k=1.19` одному чистому режиму; режим выбирался после assignment самим developer |
| `N` и fixed workload | **partial на уровне списка issues** | Issues определялись до randomization, что фиксирует task scope лучше output counts | Нет одного проекта с общей fixed completion boundary; lists выбирались developers, порядок и часть completion менялись |
| `W = X sum Z_i k_i` | **absent как project quantity** | Можно агрегировать self-reported active times post hoc | Paper оценивает expectation ratio между arms, а не суммарную AI-weighted работу одного и того же workload |
| `P` | **не варьируется и не наблюдается** | Для иллюстрации `k` результат можно условно поместить перед M1-M4 как однопоточный task-level input | Иногда developers работали над несколькими issues; число concurrent agent instances не записано. Нельзя считать study экспериментом `P=1` против `P>1` |
| Неделимость / `M_N` (M1) | **partial task-unit analogue** | Каждый заранее заданный issue является отдельной work unit | Issues длиннее двух часов предлагалось дробить; нет allocation по identical agents, longest-job bound или makespan optimization |
| DAG / `L` (M2) | **absent** | Eligibility требовала список относительно независимых work items | Precedence graph, critical path и project dependencies не собирались; знакомый repository не является заданным DAG |
| `C(P)` (M3) | **absent** | Внутри issue наблюдаются cleanup и tool failures | Они возникают уже в one-task AI workflow и должны входить в `k`; agent-agent integration overhead при росте `P` не измерен |
| `a_i^(r)` | **mechanism only** | Generation wait и autonomous Cursor steps наблюдаются в recordings | Нет полной разметки автономного agent time для всех tasks; active-time convention не задаёт отдельный `a_i` |
| `h_i^(r)` | **mechanism only** | Prompting, reading, review, cleaning, testing, debugging и manual coding явно наблюдаются | Доли 8%/9%/4% относятся лишь к отдельным categories и biased video subset; всё остальное human time не превращено в нормированное `h_i` |
| `H = X sum Z_i h_i` | **absent** | Можно видеть, что human work остаётся существенной частью AI-allowed sessions | Нет fixed workload и полного двухканального хронометража, поэтому capacity-1 сумму `H` вычислить нельзя |
| `gamma(P)` | **absent** | Developers иногда вели несколько issues, что делает switching правдоподобным | Число streams, switch events и recovery time не измерены; зависимости penalty от `P` нет |
| Makespan | **не измеряется** | Active implementation time является duration/service-time proxy для отдельного issue | Passive review wait исключён, issues могут overlap, общий start/end проекта отсутствует; outcome не равен fixed-workload elapsed makespan |

### Корректная формула переноса

Для узкой иллюстрации можно записать:

\[
\widehat{k}_{\substack{experienced\ OSS\ maintainers,\\
early\text{-}2025\ AI,\ intent\text{-}to\text{-}allow}}
=\exp(\widehat{\beta})
\approx 1.19,
\qquad 95\%\ CI\approx[1.01,1.39].
\]

Индекс обязан сохранять population, repository familiarity/maturity, task-selection rule, tool period, treatment policy и outcome definition. В M0 этот input иллюстрирует возможность `k>1`. Из него алгебраически следует лишь модельное утверждение, что при равномерном `k=1.19` идеальный параллелизм должен удовлетворять `P>1.19` для выигрыша по линейной части. **Becker et al. не проверяют этот вывод:** при `P>1` могут измениться режим, `k`, `C(P)`, `h`, `H`, `gamma(P)` и available DAG parallelism.

## Что источник поддерживает для M0-M4

1. **Контекстный знак `k>1`.** Для experienced maintainers в знакомых mature repositories разрешение early-2025 AI увеличило adjusted active implementation time на 19%, что соответствует `k≈1.19`, 95% CI `[1.01,1.39]` (PDF с. 1-2, 6, 28-30).
2. **Task/user/repository specificity.** Setting существенно отличается от synthetic greenfield tasks; familiarity, tacit context и quality bar правдоподобно влияют на `k` (PDF с. 3-4, 18-20).
3. **Измерение важнее ожиданий.** Developer и expert forecasts предсказывали ускорение, а measured effect имел противоположный знак; self-report полезности не является оценкой duration factor (PDF с. 1-2, 7-9, 34).
4. **Endogenous AI use.** Даже при возможности отказаться от AI участники часто использовали его, поскольку ошибочно считали полезным; operational `k` должен охватывать весь режим принятия решений, а не только техническую latency модели (PDF с. 18).
5. **Состав one-stream overhead.** Prompting, waiting, review, cleanup, rejected output и manual reimplementation входят в наблюдаемое время и по конвенции M0-M4 относятся к `k(P=1,r)`, а не к `C(P)` (PDF с. 8-10, 19-20, 25).
6. **Quality gate должен входить во время.** Active post-review fixes учитываются, поэтому task completion не заканчивается на первой генерации или первом PR (PDF с. 5-7, 40-42).
7. **Uncertainty должна сопровождать `k`.** Primary interval узко исключает ноль при HC3, но developer-level bootstrap шире; калибровка требует distribution или conservative quantile, а не одной точки (PDF с. 28-30).

## Что источник не позволяет утверждать

1. Что AI универсально замедляет software development на 19%.
2. Что результат применим к менее опытным разработчикам, unfamiliar repositories, greenfield tasks, другим языкам или поздним моделям.
3. Что `19% slowdown` означает снижение rate на 19%; оценено увеличение времени на 19%.
4. Что `k=1.19` является свойством Claude 3.7, Cursor Agent или любого отдельного режима: treatment смешанный и intent-to-allow.
5. Что AI ухудшил code quality: доступные review indicators не показывают установленного различия, но quality equivalence также не доказана.
6. Что фактор familiarity причинно создаёт slowdown: subgroup/factor analysis exploratory и underpowered.
7. Что можно вычислить `h` из долей prompting, waiting или review. Большая часть человеческой активности находится в других categories.
8. Что paper оценивает `W`, project effort или elapsed makespan. Он оценивает active implementation time отдельных issues.
9. Что наблюдался multi-agent parallelism. `P` не назначался, число concurrent agents не фиксировалось.
10. Что `P=2` или иной parallelism компенсирует `k=1.19`. Это вывод M0 при дополнительных предположениях, а не эмпирический результат Becker et al.
11. Что источник валидирует неделимость, DAG/`L`, `C(P)`, capacity-1 `H` или `gamma(P)`.
12. Что primary estimate полностью нечувствителен к small-cluster uncertainty: two-stage bootstrap interval шире и пересекает ноль.
13. Что study preregistered: в PDF такой статус не сообщается.

## Отличие от M0-M4

| Измерение | Becker et al. (2025) | M0-M4 |
|---|---|---|
| Центральный вопрос | Причинный эффект разрешения AI на active implementation time реальных issues | Makespan фиксированного набора связанных задач при одном разработчике и `P` agents |
| Топология | Developer выполняет issue с разрешённым набором AI tools; concurrent agent count не задан | Звезда «один developer - `P` параллельных coding agents» |
| Workload | Выбранные developers короткие issues, randomized между arms | Один фиксированный workload с `Z_i`, `W` и общей completion boundary |
| Baseline | AI-disallowed issues и pre-randomization no-AI forecasts | Последовательная no-AI работа одного developer, `T_h=X sum Z_i` |
| Outcome | Self-reported active implementation time до и после PR review | Elapsed makespan допустимого resource-constrained schedule |
| Режим | Endogenous mix Cursor Agent/chat/autocomplete/web LLM/non-use | Явный `r` или assignment `rho(i)` с отдельными `k_i^(r)` |
| Параллелизм | Не является treatment; issues иногда overlap | Явный `P`, allocation, effective parallelism и threshold |
| Зависимости | Не моделируются; tasks старались делать relatively independent | DAG и critical path `L` |
| Координация | One-stream tool/rework costs растворены в observed treatment effect | `P=1` costs входят в `k`; дополнительные integration effects входят в `C(P)` |
| Человеческое внимание | Частично видно в screen labels, но не разложено полностью | `k=a+h`, capacity-1 `H`, switching multiplier `gamma(P)` |
| Качество | Repository review и active rework; нет общей blinded quality scale | Качество вне objective, но verification/rework увеличивают task durations |
| Неопределённость | RCT estimate и CI, но 16 non-random developer clusters | Детерминированное ядро; `k` и `h` требуют внешней stochastic calibration |

Becker et al. находятся перед scheduling layer M0-M4. Они дают контекстный empirical input о знаке и масштабе duration factor при реалистичной one-issue работе. M0-M4 отвечает на следующий, не исследованный ими вопрос: что происходит с fixed workload, когда такие task-level durations сочетаются с `P`, неделимостью, DAG, integration overhead и одним последовательным человеческим ресурсом.

## Тезисы синтеза для Related Work

1. В field RCT 16 опытных maintainers выполнили 246 реальных issues в 14 зрелых repositories; разрешение early-2025 AI увеличило regression-adjusted active implementation time на 19%, 95% CI `[1%,39%]`, что даёт контекстный `k≈1.19` с CI `[1.01,1.39]` (PDF с. 1-8, 28-31, 45-46).
2. Этот результат не противоречит ускорению на synthetic tasks как универсальная «отрицательная оценка AI»: population, familiarity, repository maturity, quality bar, task granularity, treatment и outcome отличаются. Сама работа предупреждает против такого обобщения (PDF с. 3-4, 12, 18-21).
3. Developer forecasts предполагали 24% сокращение времени, post hoc estimates - 20%, economics experts - 39%, ML experts - 38%, тогда как measured sign оказался обратным. Поэтому subjective productivity не следует использовать вместо операциональной калибровки `k` (PDF с. 1-2, 7-9, 34).
4. Observed prompting, review, cleanup, rejected generations и manual fallback объясняют, как `k` может превысить единицу даже при быстрой генерации. Это one-stream overhead, уже входящий в `k`, а не evidence о `C(P)` или `gamma(P)` (PDF с. 8-10, 19-20, 25).
5. Paper не является multi-agent scaling study: работа над несколькими issues иногда overlap, но concurrent agent count и switching не измерены; parallel agent trajectories упомянуты только как неизученная alternative elicitation strategy (PDF с. 5, 25).
6. Outcome closer к effort/service time, чем к project makespan: учитывается active implementation и post-review rework, но исключается passive review wait и отсутствует общий schedule fixed workload (PDF с. 5-7, 40-42).

## Короткий вариант встраивания в Related Work

> Becker et al. (2025) провели issue-level field RCT с 16 опытными open-source разработчиками, выполнившими 246 реальных задач в 14 зрелых репозиториях, с которыми они были знакомы в среднем пять лет. Разрешение использовать инструменты начала 2025 года, преимущественно Cursor Pro с Claude 3.5/3.7 Sonnet, увеличило regression-adjusted active implementation time на 19% (95% CI `[1%,39%]`), что в наших обозначениях даёт контекстный однопоточный коэффициент `k≈1.19` с CI `[1.01,1.39]`. Этот результат следует трактовать как task-, population-, repository-, tool-period- и mode-policy-specific пример `k>1`, а не как универсальный отрицательный эффект ИИ: treatment смешивал agent, chat, autocomplete и возможность не использовать AI, задачи были сравнительно короткими, а время self-report'илось как активная работа и исключало календарное ожидание review. Исследование также не варьировало число агентов, не задавало DAG и не разделяло полное время на `a` и `h`; поэтому оно не оценивает `P`, `C(P)`, `L`, `H`, `gamma(P)` или multi-agent makespan.

## Таблица доказательных страниц

| PDF-страница | Раздел / объект | Опорное содержание |
|---:|---|---|
| 1 | Title; Abstract | Авторы, affiliation, arXiv v2/date, 16 developers, 246 tasks, 5 years repository experience, tools, forecasts, 19% slowdown |
| 2 | Introduction; Figure 1 | 19% point estimate и primary 95% CI на графике, 2-hour average, 23,000 stars, 143 labeled hours, setting caveat |
| 3 | Introduction; Background | Предупреждение против generalization, synthetic/fixed-output и field/non-fixed-output literature, heterogeneous effects по experience |
| 4 | Methodology 2.1 | Рекрутинг, более десяти лет опыта, 5 years/1,500 commits, `$150/hour`, размер и maturity repositories |
| 5 | Experimental Design 2.2 | Выбор issues, forecasts до assignment, simulated coin flip и ранняя alternative randomization, AI-allowed/disallowed, flexible order, multiple issues at a time, PR review |
| 6 | AI Tools; Data; Effect Estimation | Cursor Agent capabilities, training, prior tool experience, self-reported initial/post-review time, определение `S` и total implementation time |
| 7 | Effect Estimation; Supplementary Data | Log-linear regression, forecasts как covariate, developer/expert forecasts, Cursor analytics, interviews |
| 8 | Screen labels; Results | 128 recordings/143 hours, filters до 74/84 hours, labels, 136 vs 110 issues, 19% result |
| 9 | Forecasts; Activity | 24% developer forecast, 20% post hoc estimate, correlations `0.64/0.59`, economics/ML forecasts, raw 34% ratio caveat |
| 10-11 | Factor Analysis; Table 1 | Exploratory status 21 factors, multiple-comparison warning, evidence summary |
| 12 | Key Caveats | Setting-specific generalizability, future systems and elicitation, preliminary autonomous-agent caveat |
| 18-20 | Appendix C.1 | Familiarity, large repositories, low reliability, acceptance `<44%`, reading/editing AI code, 9% review/cleaning, tacit context |
| 20-22 | Appendix C.2.1-C.2.5 | Experiment-induced overuse, short-task selection, scope, order bias, recruitment selection |
| 23-25 | Appendix C.2.6-C.2.10 | Ease vs speed, PR quality/review times, AI experience/learning, 4% waiting, tool modes, parallel trajectories only as untested idea |
| 26-27 | Appendix C.3 | Compliance, dropout, imputation, video validation, alternative estimators |
| 28-30 | Appendix D | Regression equation, HC3 primary CI, clustered/bootstrap alternatives, `S=exp(beta)-1`, CI transformation, ratio estimator |
| 31 | Appendix E.1 | Balance of forecast difficulty, assignment proportions and p-values |
| 33 | Appendix E.3 | Первые 25 block-randomized issues, переход к fair coin, 20% slowdown без них |
| 34 | Appendix E.5-E.6 | Expert forecast sample sizes/statistics и другие treatment effects |
| 35-36 | Appendix F | Open-source review workflow, Cursor Agent/chat/autocomplete descriptions |
| 37-42 | Appendix G.1-G.2 | Recruitment criteria, compensation, issue selection, forecasts, developer instructions, active-time definition |
| 42-45 | Appendix G.3-G.6 | Training, check-ins, exit interview/survey, participant dropout, quality questions |
| 45-46 | Appendix G.7-G.8 | 16 developers, 14 repositories, per-developer/per-repository task counts, screen-label sampling caveat |
| 47-49 | Appendix G.8 | Fine-grained labels для coding, tests, prompting, waiting, reading, rejection и cleanup |

## Итоговая оценка источника

Сильная сторона Becker et al. - issue-level random assignment после фиксации реальных tasks и forecasts, experienced developer population, familiar mature repositories, inclusion post-review rework и богатые screen-recording data. Для M0-M4 это даёт хорошо очерченный контекст, в котором average duration factor оказался больше единицы: `k≈1.19`, 95% CI `[1.01,1.39]`. Работа особенно полезна как контрпример предположению, что внедрение AI обязательно означает `k<1`, и как демонстрация ненадёжности subjective speedup estimates.

Доказательная граница заканчивается до multi-agent scheduling. Treatment является intent-to-allow смесью tools и modes, primary time self-reported и active, workload не образует общий project DAG, concurrent agents не задаются, а human/agent intervals не дают полного `a+h` decomposition. Корректная роль источника в статье - контекстная калибровка `k>1` у опытных разработчиков в знакомых репозиториях. Некорректная роль - universal negative AI effect или эмпирическое доказательство того, что параллелизм `P>1` преодолевает либо усиливает это замедление.
