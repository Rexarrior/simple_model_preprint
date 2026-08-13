# Jørgensen и Shepperd (2007): systematic review software effort estimation и границы внешнего `k_hat`

## Назначение и границы обзора

Этот документ разбирает один источник применительно к статье M0-M4 о makespan фиксированного набора задач в ячейке «один разработчик - `P` кодовых ИИ-агентов». Источник нужен как карта исследований software effort estimation и как основание для ограничений внешнего оценщика `\hat{k}_i^{(r)}`. Он не является свидетельством эффективности ИИ и не содержит scheduling theorem.

Главное различие объектов:

1. Jørgensen и Shepperd изучают литературу о прогнозировании software development **effort/cost**. В сноске авторы поясняют, что используют cost и effort взаимозаменяемо, поскольку главным cost driver обычно является effort (PDF 1 / печ. 1).
2. M0-M4 требует ex ante оценки однопоточного wall-clock factor `\hat{k}_i^{(r)}`, после чего рассчитывает или ограничивает makespan с учётом `P`, неделимости, DAG, общего человеческого ресурса и overhead.

Поэтому таксономия и критика качества evidence переносятся на дизайн estimation layer по аналогии. Сам источник не устанавливает, что person-effort estimate равен elapsed task duration, `k` или project makespan.

Локальный файл содержит 55 PDF-страниц. Это авторская рукопись: на страницах напечатана внутренняя нумерация 1-55, совпадающая с номером PDF-страницы; журнальная вёрстка и журнальная пагинация 33-53 в файле отсутствуют. Ссылки ниже имеют вид «PDF-страница / печатная страница рукописи». Библиографический диапазон 33-53 нельзя использовать для реконструкции точных страниц claims в финальной вёрстке.

## Библиография и статус

**Полная ссылка:** Magne Jørgensen and Martin Shepperd. “A Systematic Review of Software Development Cost Estimation Studies.” *IEEE Transactions on Software Engineering* 33, no. 1 (2007): 33-53. DOI: [10.1109/TSE.2007.256943](https://doi.org/10.1109/TSE.2007.256943).

**Проверка идентичности:** название и авторы напечатаны на PDF 1 / печ. 1. Журнал, год, том, номер, финальная пагинация и DOI проверены по DOI-записи. Локальный PDF имеет служебный title `Microsoft Word - $ASQjorgensen_shepperd_bestreview_tse` и не является издательским макетом.

**Статус:** опубликованная журнальная systematic review article. Локальный PDF не описывает процедуру внешнего рецензирования, поэтому отдельная квалификация процедуры peer review здесь не реконструируется.

**Тип доказательства:** систематизированная карта 304 журнальных papers с категориальным анализом тем, estimation approaches, research approaches, study context и datasets. Это не meta-analysis точности estimator'ов, не risk-of-bias assessment каждого исследования и не единое head-to-head сравнение методов.

**Временная граница:** поиск завершён в апреле 2004 года. Авторы просматривали журналы начиная с их первого тома; явная начальная календарная дата корпуса не задана. Результаты описывают исследовательский ландшафт не позднее апреля 2004 года и не учитывают последующие методы, современные процессы разработки, LLM и кодовых агентов (PDF 3 / печ. 3).

## Вопросы и вклад источника

### Общая цель

Цель обзора - улучшить и направить будущие исследования software cost estimation. В отличие от более ранних обзоров, ориентированных на знакомство практиков с формальными моделями, авторы концентрируются на методах исследования и не пытаются дать исчерпывающее описание каждого estimator (PDF 1-2 / печ. 1-2).

### Десять research questions

RQ1-RQ10 охватывают:

- журналы, публикующие estimation studies;
- трудность обнаружения релевантных работ и широту related-work search;
- доминирующий журнал и возможные тематические смещения;
- устойчивость исследовательского сообщества;
- распределение тем и estimation approaches во времени;
- необходимость изменить research focus;
- применяемые research methods и study contexts;
- методологические недостатки существующих evaluations (PDF 6-7 / печ. 6-7).

Для M0-M4 наиболее важны RQ6-RQ10: какие estimator'ы изучались, на каких данных и в каких контекстах, чем измерялось их качество и насколько evidence допускает внешний перенос.

### Релевантный вклад

1. Воспроизводимо описанный ручной поиск большого журнального корпуса.
2. Многомерная таксономия estimation research, а не только перечень формальных моделей.
3. Количественная карта дисбалансов: доминирование regression-based и history-based evaluations при малом числе real-life evaluations, uncertainty studies и dataset-property studies.
4. Прямая критика arbitrary, устаревших и слабо описанных datasets.
5. Предупреждение, что неполный related-work search способен изменить сравнительный вывод об analogy и regression.
6. Research agenda: больше базовых исследований качества оценки, real-life evaluation, исследований expert judgment и связи между свойствами данных и пригодностью метода.

## Systematic review protocol и корпус

### Inclusion и exclusion

Включались журнальные papers, описывающие research по software development effort или cost estimation. Работы о размере, сложности или correlates of effort включались только тогда, когда их основной целью было улучшение effort/cost estimation. Чистые discussion/opinion papers исключались (PDF 2 / печ. 2).

Papers на одном dataset с разным фокусом считались разными papers. Авторы сочли число таких случаев небольшим и не выполняли дедупликацию на уровне studies, но прямо предупредили, что для обзора устойчивости конкретного эффекта потребовалось бы строже различать paper и study (PDF 2-3 / печ. 2-3). Следовательно, 304 - число papers, а не гарантированно независимых empirical studies или datasets.

### Поиск

Авторы вручную, выпуск за выпуском, читали titles и abstracts всех опубликованных статей более чем в 100 потенциально релевантных англоязычных журналах, начиная с volume 1. Список журналов строился из reference lists, internet search и опыта авторов; оба автора сначала составили списки независимо, затем объединили их. Кандидаты читались подробнее для решения о включении (PDF 3 / печ. 3).

Результат поиска:

- 304 включённых papers;
- 76 журналов с хотя бы одной включённой работой;
- поиск завершён в апреле 2004 года;
- приложения перечисляют журналы и papers (PDF 3, 25-51 / печ. 3, 25-51).

Конференционные papers и reports не включались главным образом из-за workload, сложности полного выявления конференций и дублирования расширенными journal versions. Авторы не заявляют, что это ограничение безвредно для обзора конкретного estimation effect; напротив, для сравнения, например, COCOMO с Function Points они считают необходимым искать все релевантные типы источников (PDF 5 / печ. 5).

### Classification schema

Каждый paper кодировался по пяти свойствам:

| Свойство | Категории верхнего уровня |
|---|---|
| Research topic | estimation method, production function, model calibration, size measures, organizational issues, uncertainty, performance measures, dataset properties, other |
| Estimation approach | regression, analogy, expert judgment, work breakdown, function points, CART, simulation, neural network, theory, Bayesian, combination, other |
| Research approach | theory, survey, experiment, case study, method development, history-based evaluation, own experience, real-life evaluation, review, simulation, other |
| Study context | students/projects, professionals/industrial projects, not relevant |
| Data set | ссылка на применённый dataset |

Категории в основном nonexclusive и создавались специально для этого обзора, а не как универсальная онтология software estimation (PDF 3-4 / печ. 3-4; определения: PDF 52-55 / печ. 52-55).

### Надёжность классификации

Первичное кодирование выполнил первый автор. Второй автор независимо проверил случайную выборку 30 papers, около 10% корпуса. Первоначально возникло 59 расхождений на 150 classification decisions, то есть 39%; менее 3% решений были явно несовместимы с тогдашними описаниями категорий. Авторы уточнили 12 category descriptions, перечитали 109 papers из проблемных категорий и внесли 21 reclassification; финальное уточнение выполнил первый автор (PDF 4 / печ. 4).

Это сильнее неконтролируемого одиночного coding, но не равно полному double coding корпуса с итоговой inter-rater statistic. Авторы сами допускают остаточные спорные и ошибочные classifications (PDF 5 / печ. 5).

### Threats to validity

Авторы выделяют:

- publication bias из-за исключения конференций/reports, непубликации non-significant или confidential results и ориентации журналов на определённые темы;
- возможное влияние собственных интересов авторов: один работал преимущественно с expert estimation, другой - с formal analogy-based models;
- риск пропустить существенную литературу других дисциплин;
- возможный пропуск national или company-specific journals;
- ошибки ручного поиска и classification (PDF 3-6 / печ. 3-6).

Неформальная проверка примерно 50 conference papers показала сходство тем, методов и контекстов с journal corpus, но это не случайная систематическая выборка и не доказывает отсутствие publication bias (PDF 5 / печ. 5).

## Findings: карта estimation approaches

### Темы исследований

Из 304 papers 184 (61%) относились к introduction/evaluation of estimation methods. Только 25 (8%) затрагивали uncertainty assessment, 16 (5%) - measures of estimation performance и 3 (1%) - dataset properties. В период 2000-2004 доля uncertainty papers выросла до 13%, но dataset properties оставались редкой темой (PDF 15-16 / печ. 15-16).

Для `\hat{k}` это означает, что большой объём method-development literature нельзя принимать за сопоставимый объём evidence о calibration, predictive uncertainty или внешней переносимости. Число публикаций о методе не является мерой его accuracy.

### Таксономия и распространённость approaches

Таблица 5 задаёт следующий охват; один paper мог относиться к нескольким категориям:

| Estimation approach | Papers | Доля корпуса |
|---|---:|---:|
| Regression, включая большинство common parametric models и COCOMO | 148 | 49% |
| Function points | 68 | 22% |
| Expert judgment | 46 | 15% |
| Theory-derived models | 39 | 13% |
| Analogy / case-based | 31 | 10% |
| Other approaches | 25 | 8% |
| Neural networks | 22 | 7% |
| CART | 14 | 5% |
| Work breakdown | 12 | 4% |
| Simulation-derived estimation | 10 | 3% |
| Bayesian | 7 | 2% |
| Combination of estimates | 5 | 2% |

Regression-based approaches доминировали во всех трёх временных периодах. Доли analogy и expert-judgment papers росли, theory-derived approaches снижались, а разнообразие иных методов увеличивалось (PDF 16-17 / печ. 16-17).

Эта таблица является **таксономией исследовательского внимания**, а не ranking качества. Источник не даёт pooled errors, общего benchmark или доказательства, что наиболее часто изучавшийся класс лучше остальных.

### Expert judgment и formal methods

Авторы отмечают расхождение между practice и research: по рассмотренным ими surveys в индустрии доминировали expert-judgment approaches, тогда как им посвящалось около 15% papers. Одновременно performance более формальных techniques описывается как erratic. Авторы рекомендуют больше изучать поддержку и улучшение expert process, а не только его замену формальной моделью (PDF 18 / печ. 18).

В summary они формулируют более сильную границу: доступное evidence не показывает, что estimation accuracy улучшается от применения formal models, и исследований реального использования таких моделей недостаточно. Среди направлений названы сочетание formal models и expert judgment, структурирование экспертного процесса, checklists и work-breakdown structures (PDF 22-23 / печ. 22-23).

Это не доказательство превосходства эксперта. Корректный вывод для `\hat{k}`: expert estimate допустим как явно маркированный источник или prior при холодном старте, но источник не даёт validated rule его объединения с model output.

## Findings: качество сравнительного evidence

### Неполный поиск меняет сравнительный вывод

Авторы разбирают собственный ранний optimistic claim об estimation by analogy. Он опирался на 6 из 20 релевантных studies, причём 3 из 6 принадлежали одному из авторов. Полный набор распределился так: 9 studies в пользу analogy, 4 inconclusive и 7 в пользу regression. Более широкий поиск сделал вывод существенно менее оптимистичным (PDF 13 / печ. 13).

Это один из самых важных claims для evidence map. Он показывает направление search/selection bias, но не устанавливает итогового победителя между analogy и regression: studies могли различаться по datasets, metrics и designs, а meta-analysis не выполнялся.

### History-based evaluation доминирует

В корпусе 166 papers (55%) использовали history-based evaluation, 141 (46%) разрабатывали estimation method, 27 (9%) были surveys, 26 (9%) reviews, 19 (6%) experiments, 17 (6%) simulations, 11 (4%) real-life evaluations и только 8 (3%) case studies. Категории nonexclusive (PDF 18-19 / печ. 18-19).

Среди papers, предлагавших или оценивавших estimation method, более 60% применяли historical data. Авторы не нашли ни одного real-life evaluation paper с углублённым сбором и анализом того, как estimation methods фактически использовались; это относилось даже к COCOMO. Их вывод ограничен найденными journal papers к дате поиска: на такой основе нельзя утверждать real-life accuracy benefit какого-либо метода (PDF 19-20 / печ. 19-20).

### Industrial context не равен prospective realism

Таблица study contexts сообщает 217 classifications (71%) как professionals/industrial projects, 21 (7%) как students/student projects и 67 (22%) как not relevant. Высокая доля industrial context повышает realism, но не снимает проблему: большинство evaluations ретроспективно применяли методы к historical datasets, а не проверяли estimator в реальном моменте принятия решения (PDF 20 / печ. 20).

Для `\hat{k}` это различие критично. Dataset из реальных завершённых задач остаётся retrospective benchmark; он не доказывает, что estimate, зафиксированный до старта новой задачи и до знания результата, будет калиброван в production workflow.

## Findings: datasets, context и uncertainty

### Availability вместо representativeness

Авторы заключают, что доступность dataset часто лучше объясняет его использование, чем representativeness. В качестве примера COCOMO 1981 dataset, основанный на технологически отличающихся проектах, был использован в 12 journal papers начиная с 1995 года. Большинство evaluations почти не обсуждало свойства datasets и оставляло external generalization читателю (PDF 20-21 / печ. 20-21).

Оценка метода на произвольно выбранном dataset мало сообщает, в каких иных контекстах и почему метод должен работать. Авторы рекомендуют перейти от удобства данных к изучению связи между project characteristics, dataset properties и estimation methods (PDF 18, 23 / печ. 18, 23).

### Uncertainty и performance measurement - слабые места корпуса

Uncertainty assessment составляла 8% papers, measures of estimation performance - 5%, dataset properties - 1%. Авторы относят к нерешённым basic issues способы сравнения estimator'ов, выбор performance measures, связь method performance со свойствами dataset и правила выбора метода (PDF 15, 17-18, 22 / печ. 15, 17-18, 22).

Следовательно, этот review не предоставляет готовой preferred metric, confidence level или error distribution для `\hat{k}`. Он поддерживает требование явно моделировать uncertainty, но не численное значение этой uncertainty.

## Точные следствия для калибровки `k_hat`

Ниже отделены findings источника от их применения к M0-M4.

| Finding источника | Следствие для `\hat{k}_i^{(r)}` в M0-M4 | Чего finding не даёт |
|---|---|---|
| Результат метода зависит от dataset properties и context | Стратифицировать наблюдения как минимум по типу задачи, инструменту/версии и режиму `r`; описывать покрытие calibration sample | Готовой таксономии AI-задач или минимального sample size |
| Устаревший доступный dataset может продолжать многократно использоваться | Версионировать инструмент и процесс, проверять temporal drift, не смешивать старые и новые поколения агента без валидации | Конкретного окна устаревания или decay coefficient |
| Arbitrary datasets плохо поддерживают external recommendations | До выбора estimator определить target population задач и критерии representativeness; отдельно валидировать на новых задачах | Доказательства, что local-only data всегда лучше cross-company data |
| History-based evaluation не равна real-life use | Фиксировать `\hat{k}` до старта задачи и затем сравнивать с realised `k`, а не подгонять и оценивать на одной выборке | Гарантии prospective accuracy |
| Uncertainty и performance measures исследованы слабо | Хранить predictive distribution/interval или верхний квантиль, проверять calibration и interval coverage наряду с point error | Формы распределения, уровня квантили или preferred accuracy metric |
| Expert judgment доминирует в practice, formal evidence erratic | Использовать expert judgment как отдельный prior/comparator и эмпирически проверять его наряду с formal estimate | Что эксперт лучше модели или что простое усреднение оптимально |
| Papers могут повторно использовать один dataset | При synthesis и validation учитывать зависимость наблюдений по проекту, команде и dataset; число papers не считать effective sample size | Полной карты shared datasets вне кодировки обзора |
| Неполный search дал optimistic analogy conclusion | Для выбора estimator включать contradictory studies и заранее фиксировать search/evaluation protocol | Универсального superiority ranking analogy против regression |

Есть ещё четыре ограничения, специфичных для переноса на M0-M4:

1. **Effort не равен elapsed duration.** Источник изучает главным образом person-effort/cost. `k_i^{(r)}` определён через однопоточное wall-clock time при полной доступности разработчика. Для `\hat{k}` нужен новый outcome protocol с едиными start/finish rules; готовую effort estimate нельзя подставлять как time ratio без преобразования и проверки.
2. **Неопределённы обе части отношения.** `\hat{k}=\widehat{T_i^{ai}(r)}/\widehat{Z_iX}` зависит не только от AI-duration estimate, но и от baseline/size estimate. Категории size measures, calibration и uncertainty показывают, что denominator нельзя считать безошибочным, однако review не выводит propagation formula.
3. **Ошибка не обязана быть общим multiplier.** Критика context и dataset dependence означает, что bias может различаться по task class и mode. Поэтому инвариантность M0-M4 к общему масштабу `k` защищает ranking только от действительно общего multiplicative factor, но не от differential miscalibration между конфигурациями.
4. **Uncertainty проходит в scheduling layer.** Ошибка `\hat{k}` меняет task weights, `W`, критический путь `L` и возможную раскладку. Jørgensen и Shepperd не анализируют этот propagation; M0-M4 должно считать свои makespan claims условными на качестве внешнего estimator или проводить sensitivity/scenario analysis.

## Mapping к параметрам M0-M4

Здесь **direct** означает тот же объект и формальную роль, **analogy** - полезный estimation-аналог с иной семантикой, **absent** - отсутствие механизма. У источника нет direct mapping к scheduling-параметрам M0-M4.

| Параметр | Статус | Соответствие в review | Точная граница |
|---|---|---|---|
| `Z` | **analogy** | Size measures, function points, work breakdown и dataset/project characteristics входят в карту estimation research | Нет нормированной task-level сложности `Z_i` в единицах `X`; review не выбирает лучший size proxy |
| `k` | **analogy** | Все классы effort estimators являются кандидатами для методологии внешнего prediction layer | Нет отношения AI wall-clock time к no-AI baseline, LLM effect и готового `\hat{k}_i^{(r)}` |
| `r` | **analogy** | Study context и project characteristics показывают необходимость условной, контекстной оценки | Нет режимов interactive/delegated/autonomous и task-level mode assignment |
| `P` | **absent** | Organizational context иногда входит в estimation studies | Нет числа параллельных агентов, capacity или effective parallelism |
| `W` | **analogy** | Development effort/cost является основным прогнозируемым aggregate outcome | Нет AI-weighted work `W=X sum_i Z_i k_i`; aggregate person-effort нельзя автоматически делить на `P` |
| `L` | **absent** | В classification schema нет critical-path lower bound | В отдельных included papers может встречаться scheduling, но systematic review не синтезирует DAG/longest-path evidence |
| `C(P)` | **absent** | Organizational issues - широкая research-topic category | Нет функции integration/coordination overhead от числа агентных потоков |
| `h` | **absent** | Expert judgment касается способа оценки, а не доли человеческой занятости в AI-task | Нет двухканального хронометража `k=a+h` |
| `H` | **absent** | Effort может измерять человеческий труд проектов | Нет суммы неперекрывающихся интервалов одного capacity-1 разработчика |
| `gamma(P)` | **absent** | Cognitive aspects expert estimation упомянуты как research gap | Нет context-switching penalty и его зависимости от `P` |
| makespan | **absent** | Cost/effort estimation - центральный outcome review | Нет resource-feasible schedule, `Cmax` objective или fixed-workload project completion time |

## Что источник поддерживает

1. Для ex ante применения M0-M4 нужен отдельный estimation layer; software estimation предлагает широкий набор классов-кандидатов, но review не устанавливает универсального победителя.
2. Regression/parametric, analogy, expert judgment, work breakdown, Bayesian methods и combinations являются различимыми подходами, которые следует оценивать в целевом контексте.
3. Внешняя переносимость estimator зависит от representativeness, возраста и свойств calibration data, а не от одной доступности dataset.
4. Retrospective performance на historical projects не заменяет prospective real-life evaluation.
5. Point accuracy недостаточна: uncertainty assessment, performance measures и dataset properties являются самостоятельными и недостаточно разработанными research topics.
6. Industry use expert judgment оправдывает его включение как comparator/prior, но не объявление ground truth.
7. Сравнительные выводы чувствительны к search coverage и vested interests; evidence map должен включать inconclusive и contradictory results.
8. Для `\hat{k}` нужны локальная контекстная проверка, явная uncertainty и обновление при смене инструмента; это применение findings review, а не готовый estimator из источника.

## Что источник не позволяет утверждать

1. Что 304 papers означают 304 независимых studies, datasets или effect sizes.
2. Что review является meta-analysis или даёт pooled accuracy любого estimation approach.
3. Что частота публикаций доказывает качество: 49% regression papers не означают превосходство regression.
4. Что analogy лучше regression: полный пример содержит смешанные результаты 9/4/7 и служит иллюстрацией search bias.
5. Что expert judgment точнее formal models либо что любой способ их combination валиден.
6. Что formal models бесполезны; авторы говорят об отсутствии достаточного real-life evidence улучшения accuracy, а не доказывают отрицательный эффект каждого метода.
7. Что industrial historical dataset равен prospective real-life evaluation.
8. Что старые или cross-organizational data всегда непригодны; требуется анализ representativeness и dataset properties.
9. Что источник задаёт confidence interval, distribution, верхнюю квантиль или допустимую ошибку для `\hat{k}`.
10. Что effort/cost estimate можно напрямую подставить как wall-clock `k_i^{(r)}` или makespan.
11. Что источник содержит evidence об LLM, Copilot, autonomous agents или topology «один разработчик - `P` агентов».
12. Что он моделирует `P`, неделимость, DAG/`L`, `C(P)`, `h`, `H`, `gamma(P)` или выводит scheduling bounds.
13. Что findings корпуса до апреля 2004 года описывают современное состояние software estimation.
14. Что исключение conferences/reports не влияет на любой вопрос: авторы допускают, что для конкретного comparative effect потребовался бы более полный source set.

## Отличие от M0-M4

| Измерение | Jørgensen и Shepperd (2007) | M0-M4 |
|---|---|---|
| Центральный вопрос | Как устроено и где методологически слабо исследование software effort/cost estimation | Каков makespan фиксированной работы при одном разработчике и `P` агентах |
| Единица анализа | Journal paper; категории могут пересекаться | Task, task-mode assignment и project DAG |
| Outcome | Преимущественно effort/cost estimate и accuracy research | Однопоточный duration factor `k`, затем project makespan |
| Метод | Systematic manual search и categorical map | Детерминированная модель M0-M4 и внешний `\hat{k}` |
| Контекст | Historical datasets, industry/student contexts, formal и judgment methods | Конкретные task/tool/mode observations одной human-agent cell |
| Параллелизм | Не является объектом synthesis | Явная capacity `P`, неделимость и resource-feasible schedule |
| Зависимости | Не синтезируются как scheduling mechanism | DAG и critical path `L` |
| Человек | Эксперт как estimator и professional context | Capacity-1 resource с `h`, `H` и `gamma(P)` |
| Результат | Research agenda и ограничения evidence | Bounds/criteria и makespan, условные на качестве duration inputs |

Источник расположен **до** M0-M4 в вычислительной цепочке. Он помогает определить, как нельзя валидировать внешний estimator, но не рассчитывает расписание. M0-M4, в свою очередь, не исправляет selection bias, concept drift, нерепрезентативные datasets или differential error в `\hat{k}`.

## Тезисы для Related Work

1. Systematic review 304 journal papers показывает широкую, но методологически неоднородную литературу: regression-based approaches доминируют, тогда как uncertainty, performance measures, dataset properties и real-life evaluation исследованы существенно реже (PDF 15-20 / печ. 15-20).
2. Сравнительное evidence нельзя сводить к популярности метода или удобному benchmark: полный набор studies по analogy дал смешанные результаты, а использование только 6 из 20 работ привело к чрезмерно optimistic claim (PDF 13 / печ. 13).
3. Для внешнего `\hat{k}_i^{(r)}` ключевы репрезентативность и актуальность task/tool/mode data, prospective проверка и predictive uncertainty; historical industrial data сами по себе не доказывают real-life accuracy (PDF 18-23 / печ. 18-23).
4. Источник картирует estimation layer, но не AI effect и не scheduling: effort/cost prediction не определяет fixed-workload makespan при `P`, DAG/`L`, `C(P)` и capacity-1 human time.

## Короткий вариант встраивания

> Jørgensen и Shepperd (2007) систематически классифицировали 304 journal papers по software effort/cost estimation. Почти половина корпуса изучала regression-based approaches, однако частота публикаций не является сравнением accuracy: авторы показывают, что неполный поиск мог превратить смешанные результаты analogy versus regression в чрезмерно оптимистичный вывод. Более 60% работ по estimation methods опирались на historical data, тогда как углублённых real-life evaluations фактического использования formal models найдено не было; uncertainty, performance measures и dataset properties также оставались редкими темами. Для M0-M4 это обосновывает отдельный и явно неопределённый estimation layer: `\hat{k}_i^{(r)}` следует калибровать и prospectively проверять на актуальных task/tool/mode data, а не переносить из удобного benchmark. При этом review не содержит AI evidence и не связывает effort estimate с makespan, который дополнительно определяется через `P`, неделимость, DAG/`L`, `C(P)`, `h`, `H` и `gamma(P)`.

## Таблица опорных страниц

| PDF | Печатная | Раздел / объект | Опорное содержание |
|---:|---:|---|---|
| 1-2 | 1-2 | Abstract; Introduction; Inclusion | Цель; 304 papers; отличие от прежних reviews; cost/effort convention; inclusion/exclusion; paper versus study |
| 3 | 3 | Identification; Classification | Manual issue-by-issue search более 100 journals; 304 papers в 76 journals; April 2004; пять classification properties |
| 4-5 | 4-5 | Classification reliability; Analysis; Threats | Проверка 30 papers; 59/150 disagreements; уточнение 12 descriptions; 109 reread, 21 changed; ограничения classification и journal-only corpus |
| 6-7 | 6-7 | Table 2 | RQ1-RQ10 и мотивация research-improvement agenda |
| 8 | 8 | Table 3 | 76 journals; top 10 содержат две трети papers; распределённость корпуса |
| 9-11 | 9-11 | Digital-library test | Google Scholar 92/304, Inspec 177/304, union 204/304; terminology и recall limitations |
| 11-13 | 11-13 | Research awareness | Узкая related-work база; disciplinary silos; example 6/20 и итог 9 analogy, 4 inconclusive, 7 regression |
| 15-16 | 15-16 | Tables 4-5 | Topics и estimation approaches; 61% method papers; 49% regression; малые доли uncertainty/performance/dataset studies |
| 17-18 | 17-18 | RQ8 | Basic research gaps; arbitrary datasets; expert judgment versus formal-technique focus |
| 18-20 | 18-20 | Table 6; RQ9 | Dominance history-based evaluation; редкость case studies и real-life evaluations; отсутствие in-depth actual-use evaluations |
| 20-21 | 20-21 | Table 7; datasets | Industrial context; availability versus representativeness; старый COCOMO dataset; слабое описание dataset properties |
| 21-23 | 21-23 | Summary | Шесть recommendations: search breadth, manual search, basic topics, real-life studies, industry-used methods, fewer arbitrary datasets |
| 52-55 | 52-55 | Appendix 3 | Операциональные определения research topics, estimation approaches, research approaches, contexts и dataset categories |

## Итоговая оценка источника

Источник является сильной первичной опорой для evidence map software effort estimation и для критики наивного внешнего `\hat{k}`. Его главная ценность не в выборе одной формулы, а в демонстрации того, что method prevalence, retrospective benchmark performance и industrial provenance dataset не гарантируют comparative или prospective validity. Особенно важны зависимость вывода от полноты поиска, редкость real-life evaluations, произвольный выбор datasets и слабое внимание к uncertainty и performance measurement.

Доказательная граница проходит перед AI и scheduling. Из review нельзя получить effect size, `k`, `h` или makespan. Корректное использование в статье: сослаться на него для обоснования context-specific, регулярно обновляемой и uncertainty-aware калибровки `\hat{k}_i^{(r)}`, а затем явно отметить, что M0-M4 принимает эти estimates как внешние входы и отдельно преобразует их в fixed-workload bounds и расписание.
