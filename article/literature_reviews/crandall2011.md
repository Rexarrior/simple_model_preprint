# Crandall et al. (2011): распределение внимания оператора при управлении несколькими роботами

## Назначение и границы обзора

Этот документ разбирает один источник применительно к модели M0-M4 для fixed-workload makespan ячейки «один разработчик - `P` кодовых ИИ-агентов». Crandall et al. особенно близки к уровню M4: один оператор обслуживает несколько semi-autonomous robots, одновременно взаимодействует только с одним роботом, а политика распределения внимания определяет, какой поток получает следующий интервал человеческого обслуживания.

Сходство является структурным, но не полным. Источник решает stochastic supervisory-control problem с фиксированным восьмиминутным горизонтом и utility objective, а не задачу завершения фиксированного объёма работ. Он не моделирует software verification, DAG задач, critical path, интеграцию изменений или project makespan. Поэтому работа поддерживает необходимость явного attention-allocation schedule и state-dependent switching/service times, но не формулу `B_4`, не численные значения `h`, `H` или `gamma(P)` и не критерий ускорения M0-M4.

## Метаданные и статус

**Полная ссылка:** Jacob W. Crandall, Mary L. Cummings, Mauro Della Penna, and Paul M. A. de Jong. “Computing the Effects of Operator Attention Allocation in Human Control of Multiple Robots.” *IEEE Transactions on Systems, Man, and Cybernetics - Part A: Systems and Humans* 41, no. 3 (May 2011): 385-397. DOI: [10.1109/TSMCA.2010.2084082](https://doi.org/10.1109/TSMCA.2010.2084082).

**Версия:** локальная копия является final published version. Это прямо указано на репозиторной обложке MIT (PDF 1). DOI resolver подтверждает журнальные метаданные: 2011, том 41, выпуск 3, страницы 385-397.

**Хронология публикации:** рукопись получена 7 сентября 2009 г., пересмотрена 3 апреля 2010 г., принята 12 июня 2010 г.; online publication датирована 21 ноября 2010 г., current version - 15 апреля 2011 г., выпуск - May 2011 (PDF 2 / журн. с. 385). Корректный библиографический год финальной выпускной версии - **2011**. Online date 2010 и copyright line `© 2010 IEEE` не меняют год цитируемого выпуска.

**Статус:** финальная опубликованная журнальная статья IEEE. PDF содержит историю received/revised/accepted и указывает редактора, организовавшего review; детали процедуры рецензирования не описаны.

**Локальный файл:** `crandall2011.pdf`.

- формат: PDF 1.4;
- объём: 14 PDF-страниц;
- SHA-256: `be16a79f62e7e49ede8d8ed54793f2246e97949a0512f0bc3622dd96132ce0cb`;
- PDF 1 - репозиторная обложка MIT;
- PDF 2-14 - журнальная статья, печатные страницы 385-397.

Ниже страницы указываются в формате `PDF / журнальная страница`.

## Исследовательские вопросы и вклад

Работа рассматривает time-critical human-multiple-robot systems (HMRS), где один оператор supervises несколько semi-automated tasks. Авторы ставят два связанных вопроса (PDF 2-3 / с. 385-386):

1. Как вычислить эффективную operator attention allocation scheme (`OAAS`), то есть scheduling policy, определяющую, какому роботу оператор должен уделять внимание в каждом состоянии системы?
2. Как использовать вычисленную политику в интерфейсе: позволить автоматике диктовать выбор робота или лишь рекомендовать его оператору?

Вклад включает:

1. применение stochastic discrete-event model для counterfactual оценки неизвестных ранее attention-allocation policies;
2. поиск приближённо оптимальной `OAAS*` в ограниченном пространстве minute-by-minute priority policies;
3. sensitivity analysis допущений о time discretization, state aggregation, switching time, interaction time и objective function;
4. два интерфейсных механизма реализации политики - Auto и Guided;
5. пользовательский эксперимент, проверяющий predictive accuracy, system effectiveness, adherence, subjective workload и preference;
6. отрицательный практический вывод: brittle model не следует использовать для жёсткого диктования внимания; рекомендации должны направлять, а не лишать оператора возможности применить judgment.

## Метод и дизайн доказательств

Работа соединяет четыре вида анализа, которые нельзя смешивать при цитировании:

1. **User Study 1:** within-subject наблюдение за 16 участниками при team sizes 2, 4, 6 и 8; из этих данных оцениваются system performance, operator strategies и stochastic structures модели (PDF 4-5 / с. 387-388).
2. **Stochastic discrete-event simulation:** эмпирически оценённые `II`, `NI`, `ST` и observed `OAAS` используются для simulation и counterfactual policy evaluation через `U(M)` (PDF 5-6 / с. 388-389).
3. **Optimization and sensitivity analysis:** genetic algorithm ищет `OAAS*` в ограниченном policy space, после чего simulation проверяет чувствительность к model assumptions. Эти результаты являются predictions, а не observed effects (PDF 6-9 / с. 389-392).
4. **User Study 2:** within-subject эксперимент с 12 новыми участниками и фиксированными восемью роботами сравнивает Manual, Guided и Auto interfaces и проверяет predictive accuracy, performance, adherence, perception и workload (PDF 10-12 / с. 393-395).

Итак, quantitative evidence состоит из двух малых user studies и model-based simulations. Предсказанный эффект `OAAS*` нужно отличать от observed result второго эксперимента.

## Среда, оператор и роботы

### RESCU и performance objective

Эксперименты проведены в симуляторе Research Environment for Supervisory Control of Unmanned Vehicles (`RESCU`). Один оператор управляет несколькими simulated robots в search-and-rescue mission. За восемь минут система должна собрать как можно больше из 22 tokens и вывести роботов из здания до истечения времени (PDF 3 / с. 386).

Целевая функция:

\[
\mathrm{Score}=\mathrm{TokensCollected}-\mathrm{RobotsLost}.
\tag{1}
\]

Позднее анализируется обобщение

\[
\mathrm{Score}=c_T\,\mathrm{TokensCollected}-c_R\,\mathrm{RobotsLost},
\qquad c_T+c_R=1.
\tag{2}
\]

Это **fixed-horizon utility**, а не makespan. Не требуется обязательно собрать все 22 tokens; незавершённая работа по окончании восьми минут отражается через outcome, а не через время завершения фиксированного workload.

### Semi-autonomy и человеческие действия

Робот автономно следует к назначенной цели с помощью Dijkstra's algorithm и estimated path costs. Оператор взаимодействует только с одним роботом одновременно и может выполнять три вида действий (PDF 3-4 / с. 386-387):

1. `Goal assignment` - назначить destination;
2. `Replanning` - изменить destination или planned path;
3. `Visual search task` - помочь роботу «поднять» token через отдельную визуальную задачу.

Сбор token состоит из автономного перемещения к цели, обязательной визуальной операции человека и автономного выхода из здания, при необходимости с monitoring/replanning. Поэтому человеческое обслуживание может возникать неоднократно и в разных состояниях одного robot stream. Оно не сведено к одной verification phase после завершения автономной работы.

Интерфейс сообщает, когда робот не имеет задания, готов к visual task или рискует остаться в здании. Но alerts сами по себе не задают полный schedule: оператор должен выбрать, какой запрос обслужить следующим (PDF 4 / с. 387).

### Robot states для scheduling policy

Политика использует пять агрегированных состояний (PDF 6 / с. 389, Table I):

| State | Содержание |
|---|---|
| `A - Assignment` | робот снаружи здания ожидает назначения |
| `I - Idle` | робот простаивает внутри здания не у token |
| `P - Payload Ready` | робот готов «поднять» token |
| `R - Re-plan` | маршрут, вероятно, не кратчайший или полезно переназначить destination |
| `G - Good Progress` | робот эффективно движется к назначенной цели |

Операторская политика задаёт приоритет состояний, а затем выбирает робота из наиболее приоритетного доступного состояния. Это event/state-dependent service discipline, а не статический round-robin schedule.

## User Study 1: влияние числа роботов и наблюдаемая политика

Первое исследование использует within-subject design с **16 участниками**. Independent variable - team size с уровнями `P = 2, 4, 6, 8`; порядок условий counterbalanced. После обучения каждый участник прошёл три practice sessions и четыре test sessions. Outcomes - tokens collected, robots lost, score и наблюдаемая `OAAS` (PDF 4 / с. 387).

Результаты (PDF 4-5 / с. 387-388):

- среднее число collected tokens достигало пика примерно при шести роботах;
- robots lost монотонно росло с team size;
- средний score был максимален при четырёх-шести роботах;
- после шести роботов добавление исполнителей снижало effectiveness;
- в среднем операторы не справлялись эффективно более чем с шестью роботами, хотя отдельные участники могли;
- лишь три оператора при восьми доступных роботах сознательно использовали меньшее число, хотя такая политика могла улучшить score.

Fig. 2 показывает 95% confidence intervals, но текст не приводит point estimates, размеры интервалов, тест общей разницы или effect size. Поэтому из статьи нельзя извлечь точный «оптимальный `P=6`»: авторы говорят о максимуме effectiveness **между четырьмя и шестью** роботами, а вывод основан на средних в конкретном RESCU scenario.

Strategy profiles показывают механизм потери performance: при восьми роботах операторы отправляли в здание слишком много роботов, а в последнюю минуту резко увеличивали replanning, пытаясь вывести их без tokens. Проблема была не только в физическом числе роботов, но и в несвоевременном распределении capacity-1 attention (PDF 4-5 / с. 387-388).

## Математическая модель внимания

### Четыре stochastic structures

HMRS задаётся кортежем (PDF 5 / с. 388):

\[
M=(II,NI,ST,OAAS).
\]

Его компоненты:

1. `Interaction impact` `II(σ)` - stochastic process изменения состояния робота во время human-robot interaction, начиная с state `σ`; структура неявно задаёт длительность одного interaction.
2. `Neglect impact` `NI(σ)` - stochastic process изменения состояния робота без человеческого вмешательства после того, как последняя interaction закончилась в state `σ`.
3. `Switching time` `ST(σ)` - probability distribution времени, необходимого оператору, чтобы определить, какого робота обслужить, при system state `σ`.
4. `OAAS(σ)` - probability distribution over robots, задающее выбор обслуживаемого робота при state `σ`.

Discrete-event simulation оценивает effectiveness модели `U(M)`. `II`, `NI` и `ST` оцениваются из observational data конкретной HMRS. Следовательно, модель не рассматривает operator attention как абстрактную константу: service and switching dynamics зависят от state и эмпирически калибруются.

### Counterfactual policy evaluation

Пусть observed model имеет вид

\[
M^O=(II^O,NI^O,ST^O,OAAS^O).
\]

Для альтернативной политики `OAAS'` авторы строят counterfactual model

\[
M'=(II^O,NI^O,ST^O,OAAS')
\]

и используют `U(M')` как prediction system effectiveness (PDF 5-6 / с. 388-389).

Ключевое допущение состоит в invariance: смена `OAAS` не должна менять `II`, `NI` или `ST`. Именно это допущение позже нарушается в эксперименте. Новый selection mechanism меняет awareness и interaction time, то есть политика распределения внимания эндогенно изменяет стоимость обслуживания.

### Оптимизационная постановка

Для множества допустимых политик `Ω` авторы ищут

\[
OAAS^*\in\Omega:
\qquad
U(M^*)\ge U(M')-\varepsilon
\]

для всех `OAAS' ∈ Ω` и малого `ε >= 0` (PDF 6 / с. 389). Это approximate utility maximization, а не минимизация makespan.

Чтобы сделать поиск конечным, вводятся два ограничения:

1. восемь минут дискретизируются на восемь одноминутных периодов;
2. в каждом периоде политика является полным preference ordering over robot states и помещает весь приоритет на текущее наиболее предпочтительное состояние.

Состояние `G` всегда имеет самый низкий приоритет, поэтому для каждого периода остаётся `4! = 24` orderings, а полное пространство содержит

\[
|\Omega|=24^8
\]

политик. `OAAS*` оценивается genetic algorithm с population 35: две лучшие policies сохраняются, остальная популяция выбирается according to fitness и изменяется mutation (50%) или crossover (50%). Авторы сообщают, что alternate parameter values мало влияли на результат, но не дают convergence proof, число поколений, seed distribution или optimality gap (PDF 6 / с. 389).

### Вычисленная политика

Для восьми роботов найденная политика задаёт отдельный priority ordering на каждую минуту (PDF 6 / с. 389, Table II):

| Минута | Priority ordering |
|---:|---|
| 1 | `R > A > I > P > G` |
| 2 | `I > A > P > R > G` |
| 3 | `P > I > R > A > G` |
| 4 | `A > I > P > R > G` |
| 5 | `I > P > A > R > G` |
| 6 | `R > I > P > A > G` |
| 7 | `I > R > P > A > G` |
| 8 | `I > P > R > A > G` |

Модель предсказывала, что по сравнению с observed policy такая схема при восьми роботах даст более одного дополнительного token, менее половины прежнего числа lost robots и прирост score почти на три пункта за session (PDF 7 / с. 390). Это **model prediction**, а не подтверждённый experimental effect; второй user study не воспроизвёл ожидаемый рост score.

## Анализ model assumptions

Section IV варьирует отдельные допущения модели. Эти результаты получены simulation, а не независимым пользовательским экспериментом (PDF 7-9 / с. 390-392).

1. **Time discretization.** Анализ от 2 до 16 periods показал, что более восьми периодов не давали существенно лучшей predicted policy. Авторы также предупреждают о возможном overfitting при более мелкой сетке и sparse data. Численный effect size не приведён.
2. **Preference-order aggregation.** Лучший ordering последней минуты зависит от политики предыдущих минут, поскольку одинаковая агрегированная state label скрывает различное число роботов в состояниях. Следовательно, minute/state priority не является Markov-sufficient representation всех relevant histories.
3. **Switching time.** Halving or doubling switching time существенно меняло predicted effectiveness, но найденная `OAAS*` оставалась лучшей среди сравниваемых policies.
4. **Interaction time.** Существенное изменение visual-search time меняло не только effectiveness, но и то, какая политика была оптимальной. Значит, policy и service-time distribution нельзя безопасно оценивать независимо.
5. **Objective weights.** При варьировании `c_T:c_R` модель не нашла политики лучше исходной `OAAS*`, вычисленной при равных weights. Это robustness result только для данного scenario и ограниченного `Ω`.

Для M4 наиболее важны пункты 3-4. Switching/service cost materially влияет на outcome, а изменение режима управления может менять саму длительность человеческого обслуживания. Поэтому `gamma(P)` нельзя считать внешним коэффициентом, зависящим только от числа потоков, без проверки зависимости от policy, interface и state composition.

## Политики и интерфейс распределения внимания

Авторы сравнивают три robot-selection mechanisms (PDF 9-10 / с. 392-393):

| Mode | Кто выбирает следующий robot stream | Свобода оператора |
|---|---|---|
| Manual | оператор | полный ручной выбор; интерфейс показывает alerts |
| Guided | модель рекомендует робота через highlight | оператор может принять или проигнорировать рекомендацию |
| Auto | оператор нажимает `Next`, система выбирает робот по `OAAS*` | прямой выбор запрещён, но recommendation для робота можно временно выключить |

`Guided` реализует management-by-consent: model schedule служит decision support, а оператор сохраняет authority. `Auto` должен был снизить scheduling effort и повысить adherence, но мог ухудшить situation awareness и увеличить interaction time для неожиданно выбранного робота.

Эти modes являются полезным формальным аналогом `r`, однако семантика отличается. В M0-M4 `r` характеризует способ выполнения software task агентом и человеком. У Crandall et al. robots выполняют ту же mission, а mode прежде всего меняет authority over selection of the next robot.

## User Study 2: проверка policy implementation

### Дизайн и выборка

Второй эксперимент - single-factor within-subject study при фиксированных восьми роботах. Independent variable - interface mode (`Manual`, `Guided`, `Auto`), порядок counterbalanced. Outcomes - score, tokens collected, robots lost, observed `OAAS`, perceived workload и qualitative assessment recommendations (PDF 10 / с. 393).

Выборка:

- **12** undergraduate students, graduate students и postdoctoral associates;
- 6 женщин и 6 мужчин;
- возраст 19-32 года, среднее 23.2;
- никто ранее не работал с RESCU.

Каждый участник прошёл общее обучение и practice mission, затем для каждого mode - отдельное знакомство, practice mission, test mission и subjective questionnaire.

### Predictive accuracy и endogeneity

Между исследованиями изменили компьютер: более чувствительный mouse wheel сократил среднее visual-search time с 20 до 15 s. Запись статьи `(75%)` означает, что новое время составило 75% прежнего, а не снижение на 75%. Это небольшое техническое изменение существенно повысило performance и сделало исходный prediction unreliable (PDF 10 / с. 393).

После обновления `II` по новому search time модель всё равно существенно overpredicted collected tokens. Predicted robots lost было менее половины observed value, хотя попадало в reported 95% confidence interval. Авторы связали остаточную ошибку с тем, что в Auto mode обслуживание робота занимало в среднем на 1.6 s больше, чем в данных первого исследования: принудительно выбранный робот требовал дополнительного восстановления situation awareness (PDF 10-11 / с. 393-394).

После повторной корректировки `II` по observed Auto interaction times predictions tokens and losses оказались внутри 95% confidence intervals. Это условная validation: модель предсказывает приемлемо, когда получает корректные interaction dynamics, но policy intervention сама меняет эти dynamics. Следовательно, результат не подтверждает transportability исходной модели в новую interface configuration.

### System effectiveness

Manual и Guided имели более высокий mean score, чем Auto, но разница между тремя modes не была статистически значимой:

\[
F(2,33)=0.50,\qquad p=0.609.
\]

Auto interaction time было примерно на 1.6 s больше Manual и на 1.0 s больше Guided. Exact group means score, confidence intervals различий и effect size для performance в тексте не приведены; значения показаны только графически. Поэтому источник не доказывает equivalence modes и не даёт точной оценки потери performance от automation (PDF 11 / с. 394).

### Adherence

Средняя correspondence выбора оператора с `OAAS*` составляла (PDF 11-12 / с. 394-395):

- random behavior - около 30%;
- Manual - около 50%;
- Guided - около 60%;
- Auto - более 95%, поскольку recommendations можно было выключать.

После четвёртой минуты Guided в основном повторял temporal pattern Manual, но был сдвинут вверх примерно на 10-20 percentage points. Recommendations влияли на выбор, однако не заменяли operator judgment.

### Perception и workload

- 75% участников считали recommendations неидеальными или неважными;
- 3 из 12 (25%) выключали отдельные recommendations в Auto; некоторые другие сообщили, что сделали бы это, если бы помнили способ;
- 8 из 12 (67%) поставили Guided на первое место по preference;
- 8 из 12 (67%) меньше всего понравился Auto;
- субъективный workload различался между modes: proportional-odds model `χ²(2)=6.98`, `p=0.0305`;
- odds higher workload были ниже для Auto, чем для Guided: `χ²(1)=9.84`, `p=0.002`;
- odds higher workload были ниже для Auto, чем для Manual: `χ²(1)=5.46`, `p=0.020` (PDF 12 / с. 395).

Auto тем самым снижал perceived workload, но вызывал frustration и не давал обнаруженного выигрыша score. Источник показывает, что human-resource scheduling имеет как temporal, так и authority/acceptance consequences; одна метрика занятости не определяет качество режима.

## Точность результатов и неопределённость

1. **Малые выборки:** 16 участников в Study 1 и 12 в Study 2. Generalization на профессиональных операторов и длительную эксплуатацию не проверена.
2. **Study 1:** Fig. 2 содержит 95% confidence intervals, но нет точных tabulated means, overall test, pairwise tests или effect sizes для team size. Формулировка «4-6 robots» точнее, чем точный optimum `P=6`.
3. **Study 2 performance:** `p=0.609` означает отсутствие обнаруженной разницы, а не equivalence Manual, Guided и Auto. Confidence interval контраста и equivalence margin отсутствуют.
4. **Workload:** приведены chi-square tests и `p`, но нет odds ratios и confidence intervals; magnitude effect не восстанавливается.
5. **Несколько outcomes:** анализируются score, tokens, losses, adherence, interaction time, preference и workload. Коррекция multiple comparisons не описана.
6. **Model selection:** `OAAS*` оптимальна лишь относительно restricted policy class `Ω`, estimated stochastic structures и genetic search. Глобальная optimality для всех history-dependent policies не доказана.
7. **Model endogeneity:** интерфейс изменил interaction time, а технический апгрейд - visual-search time. Даже малое изменение среды нарушило transportability.
8. **Single scenario:** оба исследования используют один восьмиминутный RESCU mission и simulated robots. Другие horizons, mission objectives и robot capabilities не проверены.
9. **No software evidence:** в выборках нет software developers, code review, generated artifacts или LLM agents.

## Mapping ко всем полям M0-M4

Статусы ниже означают: **direct** - конструкция непосредственно присутствует; **partial/analogy** - близка формальная роль, но отличается семантика или операционализация; **absent** - источник не содержит параметр.

| Поле M0-M4 | Статус | Соответствие у Crandall et al. | Точная граница |
|---|---|---|---|
| `X`, `Z_i`, `Z` | **absent** | Есть 22 tokens, robot states и action types | Нет baseline unit effort, нормированной сложности software task или суммы `Z_i X` |
| `k_i^(r)` / `k` | **absent** | Interface mode и policy меняют interaction time и outcome | Нет no-AI baseline и отношения `T_i^ai/(Z_i X)`; utility не является task-duration ratio |
| режим `r` | **partial direct analogue** | Manual, Guided, Auto задают authority over attention allocation | Это режим выбора следующего робота, а не interactive/delegated/autonomous execution software task; смена mode эндогенно меняет `II` |
| `P` | **direct** | Robot team size `2,4,6,8` в Study 1; `8` в Study 2 | `P` означает число доступных simulated robots, но effective utilization выбирает оператор; это не число LLM agents или непрерывный effective parallelism |
| `W = X sum Z_i k_i` | **absent** | Mission содержит до 22 token opportunities | Fixed workload не требуется завершить; objective оценивается в фиксированном horizon, поэтому `W/P` не является capacity bound статьи |
| неделимость / `M_N` | **absent** | Interactions являются отдельными service episodes | Нет набора nonpreemptive jobs с заданными processing times или longest-job lower bound |
| DAG / `L` | **absent** | Есть procedural sequence move-pickup-exit и dynamic state transitions | Нет заданного software-task precedence DAG, weighted critical path или makespan bound `L` |
| `C(P)` | **absent** | Performance падает после 4-6 robots | Падение связано как минимум с attention policy и losses; agent-agent integration multiplier не идентифицирован, robots не merge shared code |
| `h_i^(r)` / `h` | **strong structural analogue, not measured as share** | `II(σ)` включает длительность human-robot interaction; operator выполняет assignment, replanning и visual task | Нет normalizing baseline и разложения `k=a+h`; state-dependent interaction time не является коэффициентом доли software task |
| `H = X sum Z_i h_i` | **capacity mechanism direct, aggregate absent** | Один operator обслуживает только одного robot at a time; simulation размещает последовательные interactions | Статья не определяет сумму `H`, не выводит workload bound `T>=H` и не сопоставляет её с no-AI makespan |
| `gamma(P)` | **closest structural analogue: `ST(σ)`, but not direct** | `ST(σ)` - distribution switching/selection time; interaction time выросло при Auto из-за awareness recovery | `ST` зависит от full state и interface, не задано как monotone function только `P`; нет multiplicative `gamma(P)H`, линейной формы или оценки `δ` |
| makespan | **absent** | Восьмиминутный mission horizon фиксирован | Оптимизируется score внутри horizon, а не completion time фиксированного набора задач |
| M0 | **absent** | - | Нет идеально делимой fixed work и формулы `W/P` |
| M1 | **absent** | - | Нет indivisible-job scheduling bound |
| M2 | **absent** | Dynamic state transitions не равны exogenous DAG | Нет `L` или precedence-constrained makespan |
| M3 | **absent** | - | Нет `C(P)` и shared-artifact integration overhead |
| M4 | **closest analogue, but different objective** | Capacity-1 operator, explicit stochastic interaction and switching processes, state-dependent service policy | Источник детальнее агрегата `H` в dynamic scheduling, но не выводит `max{C(P)W/P,L,gamma(P)H}` и не сравнивает с no-AI baseline |

## Соответствие `h`, `H` и `gamma(P)`

### Что соответствует `h`

`II(σ)` и фактические human-robot interactions показывают, какие интервалы должны считаться человеческой работой: назначение, replanning, visual inspection, выбор следующего потока и восстановление awareness. Для software-agent модели это поддерживает включение в `h_i^(r)` не только финальной проверки, но и постановки, промежуточного вмешательства, диагностики состояния и направления исправлений.

Однако `II` описывает stochastic transition process и duration конкретного interaction, а `h_i` - нормированную суммарную занятость человека по software task. Из `II` нельзя численно получить `h_i` без нового протокола сопоставления task boundaries, baseline `Z_i X` и всех interaction episodes.

### Что соответствует `H`

Ограничение «один operator взаимодействует с одним robot at a time» непосредственно реализует capacity 1. В этом смысле источник сильнее чистой aggregate lower bound: simulation строит последовательность конкретных service episodes и учитывает, как их порядок меняет states и utility.

Но авторы не агрегируют durations в `H` и не доказывают `makespan >= H`, поскольку makespan не является objective. Для M4 работа поддерживает **resource-feasibility requirement**, а не конкретную сумму или потолок speedup.

### Что соответствует `gamma(P)`

Ближайший объект - `ST(σ)`, distribution времени на выбор следующего робота. Дополнительный механизм проявился в Auto: отсутствие собственного выбора ухудшило situation awareness и увеличило subsequent interaction time. Это похоже на context reconstruction cost, который M4 пытается агрегировать через `gamma(P)`.

Семантические различия обязательны:

1. `ST` зависит от full system state `σ`, а не только от `P`;
2. `ST` является additive stochastic interval перед servicing, а `gamma(P)` - multiplicative inflation total human time;
3. часть switching cost может проявляться не в `ST`, а внутри `II` как более длинное обслуживание;
4. Study 1 варьирует `P`, но не оценивает отдельную функцию `ST(P)` и не идентифицирует `δ`;
5. Guided/Auto показывают policy dependence: одинаковое `P=8` даёт разные interaction dynamics.

Поэтому Crandall et al. поддерживают наличие state- and policy-dependent switching overhead, но не рабочую форму `gamma(P)=1+δ(P-1)`.

## Intervention windows и resource scheduling

Термин `intervention window` не является центральной формальной переменной статьи. Ближайшие конструкции:

- event/state-triggered human-robot interactions;
- `II(σ)`, неявно задающее их duration;
- `NI(σ)`, описывающее автономное развитие потока во время neglect;
- `ST(σ)`, задающее стоимость выбора следующего потока;
- `OAAS(σ)`, определяющее service discipline capacity-1 operator;
- minute-specific priority schedule `OAAS*`.

Это важный прецедент для M4: допустимое расписание не определяется одной суммой `H`; нужно решить, **когда** и **какой** поток получает ограниченный human resource. Но у Crandall et al. окна возникают динамически из robot state и mission time. В software verification окна часто привязаны к precedence: specification до agent run, review после generation/test, затем возможный rework loop. Источник не моделирует такие fixed precedence windows и не даёт алгоритм их размещения в software DAG.

## Что источник поддерживает

1. Один человек, обслуживающий несколько semi-autonomous executors, является capacity-constrained scheduling resource: порядок человеческих interactions меняет system outcome (PDF 4-6 / с. 387-389).
2. Attention allocation следует моделировать как policy over system states, а не только как среднюю долю времени. Одинаковый total attention при другом порядке может дать другой score.
3. Human servicing включает interaction duration, autonomous neglect dynamics и switching/selection time; эти механизмы полезно разделять (PDF 5 / с. 388).
4. Оптимизация policy требует явного objective. Изменение utility weights, state aggregation или interaction dynamics потенциально меняет рекомендуемое schedule (PDF 7-9 / с. 390-392).
5. Service time является эндогенным по отношению к interface and policy. Auto selection увеличило время восстановления awareness и нарушило counterfactual invariance (PDF 10-11 / с. 393-394).
6. Большее число executors не гарантирует большую effectiveness. В Study 1 средний score достигал максимума при 4-6 robots, а дальнейший рост team size ухудшал результат при наблюдаемых policies (PDF 4 / с. 387).
7. Guidance может быть устойчивее жёсткого automation: Guided сохранял judgment, был наиболее предпочитаемым режимом и влиял на selection without fully dictating it (PDF 10-13 / с. 393-396).
8. Модель attention allocation полезна как decision support даже при недостаточной fidelity для точного dictation; authors recommend “good enough” policies и operator flexibility (PDF 13 / с. 396).

## Что источник не позволяет утверждать

1. Что optimum для software-agent cell равен `P=4`, `P=6` или любому числу из RESCU.
2. Что наблюдаемое снижение score после шести robots идентифицирует `C(P)` или `gamma(P)`.
3. Что можно вычислить численные `h_i`, `H`, `gamma(P)` или `δ` из interaction times RESCU.
4. Что `ST(σ)` эквивалентно multiplicative switching penalty `gamma(P)H`.
5. Что найденная `OAAS*` является глобально оптимальной: policy class ограничен `24^8`, а search генетический.
6. Что Auto, Guided и Manual одинаковы по performance: `p=0.609` не является equivalence test.
7. Что Auto улучшает objective: средний score не был выше, несмотря на меньший perceived workload.
8. Что model prediction «почти +3 score» подтверждён экспериментально; исходное предсказание нарушилось из-за изменившихся interaction dynamics.
9. Что фиксированный mission horizon и utility score эквивалентны fixed-workload makespan.
10. Что robot attention allocation валидирует verification workflow кодовых ИИ-агентов, shared repository, merge conflicts, test adequacy или rework.
11. Что источник поддерживает `Z`, `k`, `W`, `L`, `C(P)` или speedup относительно последовательной разработки без ИИ.
12. Что один aggregate `H` достаточен для расписания. Source, напротив, показывает зависимость outcome от temporal order, state и policy.

## Ключевые отличия от software-agent verification

| Измерение | Crandall et al. | M0-M4 для кодовых агентов |
|---|---|---|
| Objective | максимизация utility за фиксированные 8 min | минимизация makespan фиксированного workload |
| Незавершённая работа | допустима и отражается в tokens/lost robots | все заданные tasks должны завершиться |
| Автономный исполнитель | simulated mobile robot с navigation state | coding agent, создающий и изменяющий software artifact |
| Человеческая работа | assignment, monitoring, replanning, visual task, robot selection | specification, reading, verification, tests interpretation, correction direction, acceptance |
| Состояние | telemetry-like robot state и mission clock | состояние codebase, tests, requirements, latent defects и epistemic uncertainty |
| Общий артефакт | shared-code integration не моделируется | параллельные изменения создают interfaces, merge conflicts и rework через `C(P)` |
| Зависимости | endogenous stochastic transitions | exogenous/updated task DAG и critical path `L` |
| Scheduling | state-dependent online policy over next robot | fixed-workload scheduling с agent slots, human windows и precedence |
| Switching | additive distributions `ST(σ)` и mode-dependent interaction time | aggregate multiplier `gamma(P)` при `H`, если используется упрощённая форма |
| Baseline | нет no-automation completion-time baseline | `T_h=X sum Z_i` одного разработчика без ИИ |
| Validation | два малых RESCU user studies | требует coding-specific traces и двухканального хронометража |

Самое существенное различие связано с verification. В RESCU оператор часто реагирует на observable operational state и корректирует траекторию. В software development результат агента может выглядеть завершённым, но содержать latent semantic defects; проверка изменяет не только schedule, но и оценку remaining work, а обнаружение ошибки создаёт новые rework tasks и зависимости. Поэтому human intervention в M4 нельзя свести к robot-selection policy без отдельной модели correctness evidence и feedback loops.

## Отличие от M0-M4 и корректное позиционирование

Crandall et al. являются более близким источником для attention scheduling, чем законы общего вычислительного масштабирования. Они уже показывают один human controller, несколько автономно развивающихся streams, non-overlapping service, stochastic switching time, online policy и diminishing/negative returns от роста числа robots при неудачном attention allocation.

Следовательно, M4 нельзя позиционировать как первое рассмотрение одного человека в роли общего последовательного ресурса для нескольких автономных исполнителей. Корректный gap уже:

- Crandall et al. оптимизируют dynamic attention policy для fixed-horizon robot mission;
- M0-M4 связывает AI-specific one-stream duration `k_i^(r)Z_iX`, fixed workload, DAG/`L`, agent capacity `P`, shared-artifact overhead `C(P)` и human workload `h_i`, `H`, `gamma(P)` с no-AI baseline и makespan;
- источник Crandall указывает, что aggregate M4 следует дополнять state/policy dependence и явным schedule intervention windows, а `gamma(P)` нуждается в empirical calibration beyond `P` alone.

Новизну статьи следует связывать с software-specific synthesis и operational calibration, а не с самим primitive «один оператор - много автономных систем» или с идеей scheduling operator attention.

## Проверенные claims для Related Work

1. Crandall et al. моделируют human-multiple-robot system как stochastic discrete-event tuple `M=(II,NI,ST,OAAS)`, где interaction impact, neglect impact, switching-time distribution и attention-allocation policy совместно определяют expected system utility (PDF 5 / с. 388).
2. Для восьмиминутной RESCU mission policy была ограничена восемью minute-specific preference orderings over five robot states; при fixed lowest priority для Good Progress пространство содержало `24^8` policies, а `OAAS*` оценивалась genetic algorithm (PDF 6 / с. 389).
3. В первом within-subject study с 16 участниками и team sizes 2, 4, 6 и 8 средний score был максимален при 4-6 robots и снижался при дальнейшем росте; Fig. 2 показывает 95% CIs, но точный universal optimum из исследования не следует (PDF 4 / с. 387).
4. Во втором within-subject study с 12 участниками при восьми роботах Manual, Guided и Auto не различались статистически по score (`F(2,33)=0.50`, `p=0.609`), хотя Auto повышал adherence и снижал subjective workload (PDF 11-12 / с. 394-395).
5. Auto selection увеличил human-robot interaction time примерно на 1.6 s относительно Manual и нарушил допущение, что смена attention policy не меняет interaction dynamics; после корректировки `II` predictions вернулись внутрь reported 95% CIs (PDF 10-11 / с. 393-394).
6. Guided mode сохранял operator choice, был предпочитаем 8 из 12 участников и повышал correspondence с recommendations примерно с 50% в Manual до 60%, тогда как Auto давал более 95% correspondence (PDF 11-12 / с. 394-395).
7. Авторы заключают, что predictive optimization model недостаточно robust для dictation, но полезна для guidance и поиска “good enough” attention policies при сохранении human judgment (PDF 12-13 / с. 395-396).

## Короткий вариант встраивания в Related Work

> Crandall et al. (2011) рассматривают близкую topology supervisory control: один оператор распределяет capacity-1 attention между несколькими semi-autonomous robots. Их stochastic discrete-event model разделяет interaction impact, autonomous neglect dynamics, state-dependent switching time и operator attention allocation scheme, а policy определяет, какой robot stream обслуживается следующим. В исследовании RESCU средний system score достигал максимума при четырёх-шести роботах, однако жёсткая автоматизация вычисленной policy во втором эксперименте не улучшила score (`F(2,33)=0.50`, `p=0.609`) и увеличила interaction time из-за восстановления situation awareness; guided recommendations участники предпочитали чаще. Для M4 это прямой структурный прецедент явного расписания единственного human resource и важное предупреждение об эндогенности switching/service cost. Перенос ограничен: работа максимизирует utility в фиксированном восьмиминутном горизонте, не моделирует fixed-workload makespan, software verification, DAG/critical path или shared-code integration и не оценивает численные `h`, `H` либо `gamma(P)`.

## Возможная вставка в раздел о границе модели

> Агрегированная граница `T_ai >= gamma(P)H` не заменяет online scheduling человеческих интервенций. В human-multiple-robot system Crandall et al. длительность interaction, автономная динамика во время neglect, switching time и policy выбора следующего потока моделируются раздельно. Более того, смена interface policy сама увеличила interaction time, нарушив invariance counterfactual prediction. Поэтому в применении к кодовым агентам `gamma(P)` следует рассматривать как калибруемое сокращение state-, policy- и mode-dependent процесса, а точный M4 schedule должен явно размещать specification, verification и correction windows с учётом precedence и возможного rework.

## Таблица опорных страниц

| PDF | Журн. страница | Раздел / объект | Опорное содержание |
|---:|---:|---|---|
| 1 | - | MIT repository cover | полная ссылка, DOI, persistent URL, final published version |
| 2 | 385 | Abstract; Introduction | one operator, multiple semiautomated tasks; objective attention allocation; guide versus dictate; publication chronology |
| 3 | 386 | RESCU test bed | 22 tokens, 8-min horizon, score formula, autonomous navigation, visual task, interface |
| 4 | 387 | Study 1 setup/results | 16 participants; `P=2,4,6,8`; counterbalancing; 95% CIs; peak tokens near 6; score highest at 4-6 |
| 5 | 388 | Strategy analysis; Section III | late replanning under overload; tuple `M=(II,NI,ST,OAAS)`; meanings of four structures; `U(M)` |
| 6 | 389 | Counterfactual model; `OAAS*` | invariance assumption; epsilon-optimal policy; eight periods; five states; `24^8`; GA population 35; Table II policy |
| 7 | 390 | Predicted effect; Section IV | prediction >1 extra token, <half losses, nearly +3 score; discretization analysis |
| 8 | 391 | Sensitivity analysis | history dependence of preference ordering; halved/doubled switching time; visual-search-time sensitivity |
| 9 | 392 | Objective; Manual/Auto | weighted score; Auto mechanism; expected benefits and situation-awareness risks |
| 10 | 393 | Guided; Study 2 setup | management-by-consent; 12 participants; demographics; within-subject modes; 20-to-15-s system change |
| 11 | 394 | Study 2 results | adjusted predictions and 95% CIs; +1.6-s Auto interaction; `F(2,33)=0.50`, `p=0.609`; adherence rates |
| 12 | 395 | Perception; workload; conclusion | 75% criticism; preferences 8/12; workload chi-square tests; key conclusions |
| 13 | 396 | Lessons learned | model brittleness; negative effects of dictation; guidance, flexibility and “good enough” policies |

## Итоговая оценка источника

Crandall et al. (2011) - сильный близкий источник для operator attention allocation, resource scheduling и diminishing returns в topology «один человек - несколько semi-autonomous executors». Его наиболее ценный вклад для M0-M4 не в численном optimum robots, а в более детальной процессной декомпозиции human bottleneck: interaction, neglect, switching и scheduling policy влияют совместно, а стоимость обслуживания меняется при смене interface authority.

Источник одновременно ограничивает допустимые claims. Он не является моделью fixed-workload software project и не валидирует `B_4`, `h`, `H` или линейную `gamma(P)`. Корректное использование - сослаться на него как на предшественника capacity-1 attention scheduling, затем объяснить, что M0-M4 переносит эту проблему в другую objective and task semantics: makespan заданного software workload с task-specific AI effect, DAG, shared-artifact coordination и human verification. Практический вывод для развития M4 состоит в том, что aggregate lower bound следует дополнять явными intervention windows, а `gamma(P)` калибровать по состоянию, режиму и policy, не только по числу агентов.
