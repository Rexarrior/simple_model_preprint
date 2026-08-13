# Jørgensen (2007): expert judgment и formal models как внешний слой для `k_hat`

## Назначение и границы обзора

Этот документ разбирает один источник применительно к статье M0-M4 о makespan фиксированного набора задач в ячейке «один разработчик - `P` кодовых ИИ-агентов». Источник нужен прежде всего для ex ante оценки `\hat{k}_i^{(r)}`: выбора между expert judgment и formal estimation models, локальной калибровки, учёта контекстной информации, неопределённости и ошибок сравнения методов.

Jørgensen рассматривает **прогноз software development work effort**, а не эффект ИИ и не scheduling. Поэтому необходимо разделять два слоя:

1. **Estimation layer** до старта работы оценивает будущий effort. В M0-M4 к этому слою относится внешний оценщик `\hat{k}_i^{(r)}` и, при необходимости, baseline `Z_iX`.
2. **Scheduling layer** принимает длительности как вход и определяет fixed-workload makespan с учётом `P`, неделимости, DAG/`L`, `C(P)`, `h`, `H` и `gamma(P)`.

Источник относится к первому слою. Он не содержит данных об LLM, кодовых агентах или архитектуре «один человек - много агентов» и не доказывает scheduling-результаты M0-M4.

Локальный файл содержит 34 PDF-страницы. Основной текст занимает PDF 1-14, references - PDF 15-17, Appendix A с карточками 16 исследований - PDF 18-34. Внутренняя рукописная нумерация совпадает с PDF-порядком: PDF 1 / печ. 1, ..., PDF 34 / печ. 34. Это авторская версия с пометкой `Version: March, 2007, Updated May 2007`, а не финальная журнальная вёрстка. Финальная пагинация публикации 449-462 не может быть постранично сопоставлена с локальной рукописью без отдельного издательского PDF. Все опорные ссылки ниже относятся к локальному файлу и имеют вид «PDF / печатная страница».

## Библиография и статус

**Проверенная ссылка:** Magne Jørgensen. “Forecasting of Software Development Work Effort: Evidence on Expert Judgement and Formal Models.” *International Journal of Forecasting* 23, no. 3 (2007): 449-462. DOI: [10.1016/j.ijforecast.2007.05.008](https://doi.org/10.1016/j.ijforecast.2007.05.008).

**Проверка идентичности:** название и имя автора напечатаны на PDF 1 / печ. 1. Журнал, том, номер, год, финальные страницы и DOI проверены по DOI-записи. Локальная версия датирована мартом 2007 года с обновлением в мае 2007 года.

**Статус:** опубликованная журнальная обзорная статья; локальный файл является авторской рукописью. DOI подтверждает факт и реквизиты публикации, но сам PDF не описывает процедуру внешнего рецензирования.

**Тип доказательства:** целевой review 16 эмпирических сравнений expert judgment, formal models и, в четырёх исследованиях, их комбинаций. Это не meta-analysis: исследования используют разные показатели точности, поэтому автор не рассчитывает единый effect size и сводит часть результатов на уровне исследований (PDF 9-10 / печ. 9-10).

## Исследовательские вопросы и вклад

### Вопросы источника

Статья задаёт два вопроса:

1. следует ли ожидать более точных effort estimates от expert judgment или от formal models;
2. в каких условиях оценку следует основывать на expert judgment, model output или их комбинации (PDF 2 / печ. 2).

Точность понимается как отклонение оценённого effort от фактического effort. Гибкость, стоимость самого оценивания, объяснимость и удобство применения признаются важными, но не сравниваются, поскольку включённые исследования почти не сообщали такие outcomes (PDF 8 / печ. 8).

### Вклад

Релевантный для M0-M4 вклад состоит в пяти положениях:

1. expert и model-based estimates разведены по **quantification step**: tacit/intuitive quantification считается judgment-based, deliberate/mechanical quantification - model-based;
2. модель может сильно зависеть от экспертно заданных inputs, поэтому `formal model` не означает отсутствие judgment;
3. сравнение методов зависит от local calibration модели, доступной экспертам contextual information, экспертизы и способа выбора estimator;
4. обзор систематизирует ошибки и fairness problems, из-за которых наблюдаемую разницу точности нельзя автоматически приписать типу метода;
5. доступные данные не поддерживают замену экспертов моделями или моделей экспертами; комбинация может быть практической стратегией при трудности выбора (PDF 2-7, 13-14 / печ. 2-7, 13-14).

Для M0-M4 это не готовый estimator `\hat{k}`, а evidence о том, как выбирать, проверять и ограничивать внешний estimation layer.

## Метод и корпус

### Определения сравниваемых подходов

Если последний шаг преобразования понимания задачи в число является интуитивным, estimate классифицируется как judgment-based; если механическим - как model-based. Когда объединяются outputs двух или более завершённых процессов, estimate считается combination-based, а способ объединения отдельно маркируется как judgmental или mechanical (PDF 2 / печ. 2).

Это определение важно по двум причинам:

- обе категории внутренне неоднородны и не являются двумя единичными методами;
- формальная модель может получать size, complexity, skills и adjustment factors из expert judgment и унаследовать его bias (PDF 3 / печ. 3).

### Поиск и отбор

Корпус строился из двух источников:

- journal papers, найденных в связанном systematic review Jørgensen and Shepperd (2007);
- conference papers, найденных ручной проверкой результатов Inspec по запросу `('effort estimation' OR 'cost estimation') AND 'software development'`; последний поиск выполнен в феврале 2006 года (PDF 7 / печ. 7).

Было найдено 17 потенциально релевантных работ. Одна исключена из-за недостаточной информации о происхождении estimates, осталось 16 исследований. Автор прямо допускает пропуски: один дополнительный релевантный источник был обнаружен только после контакта с авторами включённых работ (PDF 7 / печ. 7).

### Кодирование и проверка

Для каждого исследования кодировались study design, способ выбора метода, модели, уровень калибровки, опыт использования модели, процесс и опыт expert judgment, motivational biases, inputs, contextual information, complexity, fairness limitations, accuracy, variance и прочие результаты. Полный шаблон и карточки исследований приведены в Appendix A (PDF 7, 18-34 / печ. 7, 18-34).

Интерпретации, основанные преимущественно на qualified guess, помечались как probable. Карточки были отправлены авторам всех 16 работ; ответили представители 13, после чего были внесены лишь небольшие исправления (PDF 8 / печ. 8).

### Уровни калибровки моделей

Jørgensen различает:

- **low calibration:** общая зависимость и стандартные adjustment factors относительно nominal project без анализа собственных historical data организации;
- **medium calibration:** часть общих корректировок заменена organization-specific productivity values;
- **high calibration:** модель построена только по завершённым проектам данной организации или организаций с действительно сходными проектами (PDF 3-4 / печ. 3-4).

Здесь `calibration` означает прежде всего **локальную адаптацию модели к организационному контексту**, а не полную вероятностную калибровку forecast intervals. Эти смыслы нельзя смешивать.

## Релевантные findings

### 1. Нет общего превосходства formal models

По сравнению средней точности моделей со средней точностью экспертов 10 из 16 исследований дали преимущество expert judgment, 6 - models. Только два исследования позволяли сравнить лучший model с лучшим expert, и в обоих лучший expert был точнее (PDF 10 / печ. 10).

Этот подсчёт нельзя превращать в универсальный effect size:

- единица агрегации - исследование, поэтому работы с 14 и 140 observations имеют одинаковый вес;
- показатели accuracy сообщались неодинаково;
- доступны не все варианты best/average/worst comparison;
- designs, tasks, models, experts и information sets различались (PDF 9-11 / печ. 9-11).

Для 12 исследований с MAPE взвешивание по числу observations дало 99% для experts и 107% для models. Однако результат был чувствителен к лабораторным исследованиям: исключение одного наиболее неточного laboratory study снизило оба weighted MAPE до 78%. Автор не предлагает эти величины как устойчивую оценку относительного эффекта метода (PDF 11 / печ. 11).

Шесть field studies разделились поровну: три в пользу models и три в пользу expert judgment; больших различий по accuracy они не сообщали. Для field studies отдельно нельзя было корректно посчитать weighted MAPE из-за нехватки сопоставимых данных (PDF 11 / печ. 11).

**Перенос к `k_hat`:** нельзя назначить фиксированную поправку точности для expert или formal estimator. Выбор метода должен проверяться на собственном task/mode corpus.

### 2. Formal models: сильные стороны и ошибки

Статистические и иные mechanical models имеют принципиальные преимущества: одинаковый input даёт одинаковый output; variables могут получать веса по predictive power; снижается зависимость от irrelevant cues, overoptimism и непоследовательности эксперта (PDF 4, 14 / печ. 4, 14).

В software effort estimation эти преимущества могут не реализоваться из-за следующих проблем:

- relationships между size, context и effort нестабильны при смене технологии, типов продукта и production methods;
- малые learning datasets и большое число variables создают overfitting;
- модель упрощают ради понятности, стоимости разработки и ограничений данных, поэтому важный контекст может быть omitted;
- size, complexity и adjustment inputs часто сами задаются экспертно;
- general or low-calibration model переносит organization-independent assumptions в неподходящий контекст;
- сложность выбора или исполнения analytical rule создаёт отдельную model-selection error (PDF 3-6, 13-14 / печ. 3-6, 13-14).

В восьми исследованиях с достаточно mechanical model use expert judgment был точнее в пяти. Следовательно, отсутствие общего model superiority нельзя объяснить только тем, что модели якобы применялись как «expert judgment in disguise» (PDF 11 / печ. 11).

В восьми исследованиях model builders одновременно были evaluators, что создавало vested-interest risk. Несмотря на это, experts оказались точнее self-developed models в пяти из восьми работ. Это наблюдение не измеряет величину publication bias, но показывает, что автор учитывает конфликт ролей как design issue (PDF 11 / печ. 11).

### 3. Expert judgment: сильные стороны и ошибки

Эксперты обычно имеют доступ к requirement text, устной информации от клиента, сведениям о конкретных developers, похожих прошлых задачах и другим `broken-leg cues`, которые трудно практически кодировать в модели. Они также гибче обрабатывают отсутствие информации и changing situations (PDF 5-6, 14 / печ. 5-6, 14).

Одновременно judgment подвержен:

- inconsistency при одинаковом input;
- неправильному weighting валидных и невалидных variables;
- misleading or poor feedback;
- dilution effect от информации низкой релевантности;
- wishful thinking и overoptimism;
- motivational bias, например в bidding или planning context;
- overconfidence в uncertainty intervals;
- непрозрачности tacit quantification step;
- ошибке выбора неподходящего expert (PDF 1, 2, 4-6, 8-9, 11-12 / печ. 1, 2, 4-6, 8-9, 11-12).

Во введении статья пересказывает более ранние данные: 90% effort prediction intervals включали actual effort только в 60-70% случаев. Это не собственный результат обзора 16 сравнений, а приведённое автором evidence из Jørgensen, Teigen et al. (2004); использовать его следует только как отдельное свидетельство overconfidence (PDF 1 / печ. 1).

Важен способ выбора эксперта. Автор указывает на relevant experience с очень сходными projects, способность вспомнить близкие analogies и previous estimation accuracy как кандидаты для отбора. В одном цитируемом исследовании корреляция прошлой и будущей accuracy среди 20 professionals составляла 0.40, а выбор более overoptimistic из двух по прошлым errors имел success rate 68%. Это вторичный, контекстный результат, а не общая надёжность expert selection (PDF 12 / печ. 12).

### 4. Local calibration и contextual information меняют сравнение

Table 2 показывает слабую, но содержательно согласованную связь между local calibration и относительной точностью models: situation-tailored models чаще конкурируют с expert judgment успешнее, чем low-calibration models. Автор называет связь weak и обсуждает counterevidence, включая случай, когда low-calibration model могла случайно соответствовать новому набору проектов (PDF 12-13 / печ. 12-13).

Table 3 показывает, что эксперты обычно получали больше контекстной информации, чем models: так было в 12 из 16 исследований. Только четыре работы дали обоим подходам одинаковую информацию; в трёх из них experts были точнее. Малое число исследований не позволяет сделать сильный causal conclusion о роли context (PDF 13 / печ. 13).

Cross-study comparison даёт MAPE 157% у experts в исследованиях с тем же input, что у models, и 36% в исследованиях, где experts имели дополнительную contextual information. Автор прямо предупреждает, что группы могут различаться по estimation complexity. Поэтому разницу нельзя трактовать как causal effect или ожидаемое улучшение `k_hat`; это лишь сильный сигнал, что context availability является важным moderator (PDF 13 / печ. 13).

Для `\hat{k}_i^{(r)}` это означает: локальная модель должна получать признаки, действительно кодирующие тип задачи, режим, инструмент, опыт разработчика и доступный контекст. Если expert использует сведения, отсутствующие в model input, сравниваются не только quantification methods, но и разные information sets.

### 5. Combination methods

Только четыре исследования оценивали combination-based estimates. В одном combination была столь же точна, как лучший model, и немного точнее expert estimate; в другом judgmental combination улучшила результат относительно обоих отдельных подходов; в третьем expert estimate был немного точнее mechanical combination; в четвёртом простое среднее expert judgment, regression и case-based reasoning оказалось точнее лучшего отдельного метода (PDF 12 / печ. 12).

Вывод статьи умеренный: четыре исследования предполагают, что combined estimates достигают accuracy, сходной с лучшим из отдельных методов, независимо от mechanical или judgmental способа объединения. Корпус слишком мал для более сильной гарантии (PDF 14 / печ. 14).

Для `k_hat` combination разумно трактовать как triangulation или ensemble, а не как доказанно оптимальную формулу. Источник не задаёт веса, prior distribution, Bayesian update или правило построения prediction interval.

### 6. Условия, при которых model особенно полезна

По modest evidence автор рекомендует models отдельно или вместе с judgment, когда:

1. situational biases создают сильный риск overoptimism;
2. объём contextual information, доступный экспертам, мал;
3. model калибрована к использующей её организации (PDF 14 / печ. 14).

Expert judgment имеет относительное преимущество, когда модель не локально калибрована, а эксперт обладает важной contextual information, отсутствующей в formal model, и умеет использовать её без доминирования irrelevant cues (PDF 14 / печ. 14).

Это условия выбора, а не theorem и не гарантия по каждому проекту.

## Ошибки и bias в сравнительных исследованиях

Источник особенно полезен тем, что различает ошибку estimator и ошибку дизайна сравнения.

| Риск | Как он искажает сравнение | Опора |
|---|---|---|
| Разные задачи для разных методов | Models могут применяться только на более поздних или простых задачах, а judgment - на ранних и unprecedented; raw accuracy становится selection-biased | PDF 8 / печ. 8 |
| Разные information sets | Выигрыш expert может отражать дополнительный context, а не лучший quantification step | PDF 5, 8, 13 / печ. 5, 8, 13 |
| Неописанный judgment process | Structured, data-supported estimation смешивается с unaided intuition в одну категорию | PDF 8 / печ. 8 |
| Нечёткая терминология | `Estimate` может означать most likely effort для model и budgeted/planned effort для expert | PDF 8-9 / печ. 8-9 |
| Разные loss functions | Model может симметрично штрафовать over/underestimate, expert - избегать завышения или оптимизировать другой управленческий риск | PDF 9 / печ. 9 |
| Estimate влияет на actual effort | Commitment к экспертному plan может менять исполнение и создавать self-fulfilling accuracy | PDF 9 / печ. 9 |
| Нерепрезентативные experts | Average students или случайно выбранные experts не представляют best available expertise | PDF 6 / печ. 6 |
| Method-selection error | Выбор плохой model или плохого expert может доминировать над свойствами класса методов | PDF 6, 11-12 / печ. 6, 11-12 |
| Model builder = evaluator | Vested interest может благоприятствовать self-developed model | PDF 11 / печ. 11 |
| Group estimation почти не изучена | Individual expert evidence плохо переносится на обычные для крупных проектов estimating groups | PDF 9 / печ. 9 |
| Publication bias неизвестен | Неизвестно, публиковались ли неудачные self-developed models с той же вероятностью | PDF 9 / печ. 9 |
| Несопоставимые accuracy measures | Нельзя получить общий процент преимущества или корректный единый effect size | PDF 9-10 / печ. 9-10 |

Пример конфounding приведён для Study 16: без adjustment model имела MAPE 0.07 против 0.18 у experts, но при сравнении проектов сходной complexity значения были 0.07 и 0.10. Автор использует это как иллюстрацию необходимости корректировать способ назначения методов задачам, а не как универсальный результат (PDF 8, 34 / печ. 8, 34).

## Практическая процедура для `k_hat`

Ниже приведён **синтез для M0-M4**, а не дословный алгоритм Jørgensen.

1. Зафиксировать target как task/mode-specific wall-clock ratio `k_i^(r)=T_i^ai(r)/(Z_iX)`, а не смешивать его с person-effort, budget, planned effort, quality или makespan.
2. Стратифицировать completed observations как минимум по типу задачи `c(i)` и режиму `r`; при смене инструмента или workflow считать перенос старой калибровки отдельной гипотезой.
3. В cold-start режиме получать structured expert estimate и сохранять его отдельно от model estimate. Указывать, какой контекст был доступен каждому estimator.
4. Параллельно строить простой locally calibrated formal benchmark на завершённых задачах. Сравнивать методы только на одних и тех же задачах, inputs, cutoff dates и accuracy/loss criterion.
5. При отсутствии устойчивого победителя использовать combination estimate и отдельно отслеживать errors каждого компонента. Согласие методов не считать доказательством правильности.
6. Сохранять point estimate вместе с uncertainty range и затем проверять empirical coverage. Источник мотивирует такую проверку evidence об overconfidence, но не задаёт конкретный interval estimator.
7. Периодически переоценивать model и expert selection по out-of-sample errors. Local calibration к организации не гарантирует forecast-interval calibration и не защищает от concept drift.
8. Передавать в M0-M4 не только `\hat{k}` или его сценарии, но и epistemic status: expert, formal model или combination; размер и свежесть calibration sample; task/mode scope; error/coverage history.

Практический вывод для текущего текста `Базовая модель.tex`: эмпирическое среднее или верхний квантиль по `(c(i),r)` является одним допустимым способом построения `\hat{k}`, но Jørgensen (2007) не доказывает, что этот способ универсально лучше expert judgment. При малой, устаревшей или плохо сопоставимой выборке structured judgment и combination остаются обоснованными кандидатами, которые затем необходимо калибровать на realized `k`.

## Mapping к параметрам M0-M4

Здесь **direct** означает тот же объект и ту же формальную роль, **analogy** - полезный estimation-аналог при другой семантике, **absent** - объект в модели источника отсутствует. У Jørgensen нет direct mapping к scheduling-ядру M0-M4.

| Параметр | Статус | Соответствие в источнике | Точная граница переноса |
|---|---|---|---|
| `Z` | **analogy** | Size, requirements, project/activity characteristics и complexity входят в effort estimation | Нет нормированной task baseline complexity `Z_i` в единицах `X`; inputs сами могут быть judgment-based и uncertain |
| `k` | **analogy** | Expert, model и combined methods прогнозируют effort; calibration/context влияют на accuracy | Нет отношения AI-assisted duration к no-AI baseline, task/tool/mode-specific `k_i^(r)` или готового estimator `\hat{k}` |
| `r` | **analogy** | Estimation context, method, information set и organizational situation меняют качество прогноза | Нет interactive/delegated/autonomous режима взаимодействия с ИИ и назначения режима отдельной задаче |
| `P` | **absent** | В отдельных проектах могут быть teams, но число параллельных исполнителей не является объектом review | Нет `P` агентов, effective parallelism или capacity constraint |
| `W` | **analogy** | Total project effort или effort отдельной activity является forecast target | Нет AI-weighted work `W=X sum_i Z_i k_i`; effort не делится автоматически на `P` |
| `L` | **absent** | Requirements и activities могут обсуждаться содержательно | Нет precedence DAG, weighted path или critical-path lower bound |
| `C(P)` | **absent** | Technology, methods и tools могут влиять на historical effort | Нет функции agent-agent integration overhead, растущей с `P` |
| `h` | **absent** | Experts являются оценщиками, а personnel/context могут быть inputs | Нет human share wall-clock duration внутри AI-assisted task |
| `H` | **absent** | Work effort измеряет человеческие затраты проекта | Нет суммы неперекрывающихся service intervals одного shared developer capacity 1 |
| `gamma(P)` | **absent** | Inconsistency и cognitive bias обсуждаются в estimation, а не execution | Нет context-switching penalty разработчика между `P` агентными потоками |
| makespan | **absent** | Forecast target - required work effort для проекта или activity | Нет fixed-workload schedule, completion time последней задачи, assignment, resource feasibility или objective `C_max` |

## Что источник поддерживает для M0-M4

1. Постфактумное определение `k_i^(r)` не является прогнозом; до старта нужен отдельный estimation process.
2. Expert judgment, locally calibrated formal model и их combination являются различными кандидатами для внешнего `\hat{k}`, причём evidence не устанавливает универсального победителя.
3. Качество formal model зависит от сходства calibration data с текущей организацией и ситуацией; low-calibration transfer особенно рискован.
4. Contextual information может давать expert преимущество, но irrelevant information, inconsistency, overoptimism и overconfidence могут его уничтожать.
5. Сравнивать estimators следует на одинаковых задачах и information sets либо явно признавать, что одновременно сравнивается доступ к информации.
6. Model/expert selection является отдельной стадией с собственной ошибкой; best-case performance метода не равна ожидаемой performance процесса выбора.
7. Combination может быть разумной страховкой при независимых ошибках и трудности выбора, но доступные четыре исследования не дают универсальной формулы или гарантии.
8. Point accuracy недостаточна для uncertainty-aware решения; confidence ranges должны проверяться по empirical coverage, хотя конкретный метод source не задаёт.

Пункты 1, 5 и 8 сформулированы как применение evidence источника к конструкции `\hat{k}`, а не как дословные определения автора.

## Что источник не позволяет утверждать

1. Что expert judgment вообще точнее formal models: результат 10 против 6 относится к средним accuracy outcomes 16 неоднородных studies.
2. Что formal models вообще точнее experts: source прямо не находит systematic superiority.
3. Что разница weighted MAPE 99% против 107% является переносимым effect size; она чувствительна к составу laboratory studies.
4. Что MAPE 157% против 36% измеряет causal benefit contextual information; сравниваемые группы могли различаться по complexity и design.
5. Что local calibration гарантирует точность или uncertainty calibration; связь с относительной performance названа weak.
6. Что combination всегда превосходит лучший отдельный метод; combination оценивали только четыре исследования с неодинаковыми results.
7. Что статья предлагает Bayesian estimator, веса ensemble, prediction distribution, upper quantile или конкретный алгоритм `\hat{k}`.
8. Что expert estimate является наблюдаемым фактом; tacit quantification, overoptimism, irrelevant cues и poor feedback остаются источниками ошибки.
9. Что model output свободен от judgment; model inputs и adjustment factors часто экспертные.
10. Что effort estimate равен elapsed time, task duration или project makespan.
11. Что source учитывает fixed workload, неделимые задачи, `P` параллельных агентов, DAG/`L`, `C(P)`, `h`, `H` или `gamma(P)`.
12. Что результаты относятся к LLM, Copilot, autonomous coding agents или любому AI effect size.
13. Что findings 2007 года описывают современное сравнительное качество estimation tools без новой проверки.
14. Что Appendix A устраняет publication bias, missing studies или ecological-validity problems; автор прямо признаёт эти ограничения.

## Отличие от M0-M4

| Измерение | Jørgensen (2007) | M0-M4 |
|---|---|---|
| Центральный вопрос | Как точнее спрогнозировать software work effort: judgment, model или combination | Каков makespan фиксированной работы при одном разработчике и `P` кодовых агентах |
| Основной outcome | Error между estimated и actual effort | Completion time и speedup относительно последовательного no-AI baseline |
| Формальность | Mechanical quantification estimate сравнивается с tacit quantification | Детерминированные формулы и scheduling bounds условны на заданных inputs |
| Baseline | Size, requirements и historical projects входят в estimator | `T_h=X sum_i Z_i` задан явно |
| AI effect | Отсутствует | Task/tool/mode-specific `k_i^(r)` и внешний `\hat{k}_i^(r)` |
| Параллелизм | Не моделируется | `P` является мощностью agent layer |
| Структура работ | Project или activity как объект effort estimate | Неделимые tasks, DAG и critical path `L` |
| Overhead | Может быть неявно отражён в historical effort/context | Однопоточный `k` отделён от растущего с `P` `C(P)` |
| Человек | Expert выступает estimator; team/person context может быть input | Один shared execution resource с `h_i`, `H` и `gamma(P)` |
| Неопределённость | Accuracy heterogeneity, overconfidence и design bias; нет единого effect size | `k` может быть random variable; решения могут использовать expectation или quantile |
| Итог | Методологические условия выбора и проверки effort estimator | Lower bounds, feasible scheduling и makespan, условные на качестве estimates |

Jørgensen находится **перед** M0-M4 в вычислительной цепочке. Он помогает решить, как получить ex ante duration input и насколько ему доверять. M0-M4 затем отвечает на иной вопрос: какой срок следует из этих inputs при конкретной структуре задач и ресурсов. Точная scheduling algebra не исправляет bias в `\hat{k}`; хороший estimator сам по себе не строит допустимое расписание.

## Тезисы для синтеза Related Work

1. В software effort estimation evidence не поддерживает безусловную замену expert judgment formal models: средняя expert accuracy была выше в 10 из 16 studies, но heterogeneity и design limitations запрещают трактовать этот счёт как общий effect size (PDF 7-11 / печ. 7-11).
2. Относительная performance зависит не только от quantification method, но и от local calibration и information set: model должна быть привязана к ситуации, а expert advantage часто связан с contextual information, отсутствующей в model inputs (PDF 3-6, 12-14 / печ. 3-6, 12-14).
3. Для `\hat{k}_i^(r)` разумно сопоставлять structured judgment, locally calibrated model и combination на одних task/mode observations; model и expert selection, overoptimism, overfitting и forecast-interval overconfidence должны учитываться как отдельные risks.
4. Источник относится к effort forecasting, не к AI evidence или scheduling: он не задаёт `P`, `W`, `L`, `C(P)`, `h`, `H`, `gamma(P)` и makespan, а только обосновывает upstream estimation layer для входов M0-M4.

## Короткое встраивание в Related Work

> Jørgensen (2007) рассматривает software effort forecasting как выбор между tacit expert quantification, mechanical formal models и их комбинациями. В 16 сравнительных исследованиях средняя expert accuracy была выше в десяти, model accuracy - в шести, однако неодинаковые metrics, tasks, information sets и designs не позволяют вывести единый effect size. Два наиболее устойчивых moderators - локальная калибровка модели и contextual information, доступная экспертам, - показывают, что ex ante `\hat{k}_i^{(r)}` нельзя выбирать как универсальный коэффициент. Для нашего estimation layer это поддерживает triangulation structured judgment и locally calibrated model по паре «тип задачи - режим» с последующей проверкой errors и uncertainty. Источник не содержит evidence об ИИ и не решает scheduling problem: `P`, DAG/`L`, `C(P)`, человеческая доля `h`, capacity-1 time `H`, `gamma(P)` и fixed-workload makespan добавляются только в M0-M4.

## Таблица опорных страниц

| PDF | Печатная | Раздел / объект | Опорное содержание |
|---:|---:|---|---|
| 1 | 1 | Title; abstract; Introduction | Идентичность рукописи; 16 studies; 10 против 6; две conditions; четыре combination studies; overoptimism и overconfidence как контекст |
| 2 | 2 | Introduction; Section 2 | RQ; definitions judgment/model/combination по quantification step; categories внутренне неоднородны |
| 3-4 | 3-4 | Model-Based Processes; Prior Research | Expert inputs внутри моделей; effort formula; low/medium/high organizational calibration; consistency и weighting как преимущества models |
| 5-6 | 5-6 | Contextual Information; Expertise | Overfitting и complexity ограничения; requirements/oral context; broken-leg cues; irrelevant information; ecological validity и method-selection error |
| 7 | 7 | Review Process | Search strategy; 17 найденных, 1 исключён, 16 reviewed; design factors; Appendix A scope |
| 8-9 | 8-9 | Review Process; Limitations | Author validation 13/16; accuracy outcome; missing process descriptions; task-selection confounding; terminology, loss functions, commitment, groups, unpublished results |
| 10 | 10 | Table 1; average accuracy | Матрица best/average/worst comparisons; 10 studies за average expert, 6 за average model |
| 11 | 11 | Weighted and field results | Weighted MAPE 99/107 и sensitivity; field studies 3/3; mechanical-use subset; builder/evaluator conflict |
| 12 | 12 | Selection; combinations; Table 2 | Выбор experts/models; результаты четырёх combinations; начало evidence о calibration level |
| 13 | 13 | Tables 2-3; contextual information | Weak calibration relationship; same/different information sets; MAPE 157/36 с оговоркой comparability; weak task-type evidence |
| 14 | 14 | Concluding Remarks | Нет основания заменять один подход другим; причины model errors; practical conditions для model, expert и combination |
| 18 | 18 | Appendix A template | Полная схема coding design issues и results |
| 19 | 19 | Study 1 | Пример laboratory design, low calibration, ограниченного expert context и judgmental combination |
| 34 | 34 | Study 16 | Пример selection-by-complexity confounding: raw MAPE 0.07/0.18, при сходной complexity 0.07/0.10 |

## Итоговая оценка релевантности

Источник является сильной опорой для отдельного estimation layer перед M0-M4. Его главная ценность не в счёте 10 против 6, а в объяснении условий сравнения: formal model выигрывает от consistency и local calibration, expert - от доступа к трудно кодируемому контексту, при этом оба подхода имеют собственные biases и selection errors. На малом и неоднородном корпусе ни один класс не признан универсально лучшим; combination поддержана как осторожная стратегия, а не как гарантированный optimum.

Граница доказательств проходит до ИИ и scheduling. Статья не оценивает кодовых агентов, не задаёт `k`, не выводит makespan и не моделирует M1-M4. Корректное использование в Related Work: сослаться на Jørgensen для обоснования expert/model/combination вариантов `\hat{k}`, local calibration, contextual moderators и uncertainty checks, а затем явно сказать, что fixed-workload makespan рассчитывается отдельной моделью по `Z`, `k`, `r`, `P`, `W`, `L`, `C(P)`, `h`, `H` и `gamma(P)`.
