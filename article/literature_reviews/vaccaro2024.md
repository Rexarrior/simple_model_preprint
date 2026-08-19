# Vaccaro, Almaatouq и Malone (2024): метаанализ human-AI synergy и границы переноса на makespan

## Назначение и границы обзора

Этот документ разбирает один локальный PDF применительно к модели M0-M4 для fixed-workload makespan ячейки «один разработчик - `P` кодовых ИИ-агентов». Vaccaro, Almaatouq и Malone нужны как метааналитическое evidence о human-AI complementarity: сравнение совместной системы не только с человеком, но и с лучшим из двух solo baselines показывает, что улучшение относительно человека ещё не означает synergy.

Главная граница переноса принципиальна. Метаанализ объединяет стандартизированные показатели task performance, в том числе accuracy, error и quality, из разнородных экспериментов. Он не публикует отдельный pooled effect для completion time, не рассматривает project makespan и не оценивает параллельную звезду «один человек - несколько агентов». Hedges' `g` нельзя переводить в коэффициент времени `k`, speedup или выигрыш по makespan.

Локальный PDF содержит 14 PDF-страниц. Основная статья имеет журнальную пагинацию 2293-2303; ссылки ниже даны на PDF-страницы локального файла, а не на журнальные номера страниц. Supplementary Information, на который ссылается основной текст, в проверенную локальную копию не входит.

## Библиография, статус и версия

**Полная ссылка:** Michelle Vaccaro, Abdullah Almaatouq, and Thomas Malone. “When Combinations of Humans and AI Are Useful: A Systematic Review and Meta-Analysis.” *Nature Human Behaviour*, 8, 2293-2303, 2024. DOI: [10.1038/s41562-024-02024-1](https://doi.org/10.1038/s41562-024-02024-1).

**Статус:** опубликованная журнальная статья. На первой странице указаны даты `Received: 6 April 2023`, `Accepted: 23 September 2024` и `Published online: 28 October 2024`, а также том, месяц и страницы выпуска: *Nature Human Behaviour*, volume 8, December 2024, 2293-2303 (PDF с. 1).

**Фактически проверенная версия:** издательский PDF основного текста `vaccaro2024.pdf`, SHA-256 `69ff4683a8513b2247a5375eaa81d8d18b3b8f51a9ba546c4daeb77a13205f74`. Числа ниже относятся именно к этой версии. Supplementary tables и figures не проверялись, поэтому результаты, доступные только в supplement, в обзор не переносятся.

Предлагаемая запись для `references.bib`:

```bibtex
@article{vaccaro2024combinations,
  author  = {Vaccaro, Michelle and Almaatouq, Abdullah and Malone, Thomas},
  title   = {When Combinations of Humans and {AI} Are Useful: A Systematic Review and Meta-Analysis},
  journal = {Nature Human Behaviour},
  year    = {2024},
  volume  = {8},
  pages   = {2293--2303},
  doi     = {10.1038/s41562-024-02024-1},
  url     = {https://doi.org/10.1038/s41562-024-02024-1}
}
```

## Исследовательский вопрос и определения

Работа задаёт два связанных вопроса: насколько эффективна human-AI collaboration в среднем и при каких условиях совместная система даёт performance gains либо losses. Авторы ищут факторы на уровне задачи, участников, AI и experimental design, объясняющие неоднородность результатов (PDF с. 1-3).

В основном анализе разведены два estimand (PDF с. 2, 7):

1. **Human-AI synergy (strong synergy):** совместная система сравнивается с тем solo condition, которое в среднем показывает лучший результат, то есть с `max(human alone, AI alone)`. Положительный `g` означает, что комбинация лучше обоих solo baselines; отрицательный - что по крайней мере один solo baseline лучше комбинации.
2. **Human augmentation:** совместная система сравнивается только с `human alone`. Положительный `g` означает улучшение относительно человека, даже если AI alone остаётся лучше совместной системы.

Термин **complementarity** используется как содержательная идея взаимодополняющих сильных сторон человека и AI. Отдельного третьего pooled estimand с названием “complementarity” авторы не вводят: строгая операционализация этого тезиса в работе - human-AI synergy относительно лучшего solo condition. Поэтому augmentation нельзя называть synergy без смены определения.

Для нашей статьи различие baselines особенно важно. M0-M4 определяет speedup относительно последовательной работы одного разработчика без AI. Такой baseline ближе к human augmentation, но не устанавливает превосходство над AI-only процессом или над лучшей доступной solo configuration. Ссылка на Vaccaro не должна превращать выигрыш относительно `T_h` в утверждение о synergy.

## Protocol и корпус

### Регистрация и стандарты

Авторы называют обзор preregistered и дают OSF preregistration. Метаанализ проводился по рекомендациям Kitchenham для systematic reviews и стандарту PRISMA; данные и код опубликованы в OSF (PDF с. 1, 3, 6, 8).

### Поиск

- Базы: ACM Digital Library, Web of Science Core Collection и Association for Information Systems eLibrary.
- Временной интервал публикаций: с 1 января 2020 года по 30 июня 2023 года.
- Поиск выполнен в июле 2023 года.
- Строка объединяла четыре группы терминов: human, AI, collaboration и experiment; поиск выполнялся по abstract.
- Дополнительно проведён backward и forward search по включённым работам (PDF с. 1, 7).

### Eligibility criteria

Для включения требовались (PDF с. 6-7):

1. оригинальный эксперимент, где человек и AI совместно выполняют задачу;
2. количественный performance outcome для `human alone`, `AI alone` и `human-AI system`;
3. experimental design, размеры условий и standard deviations либо достаточные данные для их восстановления;
4. текст на английском языке.

Исключались чистые meta-analyses и literature reviews, theoretical work, qualitative analyses, commentaries, opinions и simulations. В разделе limitations авторы также указывают, что ограничивали корпус peer-reviewed publications, хотя качество дизайнов внутри этого фильтра оставалось неодинаковым (PDF с. 5-7).

Критерий трёх условий создаёт содержательный selection boundary: метаанализ не включает процессы, где задача по определению невыполнима человеком или AI в одиночку, но выполнима только совместно. Он также исключает значительную часть human-AI исследований, сообщающих лишь `human alone` и `human-AI` без `AI alone` (PDF с. 5-6).

### Flow и единица анализа

Первичный поиск дал **5,126 papers**. После отбора в анализ вошли **74 papers**, содержащие **106 unique experiments** и **370 unique effect sizes**. Несколько effect sizes из одного эксперимента могли возникать из нескольких treatments или performance measures; experiments определялись по различным participant samples (PDF с. 1-3, 7).

Для расчёта извлекались среднее, standard deviation и число участников в условиях human alone, AI alone и human-AI. Если SD можно было восстановить из CI или SE, авторы делали это формульно; при доступных raw data пересчитывали statistics; значения только на графиках извлекали через WebPlotDigitizer после безуспешного запроса авторам. Исследование без достаточных данных исключалось (PDF с. 7).

## Outcomes и статистическая модель

### Outcome types

Корпус объединяет разные количественные measures task performance, прямо названные авторами как **task accuracy, error и quality**. Многие эксперименты использовали один показатель overall accuracy. Различались также task output: binary, categorical, numeric и open response, а задачи были разделены на decision и creation (PDF с. 3-6).

Это performance meta-analysis, а не time meta-analysis. Completion time и financial cost упомянуты авторами среди метрик, которые будущим исследованиям следует измерять наряду с качеством, но основной PDF не даёт отдельного pooled estimate для времени. Даже если отдельные включённые эксперименты содержали efficiency outcomes, проверенный основной текст не позволяет выделить из 370 effect sizes time-only subset и оценить его отдельно (PDF с. 5-6).

### Effect size

Авторы рассчитывают Hedges' `g`, то есть скорректированную на small-sample bias standardized mean difference. Для synergy baseline равен лучшему по среднему результату из human alone и AI alone; для augmentation baseline равен human alone. Безразмерность `g` позволяет объединять разные performance scales, но не делает эти шкалы одной физической величиной (PDF с. 7).

Для M0-M4 знак и масштаб дополнительно несовместимы с `k`:

- у Vaccaro положительный `g` означает лучший performance outcome;
- в M0-M4 `k<1` означает меньшее время относительно baseline;
- `g` измеряется в pooled standard deviations, а `k` является ratio длительностей.

Поэтому ни `g=-0.23`, ни `g=0.64` нельзя алгебраически преобразовать в проценты времени, `k`, speedup или makespan без исходных time distributions и общего acceptance criterion.

### Meta-analytic model

Из-за ожидаемой вариации задач, populations и designs использована random-effects model. Зависимые effect sizes вложены в experiments в three-level model. Для overlapping samples применены robust variance estimates; inference использует Knapp-Hartung adjustment и `t` distribution с числом степеней свободы `k-p`, где `k` - число experiment clusters, `p` - число coefficients. Модераторы проверялись отдельными meta-regressions (PDF с. 3, 7).

## Основные результаты и неопределённость

### Synergy против лучшего solo condition

Совместные системы в среднем показали результат ниже лучшего из human alone и AI alone:

`g = -0.23`, `t(92) = -2.89`, two-tailed `p = 0.005`, 95% CI `[-0.39, -0.07]` (PDF с. 1-3).

Авторы классифицируют величину как small. На уровне отдельных effect sizes 213 из 370 (58%) были отрицательными и 157 (42%) положительными, но эти доли не учитывают precision и dependence; основной pooled вывод задаёт three-level model, а не простой подсчёт знаков (PDF с. 2).

### Augmentation против человека

При сравнении только с human alone знак меняется:

`g = 0.64`, `t(98) = 11.87`, two-tailed `p < 0.001` при опубликованной точности, 95% CI `[0.53, 0.74]` (PDF с. 2-3).

Авторы интерпретируют этот эффект как medium-to-large. Следовательно, один и тот же корпус поддерживает среднее улучшение относительно человека, но не превосходство над лучшим solo condition. Это не противоречие, а следствие разных baselines.

### Moderator: task type

Task type значимо модерировал synergy: `F(1,104) = 7.84`, two-tailed `p = 0.006` (PDF с. 3).

- **Decision tasks:** `g = -0.27`, `t(104) = -3.20`, `p = 0.002`, 95% CI `[-0.44, -0.10]`.
- **Creation tasks:** `g = 0.19`, `t(104) = 1.35`, `p = 0.180`, 95% CI `[-0.09, 0.48]`.

Разность между task types статистически значима, но creation estimate сам по себе неотличим от нуля и основан лишь на `n=34` effect sizes. Кодирование можно считать creation task только как гипотезу для переноса: software development сочетает generation, constrained decisions, testing и integration и не совпадает автоматически с open-response creation category.

Task data также модерировали synergy (`F(4,101) = 15.24`, `p < 0.001`) и augmentation (`F(4,101) = 6.52`, `p < 0.001`), но основной текст не печатает все subgroup estimates и CI. Их нельзя восстанавливать визуально из figure или приписывать supplement без проверки (PDF с. 3-4).

### Moderator: кто лучше solo

Относительная performance human alone и AI alone была наиболее сильным напечатанным модератором synergy: `F(1,104) = 81.79`, `p < 0.001` (PDF с. 3).

- Когда **human alone был лучше AI alone**, synergy была положительной: `g = 0.46`, `t(104) = 5.06`, `p < 0.001`, 95% CI `[0.28, 0.66]`.
- Когда **AI alone был лучше human alone**, совместная система уступала AI: `g = -0.54`, `t(104) = -6.20`, `p < 0.001`, 95% CI `[-0.71, -0.37]`.

Относительная solo performance модерировала и augmentation: `F(1,104) = 24.35`, `p < 0.001`. Когда AI alone превосходил человека, human-AI system относительно human alone давала `g = 0.74`, `t(104) = 13.50`, `p < 0.001`, 95% CI `[0.63, 0.85]` (PDF с. 3). Это особенно наглядно показывает, почему augmentation не равна synergy.

Авторы предлагают механизм selective reliance: если человек в среднем сильнее AI, он может лучше распознавать случаи, когда следует принять AI recommendation. Это интерпретация, а не отдельно идентифицированный causal mediator (PDF с. 5).

### Другие moderators

Для synergy значимыми были AI type (`F(2,103) = 3.77`, `p = 0.026`) и publication year (`F(3,102) = 3.65`, `p = 0.015`). Experimental design модерировал augmentation (`F(1,104) = 4.90`, `p = 0.029`). Explanation, AI confidence, participant type и division of labour не дали статистически значимых moderator tests для synergy или augmentation (PDF с. 3-4).

Последний null result нельзя трактовать как доказательство неважности division of labour: заранее разделённые подзадачи были представлены только четырьмя effect sizes из трёх экспериментов. Их pooled synergy estimate равнялся `g = 0.22`, `t(104) = 0.69`, `p = 0.494`, 95% CI `[-0.42, 0.87]`, то есть был крайне неточным (PDF с. 5).

## Heterogeneity, publication bias и robustness

### Heterogeneity

Неоднородность очень высока:

- synergy: `I^2 = 97.7%`;
- augmentation: `I^2 = 93.8%` (PDF с. 3).

Модераторы объясняют часть вариации, но значительная доля остаётся необъяснённой. Авторы указывают на возможные взаимодействия закодированных переменных, неучтённые moderators, различия platforms и stimuli; мощности корпуса недостаточно для надёжной оценки interactions (PDF с. 5).

Следовательно, pooled estimates описывают центр крайне разнородного распределения, а не универсальную константу human-AI collaboration. Для M0-M4 это аргумент в пользу task-, population-, outcome- и mode-specific calibration, но не численная prior для `k`.

### Publication bias

Для primary outcome synergy диагностические тесты не выявили evidence of publication bias:

- Egger: `beta = -0.67`, `t(104) = -0.78`, `p = 0.438`, 95% CI `[-2.39, 1.04]`;
- rank correlation: `tau = 0.05`, `p = 0.121` (PDF с. 8).

Для augmentation, напротив, обнаружена funnel-plot asymmetry, совместимая с publication bias в пользу положительных результатов:

- Egger: `beta = 1.96`, `t(104) = 3.24`, `p = 0.002`, 95% CI `[0.76, 3.16]`;
- rank correlation: `tau = 0.19`, `p < 0.001` при опубликованной точности (PDF с. 8).

Авторы не корректировали estimates: методы adjustment способны overcorrect, поэтому исходные данные оставлены без преобразования. Корректная формулировка - «для synergy тесты не дали сигнала, для augmentation дали»; общее утверждение «publication bias отсутствует» неверно.

### Sensitivity analyses

Основные знаки и масштабы устойчивы в нескольких проверках (PDF с. 8):

- clustering на уровне paper вместо experiment: synergy `g = -0.22`, 95% CI `[-0.41, -0.04]`; augmentation `g = 0.65`, 95% CI `[0.52, 0.78]`;
- после исключения 11 synergy outliers и 9 augmentation outliers: synergy `g = -0.25`, 95% CI `[-0.39, -0.11]`; augmentation `g = 0.60`, 95% CI `[0.50, 0.69]`;
- leave-one-out: synergy summary effects от `-0.28` до `-0.19`, во всех случаях `p < 0.05`; augmentation от `0.61` до `0.66`, во всех случаях `p < 0.05`;
- без effect sizes, рассчитанных через WebPlotDigitizer или из информации, приведённой авторами в статье: synergy `g = -0.21`, 95% CI `[-0.36, -0.05]`; augmentation `g = 0.64`, 95% CI `[0.53, 0.75]`.

Эти проверки поддерживают устойчивость pooled contrast к отдельным observations и аналитическим решениям. Они не устраняют высокую heterogeneity, selection boundary корпуса и несовпадение outcomes с makespan.

## Ограничения

### Признанные авторами

1. Требование трёх conditions исключает задачи, которые невозможно выполнить одному из partners, но возможно выполнить совместно.
2. Hedges' `g` объединяет accuracy, error и quality, но samples, measures и measurement error заметно различаются; variance weighting не учитывает все источники measurement error.
3. Publication bias остаётся возможным; для augmentation диагностика прямо даёт сигнал asymmetry.
4. Лабораторные tasks, processes и participant pools могут не представлять практические human-AI configurations; возможен research-topic selection bias.
5. Даже peer-reviewed studies различаются по rigour, attention checks и incentives.
6. `I^2` очень высок; исследованные moderators объясняют только часть heterogeneity, а данных для interactions недостаточно (PDF с. 5).

### Дополнительные ограничения для M0-M4

1. **Outcome mismatch.** Performance quality/accuracy не равна elapsed time; standardized mean difference не является duration ratio.
2. **Нет fixed-quality workload.** Эксперименты используют разные performance outcomes, а единый acceptance threshold для одинакового объёма принятой работы не задан.
3. **Нет software-specific pooled estimate.** Основной текст не выделяет coding experiments и не даёт subgroup `g` для software engineering.
4. **Нет one-human-many-agents topology.** Совместная condition не означает `P` параллельных AI workers; более 95% систем в корпусе оставляли человеку final decision после AI input.
5. **Нет agent-count intervention.** `P` не варьируется как число одновременных исполнителей, поэтому diminishing returns и optimal fan-out не оцениваются.
6. **Нет two-channel timing.** Human-active и agent-autonomous intervals не разделены; `h`, `H` и switching cost не идентифицируются.
7. **Нет scheduling structure.** Не заданы project jobs, неделимость, DAG, critical path или resource-feasible schedule.
8. **Creation не равно coding.** Положительный creation estimate неточен, включает лишь 34 effect sizes и имеет CI, пересекающий ноль.
9. **Division of labour почти не представлена.** Четыре effect sizes из трёх experiments недостаточны для вывода о delegated workflow.
10. **Baseline mismatch.** M0-M4 сравнивает с human-only time, тогда как strongest synergy contrast сравнивает с лучшим solo performance; эти выводы отвечают разным вопросам.

## Mapping к параметрам модели

Здесь **conceptual support** означает полезное ограничение интерпретации, но не оценку параметра; **absent** - отсутствие соответствующего объекта или варьирования.

| Поле модели | Статус | Соответствие у Vaccaro et al. | Точная граница |
|---|---|---|---|
| baseline `X` | **absent как единица времени** | Есть human-alone, AI-alone и best-solo performance baselines | Это baselines стандартизированной performance, не базовая трудоёмкость единицы работы |
| сложность `Z_i` / `Z` | **conceptual support** | Tasks, data и outputs неоднородны; task type модерирует synergy | Нет нормированной шкалы сложности, task weights или связи с human-only duration |
| `k_i^(r)` | **неидентифицируем** | Heterogeneity показывает зависимость эффекта от task и configuration | Hedges' `g` не является `T_i^ai/(Z_iX)`; отсутствует pooled time ratio и фиксированное качество |
| режим `r` | **partial conceptual support** | Кодируются explanation, confidence, AI type, design и division of labour; процессы взаимодействия различаются | Нет сопоставимой taxonomy interactive/delegated/autonomous coding modes; division of labour почти отсутствует |
| fixed workload / `N` | **absent** | Каждый experiment задаёт некоторую task | Нет единого фиксированного набора project jobs или сопоставимого accepted output |
| `W = X sum Z_i k_i` | **absent** | Meta-analysis агрегирует standardized effect sizes | Effect sizes нельзя суммировать как объём AI-weighted работы |
| `P` | **absent как parallelism** | Есть human-AI combination | Число concurrent agents не является treatment и не оценивается |
| неделимость / `M_N` | **absent** | Отдельные experiments имеют законченные tasks | Нет раскладки jobs по исполнителям или longest-job bound |
| DAG / `L` | **absent** | Task processes могут иметь внутренние этапы | Precedence graph и critical path не заданы |
| `C(P)` | **absent** | Авторы обсуждают coordination и interaction process концептуально | Нет интеграционных издержек как функции числа agent streams, shared artifacts или merge conflicts |
| `h_i^(r)` | **conceptual support, без числа** | Most systems оставляют final decision человеку; trust и selective reliance обсуждаются как механизм | Нет хронометража prompting, review, verification и correction; performance effect не даёт human time share |
| `H = X sum Z_i h_i` | **absent** | Human involvement присутствует во многих experiments | Нет суммы непересекающихся human intervals по fixed workload |
| `gamma(P)` | **absent** | Interaction design может влиять на result | Нет context switching между `P` потоками и зависимости штрафа от `P` |
| makespan | **absent** | Outcome - task performance | Не измеряется elapsed completion time fixed project under a feasible schedule |

## Полный mapping к уровням M0-M4

| Уровень | Что требует M0-M4 | Что даёт источник | Вердикт |
|---|---|---|---|
| M0 | Идеально делимая fixed work, `W/P`, time coefficients `k` | Pooled standardized performance относительно двух baselines | Не калибрует `W`, `P` или `k`; поддерживает только контекстность AI effect и важность baseline |
| M1 | Неделимые jobs и lower bound `max(W/P, M_N)` | Отдельные experimental tasks без machine allocation | Неделимость и longest-job constraint не исследуются |
| M2 | DAG и critical path `L` | Task type/output/data как moderators | Это taxonomy outcomes, а не precedence structure; `L` отсутствует |
| M3 | Integration overhead `C(P)` при росте parallelism | Общее обсуждение coordination barriers и process design | Нет `P>1`, shared codebase или численной зависимости overhead от parallelism |
| M4 | Разложение `k=a+h`, capacity-1 human resource `H`, switching penalty `gamma(P)` | Human final decision, reliance и division of labour рассматриваются как interaction features | Есть мотивация учитывать роль человека, но нет two-channel time, one-human-many-agents schedule, `h`, `H` или `gamma(P)` |

Vaccaro et al. находятся перед time-and-scheduling layer M0-M4. Они отвечают на вопрос, когда совместная система лучше человека или лучшего solo performer по измеренной task performance. M0-M4 отвечает на другой вопрос: как externally calibrated task durations складываются в makespan fixed workload при `P` agents, dependencies, integration overhead и одном последовательном человеческом ресурсе.

## Что источник поддерживает для статьи

1. **Baseline должен называться явно.** Improvement против human alone (`g=0.64`) сосуществует с loss против best solo (`g=-0.23`); “AI helps humans” и “human-AI system is best” - разные claims (PDF с. 2-3).
2. **Human-AI complementarity не является автоматическим следствием объединения partners.** Средняя strong synergy отрицательна, а знак существенно зависит от task type и relative solo performance (PDF с. 3-5).
3. **Эффект configuration-specific.** Очень высокая heterogeneity и moderator results поддерживают хранение task, outcome, population и process context при внешней калибровке параметров модели (PDF с. 3, 5).
4. **Process design важен не меньше модели.** Авторы рекомендуют распределять subtasks по comparative strengths и стандартизировать interaction protocols, quality constraints и evaluation metrics (PDF с. 5-6).
5. **Time-only вывод требует отдельного evidence.** Авторы прямо призывают учитывать completion time, cost и error consequences дополнительно к accuracy; их собственный pooled `g` не решает эту задачу (PDF с. 5-6).
6. **Quality constraint следует фиксировать при калибровке `k`.** Без него уменьшение времени и изменение качества нельзя свести к одному duration coefficient (PDF с. 6).

Пункты 3, 5 и 6 - интерпретация результатов и рекомендаций в терминах M0-M4, а не формулировки авторов.

## Что источник не позволяет утверждать

1. Что human-AI collaboration в среднем ускоряет или замедляет работу на 23% либо 64%.
2. Что `g=-0.23` или `g=0.64` можно подставить в `k_i^(r)`.
3. Что pooled effects относятся к time, throughput, effort или fixed-workload makespan.
4. Что human-AI combinations всегда хуже: augmentation положительна, а subgroup effects гетерогенны.
5. Что creation tasks надёжно дают synergy: estimate `g=0.19` имеет 95% CI `[-0.09,0.48]` и `p=0.180`.
6. Что software development относится к creation subgroup без дополнительной проверки.
7. Что работа оценивает coding agents, production repositories, tests, maintainability, integration или long-term rework.
8. Что source поддерживает `P>1`, linear scaling, diminishing returns или оптимальное число агентов.
9. Что из average human-AI effect можно получить `C(P)`, `h`, `H` или `gamma(P)`.
10. Что отсутствие значимого moderator effect для explanation, confidence или division of labour доказывает отсутствие их влияния: statistical power и coverage ограничены.
11. Что диагностика исключила publication bias вообще: отсутствие сигнала относится к synergy, тогда как для augmentation signal обнаружен.
12. Что pooled estimate является универсальным: `I^2` превышает 90% для обоих основных outcomes.
13. Что human-only baseline M0-M4 автоматически является наиболее релевантным operational baseline; источник показывает, что вывод зависит от сравниваемой alternative.

## Отличие от M0-M4

| Измерение | Vaccaro et al. (2024) | M0-M4 |
|---|---|---|
| Центральный вопрос | Когда combination лучше человека или лучшего solo performer по task performance | Когда `P` coding agents сокращают makespan fixed workload одного разработчика |
| Объект | 74 papers, 106 experiments, 370 performance effect sizes | Один конкретный software project с tasks `i=1..N` |
| Domain | Междисциплинарные decision и creation tasks | Software engineering |
| Топология | Разные human-AI systems, обычно человек принимает final decision | Звезда: один shared developer и `P` concurrent coding agents |
| Baselines | Human alone; `max(human alone, AI alone)` | Sequential no-AI human time `T_h` |
| Outcome | Standardized task performance: accuracy, error, quality и другие measures | Elapsed makespan и speedup при фиксированном объёме принятой работы |
| Effect measure | Hedges' `g` | Duration ratio `k_i^(r)` и time quantities `W`, `L`, `H` |
| Workload | Разные isolated experimental tasks | Fixed set of weighted tasks `Z_i` |
| Parallelism | Agent count не варьируется | Явный `P` и effective parallelism |
| Dependencies | Не формализованы | DAG и critical path `L` |
| Coordination | Interaction features и process design как moderators | `C(P)` для integration overhead |
| Human resource | Final choice/reliance, без раздельного времени | `h_i`, capacity-1 `H`, verification windows и `gamma(P)` |
| Неопределённость | Three-level random-effects model, CI, very high `I^2`, bias/sensitivity tests | Детерминированное ядро; uncertainty должна входить через внешний estimator параметров |

## Проверенные claims для Related Work

1. В preregistered systematic review авторы отобрали 74 papers, содержащие 106 experiments и 370 effect sizes с обязательными human-alone, AI-alone и human-AI conditions (PDF с. 1-3, 6-7).
2. Средний вывод зависел от baseline: human-AI systems превосходили human alone (`g=0.64`, 95% CI `[0.53,0.74]`), но уступали лучшему из human alone и AI alone (`g=-0.23`, 95% CI `[-0.39,-0.07]`) (PDF с. 2-3).
3. Task type значимо модерировал synergy: для decision tasks pooled effect был отрицательным (`g=-0.27`, 95% CI `[-0.44,-0.10]`), а для creation tasks - положительным, но неточным и неотличимым от нуля (`g=0.19`, 95% CI `[-0.09,0.48]`) (PDF с. 3).
4. Relative solo performance была сильным модератором: при превосходстве человека synergy составляла `g=0.46` (95% CI `[0.28,0.66]`), а при превосходстве AI - `g=-0.54` (95% CI `[-0.71,-0.37]`); при этом heterogeneity оставалась очень высокой (`I^2=97.7%` для synergy) (PDF с. 3).

## Встраивание в статью

### Рекомендуемое место

Источник лучше поставить в подраздел эмпирики human-AI productivity после исследований отдельных coding tools и до перехода к scheduling literature. Его функция - не дать численное `k`, а установить три methodological constraints:

1. различать augmentation и synergy через explicit baseline;
2. не смешивать quality/accuracy с time/makespan;
3. калибровать AI effect по task, outcome и process configuration из-за высокой heterogeneity.

### Безопасный короткий вариант для `Related Work`

> Метаанализ Vaccaro, Almaatouq и Malone (2024), включивший 106 экспериментов и 370 effect sizes, показывает зависимость вывода о human-AI complementarity от baseline. Совместные системы в среднем превосходили человека (`g=0.64`, 95% CI `[0.53,0.74]`), но уступали лучшему из человека и AI (`g=-0.23`, 95% CI `[-0.39,-0.07]`); heterogeneity при этом превышала 90%. Тип задачи и относительная performance человека и AI по отдельности значимо меняли результат. Для нашей постановки это поддерживает task- и configuration-specific calibration и явный выбор baseline, но не даёт оценки `k` или makespan: метаанализ объединяет главным образом performance outcomes вроде accuracy, error и quality, не рассматривает звезду с `P` параллельными coding agents и не публикует отдельный pooled time effect.

### Формулировка для limitations модели

> Коэффициент `k_i^(r)` является отношением длительностей при фиксированном критерии завершения и не заменяет отдельную модель качества. Метааналитические результаты human-AI collaboration показывают, что вывод меняется при сравнении с человеком или с лучшим solo performer и существенно различается по типам задач. Поэтому standardized quality effect нельзя преобразовывать в duration ratio, а калибровка `k` должна хранить baseline, outcome, acceptance threshold и interaction mode.

## Таблица доказательных страниц

| PDF-страница | Раздел / объект | Опорное содержание |
|---:|---|---|
| 1 | Title; Abstract | Библиография и даты версии; preregistration; базы и период; 106 experimental studies, 370 effect sizes; synergy `g=-0.23`, CI; task-type и relative-performance headline moderators; общие limitations |
| 2 | Definitions; Fig. 1; Results flow | Определения synergy и augmentation; 74 papers, 106 experiments, 370 effect sizes; 213 negative и 157 positive synergy effects; augmentation `g=0.64`, CI |
| 3 | Overall effects; Heterogeneity; Moderators | Exact pooled tests; `I^2`; decision/creation estimates и CI; relative human/AI performance estimates; AI type/year/design moderators; insignificant moderators |
| 4 | Fig. 2; Discussion | Moderator categories и subgroup sizes; интерпретация task type; граница между augmentation и synergy |
| 5 | Process discussion; Limitations | Division-of-labour estimate; selective-reliance interpretation; accuracy examples; full limitations, research-topic bias, study quality и unexplained heterogeneity |
| 6 | Roadmap; Methods start | Creation-task boundary; process design и subtask allocation; commensurability criteria; quality constraints; call for completion-time/cost metrics; PRISMA/Kitchenham; eligibility criteria |
| 7 | Search; extraction; effect-size model | Search databases, dates и string; backward/forward search; data extraction/reconstruction; moderators; definitions of Hedges' `g`; three-level random effects, robust variance и Knapp-Hartung |
| 8 | Bias tests; Sensitivity | Synergy versus augmentation publication-bias tests; paper-level clustering; outlier, leave-one-out и digitization sensitivity estimates; OSF data/code |

## Итоговая оценка источника

Vaccaro et al. - сильный peer-reviewed meta-analytic source для определения human-AI synergy, демонстрации зависимости результата от baseline и документирования межисследовательской heterogeneity. Наиболее полезный для статьи вывод состоит не в среднем `g`, а в расхождении augmentation и synergy: совместная система может помогать человеку и одновременно проигрывать AI alone.

Для time model доказательная сила заканчивается до M0. Источник не оценивает completion-time ratio при фиксированном качестве, agent count, scheduling, DAG, integration overhead или shared human attention. Его корректная роль - ограничить интерпретацию эмпирического `k`: quality/accuracy effect не равен time effect, средний эффект не переносится между configurations, а baseline human alone не даёт права утверждать превосходство над best solo system.
