# Olsen и Wood (2004): fan-out одного оператора при управлении несколькими роботами

## Назначение и границы обзора

Этот документ разбирает один источник применительно к модели M0-M4 для fixed-workload makespan ячейки «один разработчик - `P` кодовых ИИ-агентов». Olsen и Wood рассматривают ближайшую концептуальную топологию: один человек распределяет внимание между несколькими полуавтономными исполнителями, которые продолжают работу между вмешательствами оператора.

Главная ценность источника для нашей статьи состоит в явном связывании полезного параллелизма с двумя временными величинами: продолжительностью самостоятельной активности исполнителя и временем человеческого взаимодействия. Работа также разделяет neglect time и activity time, раскладывает interaction time на monitoring, selection, context switching, problem solving и command expression и показывает, что фактически используемый fan-out может быть намного меньше числа доступных роботов.

Граница переноса принципиальна. Эксперименты выполнены с симулированными мобильными роботами в maze-search task, а не с кодовыми агентами. Их численные значения fan-out, activity time и interaction effort нельзя использовать для калибровки `P`, `h`, `H` или `gamma(P)` в разработке. Источник поддерживает структуру аргумента о human attention bottleneck и необходимости планировать intervention windows, но не формулы makespan M0-M4 и не численные параметры software workflow.

Локальный PDF содержит 8 страниц; печатная пагинация 231-238 совпадает с порядком PDF-страниц. Ниже ссылки имеют вид «PDF-страница / печатная страница».

Статусы mapping используются строго:

- **direct** - объект или отношение прямо определены и исследуются авторами;
- **analogy** - формальная роль сходна, но перенос в software development является нашей интерпретацией;
- **absent** - соответствующего объекта в модели источника нет.

## Библиография, metadata и статус

**Проверенная ссылка:** Dan R. Olsen Jr. and Stephen Bart Wood. “Fan-out: Measuring Human Control of Multiple Robots.” In *Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI 2004)*, Vienna, Austria, April 24-29, 2004, pp. 231-238. New York: ACM. DOI: [10.1145/985692.985722](https://doi.org/10.1145/985692.985722).

- Авторы, заголовок, аффилиация Brigham Young University, место и даты CHI 2004, страницы 231-238 и ACM ISBN `1-58113-702-8/04/0004` видны в PDF (PDF 1-8 / pp. 231-238).
- DOI, полное название proceedings и тип `proceedings-article` дополнительно сверены с Crossref; DOI в видимом тексте локального PDF не напечатан.
- Статус: опубликованная conference paper в основных proceedings CHI 2004. PDF не описывает процедуру рецензирования, поэтому отдельное утверждение о её форме по этому файлу не делается.
- Тип доказательства: концептуальная метрика, измерительная процедура и серия лабораторных экспериментов с симулированными роботами и операторами.
- Локальный файл: `/Users/rexarrior/work/articles/simple_model_full/literature/olsen_wood2004.pdf`.
- SHA-256: `672947ea4b1aee05a1068c074c4093db844bf5464305e843b1e93e3f6a29508f`.
- В рамках этой задачи `references.bib` не изменяется.

## Исследовательский вопрос и вклад

Авторы исследуют, как измерить способность одного человека одновременно управлять несколькими полуавтономными роботами и как отделить качество human-robot interface от автономности самих роботов (PDF 1-3 / pp. 231-233).

Работа отвечает на четыре связанных вопроса:

1. Как определить fan-out команды «один человек - несколько роботов»?
2. Как fan-out связан с временем самостоятельной активности робота и временем взаимодействия человека с ним?
3. Как измерить эти величины, если когнитивная часть человеческого взаимодействия непосредственно не наблюдается?
4. Можно ли использовать выведенный interaction effort для сравнения интерфейсов при разных уровнях автономности роботов?

Основной вклад источника состоит в следующем:

- fan-out определяется как число роботов, которыми один человек может управлять одновременно;
- предлагается first-order relation `FO = AT / IT`;
- neglect time отделяется от activity time через overlap активности и взаимодействия;
- activity time и фактический fan-out получают операциональные измерения;
- вместо недоступного прямому измерению interaction time вводится сравнительный индекс interaction effort `IE = AT / FO`;
- серия симуляционных экспериментов проверяет, когда это отношение работает и где оно нарушается.

Авторы прямо подчёркивают, что их цель - не детальная cognitive или ergonomic model, а сравнительная метрика для HRI designs (PDF 1 / p. 231).

## Точные определения и формулы

### Fan-out

Fan-out `FO` - число роботов, которыми человек может управлять одновременно (PDF 1 / p. 231):

```text
FO = AT / IT.
```

Здесь `AT` - activity time, а `IT` - interaction time. Содержательная логика формулы такова: чем дольше каждый робот остаётся полезно активным между вмешательствами и чем меньше внимания требует одно взаимодействие, тем больше исполнителей может обслуживать один оператор.

Формула является модельной гипотезой и отношением средних величин, а не доказанной универсальной capacity law. Уже во введении авторы предупреждают, что реальные отношения сложнее простой записи, а эксперименты на PDF 7-8 показывают систематические отклонения при низком fan-out и изменении состава interaction effort.

### Neglect time и neglect tolerance

Neglect time `NT` - время, в течение которого робот может работать, пока пользователь его игнорирует. Авторы называют `NT` мерой автономности и прямо связывают понятие с neglect tolerance Crandall и Goodrich, но исследуют несколько роботов, а не эффективность интерфейса одного робота (PDF 2 / p. 232).

Neglect time не тождествен activity time. Робот может самостоятельно двигаться, но оставаться под наблюдением пользователя, например из-за недоверия к odometry. Тогда он активен, но не neglected. Связь задаётся формулой (PDF 2 / p. 232):

```text
AT = O * IT + NT,
```

где `O` - доля interaction time, в течение которой робот одновременно остаётся активным. При управлении автомобилем `O` близко к 1, потому что движение и steering почти полностью перекрываются. При setup производственного робота `O` близко к 0, после чего возможна длительная автономная работа.

Авторы отказались от предварительного измерения `NT` через случайное размещение и случайную цель: такое измерение систематически завышало реальную neglect duration. Пользователи вмешивались заранее, давали более короткие цели из-за недоверия и создавали неопределённый overlap активности с вниманием (PDF 3-4 / pp. 233-234). Поэтому эксперименты и итоговая метрика основаны на `AT`, а не непосредственно на `NT`.

### Activity time

Концептуально `AT` - время эффективного прогресса до новой команды, прекращения прогресса или завершения команды оператора (PDF 2 / p. 232). Операционально авторы измеряют интервал от команды пользователя до первого из двух событий: робот перестаёт делать прогресс либо получает следующую команду. Значения усредняются по всем роботам в эксперименте (PDF 4 / p. 234).

Такое измерение зависит от наблюдаемого критерия effective progress. В используемой симуляции движущийся робот всегда приближается к цели, поэтому activity detection прост. Авторы признают, что для более интеллектуальных роботов баланс между достижением цели и avoidance может сделать конец activity трудно наблюдаемым (PDF 4 / p. 234).

### Interaction time и interaction effort

`IT` - время, требуемое человеку для взаимодействия с данным роботом. Авторы считают его не монолитным и выделяют четыре компонента (PDF 3 / p. 233):

1. **Robot monitoring and selection:** обзор состояний и выбор робота, которому внимание нужно следующим.
2. **Context switching:** восстановление целей и проблем нового робота после переключения.
3. **Problem solving:** анализ ситуации и планирование следующего действия.
4. **Command expression:** ввод команды через интерфейс.

Авторы предполагают, что `IT` само может расти с `FO`: больше роботов требует больше monitoring и selection, а разнообразие их ситуаций увеличивает context-switching time. Более автономный робот одновременно может уменьшить человеческий problem-solving component (PDF 3 / p. 233). Следовательно, знаменатель исходной формулы не обязан оставаться постоянным при масштабировании.

Прямо измерить полное `IT` авторы не могут, потому что значительная часть monitoring, planning и problem solving происходит в уме оператора. Из формулы можно алгебраически получить

```text
IT = AT / FO.
```

Однако на следующей странице авторы отказываются называть это точным временем и вводят (PDF 4-5 / pp. 234-235):

```text
IE = AT / FO,
```

где `IE` - interaction effort. Авторы называют `IE` unitless comparative value: он не задаёт абсолютную шкалу interaction time, но предназначен для сравнения interactive efficiency двух HRI designs. Поэтому значения в Figures 6-10 нельзя интерпретировать как непосредственно измеренные минуты человеческой работы. В подписи и тексте Figure 6 встречается выражение “computed interaction time”, но таблица и предшествующая методологическая оговорка определяют вычисляемую величину именно как interaction effort.

### Измерение фактического fan-out

Авторы обсуждают два способа (PDF 4 / p. 234):

- **Fan-out plateau:** увеличивать число роботов до насыщения task effectiveness. Это содержательно прямой способ, но он требует множества длинных прогонов для каждого размера fleet и пользователя.
- **Average active robots:** дать оператору заведомо больше роботов, чем он способен эффективно обслуживать, регулярно сэмплировать их состояния и усреднить число активных роботов за задачу. Этот способ используется в экспериментах как оценка фактического `FO`.

Второй способ не равен установленному maximum capacity. Избыточные роботы создают собственную cognitive load, а task saturation может ограничить число полезно активных роботов раньше, чем насыщается внимание человека. Авторы считают оценку пригодной для сравнений интерфейсов, но прямо называют её estimate (PDF 4 / p. 234).

## Метод и экспериментальная установка

### Почему симуляция

Авторы выбрали simulated robots по трём причинам (PDF 5 / p. 235):

- проще контролировать task conditions;
- предполагаемое отношение должно описывать взаимодействие с независимыми agents независимо от их физических характеристик;
- уровни sensory и reasoning capability проще изменять программно, чем строить fleet из 15 физических роботов трёх типов.

Симуляция устраняет crashes, holes, collisions и safety risk. Авторы признают, что это повышает trust относительно реального мира и тем самым может увеличивать activity time. Они предполагают, что эффект отразится в `AT`, не разрушая саму формулу, но отдельно это предположение не тестируют (PDF 5 / p. 235).

### Задача и outcome

Оператор управляет роботами в случайно сгенерированном maze. Роботы должны как можно быстрее коснуться всех targets. Task complexity задаётся размерами maze, плотностью obstacles и числом targets; генератор проверяет достижимость всех targets (PDF 5 / p. 235).

Основной task-effectiveness outcome - время до касания всех targets. Для fan-out используются среднее число active robots, среднее `AT` и вычисляемое `IE`. Это fixed-goal completion task внутри отдельного прогона, но не software project, не заранее заданный набор jobs и не makespan DAG в смысле M0-M4.

Использовался один интерфейс: у каждого робота есть draggable goal marker, а робот пытается достичь цели. В большинстве тестов применялся “dark world”, где непосещённые области скрыты до того, как робот их исследует (PDF 5-6 / pp. 235-236).

### Три типа роботов

Все типы имели одинаковый интерфейс и решали задачи сопоставимой сложности (PDF 6 / p. 236):

| Тип | Поведение | Ограничение |
|---|---|---|
| Simple | Движется прямо к goal | Останавливается у цели или первого obstacle |
| Bounce | Обходит локальные obstacles движениями, уменьшающими расстояние до goal | Не отступает и застревает в cul-de-sac |
| Plan | Видит obstacles в sensor radius и постоянно строит shortest path к лучшей точке на его границе | Обходит локальные dead ends, но не структуры крупнее sensor radius |

Предварительное random-placement измерение показывало рост neglect time вместе с intelligence, что дало три уровня автономности при одинаковых task и UI. Численные значения этого предварительного `NT` в статье не приведены.

### Операторы и процедура

В начальных прогонах участвовали приглашённые и оплачиваемые university students. Каждый получил около 30 минут training and practice с каждым типом робота, затем решал серию mazes (PDF 6 / p. 236). Общее число участников начальной стадии не сообщается.

Figure 5 усредняет 18 прогонов восьми участников с planning robots и иллюстрирует task saturation: в начале требуется время, чтобы запустить роботов, а по мере нахождения targets полезный fan-out падает вместе с размером оставшейся задачи (PDF 6 / p. 236).

Авторы сочли часть оплачиваемых участников недостаточно мотивированными и перешли к “robo-races”. Группы из восьми человек работали на одинаковых workstations с одинаковыми problem sets; в каждом trial вручались денежные призы за первые три места. Авторы сообщают более высокий и однородный fan-out, но не дают численной оценки эффекта incentives (PDF 7 / p. 237).

Демография, опыт управления роботами, критерии набора, число уникальных операторов во всей серии и возможное повторное участие между competitions не сообщаются.

## Полные параметры четырёх validation tests

### Test 1: базовая race condition

- 8 участников, каждый выполнял 8 races, итого 64 trial runs.
- Dark worlds.
- 18 доступных роботов и 10 targets.
- Obstacle density 35%.
- 2 races с simple robots, 3 с bounce и 3 с plan для каждого участника.
- Display condition соответствует “no scroll” с resolution `1600 x 1200`, что уточняется при описании Test 3.

### Test 2: снижение task complexity

- Авторы называют competition идентичной Test 1, кроме obstacle density 22% вместо 35%.
- Из слова “identical” следует сохранение 18 роботов, 10 targets и race design; отдельное число trial runs повторно не напечатано.
- Цель - проверить, растут ли activity time и fan-out при снижении task complexity.

### Test 3: ухудшение интерфейса

- 8 участников и 8 races, то есть 64 participant-runs.
- Те же task conditions, что в Test 1.
- Resolution снижено с `1600 x 1200` до `800 x 600`.
- Maze перестаёт помещаться на экране и требует scrolling.
- Цель - проверить, возрастает ли `IE` при заведомо менее удобном интерфейсе.

### Test 4: изменение скорости

- Те же worlds и interface, что в Test 1.
- Только simple и bounce robots.
- Speed варьируется между runs, чтобы изменить activity/neglect duration без смены intelligence или UI.
- Simple tested at speeds 3, 6, 9; bounce at 3, 6, 9, 12, 15.
- Число участников, число повторов на speed condition и единицы speed в статье не сообщаются.

Порядок conditions, randomization или counterbalancing, независимость mazes между trials и обработка learning/carryover effects для competitions не описаны.

## Результаты и неопределённость

### Test 1 и Test 2

| Test | Obstacles | Robot | Mean `FO` | Mean `AT` | Computed `IE` |
|---:|---:|---|---:|---:|---:|
| 1 | 35% | Simple | 1.46 | 4.36 | 3.06 |
| 1 | 35% | Bounce | 2.94 | 7.82 | 2.77 |
| 1 | 35% | Plan | 5.11 | 14.42 | 2.88 |
| 2 | 22% | Simple | 1.84 | 4.99 | 2.88 |
| 2 | 22% | Bounce | 3.36 | 11.36 | 3.38 |
| 2 | 22% | Plan | 9.09 | 24.18 | 2.69 |

В Test 1 рост autonomy от simple к plan сопровождается ростом `AT` и `FO`, тогда как `IE` остаётся около 2.8-3.1. Авторы сообщают, что ANOVA не обнаружила статистического различия interaction effort/time между тремя типами, и интерпретируют это как поддержку fan-out equation (PDF 7 / p. 237).

В Test 2 меньшая obstacle density увеличила `AT` и `FO`, особенно у plan robots. Авторы снова сообщают отсутствие статистического различия computed interaction effort между типами (PDF 7 / p. 237).

Статья не приводит `F`, degrees of freedom, точные `p`, effect sizes, standard deviations или confidence intervals. Единицы `AT` и `IE` в Figures 6-7 не указаны. Поэтому “no statistical difference” нельзя трактовать как доказанную эквивалентность, а численные различия нельзя оценить по precision.

### Test 3

| Robot | `IE`, no scroll | `IE`, scrolled | Reported increase | Mean `FO`, scrolled |
|---|---:|---:|---:|---:|
| Simple | 3.06 | 4.48 | 46% | 1.12 |
| Bounce | 2.77 | 3.47 | 25% | 2.47 |
| Plan | 2.88 | 3.63 | 26% | 3.97 |

Scrolling condition дала более высокий `IE` для всех трёх типов. Авторы считают это подтверждением чувствительности interaction effort к качеству интерфейса (PDF 7 / p. 237).

Одновременно результат нарушил гипотезу постоянного `IE` при одинаковом UI: в scrolling condition simple robots отличались от bounce и plan. По авторскому ANOVA bounce и plan не различались, а simple отличался от обоих; численная статистика не опубликована. Авторы объясняют аномалию сменой состава interaction: при `FO` около 1 пользователь почти непрерывно вводит команды одному simple robot, тогда как при большем `FO` растут planning, monitoring и context switching (PDF 7 / p. 237).

### Test 4

| Robot | Speed | Mean `FO` | Mean `AT` | Computed `IE` |
|---|---:|---:|---:|---:|
| Simple | 3 | 2.54 | 7.21 | 3.05 |
| Simple | 6 | 1.21 | 3.51 | 3.09 |
| Simple | 9 | 0.89 | 3.26 | 3.67 |
| Bounce | 3 | 4.44 | 13.54 | 3.51 |
| Bounce | 6 | 3.11 | 9.60 | 3.10 |
| Bounce | 9 | 1.97 | 5.76 | 2.94 |
| Bounce | 12 | 1.82 | 4.42 | 2.51 |
| Bounce | 15 | 1.62 | 4.04 | 2.53 |

С ростом speed activity time и fan-out в целом снижаются. У fastest simple robot `FO = 0.89`: оператор не поддерживает непрерывную активность даже одного робота. В этой области `IE` снова меняется, что подтверждает неполноту простой формулы при очень низком fan-out (PDF 8 / p. 238).

Для bounce robots `IE` постепенно уменьшается вместе с fan-out. Авторы связывают тренд с сокращением monitoring и context-switching components при меньшем числе одновременно обслуживаемых роботов. Это содержательно важно: interaction cost зависит от масштаба, а не является постоянным знаменателем `FO = AT/IT` (PDF 8 / p. 238).

### Общая оценка validation

Эксперименты дают **частичную**, а не полную валидацию:

- Test 1-2 согласуются с first-order prediction: рост `AT` сопровождается ростом `FO`, а вычисленный `IE` близок между типами.
- Test 3 показывает, что заведомо худший UI повышает `IE`, то есть индекс различает designs.
- Test 3-4 показывают нарушения постоянства `IE`, особенно при `FO` около 1 и при изменении monitoring/context-switching load.
- Прямого независимого измерения полного `IT` нет, поэтому `FO = AT/IT` не проверяется одновременно против независимо наблюдаемых `AT`, `FO` и `IT`.
- Проверка постоянства `IE = AT/FO` при одинаковом UI является косвенной и частично круговой: вычисляемая величина определена из двух других, а гипотеза о её постоянстве требует дополнительного предположения, что robot type не меняет cognitive problem solving при том же UI.
- Авторы сами признают, что более умные роботы могут переносить problem solving с человека на автоматику. Поэтому одинаковый видимый UI не гарантирует одинаковое полное interaction demand.

## Предположения и ограничения применимости

1. `FO = AT/IT` описывает усреднённый steady interaction cycle, но статья не задаёт queueing model, stochastic arrival process вмешательств или доказательство устойчивости schedule.
2. Average active robots используется как estimate fan-out, а не как измеренный максимум controllable fleet.
3. Для оценки `FO` оператору дают 18 роботов, но лишние роботы сами создают cognitive load; авторы признают этот источник смещения.
4. Task saturation может ограничить активность раньше human attention. Авторы меняют стартовые позиции и dark-world task, чтобы ослабить эффект, но не устраняют его формально.
5. `AT` корректно наблюдается только при надёжном criterion effective progress. В maze simulation движение означает прогресс, что не переносится автоматически на coding agent, который может долго выполнять неверную ветвь работы.
6. Simulated robots не crash и не создают safety risk; trust и intervention policy отличаются от реальных systems.
7. Race incentives повышают effort относительно обычной paid study, но могут создавать performance regime, нехарактерный для длительной supervisory work.
8. Малые группы по 8 человек, неизвестное число уникальных участников, отсутствие demographics и короткое training ограничивают external validity.
9. Не сообщены variance estimates, точные ANOVA statistics, power analysis и confidence intervals.
10. Не описаны condition order, counterbalancing, learning effects и возможная зависимость повторных trials одного участника.
11. Maze search имеет пространственно повторяющиеся команды и немедленно наблюдаемое движение. Coding tasks требуют спецификации, длительного скрытого reasoning, tests, review, integration и rework.
12. Interaction effort объявлен сравнительным индексом и не должен заменять прямой хронометраж human-active intervals.

## Связь с `h`, `H` и intervention windows

### Что близко к `h_i`

`IT` ближе всего к активной человеческой части отдельного intervention episode. Его четыре компонента покрывают содержательные элементы `h_i^(r)` нашей модели:

- monitoring и выбор потока;
- восстановление контекста;
- анализ проблемы и планирование;
- выражение команды.

Для coding agents к этому списку добавляются чтение diff, запуск и интерпретация tests, verification, acceptance, integration и направление rework. Olsen и Wood не измеряют эти действия, поэтому их `IT` является только структурным предшественником, а не определением software `h_i`.

### Что близко к `H`

Сумма всех непересекающихся human interaction episodes за фиксированный workload была бы аналогом `H`. Но источник не строит такую сумму, не фиксирует полный human-active timeline и не нормирует interaction на baseline `Z_i X`. `IE` также не является суммарным временем. Следовательно, численное `H` из статьи получить нельзя.

### Intervention windows

Пара `AT`/`IT` делает видимой структуру, которой недостаточно в агрегате `H`:

```text
human interaction -> autonomous activity -> next human interaction.
```

`AT` характеризует доступное окно между вмешательствами, а `IT` - demand одного окна на capacity-1 human resource. Если несколько роботов требуют внимания раньше, чем оператор завершил цикл, часть из них простаивает или перестаёт делать effective progress. Это прямой концептуальный аргумент в пользу явной расстановки verification/intervention windows на уровне M4.

Однако coding-agent windows могут быть расположены и на входе, и на выходе, включать промежуточные checkpoints и повторяться после rework. У Olsen и Wood episode инициируется состоянием navigation task и следующей командой; готового scheduling algorithm для software interventions работа не даёт.

### Связь с `gamma(P)`

Monitoring/selection и context switching являются прямыми механизмами дополнительной человеческой работы при росте числа параллельных исполнителей. В этом смысле источник концептуально поддерживает `gamma(P) >= 1`.

Но данные не задают функцию `gamma(P)`:

- `IT` не измеряется напрямую;
- `FO` является outcome, а не независимо варьируемым числом потоков;
- interaction composition меняется нелинейно при низком `FO`;
- problem solving может уменьшаться с autonomy, пока monitoring и switching растут;
- авторы не оценивают линейный coefficient `delta` и не доказывают monotonicity полного human time.

Поэтому рабочая форма `gamma(P) = 1 + delta(P-1)` остаётся предположением M4, которое требует отдельного хронометража coding workflow.

## Полный mapping `Z,k,r,W,P,L,C(P),h,H,gamma(P)` и M0-M4

| Поле модели | Статус | Соответствие у Olsen и Wood | Точная граница |
|---|---|---|---|
| `Z_i` / `Z` | **analogy** | Task complexity задаётся maze dimensions, obstacle density и targets | Нет task-level baseline complexity в единицах `X`; complexity не сводится к одному `Z_i` |
| `k_i^(r)` / `k` | **absent** | Сравниваются robot autonomy и UI conditions | Нет отношения AI-assisted duration к no-AI duration одного разработчика и нет коэффициента полной software-task work |
| режим `r` | **analogy** | Robot type меняет autonomy, а scrolling меняет UI | Это system/interface conditions, но не interactive/delegated/autonomous coding modes с task-specific assignment |
| `W = X sum Z_i k_i` | **absent** | Есть maze trial и targets | Нет заданного набора software jobs и суммы transformed work |
| `P` | **direct по topology, analogy по величине** | Один оператор имеет 18 доступных роботов; число исполнителей явно присутствует | Доступный fleet не равен фактическому `FO`; `P` M0-M4 - число agent slots, а `FO` - performance-dependent estimate useful concurrency |
| неделимость / M1 | **analogy** | Роботы и targets дискретны | Нет job durations, machine assignment и longest-job bound `M_N` |
| DAG / `L` / M2 | **absent** | Maze имеет spatial constraints и shrinking search frontier | Нет precedence graph фиксированного набора работ и critical-path length |
| `C(P)` / M3 | **absent** | Несколько роботов создают monitoring load | Это human-side attention cost, а не agent-agent integration, merge conflicts или coherency multiplier |
| `h_i^(r)` / `h` | **analogy** | `IT` и его четыре компонента описывают active operator demand | `IT` не измерено напрямую, не нормировано на `Z_i X` и не включает software verification semantics |
| `H = X sum Z_i h_i` | **absent** | Наблюдается повторяющееся обслуживание нескольких роботов | Нет суммы непересекающихся human intervals фиксированного workload; `IE` не является `H` |
| `gamma(P)` | **conceptual analogy** | Monitoring/selection и context switching должны расти с числом одновременно обслуживаемых ситуаций | Нет параметрической функции, численного penalty или доказанной monotonicity |
| intervention windows / M4 schedule | **direct structural analogue** | Interaction episodes чередуются с autonomous activity; оператор обслуживает роботов последовательно | Нет точного расписания input/review/rework phases coding tasks |
| human capacity bottleneck / M4 | **direct по предмету HRI, analogy для software** | Fan-out измеряет leverage ограниченного внимания одного оператора | Источник не доказывает capacity bound для разработчика и кодовых агентов |
| makespan | **analogy** | Task effectiveness включает time until all targets are touched | Это completion time maze search, а не makespan заданного software workload относительно no-AI baseline |

### Отношение к уровням

- **M0:** источник опровергает наивное отождествление installed fleet с эффективным параллелизмом, но не задаёт `W/P`.
- **M1:** дискретность роботов присутствует, однако scheduling неделимых jobs и bound `M_N` отсутствуют.
- **M2:** task saturation и frontier ограничивают полезную concurrency, но не являются DAG или `L`.
- **M3:** human monitoring overhead нельзя помещать в `C(P)`, поскольку в нашей учётной конвенции `C(P)` оставлен для agent-agent integration.
- **M4:** это наиболее близкий уровень. Один оператор является capacity-limited resource, interaction episodes не могут полноценно выполняться одновременно, а autonomous activity создаёт окна для обслуживания других исполнителей.

## Что источник поддерживает для нашей статьи

1. **Fan-out является свойством всей human-autonomy-task-interface configuration.** Число полезно обслуживаемых исполнителей определяется не только их количеством, но и автономностью, task complexity, UI и поведением оператора (PDF 2-8 / pp. 232-238).
2. **Human attention получает leverage только между вмешательствами.** Чем больше `AT` относительно human interaction demand, тем больше параллельных executors потенциально может обслужить один человек (PDF 1-3 / pp. 231-233).
3. **Neglect tolerance и activity time различаются.** Доверие и наблюдение могут занимать внимание даже при самостоятельном движении робота, поэтому автономная работа агента не означает автоматически свободное человеческое время (PDF 2-4 / pp. 232-234).
4. **Human interaction не сводится к вводу команды.** Monitoring, selection, context switching и problem solving могут доминировать над command expression (PDF 3-4 / pp. 233-234).
5. **Interaction cost зависит от масштаба.** Авторы ожидают роста monitoring и switching при большем fan-out, а Test 3-4 показывают изменение состава interaction effort при разном `FO` (PDF 3, 7-8 / pp. 233, 237-238).
6. **Доступное число исполнителей не равно effective concurrency.** При 18 доступных роботах средний measured fan-out во многих conditions был существенно ниже, а task saturation дополнительно снижала использование fleet (PDF 4, 6-8 / pp. 234, 236-238).
7. **Окна вмешательства нужно моделировать во времени.** Средняя сумма human work недостаточна, если несколько executors одновременно достигают конца autonomous activity и требуют одного оператора.
8. **Одна простая ratio model является только first-order approximation.** Систематические отклонения при низком fan-out требуют учитывать composition и endogeneity interaction demand (PDF 7-8 / pp. 237-238).

Пункт 7 является синтезом нашей модели с временной структурой `AT`/`IT`, а не сформулированной авторами scheduling theorem.

## Что источник не позволяет утверждать

1. Что численный fan-out роботов переносится на число coding agents, которыми способен управлять разработчик.
2. Что `FO` следует подставлять вместо `P`: `FO` является measured outcome полезной активности, тогда как `P` - ресурсная capacity конфигурации.
3. Что `FO = AT/IT` является точным универсальным законом. Авторы называют его гипотезой и показывают отклонения.
4. Что `IE = AT/FO` является непосредственно измеренным временем человека. Авторы специально отказываются от такой интерпретации.
5. Что `NT`, `AT` или `IE` равны `h_i`, `H` или `gamma(P)H` без дополнительной нормировки и хронометража.
6. Что `gamma(P)` линейна или что coefficient `delta` можно оценить по Figures 6-10.
7. Что monitoring/context switching следует учитывать в `C(P)`: в M0-M4 это человеческие, а не agent-agent издержки.
8. Что повышение autonomy всегда повышает throughput или уменьшает human work: task saturation, trust и changing problem-solving demand нарушают простую монотонность.
9. Что ANOVA доказала эквивалентность interaction effort: точные statistics, confidence intervals и equivalence margins отсутствуют.
10. Что race performance обобщается на длительную работу разработчика с несколькими repository contexts.
11. Что maze completion time является software makespan, а targets и obstacles задают `W`, DAG или `L`.
12. Что источник поддерживает task-specific AI effect `k`, baseline `Z_i X`, agent integration overhead `C(P)` или критерии ускорения M0-M4.

## Отличие от M0-M4

| Измерение | Olsen и Wood (2004) | M0-M4 |
|---|---|---|
| Центральный вопрос | Сколько полуавтономных роботов способен одновременно обслуживать один оператор и как сравнивать HRI designs | Когда ячейка «один разработчик - `P` coding agents» сокращает fixed-workload makespan |
| Топология | Один оператор и fleet simulated mobile robots | Один разработчик и `P` параллельных кодовых agent slots |
| Workload | Maze search до касания всех targets | Заданный набор software tasks с baseline `Z_i X` |
| Автономный интервал | `AT`, effective activity между командами | Агентная часть `a_i`, расположенная между human phases |
| Human demand | Латентное `IT`; сравнительный proxy `IE` | Двухканально измеренное `h_i`, сумма `H` и penalty `gamma(P)` |
| Useful concurrency | Empirical `FO`, среднее число active robots | Resource parameter `P`, ограниченный неделимостью, DAG и human schedule |
| Зависимости | Spatial obstacles, frontier и task saturation | Явный DAG и critical path `L` |
| Coordination | Monitoring и switching оператора | Human penalty `gamma(P)` отдельно от agent integration `C(P)` |
| Outcome | Target-search completion, `AT`, `FO`, `IE` | Makespan и speedup относительно последовательного no-AI baseline |
| Validation | Small repeated laboratory races in simulation | Детерминированные bounds; параметры должны калиброваться на coding workflows |

Olsen и Wood находятся ближе к M4, чем общая метафора закона Амдала: они явно рассматривают одного человека, несколько автономных исполнителей и повторяющиеся intervention episodes. Но их модель одновременно уже и динамичнее. Она уже, потому что не содержит `Z`, `k`, `W`, DAG, integration и software verification. Она динамичнее, потому что связывает capacity с интервалами между вмешательствами и показывает изменение самого interaction demand при разном fan-out, тогда как `gamma(P)H` в текущем M4 остаётся агрегированной lower bound.

## Проверенные тезисы синтеза

1. **Прямой тезис источника:** fan-out - число роботов, которыми один человек может управлять одновременно; first-order hypothesis связывает его с отношением activity time к interaction time, `FO = AT/IT` (PDF 1, 3 / pp. 231, 233).
2. **Прямая оговорка источника:** neglect time и activity time не совпадают, потому что самостоятельная активность может перекрываться с вниманием оператора; формально `AT = O*IT + NT` (PDF 2 / p. 232).
3. **Прямой методологический тезис:** из-за невозможности непосредственно измерить полное interaction time авторы используют `IE = AT/FO` только как comparative interaction-effort index, а не точное время (PDF 4-5 / pp. 234-235).
4. **Прямой эмпирический тезис:** при одинаковом UI более автономные robots обычно имели большие `AT` и `FO`; ухудшение интерфейса scrolling увеличивало `IE` (PDF 7 / p. 237).
5. **Прямая граница validation:** при низком fan-out и varying speed состав interaction менялся, а computed `IE` переставал быть постоянным; авторы заключают, что простая формула не охватывает всей сложности (PDF 7-8 / pp. 237-238).
6. **Наше сопоставление:** `AT` соответствует окну автономной работы, а `IT` - human intervention demand, поэтому источник концептуально поддерживает необходимость планировать непересекающиеся human windows в M4.
7. **Наше сопоставление:** monitoring/selection и context switching являются механизмами для `gamma(P)`, но работа не определяет форму или значение этой функции для coding agents.
8. **Граница переноса:** measured robot fan-out нельзя превращать ни в рекомендуемое `P`, ни в численную калибровку `h/H` для software development.

## Короткий вариант встраивания в Related Work

> Olsen и Wood (2004) рассматривают fan-out команды «один оператор - несколько полуавтономных роботов», определяя его как число одновременно управляемых исполнителей и предлагая first-order relation `FO = AT/IT`, где `AT` - время полезной активности робота между вмешательствами, а `IT` - человеческое interaction time. Они отделяют activity time от neglect tolerance и показывают, что взаимодействие включает не только ввод команды, но также monitoring, выбор следующего робота, восстановление контекста и problem solving. В симуляционных maze-search experiments рост автономности обычно сопровождался ростом activity time и fan-out, а ухудшение интерфейса увеличивало вычисляемый interaction effort. Однако авторы не измеряют `IT` напрямую, трактуют `AT/FO` только как сравнительный индекс и фиксируют отклонения простой формулы при низком fan-out. Для M4 это ближайшая концептуальная опора human attention bottleneck и расписания intervention windows: `AT` соответствует автономному окну, а `IT` - спросу на общий capacity-1 human resource. Численные fan-out роботов при этом не переносятся на coding agents и не калибруют `P`, `h`, `H` или `gamma(P)`.

## Таблица evidence pages

| PDF | Печатная | Раздел / объект | Проверяемое содержание | Роль для M0-M4 |
|---:|---:|---|---|---|
| 1 | 231 | Title; Abstract; Introduction | Metadata; fan-out как число robots одного operator; `FO=AT/IT`; цель сравнительной HRI metric; search-and-rescue domain | Прямое определение topology и formula |
| 2 | 232 | Prior Work; Sample Robot World | Neglect time, activity time, отличие наблюдения от neglect; `AT=O*IT+NT`; car/manufacturing examples | Структура autonomy и intervention windows |
| 3 | 233 | Rationale for Fan-out | Fan-out как leverage human attention; четыре компонента `IT`; ожидаемый рост monitoring/context switching с `FO` | Концептуальная опора `h` и `gamma(P)` |
| 3-4 | 233-234 | Measuring NT and AT | Зависимость от task complexity, robot ability и user understanding; провал a priori `NT`; operational `AT` | Границы измерения autonomy |
| 4 | 234 | Measuring FO; Task Saturation | Fan-out plateau; average active robots; excess-robot cognitive load; task saturation | Различие installed `P` и effective concurrency |
| 4-5 | 234-235 | Measuring IT; Interaction Effort | Невозможность прямого полного `IT`; `IT=AT/FO`; переход к unitless comparative `IE=AT/FO` | Запрет трактовать `IE` как `h` или `H` |
| 5 | 235 | Robot Simulations; Task | Причины simulation; отсутствие crashes/safety; random maze; complexity controls; target-completion outcome; common UI | Experimental assumptions и external-validity boundary |
| 6 | 236 | Three Robot Types | Simple, bounce, plan; одинаковые UI/task; различная autonomy | Controlled variation of executor autonomy |
| 6-7 | 236-237 | Validation procedure | University students, training; task saturation; robo-races и incentives; Test 1 design, 64 runs | Operators, task и motivation |
| 7 | 237 | Figures 6-7 | Test 1-2 values; рост `AT`/`FO`; reported ANOVA without detailed statistics | Частичная поддержка first-order relation |
| 7 | 237 | Figures 8-9 | Scrolling raises `IE`; non-uniformity for simple robot; low-fan-out change in interaction composition | UI effect и граница constant `IT` assumption |
| 7-8 | 237-238 | Figure 10 | Speed manipulation; снижение `AT` и `FO`; `FO<1`; trend in `IE` | Endogeneity и нелинейность attention cost |
| 8 | 238 | Conclusions | Equation models many effects but misses underlying complexity, especially at low fan-out | Корректная ограниченная формулировка synthesis claim |

## Итоговая оценка релевантности

Olsen и Wood - ближайший концептуальный источник для topological claim «один человек - много автономных исполнителей». Работа не просто утверждает ограниченность внимания, а связывает её с длительностью автономных интервалов и стоимостью повторных вмешательств. Особенно полезны различие neglect/activity time, декомпозиция interaction time и наблюдение, что доступный fleet, фактический fan-out и task demand являются разными величинами.

Для M0-M4 источник сильнее всего поддерживает мотивацию уровня M4 и необходимость перейти от агрегата `H` к явным intervention windows при построении точного расписания. Он также даёт механизм для `gamma(P)`: monitoring, selection и context reacquisition растут при multiplexing нескольких потоков. Доказательная сила заканчивается до численной параметризации. `IE` не является временем, `FO` не равен `P`, experiments малы и специфичны для robot maze simulation, а формула имеет выявленные авторами отклонения. Корректная роль источника - conceptual predecessor и measurement warning, но не calibration source для coding agents.
