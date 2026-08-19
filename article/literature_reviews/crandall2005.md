# Crandall et al. (2005): human-robot multitasking, neglect tolerance и fan-out

## Назначение и границы обзора

Этот документ разбирает один источник применительно к модели fixed-workload makespan ячейки «один разработчик - `P` кодовых ИИ-агентов». Основной фокус: управление одним оператором несколькими роботами, распределение внимания, interaction/neglect time, fan-out, feasibility гетерогенной команды, прогноз team performance, workload-performance tradeoff и экспериментальная проверка предложенных схем.

Источник является одним из наиболее близких эмпирико-формальных предшественников уровня M4. Он прямо моделирует capacity-1 внимание одного оператора и интервалы, в которые независимые автономные исполнители могут обходиться без него. Однако его центральная постановка является циклической и performance-threshold-based: робот непрерывно действует, его performance меняется во время neglect и interaction. M0-M4, напротив, рассматривает конечный фиксированный workload, task completion, DAG и makespan. Поэтому Crandall et al. поддерживают механизм ограниченного внимания и конечного fan-out, но не доказывают формулу M4 и не дают калибровки для кодовых агентов.

Ссылки ниже имеют вид «PDF-страница / печатная страница». PDF 1 является обложкой BYU ScholarsArchive; журнальная статья занимает PDF 2-13, соответствующие печатным страницам 438-449.

## Библиография, версия и статус

**Проверенная журнальная запись:** Jacob W. Crandall, Michael A. Goodrich, Dan R. Olsen, Jr., and Curtis W. Nielsen. “Validating Human-Robot Interaction Schemes in Multitasking Environments.” *IEEE Transactions on Systems, Man, and Cybernetics - Part A: Systems and Humans* 35, no. 4 (July 2005): 438-449. DOI: [10.1109/TSMCA.2005.850587](https://doi.org/10.1109/TSMCA.2005.850587). ISSN `1083-4427`.

- Авторы, заголовок, журнал, том, выпуск, месяц, год, страницы и DOI совпадают в журнальной вёрстке и Crossref.
- Crossref классифицирует источник как `journal-article`, издатель - IEEE.
- На первой журнальной странице указано: manuscript received 31 July 2004, revised 14 March 2005, recommended by the Guest Editors (PDF 2 / печ. 438).
- Репозиторная обложка называет документ peer-reviewed article и связывает его с записью BYU Faculty Publications 363 (PDF 1).
- **Коррекция проектных заметок:** правильный диапазон страниц - **438-449**. Диапазон `528-542`, указанный в `tmp_docs/simple_model_full_source_notes.md`, к этой статье не относится.
- Локальный файл: `crandall2005.pdf`.
- SHA-256: `5c2c8db0538fa3dee4634992252c5e920af4b513d630f7f3d566c43d10f2f7e2`.
- Локальная копия содержит 13 PDF-страниц: репозиторную обложку и 12 страниц журнальной статьи. Метаданные PDF дают заголовок статьи и 13 страниц.
- Дата проверки: 2026-08-04.

**Тип доказательства:** статья объединяет аналитические определения, secondary-task methodology, simulation user study, небольшой real-robot study и between-subjects comparison предсказанной и наблюдаемой производительности трёхроботных конфигураций. Это не чистая теоретическая работа и не один единый RCT с заранее заданным primary endpoint.

## Исследовательский вопрос и заявленный вклад

Авторы не формулируют один нумерованный RQ. Их цель состоит в проверке того, могут ли оценки neglect time (`NT`) и interaction time (`IT`) использоваться для трёх задач проектирования (PDF 2 / печ. 438):

1. определить максимальное число роботов, которыми способен управлять один человек;
2. установить feasibility конкретной конфигурации гетерогенной multirobot team;
3. предсказать performance команды при предположениях независимости.

Дополнительный методический вопрос: можно ли получить `NT` и `IT` из эксперимента с одним роботом и secondary task, а затем перенести эти оценки на one-operator-many-robots configuration. Авторы проверяют метод в симуляции, демонстрируют его на реальном роботе и сравнивают prediction с observed completion time для команд из трёх роботов (PDF 2, 4, 6-11 / печ. 438, 440, 442-447).

## Формальная схема источника

### Interaction scheme

Авторы разделяют robot autonomy и human interface и определяют interaction scheme как упорядоченную пару (PDF 2 / печ. 438):

```text
interaction scheme = (autonomy, interface).
```

Autonomy определяет, как робот действует без человека; interface определяет, как оператор воспринимает состояние робота и передаёт инструкции. Схема является ближайшим аналогом режима `r`, поскольку изменение autonomy/interface меняет и автономный интервал, и требуемое человеческое обслуживание. Но `r` в M0-M4 относится к software workflow и задаёт task-specific duration factor `k_i^(r)`, которого в Crandall et al. нет.

### Neglect time и interaction time

- **Neglect time (`NT`)** - ожидаемое время, в течение которого робот можно игнорировать до падения performance ниже выбранного threshold (PDF 2 / печ. 438).
- **Interaction time (`IT`)** - ожидаемое время взаимодействия, необходимое, чтобы вернуть робота к peak performance после возобновления обслуживания (PDF 2 / печ. 438).
- **Neglect tolerance** определяется парой `(NT, IT)`, а не одним временем: оба интервала нужны для multitasking feasibility (PDF 6 / печ. 442).

`NT` и `IT` не являются постоянными свойствами робота. Они зависят от task, interaction scheme, world complexity и выбранного performance threshold. Более высокий требуемый average performance обычно означает более короткий neglect interval и более высокую долю внимания оператора (PDF 4-6 / печ. 440-442).

### Fan-out для однородных независимых роботов

Для homogeneous independent robots авторы задают (PDF 4 / печ. 440):

```math
Fanout = \frac{NT}{IT} + 1 = \frac{NT+IT}{IT}.
```

Отношение `NT/IT` показывает, сколько других роботов оператор успевает обслужить, пока исходный робот автономно работает; `+1` возвращает исходного робота. Формула задаёт upper bound при предположении одинаковых роботов, независимых задач и повторяющегося цикла neglect/interaction. Статья не вводит округление как отдельную формулу, хотя фактическое число роботов целое.

### Feasibility гетерогенной команды

Для робота `i` вводится

```math
N_i=(NT_i,IT_i),
```

а команда из `M` роботов задаётся как `T={N_i:i=1,...,M}`. Команда объявляется feasible тогда и только тогда, когда neglect interval каждого робота вмещает обслуживание всех остальных (Equation 1, PDF 4 / печ. 440):

```math
T\text{ feasible}\quad\Longleftrightarrow\quad
\forall i:\ NT_i \ge \sum_{j\ne i} IT_j.
```

Это явное capacity-1 ограничение человеческого ресурса. Оно не включает DAG, release times, agent-agent conflicts, output integration или sequence-dependent switching cost.

### Neglect-impact и interface-efficiency curves

Авторы строят две task- и complexity-dependent кривые (PDF 4-6 / печ. 440-442):

- **neglect-impact curve** описывает изменение expected robot performance во время `time-off-task`;
- **interface-efficiency curve** описывает восстановление performance во время `time-on-task` после neglect.

Performance threshold пересекает эти кривые и тем самым дискретизирует interaction и neglect в кванты `IT` и `NT`. На interface-efficiency curve предусмотрен начальный switching interval: после возвращения внимания оператору нужно восстановить awareness, а performance робота в это время может продолжать падать (PDF 5 / печ. 441, Fig. 4).

Это более содержательная фазовая модель, чем один агрегат `H`: она указывает, когда человеческое внимание требуется. Одновременно она уже M4, поскольку описывает повторяющийся цикл одного непрерывного robot task, а не произвольные входные, промежуточные и выходные окна конечной coding task.

### Instantaneous performance metric

В simulation study робот движется к цели со скоростью до 30 in/s. Для малого интервала `t_e` источник определяет instantaneous capacity, work и performance (Equations 2-4, PDF 7 / печ. 443):

```math
ic=30t_e,
```

```math
iw_i=\frac{d_i-d_{i-t_e}}{t_e},
```

```math
ip_i=\frac{iw_i}{ic}
=\frac{d_i-d_{i-t_e}}{30t_e^2},
```

где `d_i` - shortest-path distance до цели в момент `i`, вычисленная алгоритмом Дейкстры по топологической карте. Значение `ip_i` усекается до диапазона `[-1,1]`. Авторы прямо предупреждают, что сумма instantaneous values не обязана совпадать с performance за весь интервал, но считают метрику близким приближением (PDF 7 / печ. 443).

Эта метрика специфична для навигации и не соответствует ни `k`, ни makespan coding workload.

### Прогноз team performance

Для каждого робота выбирается interaction scheme `pi_i`; вектор схем равен

```math
pi=(pi_1,pi_2,...,pi_M),
```

а вектор neglect characteristics -

```math
N(pi)=(N_1(pi_1),N_2(pi_2),...,N_M(pi_M)).
```

При предположении независимости expected average team performance определяется как среднее индивидуальных temporal-average performances (Equation 5, PDF 9 / печ. 445):

```math
J(pi)=\frac{1}{M}\sum_{i=1}^{M}\bar{J}_i(pi_i).
```

Design problem состоит в выборе `pi`, performance thresholds и соответствующих `(NT,IT)`, максимизирующих `J(pi)` при feasibility `N(pi)` по Equation 1 (PDF 9-10 / печ. 445-446).

Это не makespan optimization: objective - средняя robot performance, хотя validation experiment дополнительно измеряет completion time фиксированных девяти целей.

### Robot attention demand и performance-workload tradeoff

Robot attention demand определяется как доля interaction cycle, занятая человеком (PDF 11 / печ. 447):

```math
RAD=\frac{IT}{IT+NT}.
```

Авторы интерпретируют `RAD` как оценку доли времени человека, выделенной одному роботу, с оговоркой: она является workload proxy лишь постольку, поскольку time commitment действительно предсказывает workload.

Из двух формул статьи алгебраически следует

```math
Fanout=\frac{1}{RAD}.
```

Это следствие определений, а не отдельный эмпирический закон. Для `M` однородных роботов условие `M <= Fanout` эквивалентно aggregate attention utilization `M*RAD <= 1`. Именно эта связь наиболее близка к M4, но она относится к stationary repeated cycles и не равна fixed-workload bound `T_ai >= gamma(P)H`.

## Метод и выборки

### Study 1: simulated robots и три interaction schemes

**Цель:** оценить neglect-impact/interface-efficiency curves и показать, как из них получить `NT`, `IT`, fan-out и workload-performance tradeoff (PDF 6-8 / печ. 442-444).

**Interaction schemes:**

1. `Teleop`: shared teleoperation, оператор управляет joystick, робот избегает препятствий;
2. `P2P`: point-to-point commands на следующем intersection/decision point плюс отдельные low-level commands;
3. `Scripted`: последовательность waypoints, по которой робот автономно движется с obstacle avoidance.

**Участники и объём:** 40 volunteer undergraduate computer science and engineering students без опыта управления этими роботами; 120 десятиминутных test sessions. Каждый участник прошёл три sessions и использовал в сумме две interaction schemes. Sessions распределены неравномерно: 15 `Teleop`, 48 `P2P`, 57 `Scripted` (PDF 7 / печ. 443).

**Tasks:** secondary task был либо управлением вторым роботом, либо решением двузначных arithmetic problems. После завершения human service роботу назначался случайный neglect interval; до его истечения оператор не мог вернуться к роботу. Если оба робота находились в neglect, оператор решал арифметическую задачу (PDF 7 / печ. 443).

**Worlds:** 21 simulated world с разными branching factor и clutter; один training world и 20 test worlds. Complexity оценивалась в `[0,1]` по sonar signatures, directional entropy, изменениям sonar values и velocity; подробности estimator вынесены в thesis [53], а не приведены полностью в статье (PDF 7 / печ. 443).

**Neglect schedules:** `Scripted` - 10, 20, 30, 40, 50, 60 s; `P2P` - 5, 10, 15, 20, 25, 30 s; `Teleop` - 10 s (footnote 5, PDF 7 / печ. 443).

### Study 2: реальный Pioneer II

**Цель:** показать применимость secondary-task methodology вне simulator (PDF 8-9 / печ. 444-445).

- Один Pioneer II с camera, laser range finder и sonar работал в condemned building с добавленными boxes.
- Использовались два мира: low и higher complexity; complexity была категориальной (`1` и `2`), а не вычисленной сенсорами.
- Сравнивались `P2P` и `Scripted`.
- Secondary task - Tetris, а не arithmetic/second robot.
- Выборка - 8 college students с предыдущим опытом управления роботом через сходный interface (PDF 9 / печ. 445).

Это study одного физического робота с переключением на secondary task, а не реальная команда из нескольких одновременно управляемых роботов.

### Study 3: prediction и observed three-robot performance

**Цель:** проверить, переносится ли performance, оценённая по single-/two-robot secondary-task curves, на team of three robots (PDF 9-11 / печ. 445-447).

**Interaction schemes:** `P2P` и `ROI` (region-of-interest). `ROI` использует automated path planning и exploration, генерируя waypoints для Scripted execution.

**Первая группа:** 13 male and female volunteers разных background и возраста `13-50+`, без предыдущего опыта управления роботами. После training каждый участник выполнил шесть пятиминутных sessions в simulated worlds трёх complexity levels. Secondary tasks - math problems и управление вторым роботом той же схемой. Эти данные дали neglect/interface curves и predictions (PDF 10 / печ. 446).

**Предсказываемые конфигурации:** для трёх роботов рассмотрены четыре уникальные комбинации `PPP`, `PPR`, `PRR`, `RRR`, где `P` означает `P2P`, `R` - `ROI`. Thresholds выбирались для максимизации Equation 5 при feasibility constraint (PDF 10 / печ. 446).

**Вторая группа:** 24 участника управляли тремя роботами в тех же мирах. В каждый момент существовали три цели; любой робот мог взять любую цель. После сбора цели появлялась следующая; session завершалась после девяти целей. Пользователь мог в любой момент переключиться на любого робота кликом по карте (PDF 10 / печ. 446).

**Объём:** для каждой пары «world complexity x team configuration» получено 9-15 performance samples (PDF 10 / печ. 446).

**Ключевое нарушение предположения:** robots/tasks были не полностью независимы. Любой робот мог собрать любую цель, а несколько роботов ускоряли exploration. Авторы рассматривают это как источник части prediction error (PDF 10-11 / печ. 446-447).

## Результаты

### Simulation study

При world complexity `0.35` `Teleop` быстрее других схем достигает peak performance при interaction. `P2P` достигает примерно того же peak, но медленнее; `Scripted` достигает более низкого peak (Fig. 6a, PDF 8 / печ. 444).

При neglect различие меняется. Через 30 s `Scripted` сохраняет expected performance около 40% capacity, тогда как `Teleop` и `P2P` уже достигли или приблизились к нулю. Поэтому `Scripted` более neglect-tolerant (Fig. 6b, PDF 8 / печ. 444).

Для average robot performance около `0.30` Fig. 7 показывает tradeoff: `Teleop` требует почти постоянного внимания, `P2P` - существенно больше внимания, чем `Scripted`; рост complexity с `0.30` до `0.50` уменьшает доступные neglect intervals (PDF 8 / печ. 444). Статья показывает значения только графически, без таблицы и confidence intervals, поэтому точные секунды из высоты столбцов в этот обзор не переносятся.

### Switching cost

Fig. 4 и Fig. 6a показывают delay между возвратом внимания и заметным ростом performance. Авторы называют его switching cost estimate, но прямо предупреждают, что такая оценка может быть неточной, и оставляют дальнейшее изучение switching costs будущей работе (PDF 5, 8 / печ. 441, 444).

Следовательно, источник подтверждает наличие resumption/switching mechanism только качественно. Он не оценивает функцию switching cost от числа роботов и не валидирует `gamma(P)`.

### Real-robot study

В реальном мире `P2P` достигал более высокого performance, чем `Scripted`, но быстрее деградировал при neglect. `Scripted` требовал меньшего workload и оставался более устойчивым к neglect, но давал более низкий performance (PDF 9 / печ. 445).

В simulator `Scripted` доминировал `P2P` сильнее. В real-robot environment преимущество ослабло из-за localization errors: waypoints на карте неточно переносились в robot reference frame. Это показывает context dependence interaction scheme и важность task/environment-specific calibration (PDF 9 / печ. 445).

### Three-robot prediction validation

Predicted и observed completion times были близки прежде всего при low complexity, но авторы отдельно отмечают, что данные не были statistically significant. Fig. 10 показывает 95% confidence intervals для observed values, однако статья не приводит численные intervals, test statistic, `p` или effect size (PDF 10-11 / печ. 446-447).

При большей complexity модель заметно завышала completion time для `PPP` при `C=1` и `C=2`, а также `PPR` при `C=2`. В условиях высокой нагрузки участники использовали interdependence: размещали роботов в разных regions («zone defense») и уделяли внимание только тем зонам, где появлялась цель. Эта адаптация давала actual time ниже prediction, построенного на independent-task assumption (PDF 10-11 / печ. 446-447).

Несмотря на ошибки абсолютных значений, ordering predicted team performance был почти идентичен ordering observed performance. Авторы интерпретируют это как evidence, что analysis может выбирать вероятно лучшую configuration даже при небольших нарушениях independence. Это описательный вывод по одному experiment, а не формальная гарантия ranking consistency (PDF 11 / печ. 447).

В случаях наибольшей ошибки модель предсказывала, что два робота были бы столь же эффективны, как три. Авторы трактуют это как способность модели выявлять operator overload (PDF 11 / печ. 447).

### Workload-performance tradeoff

Cross-plots `RAD` и average performance показывают Pareto-like tradeoff. Для real-robot data `Scripted` требует меньший operator workload, тогда как `P2P` даёт более высокий average robot performance; ни одна схема не является безусловно лучшей по обеим координатам (PDF 11-12 / печ. 447-448).

## Неопределённость и ограничения экспериментов

1. **Simulation sample:** 40 участников - undergraduate CS/engineering students без robot-driving experience. Это удобная, а не репрезентативная выборка профессиональных operators.
2. **Неравномерный exposure:** 15/48/57 sessions для `Teleop`/`P2P`/`Scripted`; причины объясняются требуемым sampling domain, но сравнение имеет разную точность по схемам.
3. **Короткие sessions:** simulation estimates получены из трёх десятиминутных sessions на участника; prediction curves - из шести пятиминутных sessions первой группы.
4. **Неполная статистическая отчётность:** для основных neglect/interface curves нет confidence bands, model-fit diagnostics или inferential comparisons. Полные curves для всех complexities вынесены в thesis [53].
5. **Real-robot sample:** только 8 college students, уже знакомых с похожим interface; confidence intervals и tests не приведены.
6. **Prediction study:** первая и вторая группы различаются; prediction строится на 13 участниках, observed three-robot result - на 24. Для cell доступно 9-15 samples.
7. **Явная non-significance:** авторы сами пишут, что agreement prediction/observation не statistically significant; Fig. 10 даёт только графические 95% intervals.
8. **Нарушение independence:** любой робот мог взять любую цель, а общая exploration меняла task environment. Именно это позволило adaptive strategy и создало систематические errors в сложных условиях.
9. **Outcome mismatch:** Equation 5 оптимизирует average robot performance, тогда как validation figure сравнивает time to collect nine goals. Статья не выводит общий theorem, связывающий эти outcomes.
10. **Performance metric approximation:** instantaneous metric clipping и shortest-path approximation не гарантируют равенства интегральной task performance; это оговорено авторами.
11. **Неизмеренная cognitive workload:** `RAD` - time-fraction proxy, а не психометрическая или физиологическая мера workload. Memory load, error recovery и stress могут не быть пропорциональны interaction time.
12. **Switching не идентифицирован:** initial delay на interface curve смешивает awareness recovery, interface latency, robot dynamics и собственно task-switch cost.

## Mapping к `Z,k,r,W,P,L,C(P),h,H,gamma(P)` и M0-M4

Здесь **direct** означает объект, прямо определённый в источнике; **analogy** - сходную формальную роль при другой предметной семантике; **absent** - отсутствие соответствующего механизма.

| Поле M0-M4 | Статус | Соответствие у Crandall et al. | Точная граница |
|---|---|---|---|
| `Z_i` | **absent** | Есть navigation task, goals и world complexity | Нет baseline task complexity, нормированной единицы `X` или конечного списка software jobs |
| `k_i^(r)` / `k` | **absent** | Interaction scheme меняет performance и attention demand | Нет отношения AI duration к no-AI duration; performance curves нельзя переводить в `k` |
| режим `r` | **analogy, сильная** | `pi_i=(autonomy,interface)`; сравниваются Teleop, P2P, Scripted, ROI | Это robot control mode, а не coding workflow; одна схема может иметь разные `(NT,IT)` при разных threshold/complexity |
| `W=X sum Z_i k_i` | **absent** | Есть непрерывная robot activity и repeated interaction cycles | Нет суммарной конечной работы, аддитивных task durations или fixed project workload |
| `P` | **direct structural analogue** | `M` robots; fan-out оценивает maximum manageable count; validation фиксирует `M=3` | Роботы не являются identical coding-agent slots; formula предполагает independent repeated tasks и integer team size |
| `L` | **absent** | Independent-task assumption; в validation есть shared goals | Нет inter-task precedence DAG и critical path; shared goals дают substitution, а не precedence |
| `C(P)` | **absent** | При overload падает performance, возможны adaptive team strategies | Нет agent-agent integration work, merge conflicts или multiplicative overhead от числа исполнителей |
| `h_i^(r)` / `h` | **analogy** | `IT_i` - active human service; `RAD_i` - human fraction interaction cycle | `IT` не нормирован на no-AI baseline и не включает обязательно всю specification/verification/rework работу coding task |
| `H=X sum Z_i h_i` | **analogy, сильная** | Feasibility требует разместить все `IT_j` в доступных `NT_i`; для homogeneous team `M*RAD<=1` | Это steady-state utilization, а не total human work конечного workload; сумма `IT` зависит от threshold и cycles |
| `gamma(P)` | **conceptual support only** | После переключения есть awareness-recovery delay; authors call it switching cost estimate | Cost не отделён чисто, не оценён как функция `P`, не дана параметрическая форма; авторы оставляют вопрос future work |
| makespan | **partial empirical overlap** | Three-robot study измеряет time to collect fixed nine goals | Основная objective - average performance `J(pi)`; нет no-AI baseline, software workload или speedup `T_h/T_ai` |

### Mapping по уровням

| Уровень | Что совпадает | Что отсутствует |
|---|---|---|
| M0 | Несколько автономных исполнителей могут действовать параллельно | Нет идеально делимой конечной работы, `W/P`, baseline или `k` |
| M1 | Fan-out сначала выводится для homogeneous independent robots | Нет finite indivisible jobs, longest-job bound `M_N` или machine assignment makespan |
| M2 | Независимость сформулирована явно и проверена как критичное assumption | Нет DAG, precedence constraints и `L`; validation частично нарушает independence через shared goals |
| M3 | Наблюдается снижение usefulness дополнительного робота при overload | Нет `C(P)` и agent-agent integration overhead; причина насыщения - human attention и task structure |
| M4 | Один оператор является capacity-1 resource; есть task-specific human windows, fan-out, feasibility и attention-performance tradeoff | Нет fixed-workload aggregate `H`, общего bound `max{C(P)W/P,L,gamma(P)H}`, входной/выходной coding verification и калибровки `gamma(P)` |

## Что источник поддерживает для нашей статьи

1. **One-operator-many-executors - эмпирически исследуемая topology.** Работа прямо рассматривает одного человека и несколько remote robots, а не только one-human-one-tool interaction (PDF 2-4 / печ. 438-440).
2. **Человеческое внимание задаёт конечный fan-out.** Дополнительный исполнитель полезен только тогда, когда его interaction demand помещается в autonomous/neglect intervals остальных (PDF 4 / печ. 440).
3. **Fan-out зависит от режима и performance requirement.** Autonomy, interface, task complexity и threshold совместно определяют `NT`, `IT`, performance и maximum manageable count; универсального числа роботов нет (PDF 4-6 / печ. 440-442).
4. **Human windows должны быть размещены во времени.** Equation 1 является operational feasibility constraint, а не только statement о суммарной человеческой занятости (PDF 4 / печ. 440).
5. **Существует performance-workload frontier.** Снижение human attention может сопровождаться снижением task performance; оптимизация только makespan или только workload неполна без requirement на качество (PDF 11-12 / печ. 447-448).
6. **Режим interaction меняет обе стороны tradeoff.** Более автономная Scripted схема допускает более длительный neglect, но может давать меньший peak/average performance; P2P требует большего внимания ради более высокого performance в real-world study (PDF 8-9, 11-12 / печ. 444-445, 447-448).
7. **Single-executor measurements могут быть основой team configuration model**, но только при проверяемых assumptions. В study ranking configurations оказался устойчивее абсолютных predictions (PDF 9-11 / печ. 445-447).
8. **Overload может сделать дополнительного исполнителя бесполезным.** Ошибки prediction возникли именно в configurations, где model указывала, что два робота могут быть столь же эффективны, как три (PDF 11 / печ. 447).
9. **Switching/resumption mechanism реален как design concern**, но эта работа поддерживает лишь его наличие, а не численную форму `gamma(P)` (PDF 5, 8, 12 / печ. 441, 444, 448).

## Что источник не позволяет утверждать

1. Что fan-out robots численно переносится на coding agents.
2. Что `IT_i=Z_i h_i X`, `RAD=h/k`, сумма interaction times равна `H` или что эти соответствия не требуют отдельной операционализации.
3. Что `Fanout=1/RAD` является fixed-workload speedup law. Это steady-state relation между interaction-cycle fractions.
4. Что добавление `P` coding agents даёт ускорение, saturation или slowdown с конкретным effect size.
5. Что Crandall et al. валидируют bound `T_ai>=gamma(P)H`, потолок `1/h_bar_w` или линейную форму `gamma(P)=1+delta(P-1)`.
6. Что initial delay interface-efficiency curve является чистым context-switch cost: сами авторы называют estimate потенциально неточным.
7. Что Equation 1 остаётся достаточным после добавления DAG, release times, output verification, rework cycles, heterogeneous human phases или sequence-dependent setup.
8. Что source model содержит `Z`, task/mode-specific `k`, `W`, `L` или agent-agent `C(P)`.
9. Что почти одинаковый ranking predicted/observed configurations статистически доказан или переносится на другие tasks/team sizes.
10. Что абсолютные predictions подтверждены: authors прямо отмечают non-significance и systematic discrepancy в complex worlds.
11. Что средняя robot performance эквивалентна coding quality, task success или project makespan.
12. Что robots/tasks в validation были полностью independent: любой робот мог собрать любую цель, и участники использовали эту interdependence.
13. Что более автономный режим всегда лучше. `Scripted` снижал workload, но мог снижать performance и страдал от localization error.

## Отличие от fixed-workload coding-agent model

| Измерение | Crandall et al. (2005) | M0-M4 |
|---|---|---|
| Центральный вопрос | Сколько robots/tasks может обслуживать оператор и какая configuration максимизирует average performance при workload constraint | Когда ячейка с `P` кодовыми агентами сокращает makespan фиксированного набора работ |
| Временная постановка | Повторяющиеся neglect/interaction cycles, потенциально неограниченный horizon | Конечный fixed workload и project completion |
| Исполнители | Remote mobile robots в navigation/exploration | Кодовые ИИ-агенты или agent work streams |
| Роль человека | Периодически возвращает robot к peak performance | Формулирует, читает, проверяет, исправляет и интегрирует результаты задач |
| Автономный интервал | Robot performance обычно деградирует при neglect | Coding agent может продолжать, завершиться, заблокироваться или ждать review; монотонная деградация не обязательна |
| Режим | `(autonomy,interface)` | `r`, свойство task-tool-workflow configuration |
| Human metric | `IT`, `NT`, `RAD`, Equation 1 | `h_i`, total `H`, explicit non-overlap human intervals, `gamma(P)` |
| Team-size metric | Fan-out и feasibility | `P` плюс competing lower bounds M0-M4 |
| Work structure | Independent repeated tasks; validation допускает substitutable shared goals | Indivisible jobs, DAG, critical path `L`, shared code artifacts |
| Outcome | Instantaneous/average robot performance; в validation time to nine goals | Makespan и speedup относительно sequential no-AI baseline |
| Coordination | Independence assumption; adaptive zone defense при shared goals | Agent-agent integration overhead `C(P)` и explicit dependencies |
| Validation | Three user studies в simulator/real robot, малые samples и ограниченная inference | Детерминированная model, параметры которой требуют внешней coding-specific calibration |

Ключевое различие для M4: `H` - total human service requirement фиксированного workload, тогда как Crandall et al. задают utilization одного оператора в повторяющемся cycle. Их модель лучше описывает частоту вмешательств и performance threshold; M4 лучше связывает human bottleneck с project makespan, но в текущем агрегированном виде не выводит допустимость конкретного cyclic attention schedule.

## Проверенные claims для Related Work

1. Crandall et al. формализуют fan-out одного оператора над homogeneous independent robots как `(NT+IT)/IT` и задают feasibility heterogeneous team условием, что neglect interval каждого робота не меньше суммы interaction times всех остальных (PDF 4 / печ. 440).
2. Neglect tolerance является парой `(NT,IT)`, зависящей от task, autonomy/interface scheme, environment complexity и performance threshold; поэтому maximum manageable team size не является постоянной характеристикой оператора или робота (PDF 4-6 / печ. 440-442).
3. Secondary-task studies с 40 участниками в simulator и 8 участниками с real robot показали tradeoff: более автономная Scripted схема дольше сохраняла performance без внимания и требовала меньшего workload, тогда как P2P в real-world setting достигала более высокого performance ценой более частого внимания (PDF 7-9, 11-12 / печ. 443-445, 447-448).
4. Для трёхроботных `P2P/ROI` configurations predicted и observed completion times были ближе при low complexity, а configuration ranking почти совпал; однако authors назвали data statistically non-significant, и absolute predictions систематически ошибались там, где участники использовали task interdependence при overload (PDF 10-11 / печ. 446-447).
5. `RAD=IT/(IT+NT)` является proxy доли человеческого времени, а не полной cognitive workload measure; source не оценивает switching penalty как функцию team size (PDF 8, 11 / печ. 444, 447).
6. Для M0-M4 источник поддерживает capacity-1 attention, intervention windows и mode-dependent fan-out, но не `k`, `W`, DAG/`L`, `C(P)`, fixed-workload `H` или `gamma(P)` для coding agents.

## Вариант встраивания в Related Work

> Близкую one-human-many-executors постановку исследуют Crandall et al. (2005) для управления несколькими роботами. Они характеризуют interaction scheme через neglect time `NT`, в течение которого робот сохраняет допустимую производительность без оператора, и interaction time `IT`, необходимое для восстановления performance. Для однородных независимых роботов fan-out равен `(NT+IT)/IT`, а гетерогенная команда feasible, если для каждого робота его `NT_i` вмещает сумму `IT_j` всех остальных. Secondary-task studies в симуляции и с реальным роботом показывают, что autonomy/interface mode меняет одновременно attention demand и robot performance; трёхроботная validation также обнаруживает ошибки абсолютного прогноза при operator overload и нарушении independence. Эта работа является прямой опорой для моделирования одного человека как capacity-1 resource и явного планирования intervention windows. Однако её steady-state neglect cycles и average robot performance не эквивалентны fixed-workload coding makespan: она не содержит task-specific `k`, DAG/`L`, integration overhead `C(P)` и не оценивает `gamma(P)` для нескольких coding contexts.

## Таблица опорных страниц

| PDF | Печатная | Раздел / объект | Опорное содержание |
|---:|---:|---|---|
| 1 | - | BYU ScholarsArchive cover | Репозиторная запись, peer-reviewed label, authors/title, journal citation и Faculty Publications 363 |
| 2 | 438 | Abstract; Introduction | One-human-many-robots motivation; определения `NT` и `IT`; interaction scheme; цели feasibility и performance prediction; DOI и manuscript dates |
| 3 | 439 | Related Literature; Fanout and Feasibility | Autonomy taxonomy; task switching; начало fan-out; определение independent robots |
| 4 | 440 | Fanout and Feasibility; Neglect Tolerance | `Fanout=(NT+IT)/IT`; `N_i`; Equation 1 `NT_i>=sum IT_j`; capacity-1 feasibility; начало neglect/interface curves |
| 5 | 441 | Neglect Tolerance | Neglect-impact/interface-efficiency curves; task/world complexity; switching interval; threshold и alternating cycles |
| 6 | 442 | Neglect Tolerance; User Study | Neglect tolerance `(NT,IT)`; average performance vs attention tradeoff; secondary-task methodology; 40-subject study purpose; Teleop/P2P/Scripted |
| 7 | 443 | Performance Metric; Complexity; Protocol | Equations 2-4; metric truncation; 21 worlds; two secondary tasks; 40 students, 120 sessions, 15/48/57 allocation; neglect-time ranges |
| 8 | 444 | Simulation Results; Fig. 6-7 | Complexity `0.35`; Scripted after 30 s neglect около 40% capacity; attention tradeoff для performance `0.30`; switching-cost caveat; начало real-robot study |
| 9 | 445 | Real-Robot Results; Team Performance | 8 experienced college users; Tetris secondary task; P2P vs Scripted; localization limitation; `pi`, `N(pi)`, Equation 5 |
| 10 | 446 | Prediction User Study | Optimization subject to feasibility; first group 13, six 5-min sessions; P2P/ROI; PPP/PPR/PRR/RRR; second group 24, three robots, nine goals, 9-15 samples; incomplete independence |
| 11 | 447 | Prediction Results; Workload Tradeoff | Fig. 10 with 95% CIs; non-significance; errors PPP/PPR at higher complexity; zone defense; near-preserved ranking; overload; `RAD=IT/(IT+NT)` |
| 12 | 448 | Workload Tradeoff; Conclusion | Scripted lower workload vs P2P higher performance; conclusions; limits and future work on general multitasking, thresholds, interdependence and switching |
| 13 | 449 | References; author bios | Завершение references и библиографическая граница статьи |

## Итоговая оценка релевантности

Crandall et al. (2005) - сильный первичный источник для formal и empirical justification самой идеи M4: один оператор обслуживает несколько автономных исполнителей, его взаимодействия не могут перекрываться, а допустимый fan-out определяется отношением автономных и человеческих интервалов. Особенно полезны heterogeneous-team feasibility Equation 1, связь `Fanout=1/RAD`, зависимость capacity от interaction scheme и evidence, что absolute team predictions разрушаются при overload и нарушении independence.

Доказательная сила источника заканчивается до coding-specific fixed-workload model. В нём нет no-AI baseline, task factor `k`, конечной работы `W`, DAG/`L`, integration overhead `C(P)` или параметрической `gamma(P)`. `RAD` нельзя подставлять вместо `h`, а robot fan-out нельзя использовать как численную оценку числа coding agents. Корректная роль источника - обосновать capacity-1 attention, intervention scheduling и performance/fan-out tradeoff, одновременно явно отделив steady-state robot supervision от makespan конечного software project.
