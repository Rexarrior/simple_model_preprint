# Bryant и Kirkham (1983) о Boehm (1981): литобзор по одному источнику

## Назначение и границы обзора

Этот документ разбирает локальный PDF `/Users/rexarrior/work/articles/simple_model_full/literature/boehm1981.pdf` применительно к статье M0-M4 о makespan фиксированного набора задач в ячейке «один разработчик - `P` кодовых ИИ-агентов». Фокус: исходный COCOMO, типы моделей и development modes, размер, effort, development schedule, cost drivers, эмпирическая калибровка и ограничения.

Критически важно: локальный PDF не является книгой Barry W. Boehm *Software Engineering Economics* (1981). Это 17-страничный обзор книги, опубликованный A. Bryant и J. A. Kirkham в 1983 году. Он пересказывает и критикует главным образом первые девять глав книги, приводит ссылки на её страницы и воспроизводит ряд формул COCOMO. Поэтому ниже:

- утверждения Bryant и Kirkham о прочитанном и реализованном ими COCOMO считаются прямым содержанием PDF;
- положения, приписанные Boehm, обозначаются как пересказ рецензентов, а не как независимо проверенный текст книги;
- PDF нельзя библиографически выдавать за Boehm (1981) или использовать как полную проверку всех 33 глав книги;
- формулы приводятся в той форме, в которой они напечатаны в обзорном эссе.

Ссылки имеют вид «PDF-страница / печатная страница». Для этого файла смещение постоянно: печатная страница равна PDF-странице плюс 43. SHA-256 проверенного файла: `084081a2b447429838b1fb626bd18bed745930cad2f29fa62b8cab138d72fdf9`.

## Библиография и статус

**Анализируемый источник:** A. Bryant and J. A. Kirkham. “B. W. Boehm Software Engineering Economics: A Review Essay.” *ACM SIGSOFT Software Engineering Notes*, vol. 8, no. 3, July 1983, pp. 44-60. Название, авторы, издание, том, номер, дата и начальная страница напечатаны на первой странице PDF (PDF 1 / печ. 44); конечная страница - 60 (PDF 17 / печ. 60). DOI, ISSN и сведения о процедуре рецензирования в PDF не указаны, поэтому здесь не реконструируются.

**Рецензируемая книга:** Barry W. Boehm, *Software Engineering Economics*, Prentice Hall, 1981. Именно такая идентификация дана Bryant и Kirkham на первой странице. Иные metadata книги по этому PDF не добавляются.

**Статус:** обзорное эссе в профессиональном периодическом издании ACM SIGSOFT. Это вторичный источник о COCOMO, а не первичная публикация модели и не современное эмпирическое исследование. Авторы сообщают о внимательном изучении книги и собственной реализации Basic и Intermediate COCOMO, но не описывают формальный протокол независимого воспроизведения или внешнего рецензирования (PDF 1 / печ. 44).

**Ограничение охвата:** в редакционной приписке Boehm отвечает, что авторы достаточно внимательно изучили первые 9 из 33 глав, но не охватили остальную часть книги, где обсуждаются многие поднятые ими вопросы (PDF 17 / печ. 60). Следовательно, критика полезна как современная самой модели проверка её предпосылок, но не как полный обзор всей книги.

## Вопрос и вклад источника

### Вопрос

Bryant и Kirkham спрашивают, насколько COCOMO пригоден для достаточно точной ранней оценки стоимости и графика разработки и оправданы ли широкие экономические и управленческие притязания книги. Их предмет - software cost estimation и связанное с ним прогнозирование labour effort, calendar schedule, staffing и productivity. Это не задача построения оптимального расписания фиксированного набора работ.

### Вклад

Релевантный для M0-M4 вклад состоит из четырёх частей:

1. компактная реконструкция трёх уровней COCOMO и трёх development modes;
2. явное разведение total effort в labour months, development schedule в календарных месяцах и среднего staffing как их отношения;
3. описание эмпирического происхождения уравнений и multiplicative cost-driver architecture;
4. ранняя критика неопределённого size input, проверки точности на той же базе, на которой построены уравнения, независимости cost drivers и component-level aggregation.

Источник важен для проектирования внешнего baseline-оценщика и процедуры калибровки `k_hat`, но не является формальной моделью распределения неделимых задач между параллельными агентами.

## Постановка, метод и тип аргумента

- **Объект анализа:** книга Boehm и первые две версии COCOMO; Detailed COCOMO описан, но далее почти не разбирается (PDF 6 / печ. 49).
- **Метод:** критическое чтение, реконструкция формул, собственная реализация Basic и Intermediate COCOMO, численные sensitivity examples и проверка внутренней согласованности предпосылок.
- **Данные исходной модели:** по пересказу авторов, COCOMO database содержит 63 проекта разных типов и контекстов; около 75% разработаны в 1975-1979 годах, 50% реализованы на mainframes (PDF 7 / печ. 50; с отсылкой к Boehm p. 83 и pp. 494-499).
- **Outcomes COCOMO:** labour months (`LM`), development time (`TDEV`), full-time-equivalent personnel (`FSP`), productivity и распределение effort/schedule по фазам.
- **Доказательная сила:** PDF надёжен как первичный текст критики 1983 года и как вторичное описание формул. Он не заменяет проверку формул, коэффициентов и claims по самой книге Boehm.

## Релевантные модели, формулы и результаты

### 1. Basic, Intermediate и Detailed COCOMO

Basic COCOMO строит order-of-magnitude estimates по двум входам: project size в KDSI и development mode. Из них оцениваются labour months, development schedule, staffing, productivity и фазовые профили (PDF 4, 6 / печ. 47, 49).

Intermediate COCOMO сохраняет size и mode, но корректирует nominal effort произведением 15 effort multipliers, образующим effort adjustment factor (`EAF`). Detailed COCOMO применяет multipliers по-разному к отдельным фазам разработки и сопровождения, а не только ко всему проекту (PDF 6 / печ. 49). Это иерархия детализации **оценочной модели**, не иерархия ограничений расписания, подобная M0-M4.

### 2. Размер как главный предиктор и его проблема

Размер задаётся в delivered source instructions (`DSI`) или тысячах DSI (`KDSI`). В определение включаются созданные проектом source instructions, преобразуемые в machine code; комментарии и неизменённые utilities исключаются, а тщательно разработанный support software может учитываться (PDF 4 / печ. 47; пересказ Boehm pp. 58-59).

Bryant и Kirkham указывают на эндогенность такого baseline: ранняя estimate должна опираться на KDSI, но достаточно точное знание числа строк обычно появляется лишь после существенной проработки проекта. В примерах книги size, по их критике, просто задаётся или объявляется результатом initial study. Ошибка size затем нелинейно переносится в effort и schedule (PDF 4-5 / печ. 47-48). На заключительной странице это названо фундаментальной проблемой модели (PDF 17 / печ. 60).

Для M0-M4 отсюда следует не равенство `Z = KDSI`, а требование явно определить и независимо валидировать baseline complexity `Z`. KDSI является историческим примером size proxy; источник одновременно показывает опасность считать такой proxy наблюдаемым без ошибки.

### 3. Development modes не равны режиму `r`

COCOMO различает:

- **organic:** относительно небольшие команды в знакомой внутренней среде, с меньшими communication overhead;
- **embedded:** tight constraints, интенсивные verification, validation, configuration management и quality assurance в тесно связанном комплексе hardware, software, regulation и operational procedures;
- **semidetached:** промежуточный либо смешанный случай (PDF 8 / печ. 51; пересказ Boehm pp. 78-80).

Эти modes классифицируют **контекст проекта и команды**. Режим `r` в M0-M4 классифицирует способ взаимодействия разработчика с ИИ для конкретной задачи. Совпадение слова mode не создаёт прямого математического соответствия. Полезна лишь методологическая аналогия: оценку следует стратифицировать по содержательно различным условиям исполнения.

### 4. Basic COCOMO: effort отдельно от elapsed schedule

Labour month определяется как 152 рабочих часа. Basic COCOMO оценивает total labour effort следующими уравнениями (PDF 8 / печ. 51):

\[
\begin{aligned}
LM_{org} &= 2.4\,(KDSI)^{1.05},\\
LM_{semi} &= 3.0\,(KDSI)^{1.12},\\
LM_{emb} &= 3.6\,(KDSI)^{1.20}.
\end{aligned}
\]

Development period затем оценивается отдельно:

\[
\begin{aligned}
TDEV_{org} &= 2.5\,(LM)^{0.38},\\
TDEV_{semi} &= 2.5\,(LM)^{0.35},\\
TDEV_{emb} &= 2.5\,(LM)^{0.32}.
\end{aligned}
\]

Авторы указывают, что вывод этих уравнений находится в chapter 29 книги. Средний staffing вычисляется как

\[
FSP = \frac{LM}{TDEV},
\]

а productivity - как `KDSI/LM` (PDF 9 / печ. 52).

Это место принципиально для Related Work: `LM` - суммарное person-month effort, `TDEV` - calendar duration, а `FSP` - выведенный средний staffing. Они не взаимозаменяемы. Более того, ни одно из этих уравнений не строит task assignment, не проверяет resource-feasible schedule и не минимизирует `C_max`.

Таблица medium-size project profiles показывает различие на числах: total effort для organic, semidetached и embedded modes равен соответственно 91, 146 и 230 LM, тогда как total schedule округлённо равен 14 месяцам во всех трёх случаях; средний staffing меняется от 6.5 до 16.4 FSP (PDF 9 / печ. 52). На следующей странице авторы подчёркивают, что effort растёт от organic к embedded, хотя schedule зависит от размера иначе; по фазам доли effort и schedule также различаются (PDF 10 / печ. 53).

### 5. Cost drivers и Intermediate COCOMO

Basic COCOMO учитывает главным образом DSI, а для maintenance - annual change traffic; hardware constraints, personnel и другие факторы отсутствуют. Intermediate COCOMO добавляет 15 cost drivers (PDF 11 / печ. 54):

- product: `RELY`, `DATA`, `CPLX`;
- computer: `TIME`, `STOR`, `TURN`;
- personnel: `ACAP`, `AEXP`, `PCAP`, `VEXP`, `LEXP`;
- project: `MODP`, `TOOL`, `SCED`.

Каждый driver получает rating и effort multiplier относительно nominal value `1.0`; итоговый `EAF` есть произведение multipliers. Воспроизведённые обзором nominal Intermediate equations имеют вид (PDF 12 / печ. 55):

\[
\begin{aligned}
LM_{org} &= 3.2\,(KDSI)^{1.05},\\
LM_{semi} &= 3.0\,(KDSI)^{1.12},\\
LM_{emb} &= 2.8\,(KDSI)^{1.20},
\end{aligned}
\]

после чего nominal effort корректируется `EAF`, а из скорректированных величин пересчитываются schedule, staffing и productivity. В примере 128 KDSI embedded project повышение `RELY` до multiplier `1.15` меняет effort с 945.8 до 1087.7 LM, `TDEV` с 22.4 до 23.4 месяца, staffing с 42.2 до 46.5 FSP и productivity со 135 до 118 DSI/month (PDF 12 / печ. 55).

Драйвер `TOOL` показывает, что качество средств разработки исторически рассматривалось как фактор effort. Однако он объединяет compilers, assemblers, loaders и diagnostic aids и не является оценкой современного ИИ, task/mode-specific ratio или human supervision. Использовать `TOOL` как готовое значение `k` нельзя.

`SCED` показывает ещё одну границу между сроком и усилием. В приведённом обсуждении сжатие nominal schedule до 75% повышает effort с 10 до 12.3 LM, уменьшает `TDEV` с 5.22 до 3.92 месяца и повышает staffing с 1.92 до 3.14 FSP. Авторы критикуют неясную симметрию штрафа при растяжении schedule (PDF 14 / печ. 57). Это параметрическая time-effort trade-off estimate, но не алгоритм назначения фиксированных задач исполнителям.

### 6. Калибровка и заявленная точность

Все COCOMO equations, по обзору, получены из базы 63 проектов. Сопоставление estimates с actuals на этой базе служит основанием заявленной точности. Bryant и Kirkham отдельно отмечают методологическую проблему использования одного набора и для вывода equations, и для оценки accuracy; оправдания этой процедуре в рассмотренном ими тексте они не находят (PDF 7 / печ. 50).

Обзор передаёт два связанных claims: общий ориентир «within 20% of actual costs, 70% of the time» и утверждение для Intermediate COCOMO «within 20% of project actuals 68% of the time» (PDF 3 / печ. 46; PDF 11 / печ. 54; ссылки на Boehm pp. 32 и 115). Это **сообщённые в обзоре заявления**, а не независимо воспроизведённый результат Bryant и Kirkham.

Их критика дополнительно касается:

- усиления исходной size error степенными уравнениями и multipliers (PDF 4-5 / печ. 47-48);
- возможной зависимости cost drivers и неправдоподобных комбинаций ratings (PDF 14 / печ. 57);
- proportional component allocation, которое может противоречить заявленным diseconomies of scale и modularity (PDF 15-16 / печ. 58-59);
- отсутствия ясного происхождения early-stage size input (PDF 17 / печ. 60).

Для современного `k_hat` это аргумент в пользу out-of-sample validation, локальной перекалибровки, явной uncertainty и проверки interactions, а не основание взять коэффициенты COCOMO без изменений.

## Что COCOMO может дать baseline и внешнему `k_hat`

### Поддерживаемая роль

COCOMO может обосновать **архитектуру внешнего оценивания**, но не конкретный AI effect:

1. baseline следует строить из наблюдаемого size/complexity proxy и исторически калиброванной функции effort;
2. контекст нужно стратифицировать по типам проекта или задачи, а не переносить одну среднюю оценку на всё;
3. product, platform, personnel и process/tool factors могут корректировать nominal estimate;
4. параметры должны калиброваться на completed work и проверяться на данных, не использованных для fit;
5. sensitivity analysis должна показывать, какие входы определяют решение.

В M0-M4 COCOMO-подобная модель могла бы быть одним из внешних способов оценить no-AI baseline `Z_i X` или ранжировать baseline complexity `Z_i`, если размер и локальная калибровка доступны. Затем `k_hat_i^(r)` всё равно требует отдельных наблюдений с ИИ в той же task/mode stratum:

\[
\hat{k}_i^{(r)} \approx
\frac{\widehat{T_i^{ai}(r)}}{\widehat{T_i^{no\text{-}ai}}}.
\]

Сам COCOMO оценивает знаменатель лишь косвенно и на другом уровне агрегации; числитель и AI-specific ratio в источнике отсутствуют.

### Неподдерживаемая роль

Нельзя без дополнительных данных:

- приравнивать KDSI к `Z_i`;
- приравнивать `LM` к elapsed baseline одного разработчика или к `W`;
- считать `TOOL` готовым estimator современного `k_hat`;
- переносить organic/semidetached/embedded в interactive/delegated/autonomous `r`;
- выводить из `TDEV` оптимальный makespan при заданном `P`;
- считать COCOMO component estimates расписанием независимых или зависимых задач.

## Mapping к параметрам M0-M4

Здесь **direct** означает тот же формальный объект при близкой роли, **analogy** - полезное сходство при иной семантике или единицах, **absent** - объект источником не моделируется.

| Параметр | Статус | Что есть в PDF | Граница переноса |
|---|---|---|---|
| `Z` | **analogy** | DSI/KDSI как size proxy; component sizes | Это размер кода, а не нормированная task-level baseline complexity; early estimate сама проблематична |
| `k` | **analogy** | Multiplicative effort multipliers и общий `EAF`; `TOOL` как один driver | Multipliers меняют aggregate effort, а не task/mode-specific elapsed-time ratio `T_i^ai/(Z_iX)` |
| `r` | **analogy** | Organic, semidetached, embedded development modes | Это классы проектного контекста, не режим взаимодействия человека с ИИ |
| `P` | **absent** | `FSP=LM/TDEV` как выведенный средний staffing | Нет экзогенного числа одинаковых агентных исполнителей и capacity constraint «не более `P` одновременных задач» |
| `W` | **analogy** | Total labour effort `LM` и фазовое effort distribution | Person-month effort имеет другие единицы и семантику, чем сумма AI-weighted task durations `X sum Z_i k_i` |
| `L` | **absent** | Waterfall phases и phase profiles | Нет task DAG, weighted longest path или critical-path lower bound |
| `C(P)` | **analogy** | Качественное обсуждение communication overhead и diseconomies of scale | Нет функции overhead от числа параллельных агентов; size exponent и project mode не заменяют `C(P)` |
| `h` | **absent** | Personnel capability cost drivers и фазовый staffing | Нет доли человеческой занятости внутри task duration с ИИ |
| `H` | **absent** | Total human labour effort всех работников | Нет одного shared developer capacity 1 и суммы его неперекрывающихся service intervals |
| `gamma(P)` | **absent** | Communication overhead обсуждается качественно | Cognitive switching одного человека между `P` агентными потоками не моделируется |
| makespan | **analogy** | `TDEV` предсказывает elapsed development schedule | Это регрессионная schedule estimate, а не `C_max` явно построенного resource-feasible расписания фиксированных задач |

В этом mapping нет direct-соответствий scheduling-ядру M0-M4. Сильная связь источника лежит в estimation layer, а не в allocation/scheduling layer.

## Что источник поддерживает

1. **Строгое различение effort и elapsed schedule.** `LM`, `TDEV` и `FSP` являются разными величинами и связаны нелинейно.
2. **Необходимость внешнего baseline estimator.** Size и context служат входами модели до начала проекта; точность M0-M4 как predictive model также зависит от качества внешних `Z` и `k_hat`.
3. **Историческую калибровку по completed projects.** Параметрическая модель может быть fitted на прошлых проектах, но должна проверяться независимо.
4. **Контекстность оценки.** Development mode и cost drivers показывают, что один коэффициент не должен переноситься между различными продуктами, платформами, людьми и процессами.
5. **Нелинейность size-effort relation.** Степени больше единицы выражают diseconomies of scale и не поддерживают безусловно аддитивный baseline по крупным компонентам.
6. **Sensitivity analysis.** Multipliers позволяют исследовать, как изменение предпосылок влияет на effort и schedule; аналогичный анализ нужен для `k_hat`, `h`, `C(P)` и `gamma(P)`.

## Что источник не позволяет утверждать

1. Что локальный PDF является первичным текстом Boehm (1981) или полным изложением COCOMO.
2. Что `person-month effort = elapsed time`. Даже в Basic COCOMO `LM` и `TDEV` оцениваются разными уравнениями.
3. Что `TDEV` является оптимальным makespan фиксированного набора задач. В PDF нет assignment variables, machine capacities, feasible schedule или objective `min C_max`.
4. Что источник моделирует неделимость задач, DAG, critical path `L` или list scheduling.
5. Что `FSP` эквивалентен `P`. Это среднее число full-time-equivalent personnel, выведенное после estimate effort и schedule, а не заданная мощность параллельного ресурса.
6. Что communication overhead COCOMO задаёт `C(P)` для звезды «один разработчик - агенты».
7. Что cost driver `TOOL` оценивает эффект LLM, coding agent, autonomous workflow или проверки с участием человека.
8. Что development modes COCOMO являются режимами `r` M0-M4.
9. Что источник определяет `h`, `H`, `gamma(P)` или потолок ускорения по одному разработчику.
10. Что 63 исторических проекта дают применимую без перекалибровки модель современной AI-assisted development.
11. Что заявленная accuracy является независимой out-of-sample validation; именно это обзор ставит под вопрос.
12. Что COCOMO напрямую даёт `k_hat`. Он может оценивать часть baseline, но AI numerator требует отдельной выборки по паре «тип задачи - режим».

## Отличие от M0-M4

| Измерение | COCOMO в пересказе Bryant и Kirkham | M0-M4 |
|---|---|---|
| Центральный вопрос | Сколько aggregate effort, calendar months, staff и cost потребует проект | Каков makespan заданного workload при одном разработчике и `P` агентах |
| Вход масштаба | Project/component size в DSI/KDSI | Task-level baseline complexity `Z_i` и единица времени `X` |
| Эффект инструмента | Один из aggregate cost drivers (`TOOL`) | Операциональный task/mode-specific `k_i^(r)` |
| Режим | Organic/semidetached/embedded project context | Interactive/delegated/autonomous human-AI workflow |
| Параллелизм | Средний staffing выводится как `LM/TDEV` | `P` задаёт число доступных agent streams |
| Структура задач | Фазы lifecycle и component estimates | Неделимые tasks, explicit DAG и critical path `L` |
| Overhead | Встроен в fitted exponents, modes и multipliers | Разделён на `C(P)` и человеческий `gamma(P)H` |
| Человек | Aggregate personnel attributes и labour effort | Один shared sequential resource с `h_i` и `H` |
| Результат | Parametric estimate effort и schedule | Lower bounds и достижимый/оптимальный makespan explicit schedule |

COCOMO относится к слою **effort/cost forecasting**. M0-M4 относится к слою **fixed-workload scheduling and makespan analysis**, принимая task durations и их AI-specific modifiers как вход. Эти слои могут соединяться, если COCOMO-подобный estimator поставляет baseline, но не должны сливаться в одну модель.

## Тезисы для синтеза Related Work

1. Исходный COCOMO исторически показывает, что project effort и development schedule должны оцениваться раздельно: person-months не являются calendar months, а staffing является третьей величиной, выведенной из первых двух (PDF 8-10 / печ. 51-53).
2. COCOMO даёт полезный шаблон внешнего estimator: size proxy, contextual strata, multiplicative drivers, calibration on completed projects и sensitivity analysis. Для `k_hat` этот шаблон требует AI-specific task/mode observations и независимой validation, которых в источнике нет (PDF 7, 11-14 / печ. 50, 54-57).
3. Формулы `TDEV(LM)` прогнозируют aggregate schedule, но не решают scheduling problem. Они не распределяют неделимые tasks по `P` agents, не учитывают DAG/critical path и не строят resource-feasible makespan.
4. Главная предосторожность источника актуальна для M0-M4: неопределённый baseline input и in-sample calibration способны доминировать над последующей формальной точностью. Поэтому predictive claims M0-M4 должны отделяться от точных постфактумных identities.

## Короткий вариант встраивания в Related Work

> COCOMO относится прежде всего к параметрической оценке software effort и cost, а не к теории расписаний. В пересказе и критическом разборе Bryant и Kirkham (1983) Basic COCOMO сначала оценивает aggregate effort в labour months по размеру KDSI и development mode, затем отдельным степенным уравнением получает calendar development time; средний staffing определяется как отношение этих величин. Intermediate COCOMO корректирует nominal effort произведением cost-driver multipliers. Такая архитектура мотивирует внешний baseline estimator и эмпирическую калибровку `k_hat`, но не задаёт `k_hat` для ИИ: cost driver `TOOL` не является task/mode-specific отношением длительностей. COCOMO также не распределяет фиксированные неделимые задачи между `P` исполнителями, не моделирует DAG, critical path или общий человеческий ресурс. Поэтому M0-M4 использует effort-estimation literature как upstream-слой для `Z` и `k_hat`, строго отделяя его от makespan и scheduling.

Редакционная оговорка: если в итоговой статье требуется ссылка именно на Boehm (1981), необходимо проверить первичную книгу и добавить её собственную библиографическую запись. На основании текущего файла корректно цитировать Bryant и Kirkham (1983) как вторичный обзор.

## Таблица опорных страниц

| PDF | Печатная | Страница книги, указанная в обзоре | Опорное содержание |
|---:|---:|---|---|
| 1 | 44 | 1 | Идентификация review essay и книги; цель авторов; заявлена реализация первых двух версий COCOMO |
| 3 | 46 | 18, 20ff, 32 | Фокус на productivity/maintenance; различение целей; reported accuracy norm и необходимость проверить assumptions |
| 4 | 47 | 58-59, 63 | Basic/Intermediate/Detailed; KDSI как основной вход; критика ранней оценки size |
| 5 | 48 | - | Sensitivity size error; диапазоны effort, schedule, staffing и cost; риск усиления исходной ошибки |
| 6 | 49 | - | Три версии COCOMO; EAF как произведение 15 multipliers; Detailed применяет их по фазам |
| 7 | 50 | 36-41, 46-54, 83, 494-499 | 63 проекта, период и mainframes; критика fit и accuracy на одной базе; lifecycle и фазовые activity categories |
| 8 | 51 | 59, 76, 78-80; chapter 29 | Три development modes; labour month = 152 hours; Basic effort и `TDEV` equations |
| 9 | 52 | 92 | `FSP=LM/TDEV`, productivity; medium-size profiles с разными effort и staffing при близком schedule |
| 10 | 53 | 71, 76, 80, 89 | Diseconomies of scale; различия фазовых effort и schedule; maintenance traffic |
| 11 | 54 | 114-115, 121, 155 | Ограничения Basic; 15 Intermediate cost drivers; reported claim within 20% 68% of time |
| 12 | 55 | 121, 125ff | Intermediate nominal effort equations; EAF; численный пример `RELY`; sensitivity analysis |
| 13 | 56 | 123, 130 | Personnel drivers, `MODP`, `TOOL`, начало критики `SCED` |
| 14 | 57 | 138, 466ff | Schedule compression меняет effort, `TDEV` и staffing; interactions cost drivers; adaptation formula |
| 15-16 | 58-59 | 134-146ff | Equivalent adapted size; component-level estimation; критика proportional allocation и обсуждение diseconomies/modularity |
| 17 | 60 | - | Итоговая критика size input, independence drivers и component method; комментарий Boehm об охвате лишь 9 из 33 глав |

## Итоговая оценка релевантности

Источник релевантен как ранняя критическая реконструкция estimation layer: он позволяет корректно объяснить, откуда может появиться внешний baseline и почему `k_hat` требует калибровки, стратификации и независимой проверки. Его сильнейший вклад в Related Work - не конкретные коэффициенты 1981 года, а строгое разведение aggregate effort, elapsed schedule и staffing.

Для scheduling layer источник слаб. В нём нет fixed task set, неделимости, `P` одинаковых исполнителей, DAG, `L`, resource-feasible allocation, `C(P)`, `h`, `H` или `gamma(P)`. Поэтому COCOMO нельзя подавать как предшественника формулы makespan M0-M4. Корректная связь последовательна: effort/cost model может дать внешний baseline estimate; M0-M4 затем решает иной вопрос о завершении заданной работы при конкретной человеко-агентной архитектуре.
