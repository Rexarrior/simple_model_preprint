# Barke, James и Polikarpova (2023): режимы взаимодействия с Copilot, grounding и состав человеческой работы

## Назначение и границы обзора

Этот документ разбирает один источник применительно к модели M0-M4 для fixed-workload makespan ячейки «один разработчик - `P` кодовых ИИ-агентов». Barke et al. особенно полезны для содержательной операционализации режима взаимодействия `r` и состава человеческой доли `h_i^(r)`: исследование наблюдает декомпозицию и планирование, способы prompting, просмотр альтернатив, принятие и отклонение подсказок, проверку, редактирование и отладку сгенерированного кода.

Граница переноса принципиальна. Работа изучает одного программиста с одним интерактивным GitHub Copilot и не сравнивает этот процесс с no-AI baseline. Она не варьирует число агентов, не разделяет настенное время на человеческий и автономный каналы и не оценивает project completion time. Поэтому источник описывает механизмы для `r` и наполняет перечень действий внутри `h`, но не даёт численных `k`, `h`, `H`, `gamma(P)` или multi-agent speedup.

Локальный PDF содержит 27 страниц. PDF-страницы 1-27 соответствуют напечатанным фолио `78:1`-`78:27`; ниже указываются обе нумерации.

## Библиография, статус и версия

**Полная ссылка:** Shraddha Barke, Michael B. James, and Nadia Polikarpova. “Grounded Copilot: How Programmers Interact with Code-Generating Models.” *Proceedings of the ACM on Programming Languages*, vol. 7, OOPSLA1, Article 78, April 2023, 27 pages. DOI: [10.1145/3586030](https://doi.org/10.1145/3586030) (PDF 1; printed p. 78:1).

**Статус:** опубликованная peer-reviewed архивная статья PACMPL, выпуск OOPSLA1. На последней странице указаны даты `Received 2022-10-28; accepted 2023-02-25`; титульная страница содержит издательские реквизиты ACM, DOI и лицензию CC BY 4.0. Это не препринт. Конкретная процедура рецензирования и число рецензентов в PDF не описаны (PDF 1, 27; printed pp. 78:1, 78:27).

**Проверенная версия:** издательская PDF-версия с датой публикации April 2023, `Proc. ACM Program. Lang. 7, OOPSLA1, Article 78`. Отдельный номер ревизии в документе отсутствует. Локальная копия: `barke2023.pdf`, SHA-256 `d73402c4a8890dc076be999d108e69f9b1967d6663c95f79c64343c293e161db`.

## Исследовательский вопрос и вклад

Исходный вопрос grounded-theory исследования сформулирован широко: **«How do programmers interact with Copilot?»** Введение конкретизирует его через четыре группы вопросов: для каких задач программистам нужна помощь, как они сообщают намерение инструменту, как проверяют соответствие сгенерированного кода своему намерению и как справляются с ошибками (PDF 1, 5; printed pp. 78:1, 78:5).

Основной вклад - первая, по утверждению авторов, grounded theory взаимодействия пользователей с AI programming assistant. Теория выделяет два динамических режима:

1. **Acceleration:** программист знает, что делать дальше, сам ведёт разработку и использует Copilot, чтобы быстрее выполнить уже спланированное code action.
2. **Exploration:** программист не уверен в следующем шаге, позволяет Copilot участвовать в планировании, исследует варианты, API или алгоритмы и тщательнее проверяет результат.

Авторы не представляют эти режимы как два разных продукта или стабильные типы пользователей. Один программист может многократно и плавно переключаться между ними в ходе одной задачи (PDF 2, 7; printed pp. 78:2, 78:7). Для M0-M4 это означает, что `r` в интерактивном классе может потребовать более мелкой временной разметки, чем один постоянный label на всю задачу.

Дополнительный вклад состоит в закрытом повторном кодировании записей, описательном сравнении prompting и validation между режимами, проверке зависимости режимов от опыта и характера задачи, а также в качественном сопоставлении теории с пятью публичными livestream (PDF 2, 15-20; printed pp. 78:2, 78:15-78:20).

## Метод, выборка и задачи

### Участники

Основная выборка состояла из **20 участников**, набранных через личные контакты, Twitter и Reddit. Авторы относят 15 участников к academia и 5 к industry; девять ранее использовали Copilot в разной степени, одиннадцать не использовали. Участников не оплачивали, но не имевшим Copilot после исследования предоставляли продолженный доступ к technical preview. Кандидатов, никогда не использовавших целевой язык, исключали (PDF 4-5; printed pp. 78:4-78:5).

Таблица участников показывает неоднородный, но не репрезентативный состав: профессора, postdoc, undergraduate и PhD students, software engineers, cybersecurity developer и founder. Самооценка опыта в языке имела категории Occasional, Regular и Professional; авторы предпочли её числу лет опыта (PDF 5; printed p. 78:5).

### Протокол

Сессия длилась около часа. Сначала участник выполнял короткую, позднее уточнённую как пятиминутную, тренировочную задачу для знакомства с code completion, natural-language prompts и multi-suggestion pane. Затем в течение примерно 20-40 минут он решал основную задачу с think-aloud, мог включать Copilot в привычный workflow, но не был обязан использовать его. После задачи проводилось semi-structured interview. Экран, речь и сессия записывались и транскрибировались (PDF 5, 24; printed pp. 78:5, 78:24).

Такой дизайн ориентирован на обнаружение поведенческих механизмов, а не на причинную оценку производительности. В нём нет рандомизированной control group, повторного выполнения одной задачи без Copilot или стандартизированного acceptance gate.

### Задачи

В ходе теоретической выборки использовались четыре задания (PDF 6-7; printed pp. 78:6-78:7):

| Задача | Языки | Содержание | Предоставлено / canonical solution |
|---|---|---|---:|
| Chat Server | Python или Rust | Реализовать business logic защищённого chat application с малой state machine; networking в основном предоставлен | 253/369 LOC; 61/83 LOC |
| Chat Client | Python или Rust | Реализовать networking с custom cryptographic API и стандартным, часто незнакомым socket API | 262/368 LOC; 52/84 LOC |
| Benford's Law | Rust и Python | Сгенерировать Fibonacci и reciprocal sequences, затем построить графики через незнакомый многим `matplotlib` | 9 LOC; 35 LOC |
| Advent of Code | Python, Rust, Haskell или Java | Строковая задача с точной спецификацией, тестовым примером и двумя независимыми подзадачами | 2-18 LOC; 29-41 LOC |

Chat Server и Chat Client требовали работы в созданной авторами существующей кодовой базе. Benford's Law был намеренно разделён на знакомую часть для acceleration и незнакомую API-часть для exploration. Advent of Code добавили для более подробного наблюдения validation на разных уровнях гранулярности (PDF 6-7; printed pp. 78:6-78:7).

### Grounded-theory процесс

Авторы следовали Straussian Grounded Theory. Они начали без готовой двухрежимной гипотезы, после каждой сессии размечали релевантные эпизоды с учётом речи, действий и body language и чередовали сбор и анализ данных. Первые два видео первые два автора кодировали совместно для согласования стиля; последующие видео кодировал один из них с обсуждением обоими (PDF 5-6; printed pp. 78:5-78:6).

После восьмой сессии паттерны начали складываться в acceleration и exploration. Затем авторы добавили третью задачу для проверки возникающей теории и четвёртую для изучения validation. К двадцатому участнику они объявили theoretical saturation: новые данные укладывались в теорию и не давали неожиданных наблюдений (PDF 6; printed p. 78:6).

После закрытия codebook все видео были повторно размечены фиксированным набором кодов для mode, prompting, validation и исхода подсказки (`accept`, `reject`, `repair`). Дополнительно один автор тем же закрытым codebook закодировал пять livestream с YouTube и Twitch: два Advent of Code и три web-development видео (PDF 15, 19; printed pp. 78:15, 78:19).

PDF не сообщает inter-rater reliability, число первоначальных кодов, формальную проверку saturation или inferential model для количественного сравнения режимов. Поэтому временные и частотные показатели следует читать как описательные характеристики размеченного корпуса, а не population prevalence или causal effects.

## Точный смысл groundedness

Термин требует разведения двух смыслов, чтобы не приписать статье лишний construct.

### Методологическая groundedness

Слово *Grounded* в названии прежде всего относится к **Grounded Theory**: категории и итоговая двухрежимная теория выводились итеративно из записей поведения и интервью, а задачи менялись посредством theoretical sampling. Это качественная укоренённость теории в наблюдаемых данных, а не метрика factual correctness или repository grounding модели (PDF 2, 5-6; printed pp. 78:2, 78:5-78:6).

### Контекстное grounding взаимодействия

Copilot строил inline suggestion по некоторому предшествующему содержимому файла у курсора, включая код и natural-language comments. Программисты создавали или меняли этот контекст кодом, именами, type signatures и специальными комментариями-промптами. В exploration они добавляли детали, переписывали комментарии после неудачных подсказок и иногда удаляли служебные комментарии после взаимодействия (PDF 3, 8, 11; printed pp. 78:3, 78:8, 78:11).

Однако видимость grounding была неполной. Участники не понимали, какой объём и какие части codebase видит Copilot, иногда ошибочно считали закомментированный код невидимым и хотели явно выбирать или изолировать context. Это поддерживает включение подготовки и контроля контекста в `h`, но не доказывает, что более длинный prompt или больший repository context повышает качество результата (PDF 20; printed p. 78:20).

Проверка результата создаёт отдельное, **человеческое grounding относительно intent и внешних опор**: участники сопоставляли код с ожидаемым паттерном, читали его построчно, исполняли программу и тесты, использовали REPL, static analysis и документацию. Повторение одного API pattern в multi-suggestion pane иногда повышало их уверенность, но авторы описывают это как восприятие участника, а не как калиброванную confidence модели; кроме того, они наблюдали anchoring на первой подсказке (PDF 9, 13-14; printed pp. 78:9, 78:13-78:14).

Следовательно, источник не даёт численной groundedness score. Для M0-M4 он даёт перечень процедур, которыми человек связывает предложение с задачей, кодовой базой, спецификацией и проверяемым поведением.

## Основные результаты

### Два режима и их условия

**Acceleration** возникает после того, как программист смог декомпозировать задачу на понятные microtasks. Программист остаётся «водителем», использует Copilot как intelligent autocomplete и предпочитает suggestion, совпадающий с текущей малой logical unit. Длина такой единицы зависит от языка и контекста: строка, вызов функции, аргументы или цикл. Знание алгоритма в наблюдениях было важнее одного лишь опыта языка или Copilot (PDF 7-8; printed pp. 78:7-78:8).

**Exploration** возникает при незнакомой задаче, API, способе декомпозиции или неожиданном поведении кода. Здесь Copilot участвует в поиске следующего шага: предлагает starting point, структуру, API или альтернативы. Склонность исследовать также связывалась с доверием и ожиданиями пользователя; чрезмерная уверенность могла приводить к over-reliance и малому прогрессу (PDF 10-11; printed pp. 78:10-78:11).

Это не простое деление задач на «лёгкие» и «трудные». Один и тот же участник переключается между режимами по мере того, как становится понятна или, наоборот, ломается текущая подзадача. Task familiarity, algorithmic understanding, language expertise, prior Copilot use и trust влияют на долю времени в режимах (PDF 7, 16-17; printed pp. 78:7, 78:16-78:17).

### Prompting и programmer actions

В закрытом codebook различались четыре способа вызова Copilot (PDF 17-18; printed pp. 78:17-78:18):

1. **Code prompt:** пользователь пишет код, а Copilot предлагает продолжение; с точки зрения пользователя вызов часто непреднамеренный.
2. **Context prompt:** suggestion появляется, когда пользователь не пишет новый код; для модели неотличим от code prompt, но отличается по user interaction.
3. **Comment prompt:** пользователь намеренно формулирует natural-language comment для Copilot.
4. **Multi-suggestion pane:** пользователь намеренно вызывает отдельную панель с вариантами.

В acceleration reported measure для code prompts равна 71.4%, для context prompts - 15.2%, для comment prompts - 13.1%. В exploration comment prompts использовались гораздо чаще: 57.2%; также возрастало использование multi-suggestion pane. Единица этой меры описана не вполне последовательно: основной текст называет её aggregate percentage of times, тогда как подпись и ось Figure 6 говорят о percentage of total prompting time. Поэтому числа следует использовать как описательную prevalence-характеристику размеченного корпуса, а не как точно определённую event probability, time share или оценку для произвольного разработчика (PDF 17-18; printed pp. 78:17-78:18).

Exploration менял обычный workflow: участники писали комментарии специально для Copilot, уточняли и переписывали их, а затем иногда удаляли как не имеющие документационной ценности. В multi-suggestion pane они сравнивали варианты, выбирали один, cherry-pick фрагменты нескольких, искали API как замену Stack Overflow и пытались судить об уверенности Copilot по повторяющимся patterns (PDF 11-13; printed pp. 78:11-78:13).

### Verification и repair

В acceleration подсказку часто быстро проверяли pattern matching по ожидаемым именам, control structures и общей форме. Не соответствующие ожиданию варианты быстро отклоняли; почти правильный короткий вариант могли принять и немедленно исправить, не выходя из flow (PDF 9-10; printed pp. 78:9-78:10).

В exploration проверка была более явной и содержала четыре стратегии (PDF 13-14; printed pp. 78:13-78:14):

1. examination кода, иногда построчное;
2. execution, tests или REPL на малом input;
3. IDE-integrated static analysis и type checking;
4. сверку с IDE или web documentation.

Static analysis работал в фоне, поэтому авторы не смогли точно хронометрировать время его использования. По остальным стратегиям exploration больше опирался на действия, поддерживающие comprehension, прежде всего examination и documentation; acceleration относительно чаще использовал execution для быстрого feedback. Это описательное различие, а не экспериментально назначенная validation policy (PDF 18; printed p. 78:18).

В exploration участники чаще принимали большой или неполный фрагмент как материал для дальнейшего редактирования, сохраняли control-flow skeleton, удаляли тела ветвей или постепенно ремонтировали suggestion. Обратная сторона: generated code мог быть труднее понять и отладить, чем собственный; в одном описанном случае участник не локализовал тонкую ошибку режима открытия файла и пошёл по неверной debugging trajectory (PDF 14-15; printed pp. 78:14-78:15).

### Временные и workflow evidence

В сумме по 20 участникам размеченное время взаимодействия с Copilot составило **248.6 минуты в exploration** и **104.7 минуты в acceleration**. Авторы связывают это с более медленным и deliberate характером exploration, но отношение `248.6/104.7` нельзя трактовать как slowdown: режимы не назначались случайно, exposure различался, а задачи специально менялись для сбора данных об обоих режимах (PDF 15-16; printed pp. 78:15-78:16).

Professional language users проводили относительно больше времени в acceleration. При примерно одинаковом total interaction time участники с prior Copilot usage меньше исследовали и больше ускорялись, чем новые пользователи. Chat Client и Benford's Law, содержащие незнакомые API, сдвигали всех участников к exploration; Chat Server с простой business logic - к acceleration. Для Python и Rust авторы не увидели заметного различия, а по Haskell и Java данных было слишком мало (PDF 16-17; printed pp. 78:16-78:17).

Длинные suggestions могли нарушать flow даже в acceleration. Трое участников, ранее отключивших Copilot, называли distractions от always-on suggestions одной из причин. Multi-suggestion pane также создавал cognitive load из-за отдельного окна и необходимости различать похожие варианты (PDF 9, 13; printed pp. 78:9, 78:13).

Пять livestream дали совместимые qualitative patterns: well-defined work чаще сопровождалась acceleration, exploratory work - comments и просмотром вариантов; streamers также применяли tests, examination и documentation. Классификация одного видео внутри статьи неоднозначна: Sec. 5.2.1 относит S5 к exploratory tasks, а Sec. 5.2.3 перечисляет S5 среди relatively well-defined tasks. Это дополнительная triangulation, но не независимая репрезентативная репликация: видео публичны, выборка мала, а кодировал их один автор (PDF 19-20; printed pp. 78:19-78:20).

### Outcomes, которые фактически измерены

Основной outcome - качественная теория поведения, а не productivity effect. Количественная часть описывает время в режимах, prompting strategies, validation activities и outcomes отдельных suggestions (`accept`, `reject`, `repair`). В статье нет treatment-control оценки completion time, success rate, quality-adjusted output или project makespan (PDF 15-18; printed pp. 78:15-78:18).

Поэтому формулировки «acceleration быстрее exploration» или «Copilot ускоряет в acceleration» в контексте M0-M4 нельзя превращать в численный `k`. Название режима отражает роль Copilot в уже спланированном action и наблюдаемую быстроту отдельных interactions, а не causal comparison полного task duration с baseline без ИИ.

## Как источник операционализирует `r`

В M0-M4 верхний уровень `r` различает interactive, delegated и autonomous organization. Barke et al. исследуют только **interactive Copilot**, но показывают, что этот label скрывает как минимум два существенно разных workflow state. Корректная операционализация может быть двухуровневой:

- верхний режим: `r = interactive-Copilot`;
- временной подрежим: `r_i(t) in {acceleration, exploration}`;
- observable features: способ prompting, scope suggestion, число просматриваемых альтернатив, validation policy, repair policy и способ управления context.

Если модели нужна одна метка на задачу, следует либо классифицировать её по преобладающему подрежиму, либо оценивать `k_i` и `h_i` для наблюдаемой смеси режимов. Более точный протокол размечает переходы во времени и суммирует человеческие интервалы по обоим состояниям. Barke et al. не дают коэффициентов для такого агрегирования, но дают codebook-level категории, по которым его можно спроектировать.

Содержательно режимы различаются так:

| Компонент `r` | Acceleration | Exploration |
|---|---|---|
| Состояние задачи | Следующий шаг и microtask понятны | Декомпозиция, API, алгоритм или причина ошибки неясны |
| Кто ведёт | Программист; Copilot завершает мысль | Copilot помогает планировать и искать варианты |
| Prompting | Преимущественно code/context prompts | Comment prompts и multi-suggestion pane |
| Scope | Малая logical unit | Альтернативы, большие snippets, skeletons |
| Validation | Быстрый pattern matching, rapid execution | Examination, execution/REPL, static analysis, documentation |
| Решение по suggestion | Быстро принять/отклонить, максимум малый repair | Сравнить, cherry-pick, принять и существенно редактировать |
| Workflow risk | Distraction и break of flow | Cognitive overload, anchoring, over-reliance, debugging чужого кода |

Это taxonomy поведения внутри интерактивной работы. Она не является taxonomy нескольких автономных agents и не задаёт рост `P`.

## Какие действия наполняют `h`

Источник наблюдает следующие виды активной человеческой работы, которые двухканальный хронометраж M0-M4 должен относить к `h_i^(r)`, если они причинно связаны с выполнением задачи:

1. понимание требования и декомпозиция задачи на microtasks;
2. выбор следующего code action и размера logical unit;
3. написание code, context и comment prompts;
4. уточнение prompt и подготовка видимого Copilot контекста;
5. вызов multi-suggestion pane, просмотр, сравнение и cherry-picking альтернатив;
6. чтение и pattern matching короткой подсказки;
7. подробное examination generated code;
8. принятие, отклонение или частичное принятие suggestion;
9. execution, написание/запуск tests и проверка через REPL;
10. чтение diagnostics static analyzer/type checker и принятие решения по ним;
11. сверка с IDE/web documentation;
12. editing, repair, удаление лишнего кода и заполнение skeleton;
13. debugging и локализация ошибки в generated code;
14. cleanup служебных comments после prompting;
15. восстановление flow после отвлекающей или длинной suggestion.

Не вся длительность сессии автоматически является `h`. Ожидание генерации, фонового анализа или tests относится к agent share `a`, если разработчик в этот момент действительно свободен и может обслуживать другой поток. Напротив, визуальное ожидание ответа при удержании внимания может остаться человеческим интервалом. Для этого различия нужен двухканальный event log; Barke et al. его не публикуют.

**Численное `h` выводить нельзя.** `248.6` и `104.7` минуты агрегированы по разным участникам, задачам и interaction states и не нормированы на baseline work `Z_i X`. Они не являются human shares. Counts prompting или validation также не задают длительность действий.

## Ограничения и угрозы применимости

Авторы прямо отмечают следующие ограничения (PDF 23-24; printed pp. 78:23-78:24):

1. Участники решали задания авторов, а не собственные проекты; знакомая codebase и отсутствие study time pressure могли бы изменить поведение.
2. Задания касались code authorship, а не систематического refactoring, testing, debugging и других стадий software engineering.
3. Выборка из 20 человек смещена к academia и не представляет всех программистов.
4. Одиннадцать участников ранее не использовали Copilot; пятиминутного обучения могло быть недостаточно, а новые пользователи иногда over-rely на инструмент.
5. Ранее использовавшие Copilot могли закрепить поведение на основе ранних, быстро менявшихся версий technical preview.
6. Наблюдение было кратким; longitudinal adaptation не изучалась.
7. Быстрое развитие code-generating models может ограничить перенос результатов на новые инструменты.

Для M0-M4 дополнительно важны следующие границы дизайна:

1. Нет control condition без Copilot, поэтому не идентифицируется `k`.
2. Нет двухканального хронометража active human и autonomous tool time, поэтому не идентифицируется `h`.
3. Нет concurrent agents, shared supervision queue, integration нескольких веток или переключения между агентными задачами.
4. Tasks короткие и искусственно подобраны для theoretical sampling; распределение режимов не является естественной workload mix production team.
5. Количественная часть преимущественно descriptive: PDF не приводит uncertainty intervals или inferential tests для mode-time и strategy differences.
6. Qualitative coding после первых двух видео в основном выполнял один coder; независимая agreement statistic не сообщается.
7. Livestream corpus self-selected и кодировался одним автором; он подтверждает узнаваемость паттернов, но не prevalence.
8. Tool snapshot относится к раннему inline Copilot/Codex, а не к современному repository-level autonomous coding agent.
9. Quality, maintainability, security, defect escape и downstream rework не измерены как outcomes.

## Mapping ко всем полям M0-M4

Здесь **direct descriptive support** означает, что источник непосредственно описывает механизм, но не обязательно измеряет модельный коэффициент; **conceptual support** - близкий механизм без нужной операционализации; **absent** - объект или варьирование отсутствуют.

| Поле модели | Статус | Соответствие в источнике | Точная граница |
|---|---|---|---|
| `Z_i` / `Z` | **conceptual support** | Четыре задачи различаются по знакомству с алгоритмом/API, структуре codebase и возможности декомпозиции; эти свойства меняют mode mix | Нет общей численной шкалы baseline complexity и no-AI времени `Z_i X`; LOC не эквивалентны `Z_i` |
| `k_i^(r)` | **conceptual support, численно absent** | Режим, task familiarity, expertise и validation workflow правдоподобно меняют полную длительность | Нет no-AI/control completion time и ratio `T_i^ai/(Z_i X)`; mode-time не является `k` |
| режим `r` | **direct descriptive support** | Acceleration и exploration с точными prompting, validation и repair patterns внутри interactive Copilot | Это динамические подрежимы одного interactive tool, а не сравнение interactive/delegated/autonomous configurations |
| `P` | **фиксирован концептуально как `P = 1`** | Один участник взаимодействует с одним Copilot над одной активной задачей | Multi-suggestion pane показывает альтернативы одного инструмента, а не до десяти одновременно работающих agents; `P` не варьируется |
| `W = X sum Z_i k_i` | **absent** | Есть несколько типов экспериментальных задач | Нет фиксированного проектного workload одного разработчика и суммируемых task weights |
| неделимость / `M_N` | **conceptual support** | Участники выделяют microtasks; scope suggestion и granular logical units влияют на flow | Нет parallel-machine scheduling, longest-job bound или фиксированного набора неделимых jobs |
| DAG / `L` | **conceptual support** | Декомпозиция, последовательность microtasks и две независимые подзадачи Advent of Code показывают внутреннюю структуру работы | Precedence edges, веса вершин и critical path формально не заданы и не измерены |
| `C(P)` | **absent** | Наблюдаются per-interaction overhead и сложности одного code context | Нет `P>1`, agent-agent integration, parallel branches, merge conflicts или зависимости overhead от `P` |
| `h_i^(r)` | **direct descriptive support состава, численно absent** | Наблюдаются planning, prompting, context preparation, review, validation, decision, editing, repair, debugging и cleanup | Активное человеческое время не нормировано на baseline и не отделено полностью от tool time; значение и доля `h` неизвестны |
| `H = X sum Z_i h_i` | **absent** | Публикуется pooled time по interaction modes | Pooled mode-time по участникам не является суммой human intervals фиксированного workload и не может использоваться как `H` |
| `gamma(P)` | **conceptual support только общего cognitive-cost mechanism** | Long suggestions нарушают flow; multi-suggestion pane создаёт cognitive load; пользователи переключаются между reading, writing и debugging | Это переключения внутри одной задачи/интерфейса, а не между `P` concurrent agent contexts; зависимость от `P` и `delta` не оценены |
| makespan | **absent как outcome M0-M4** | Core task выполнялась в ограниченной 20-40-минутной study phase; размечено interaction time | Нет стандартизированного project finish, control baseline, fixed multi-job workload или resource-feasible schedule; task completion time не анализируется как productivity outcome |

## Что источник поддерживает для M0-M4

1. **Интерактивный `r` неоднороден.** Даже в одном продукте и одной задаче программист переключается между acceleration и exploration; использование одного среднего `k_i^(interactive)` скрывает разные prompting, validation и repair workflows (PDF 7-15; printed pp. 78:7-78:15).
2. **Состав `h` шире prompting и final review.** В него входят декомпозиция, управление context, просмотр альтернатив, examination, tests/REPL, static-analysis feedback, документация, repair, debugging и cleanup (PDF 8-15; printed pp. 78:8-78:15).
3. **Task/mode-specific калибровка необходима.** Незнакомый API и неопределённость следующего шага сдвигают работу в exploration, тогда как понятные microtasks способствуют acceleration; expertise и prior use также меняют mode mix (PDF 8, 10, 16-18; printed pp. 78:8, 78:10, 78:16-78:18).
4. **Verification policy является частью режима.** Быстрый pattern matching и execution в acceleration отличаются от examination, documentation и редактирования в exploration; эти различия должны входить в definition и measurement protocol пары «задача - режим» (PDF 9, 13-14, 18; printed pp. 78:9, 78:13-78:14, 78:18).
5. **Grounding требует человеческих действий.** Подготовка контекста, уточнение prompts и проверка результата относительно intent/tests/docs создают observable human intervals; при этом пользователь не всегда знает, какой context использует модель (PDF 11, 13-14, 20; printed pp. 78:11, 78:13-78:14, 78:20).
6. **Большая генерация не равна меньшей человеческой работе.** Long suggestions могут прерывать flow, а accepted generated code - требовать понимания и сложной отладки; поэтому `h` нельзя оценивать по числу нажатий или объёму сгенерированного кода (PDF 9, 13-15; printed pp. 78:9, 78:13-78:15).

## Что источник не позволяет утверждать

1. Что Copilot ускоряет или замедляет full-task completion относительно работы без ИИ.
2. Что acceleration имеет численный `k<1`, а exploration - `k>1`: labels не являются treatment effects.
3. Что `248.6/104.7` измеряет relative productivity, `k`, human share или отношение длительностей одинаковых задач.
4. Что долю `h` можно вычислить из числа prompting/validation episodes или времени, агрегированного по режимам.
5. Что Copilot suggestion context является полным repository grounding или что статья измеряет groundedness score.
6. Что pattern repetition в multi-suggestion pane является calibrated model confidence.
7. Что decomposition причинно сокращает task duration, critical path `L` или makespan: стратегия не рандомизирована, формального DAG нет.
8. Что multi-suggestion pane представляет несколько агентов или `P>1`.
9. Что наблюдаемый cognitive load задаёт `gamma(P)` для concurrent agent streams.
10. Что источник оценивает `W`, неделимость, `C(P)`, `H`, project makespan, diminishing returns или оптимальное число агентов.
11. Что результаты раннего Copilot/Codex без новой проверки переносятся на delegated и autonomous coding agents.
12. Что mode proportions репрезентативны для production workload: задачи адаптировались в ходе theoretical sampling и выборка смещена к academia.

## Отличие от M0-M4

| Измерение | Barke et al. (2023) | M0-M4 |
|---|---|---|
| Центральный вопрос | Как программисты взаимодействуют с интерактивным Copilot | Когда `P>1` coding agents сокращают fixed-workload makespan |
| Тип исследования | Grounded-theory user study плюс descriptive recoding и livestream triangulation | Детерминированная scheduling/scalability model с внешней эмпирической калибровкой |
| Топология | Один programmer - один inline assistant - одна активная task | Один общий developer - до `P` параллельных agent streams |
| Режимы | Динамические acceleration/exploration внутри interactive use | Task-specific organizational `r`: interactive, delegated, autonomous и их варианты |
| Grounding | Наблюдаемое формирование context и human validation; grounded theory как метод | Не отдельный параметр; влияет на `k` и `h` через specification/verification workflow |
| Outcome | Поведенческая теория, mode time, prompting/validation/actions | Makespan, speedup и competing lower bounds |
| Baseline и `k` | No-AI baseline отсутствует | `k_i^(r)=T_i^ai(r)/(Z_i X)` |
| Работа человека | Подробно наблюдаемый состав действий | Явный `h_i`, capacity-1 сумма `H`, двухканальный timing |
| Структура задач | Экспериментальные tasks и participant-defined microtasks | Fixed jobs, неделимость, DAG и critical path `L` |
| Масштабирование | Не изучается | `P`, `C(P)`, `gamma(P)` и ресурсно допустимое расписание |

Barke et al. находятся **перед** scheduling layer M0-M4. Они дают эмпирическую taxonomy того, что происходит внутри одной интерактивной task duration и какие интервалы нужно увидеть при калибровке `r` и `h`. M0-M4 добавляет отсутствующие baseline complexity, fixed workload, concurrent agents, DAG, integration overhead, единый human resource и makespan objective.

## Проверенные claims для Related Work

1. В grounded-theory исследовании 20 участников, решавших четыре типа programming tasks на Python, Rust, Haskell и Java, Barke et al. выделили два динамических режима: acceleration, где программист уже знает следующий шаг и использует Copilot как completion, и exploration, где Copilot помогает искать следующий шаг, API или структуру решения (PDF 2, 4-7; printed pp. 78:2, 78:4-78:7).
2. Режимы отличались наблюдаемым workflow: reported prompting measure для code prompts в acceleration равна 71.4%, а для comment prompts в exploration - 57.2%; exploration также чаще включал multi-suggestion pane, подробное examination и documentation. PDF неоднозначно называет эту меру то долей вызовов, то долей prompting time, поэтому числа следует цитировать как descriptive prevalence, а не event probability (PDF 17-18; printed pp. 78:17-78:18).
3. Validation имела несколько человеческих форм: pattern matching, examination, execution/tests/REPL, static analysis и documentation; generated code также принимали частично, редактировали и отлаживали, причём участники иногда находили его труднее для debugging, чем собственный код (PDF 9, 13-15; printed pp. 78:9, 78:13-78:15).
4. Для M0-M4 работа поддерживает содержательную детализацию `r` и перечень действий внутри `h`, но не численную калибровку: в ней нет no-AI baseline, разделения human/agent time или variation in `P`, поэтому mode-time нельзя переводить в `k`, `h`, `gamma(P)` или multi-agent makespan (PDF 15-18, 23-24; printed pp. 78:15-78:18, 78:23-78:24).

## Короткий вариант встраивания в Related Work

> Barke, James и Polikarpova (2023) на основе grounded-theory исследования 20 участников показали, что работа с интерактивным GitHub Copilot чередуется между двумя режимами. В acceleration программист знает следующий шаг, использует преимущественно inline code completion и быстро проверяет короткие подсказки по ожидаемым patterns. В exploration Copilot участвует в поиске решения: пользователь пишет comment prompts, просматривает альтернативы, сверяет код исполнением, static analysis и документацией, затем редактирует или отлаживает результат. Для нашей модели эта taxonomy уточняет режим `r` и показывает, что в `h_i^(r)` должны входить декомпозиция, подготовка контекста, prompting, review, verification, repair и debugging. Однако исследование не сравнивает completion time с no-AI baseline, не разделяет человеческое и агентное время и рассматривает только одного интерактивного ассистента; поэтому оно не даёт численных `k` или `h` и не является evidence о scaling при `P>1`.

## Таблица доказательных страниц

| PDF | Printed | Раздел / объект | Опорное содержание |
|---:|---:|---|---|
| 1-2 | 78:1-78:2 | Title; Introduction; contribution | Библиография, DOI, вопросы об interaction, вклад grounded theory, краткое определение acceleration/exploration, 20 участников и четыре языка |
| 3-4 | 78:3-78:4 | Examples; Method | Inline context, intelligent autocomplete, explicit comment prompt, multi-suggestion pane, broad definition validation, состав sample |
| 5-7 | 78:5-78:7 | Participants; Protocol; GT; Tasks; Theory | Таблица участников, one-hour protocol, 20-40-minute core task, coding process, theoretical sampling/saturation, четыре задачи, fluid mode switching |
| 8-10 | 78:8-78:10 | Acceleration | Microtask decomposition, logical units, flow disruption, pattern-matching validation, accept/reject/minor repair |
| 10-15 | 78:10-78:15 | Exploration | Novelty/unexpected behavior, trust/over-reliance, comment prompts, context work, alternatives/cherry-picking, examination/execution/static analysis/docs, editing и debugging |
| 15-18 | 78:15-78:18 | Quantitative analysis | Closed recoding, `248.6` vs `104.7` minutes, expertise/prior use/task patterns, exact prompting percentages, validation differences и limitation static-analysis timing |
| 19-20 | 78:19-78:20 | Livestream analysis; recommendations | Пять streams, compatible behavior, testing/docs/examination, context uncertainty и запрос control over context |
| 21-22 | 78:21-78:22 | Recommendations | Mode-aware output, small logical units, cognitive load alternatives, suggestions with holes, always-on validation |
| 23-24 | 78:23-78:24 | Related Work; Limitations | Отличие от comparative task-time studies, designed tasks, authorship-only scope, academia-skewed sample, 11 novices, отсутствие longitudinal observation |
| 27 | 78:27 | Publication history | `Received 2022-10-28; accepted 2023-02-25` |

## Итоговая оценка источника

Barke et al. - сильный первичный источник для механизма интерактивной работы programmer-Copilot. Его главное значение для M0-M4 не в productivity effect, а в доказательном описании того, что label «interactive» скрывает acceleration и exploration с разными prompting, grounding, validation и repair workflows. Работа также даёт конкретный перечень активных действий разработчика, которые должны попадать в `h_i^(r)`.

Доказательная сила заканчивается до уровня multi-agent scheduling. Отсутствуют no-AI baseline, двухканальный timing, `P>1`, fixed project workload, DAG и makespan outcome. Поэтому корректная роль Barke et al. в статье - операционализировать `r`, grounding/verification и состав `h`, одновременно явно отказаться от вывода численных `k/h` и от любого переноса на multi-agent scaling без нового измерения.
