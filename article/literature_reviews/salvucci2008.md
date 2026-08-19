# Salvucci и Taatgen (2008): threaded cognition, concurrent multitasking и последовательный procedural resource

## Назначение и границы обзора

Этот документ разбирает Salvucci и Taatgen применительно к модели M0-M4 для fixed-workload makespan ячейки «один разработчик - `P` кодовых ИИ-агентов». Источник нужен прежде всего как когнитивная теория concurrent multitasking: несколько активных целей порождают автономные processing threads, разные ресурсы могут работать параллельно, но каждый отдельный ресурс обслуживает только один запрос за раз, а центральный procedural resource последовательно инициирует дальнейшую обработку.

Это сильная концептуальная опора для предположения M4 о разделяемом последовательном ресурсе и для качественного механизма interference при одновременном ведении нескольких контекстов. Однако статья не исследует разработчиков, программирование или ИИ-агентов, не оценивает project makespan и не даёт численных значений для `h`, `H` или `gamma(P)`.

Особенно важна терминологическая граница. Теория описывает преимущественно **concurrent interleaving** на субсекундном и секундном масштабе. Авторы прямо относят последовательное чередование задач и переключение между долгими проектами к соседней, но иной постановке task switching/interruption. Поэтому на Salvucci и Taatgen можно ссылаться как на источник serial procedural bottleneck, resource conflicts и interleaving, но не как на прямое доказательство линейного или вообще зависящего только от `P` switch penalty.

В локальном PDF 30 страниц издательской журнальной вёрстки. PDF-страницы 1-30 совпадают с печатными страницами 101-130. Ниже ссылки имеют вид «PDF / печатная страница».

## Библиография, версия и статус

**Проверенная ссылка:** Dario D. Salvucci and Niels A. Taatgen. “Threaded Cognition: An Integrated Theory of Concurrent Multitasking.” *Psychological Review* 115, no. 1 (2008): 101-130. DOI: [10.1037/0033-295X.115.1.101](https://doi.org/10.1037/0033-295X.115.1.101).

- Титульная страница указывает журнал, год, том, выпуск, страницы, APA copyright и DOI (PDF 1 / печ. 101).
- Crossref подтверждает тип `journal-article`, издателя American Psychological Association, том 115, выпуск 1 и страницы 101-130; связанный PDF обозначен как version of record.
- В конце статьи указаны даты: received 12 October 2006, revision received 1 August 2007, accepted 2 August 2007 (PDF 30 / печ. 130).
- **Статус:** опубликованная рецензируемая журнальная теоретико-модельная статья. Основное доказательство в ней состоит из полностью специфицированной computational theory и симуляций на данных ранее опубликованных экспериментов, а не из нового исследования с собственной выборкой участников.
- Финансирование: Office of Naval Research, гранты `N00014-03-1-0036` и `N00014-06-1-0055` (PDF 1 / печ. 101).
- Локальный файл: `salvucci2008.pdf`.
- SHA-256: `d67027614a14804e073009ed3975cede4fc9c1a582fab733344adc3e15091450`.
- Дата проверки: 2026-08-04.

## Исследовательский вопрос и заявленный вклад

Авторы не формулируют нумерованный RQ. Центральный вопрос можно восстановить из введения так: можно ли дать общую, domain-independent и вычислительно точную теорию concurrent multitasking, которая объясняет как интерференцию, так и отсутствие интерференции без специализированного executive process для каждой комбинации задач (PDF 1-2 / печ. 101-102).

Заявленный ответ - **threaded cognition**:

1. cognition поддерживает множество активных целей;
2. каждая цель порождает thread обработки по cognitive, perceptual и motor resources;
3. threads автономно запрашивают и освобождают ресурсы;
4. общий serial procedural resource разрешает только одно rule firing за раз;
5. конфликт между готовыми threads разрешается в пользу least recently processed thread;
6. concurrent behavior возникает без отдельного центрального supervisory executive (PDF 2, 7-12 / печ. 102, 107-112).

Вычислительный вклад состоит в реализации механизма в ACT-R. Авторы утверждают, что независимо построенные single-task models можно объединить как threads и получить непосредственные predictions для совместного выполнения. Эту общность они иллюстрируют четырьмя группами задач: dual choice, tracking plus choice, reading plus dictation и driving с несколькими secondary tasks (PDF 13 / печ. 113).

## Метод исследования

### Тип работы

Это не единый эксперимент и не meta-analysis. Метод сочетает:

- формулировку набора архитектурных assumptions;
- их computational instantiation в threaded ACT-R;
- повторное использование или адаптацию ранее разработанных component models;
- simulation runs для нескольких representative task domains;
- сравнение model output с опубликованными human data, обычно через графики, `R^2` и RMSE (PDF 4-26 / печ. 104-126).

Авторы выбрали четыре домена как иллюстративное покрытие нескольких осей: наличие или отсутствие dual-task interference, practice effects, laboratory versus real-world task и reuse/transfer модели. Это целенаправленная representative selection, а не систематическая выборка всех multitasking studies (Table 1, PDF 13 / печ. 113).

### Архитектурная основа

Computational framework основан на ACT-R и расширяет стандартный single-goal buffer до множества одновременно активных goals. Thread определяется как вся обработка в интересах одной цели, включая procedural rule firings и инициированные ими perceptual, motor и declarative processes (PDF 7-8 / печ. 107-108).

Важная методическая особенность: параметры не везде фиксировались одинаково. В dual-choice и tracking-choice models новые параметры для подгонки основных fits не оценивались; reading/dictation и driving models включали отдельные estimated или re-estimated timing/control parameters. Table 2 подробно перечисляет происхождение component models и parameter settings (PDF 26 / печ. 126). Поэтому высокие `R^2` показывают соответствие конкретным агрегированным кривым, но не являются единым out-of-sample test всей теории.

## Теория и архитектура ресурсов

### Набор ресурсов

Исходное предположение делит human processing resources на три широких класса (PDF 4 / печ. 104):

1. **cognitive resources**, обрабатывающие информацию и направляющие дальнейшее восприятие и действие;
2. **perceptual resources**, получающие информацию из внешней среды;
3. **motor resources**, выполняющие действия во внешней среде.

Cognitive resources дополнительно разделены на:

- **declarative resource**, хранящий factual knowledge как chunks и выполняющий retrieval;
- **procedural resource**, представляющий skill как goal-directed production rules, интегрирующий результаты других resources и инициирующий новые requests (PDF 4-6 / печ. 104-106).

В simulations явно используются visual и auditory perceptual resources и manual motor resource. Visual и auditory systems имеют собственные processing modules и buffers. Declarative module допускает только один retrieval request одновременно. Manual actions также проходят через отдельный serial resource; в tracking-choice model обе руки при этом представлены одним manual module (PDF 4-5, 16-17 / печ. 104-105, 116-117).

### Modules и buffers

Каждый resource представлен module, который выполняет обработку, и одним или несколькими buffers, через которые procedural resource получает результаты и отправляет новые requests. Resource считается занятым не только пока module выполняет process, но и пока его неиспользованный результат остаётся в buffer. Последующее production rule использует результат, очищает buffer и тем самым освобождает resource (PDF 4-5, 10-11 / печ. 104-105, 110-111).

Эта деталь важна для аналогии с агентным workflow: завершение автономной операции ещё не означает, что общий процесс может двигаться дальше. Результат может ждать последовательного consuming/decision step. Но в источнике речь идёт о когнитивном buffer и rule firing на миллисекундном масштабе, а не об очереди pull requests или окон human review.

### Serial procedural bottleneck

Procedural resource является центральным узлом архитектуры. Он сопоставляет доступные buffer contents и goals с production rules, после чего инициирует perception, retrieval или motor action. В ACT-R одно rule firing занимает 50 ms, и только одно rule может выполняться в каждый момент (PDF 5-6, 9-10 / печ. 105-106, 109-110).

При этом procedural resource **не занят непрерывно**. Thread чередует короткие procedural blocks с более длинной обработкой на peripheral resources. Пока один thread ждёт vision, audition, retrieval или motor completion, procedural resource может обслужить другой thread. Именно эти slack intervals позволяют concurrent tasks эффективно interleave и иногда достигать perfect time sharing (PDF 6, 8-11 / печ. 106, 108-111).

Последовательный procedural resource не является единственным возможным bottleneck. Interference может отдельно возникнуть на:

- declarative memory, когда threads одновременно требуют retrieval;
- visual или auditory resource, когда tasks используют один perceptual channel;
- manual или иной motor resource, когда responses конфликтуют;
- procedural resource, даже если perceptual и motor modalities различны (PDF 8-10, 12-13 / печ. 108-110, 112-113).

### Resource seriality и допустимый параллелизм

Сильное assumption теории гласит: каждый cognitive, perceptual и motor resource выполняет requests последовательно, по одному за раз. Одновременно авторы допускают два вида parallelism:

1. разные resources могут работать параллельно, например visual encoding одного thread и auditory encoding другого;
2. внутренняя реализация отдельного resource может включать parallel activity, но на выбранном уровне абстракции resource принимает только один request одновременно (PDF 9 / печ. 109).

Таким образом, threaded cognition не утверждает, что «человек целиком выполняет только одно действие». Она утверждает exclusive use каждого абстрактного resource при возможности параллельной работы разных resources. Это тоньше и менее ограничительно, чем scalar capacity-1 human resource в M4.

### Greedy, polite acquisition

Threads запрашивают ресурс **greedily**, то есть сразу, как только он нужен и может быть запрошен production rule, и освобождают его **politely**, как только processing и consumption результата завершены. Базовый механизм не планирует заранее будущие collisions, не задерживает request стратегически и не назначает явные task priorities (PDF 10-11 / печ. 110-111).

Авторы допускают, что explicit planning, interruption и priority control могут потребовать дополнительных supervisory threads или rules. Но такие deliberate strategies не являются частью базового greedy mechanism и не моделируются в основных demonstrations (PDF 10, 27 / печ. 110, 127).

### Разрешение procedural conflicts

Если несколько threads одновременно готовы выполнить production rule, procedural resource выбирает **least recently processed thread**. Политика должна:

- балансировать доступ к procedural processing;
- предотвращать starvation;
- при похожих resource profiles порождать естественное чередование threads;
- не мешать high-frequency thread часто выполняться, когда второй thread долго занят peripheral process (PDF 11 / печ. 111).

Это конкретный interleaving scheduler, а не switch-cost function. Он задаёт порядок обслуживания, но не вводит отдельный постоянный штраф за каждое переключение между thread identities.

### Learning и practice

На раннем этапе task instructions хранятся declaratively и многократно извлекаются interpreter rules. Production compilation постепенно превращает эти instructions в task-specific procedural rules. С практикой уменьшаются:

- число declarative retrievals;
- конфликты за declarative resource;
- общее число procedural steps;
- dual-task interference (PDF 7, 10, 12-15 / печ. 107, 110, 112-115).

Следовательно, interference является свойством не только pair of tasks, но и уровня skill/practice. Это противоречит интерпретации `gamma(P)` как постоянной, переносимой между пользователями и стадиями освоения workflow.

## Предсказания теории

Авторы формулируют семь ключевых claims и выводят из них следующие качественные predictions (PDF 12-13 / печ. 112-113):

1. Shared perceptual или motor resources обычно ухудшают performance одной или обеих задач.
2. Даже при разных perceptual/motor modalities возможна interference из-за procedural bottleneck.
3. Если procedural requests разнесены во времени и другие resources не конфликтуют, dual-task performance может совпасть с single-task performance.
4. Practice обычно уменьшает interference за счёт proceduralization и снижения declarative demand.
5. Точная interference зависит от temporal structure и resource profile задач, а не только от их числа.

Последний пункт особенно важен для M4. Увеличение `P` повышает число потенциальных collisions, но теория не выводит универсальную монотонную функцию потерь от количества threads. Два threads могут давать практически perfect time sharing, а один demanding secondary thread может создать сильную interference.

## Валидационные домены, задачи и model fit

Статья не проводит новые participant studies. Она моделирует данные ранее опубликованных экспериментов и в отдельных случаях переносит ранее валидированные component models в новую concurrent configuration.

| Домен | Данные и task | Механизм в модели | Reported fit и граница |
|---|---|---|---|
| Dual choice | Schumacher et al. (2001): visual-manual и aural-vocal choice, single/dual task, practice и PRP variants | Novice interference в основном из-за declarative retrievals; после compilation возможен perfect time sharing; priority instruction меняет initiation threads | Exp. 1 `R^2=.96`, RMSE `.026`; PRP Exp. 2 `R^2=.95`, RMSE `.016`; incongruent mapping Exp. 3 `R^2=.98`, RMSE `.020` (PDF 14-16 / печ. 114-116). Новые fit parameters для dual-choice model не оценивались по Table 2 |
| Tracking plus choice | Continuous cursor tracking easy/hard плюс occasional left/right arrow at varying visual offset, данные Martin-Emerson и Wickens (1992) | Threads конфликтуют за visual и manual resources; choice temporarily delays tracking | Tracking error `R^2=.97`, RMSE `.68`; choice response time `R^2=.74`, RMSE `.06` (PDF 16-18 / печ. 116-118). 16 simulation trials на offset-condition, без estimated architectural parameters |
| Reading plus dictation | Spelke, Hirst и Neisser (1976): два участника, 85 days, reading stories while writing dictated words | Novice dictation требует declarative retrieval для letters; compilation сокращает interference; после spoken word остаются длинные intervals для reading | Human reading приблизилась к single-task speed; model: 298 words/min single, 229 Week 1 dual, 270 Week 6 dual. Fit показан на normalized curves без `R^2`/RMSE (PDF 18-20 / печ. 118-120). Данные шумные, всего два участника; model содержит estimated timing/learning parameters |
| Driving plus choice | Levy, Pashler и Boer (2006): continuous following/steering, discrete choice и braking at different SOA | Procedural collisions задерживают braking; visual condition также конкурирует с driving vision | SOA reaction times `R^2=.97`, RMSE `.04`; modality comparison `R^2=.95`, RMSE `.04` (PDF 20-22 / печ. 120-122). Driver model re-estimated по нескольким control parameters и добавлен voice-recognition delay |
| Driving plus phone dialing | Salvucci (2001b): seven-digit full/speed, manual/voice dialing while simulated driving | Manual dialing делит visual/manual resources с driving; voice conditions избегают основного perceptual-motor conflict | Dialing time `R^2=.99`, RMSE `.49`; lateral velocity `R^2=.96`, RMSE `.02` (PDF 22-24 / печ. 122-124). Driving stability parameter re-estimated; component dialing model перенесён из прежней работы |
| Driving plus sentence span | Alm и Nilsson (1995): car following/braking плюс listening, sensibility judgments, memorization/rehearsal и recall | Частые rule firings и rehearsal создают прежде всего procedural/declarative cognitive contention без основного perceptual-motor overlap | Human brake-time increment `.56 s`, model `.54 s`; absolute times расходятся: data около `1.6/2.2 s`, model `1.00/1.54 s`. Model reproduces no lateral-position effect (`.19 m` driving only, `.18 m` dual; PDF 24-26 / печ. 124-126) |

### Что показывают fits

1. Одна architecture может воспроизводить qualitatively different regimes: interference, no interference и practice-dependent reduction.
2. Источник разделяет причины interference по resource type, а не объединяет их в один общий overhead.
3. Перенос component models между domains демонстрирует заявленную compositionality хотя бы на выбранных задачах.
4. Driving plus sentence span показывает procedural interference даже без выраженного perceptual/motor conflict: braking response замедляется, хотя lane position почти не меняется (PDF 25-26 / печ. 125-126).

### Что fits не доказывают

1. Домены выбраны авторами как illustrative representative set, а не preregistered exhaustive test.
2. Показатели fit рассчитаны для разных outcomes и datasets; их нельзя агрегировать в единый effect size.
3. Часть models и parameters была ранее валидирована, часть адаптирована, часть estimated/re-estimated для текущей simulation. Это не единый чистый holdout test.
4. Высокий `R^2` на агрегированных curves не гарантирует правильность trial-level process или уникальность механизма.
5. Reading/dictation опирается на старое исследование с двумя участниками и шумными summary data.
6. В sentence-span domain model хорошо воспроизводит **increment**, но заметно недооценивает оба absolute braking times; авторы прямо признают расхождение и отсутствие объяснения различия baseline между studies (PDF 25 / печ. 125).
7. Ни один fit не относится к minute-to-hour software work, developer context recovery или нескольким автономным agents.

## Task switching, interleaving и interruption

### Что теория объясняет напрямую

Threaded cognition непосредственно объясняет fine-grained **interleaving** concurrent tasks. Переключение procedural processing возникает, когда readiness разных threads чередуется или несколько threads одновременно претендуют на serial procedural resource. Delay появляется из-за ожидания занятого resource, включая procedural, declarative, visual, auditory или motor resource (PDF 8-13 / печ. 108-113).

Такой mechanism близок к очереди у общего human decision channel. Если два agent contexts одновременно требуют интерпретации или решения разработчика, один должен ждать. Если один context ждёт автономной операции, человек может обслужить другой.

### Что находится вне прямого охвата

В General Discussion авторы ограничивают основную теорию nondeliberative concurrent multitasking на субсекундном и секундном масштабе. Они прямо не предназначают её для переключения между work projects на протяжении минут или часов (PDF 27 / печ. 127).

Последовательное alternating task switching также не считается threaded case. Для него model должен явно менять control state, вероятно через memory retrieval или другую costly cognitive operation. Авторы ссылаются здесь на отдельные ACT-R accounts task-switch costs, но сами не выводят и не валидируют универсальную switch-cost model (PDF 28 / печ. 128).

Interruption/resumption обсуждается как совместимое расширение. Исходный task thread может поддерживать goal activation через rehearsal либо потерять context и затем восстановить его retrieval. Однако это conceptual discussion на основе Trafton et al. и Altmann/Trafton, а не отдельная simulation или новый experiment данной статьи (PDF 28 / печ. 128).

### Следствие для `gamma(P)`

Для M4 источник поддерживает только механизм, из которого **может** возникать дополнительное человеческое время:

- ожидание serial procedural resource;
- повторное извлечение task/control state;
- interference в declarative memory;
- задержка из-за совпадения perceptual или motor demands;
- дополнительное planning/rehearsal как отдельная cognitive work.

Но источник не поддерживает следующие свойства рабочей формы M4:

- что penalty является только функцией числа agents `P`;
- что `gamma(P)` обязательно монотонна для фиксированного workload;
- что penalty мультипликативно масштабирует всё `H`;
- что `gamma(P)=1+delta(P-1)`;
- что один дополнительный agent создаёт одинаковую marginal loss независимо от temporal overlap, modality, task similarity, practice и interruption pattern.

В терминах threaded cognition более естественной была бы event- или resource-level model: стоимость определяется числом и расположением collisions, требованиями retrieval/resumption и overlap resource profiles. Агрегат `gamma(P)H` может использоваться как coarse empirical approximation, но его форму и параметры нужно оценивать отдельно на coding workflow.

## Mapping ко всем полям `Z,k,r,W,P,L,C(P),h,H,gamma(P)`

Здесь **direct theory** означает объект, прямо заданный архитектурой источника; **structural analogy** - близкую роль при другой семантике и временном масштабе; **absent** - отсутствие соответствующего объекта.

| Поле M0-M4 | Статус | Соответствие у Salvucci и Taatgen | Точная граница |
|---|---|---|---|
| `Z_i` / `Z` | **absent** | Task models содержат последовательности production, resource timings и environmental events | Нет baseline complexity software job, нормированной единицы `X` или конечного набора project tasks |
| `k_i^(r)` / `k` | **absent** | Есть single-task и dual-task performance, reaction times, reading speed, tracking/driving measures | Нет AI/no-AI duration ratio и единого wall-clock coefficient; outcomes неоднородны |
| режим `r` | **structural analogy** | Task representation, modality, priority instruction, skill level и practice меняют resource usage/interference | Это не taxonomy interactive/delegated/autonomous coding mode и не параметр одной пары task-tool-workflow |
| `W = X sum Z_i k_i` | **absent** | Threads имеют local process timelines | Нет additive fixed project workload или суммы AI-weighted task durations |
| `P` | **partial structural analogy** | Число одновременно active threads/goals | Thread не равен coding agent: одна complex task может иметь несколько threads, а один agent context может порождать несколько human goals; большинство validations dual-task |
| `L` | **absent** | Внутри thread есть procedural sequence и causal order resource requests | Нет project DAG, weights vertices или critical-path makespan bound |
| `C(P)` | **absent** | Есть human cognitive/perceptual/motor resource contention | Нет agent-agent integration, merge conflicts, shared code coherency или multiplicative overhead на `W/P`; такую interference следует относить к human side, не к `C(P)` |
| `h_i^(r)` / `h` | **conceptual support** | Procedural, declarative, perceptual и motor processing описывают состав active human work | Source не агрегирует их в одну non-overlapping duration и не нормирует на `Z_i X`; разные resources могут работать параллельно |
| `H = X sum Z_i h_i` | **structural analogy, ограниченная** | Serial procedural processing across threads создаёт общий capacity-1 channel; другие resources также exclusive-use по отдельности | Нет total human service fixed workload. Scalar `H` объединяет ресурсы, которые theory намеренно разделяет и частично допускает выполнять параллельно |
| `gamma(P)` | **conceptual mechanism only** | Resource collisions, declarative retrieval, control-state recovery и interleaving могут создавать delay | Нет функции от `P`, multiplicative form, monotonicity, coding calibration или minute-hour validation; concurrent threading и sequential task switching разведены авторами |
| makespan | **absent** | Есть completion/reaction times отдельных laboratory events и continuous performance | Нет срока завершения фиксированного набора jobs под DAG, agents и shared developer |

### Mapping по уровням M0-M4

| Уровень | Что источник добавляет к интерпретации | Что отсутствует |
|---|---|---|
| M0 | Разные task processes могут частично выполняться параллельно на разных resources | Нет идеально делимой работы, `W/P`, baseline и `k` |
| M1 | Exclusive-use resource создаёт waiting даже при независимых threads | Нет finite indivisible jobs, machine assignment и longest-job bound |
| M2 | Within-thread order показывает, что temporal structure влияет на overlap | Нет inter-task DAG и `L`; active goals не являются project vertices |
| M3 | Resource contention показывает общий принцип diminishing effective parallelism | Нет agent-agent `C(P)`; observed interference находится внутри human cognitive architecture |
| M4 | Serial procedural resource, waiting buffers и interleaving дают наиболее сильную теоретическую аналогию shared human bottleneck | Нет scalar fixed-workload `H`, explicit human windows software tasks и проверенной `gamma(P)`; M4 грубее объединяет несколько distinct human resources |

## Что источник поддерживает для нашей статьи

1. **Concurrent multitasking не равно полному параллелизму.** Несколько active goals могут продвигаться одновременно только постольку, поскольку их resource demands не конфликтуют (PDF 2-3, 8-13 / печ. 102-103, 108-113).
2. **Есть общий serial procedural bottleneck.** Cognition обрабатывает results и инициирует new resource requests только для одного thread за раз (PDF 9-10 / печ. 109-110).
3. **Ожидание может возникать после завершения peripheral work.** Result остаётся в buffer до consuming production rule, что является полезной аналогией очереди результатов, ожидающих developer review (PDF 4-5, 10-11 / печ. 104-105, 110-111).
4. **Parallel slack реален.** Пока один thread ожидает perception, memory или motor process, procedural resource может продвинуть другой; поэтому one-human-many-streams architecture не обязана быть полностью последовательной (PDF 6, 8-11 / печ. 106, 108-111).
5. **Interference зависит от resource profile и timing.** Shared modality, simultaneous readiness и frequency procedural steps важнее одного числа active tasks (PDF 8-13, 26 / печ. 108-113, 126).
6. **Perfect time sharing иногда возможно.** При разных resources и удачном temporal interleaving dual-task performance может приблизиться к single-task performance (PDF 13-15 / печ. 113-115).
7. **Practice меняет interference.** Proceduralization снижает declarative retrieval и procedural demand; capacity нельзя считать постоянной характеристикой только человека или набора задач (PDF 7, 10, 12-15 / печ. 107, 110, 112-115).
8. **Cognitive interference возможна без perceptual/motor conflict.** Driving plus sentence span замедлял brake response преимущественно через частые cognitive steps (PDF 24-26 / печ. 124-126).
9. **Базовое interleaving может возникать без explicit executive scheduler.** Greedy/polite threads и least-recently-processed policy дают parsimonious mechanism для routine concurrent performance (PDF 10-12 / печ. 110-112).
10. **Fine-grained interleaving и long-horizon switching нужно разводить.** Сами авторы ограничивают scope и отправляют task switching/interruption к дополнительным memory/control mechanisms (PDF 27-28 / печ. 127-128).

## Что источник не позволяет утверждать

1. Что Salvucci и Taatgen исследовали программирование, разработчиков, ИИ или autonomous agents.
2. Что `P` threads численно равно `P` coding agents или что study варьирует useful agent fan-out.
3. Что serial procedural resource доказывает полную последовательность **всей** человеческой работы: разные perceptual, motor и cognitive resources могут работать параллельно.
4. Что procedural rule-firing time 50 ms можно использовать как стоимость developer decision, review или context switch.
5. Что сумму procedural blocks можно непосредственно принять за `H` или `h_i Z_i X`.
6. Что `gamma(P)` зависит только от количества потоков. В source interference зависит от temporal overlap, resource modality, learned representation и practice.
7. Что `gamma(P)` монотонна, линейна или мультипликативна по отношению ко всему `H`.
8. Что least-recently-processed policy моделирует priority scheduling, strategic batching, deliberate interruption management или оптимальное распределение developer attention.
9. Что высокие model fits являются независимой coding-agent calibration или universal validation всех resource assumptions.
10. Что отсутствие interference в trained dual-choice case переносится на unfamiliar software contexts. Теория сама предсказывает большую declarative interference на раннем этапе learning.
11. Что paper оценивает fixed-workload project makespan, throughput, quality, `Z`, `k`, `W`, DAG/`L` или agent-agent `C(P)`.
12. Что concurrent threading является общей теорией классического task-switch cost. Авторы прямо выводят sequential alternation за основной scope.
13. Что minute-to-hour context restoration между repositories, tickets или agents эмпирически проверен в этой статье.
14. Что добавление agents обязательно вызывает slowdown. Теория допускает и interference, и near-perfect sharing в зависимости от resource/time structure.

## Отличие от fixed-workload coding-agent model

| Измерение | Salvucci и Taatgen (2008) | M0-M4 |
|---|---|---|
| Центральный вопрос | Как multiple cognitive task threads concurrently используют serial resources и когда возникает interference | Когда один разработчик с `P` coding agents сокращает makespan fixed workload |
| Единица анализа | Active goal/thread и production/resource event | Software task `i`, agent work stream и project schedule |
| Временной масштаб | Преимущественно subsecond-to-seconds nondeliberative multitasking | Минуты, часы и дни task execution/review/integration |
| Parallelism | Между distinct cognitive, perceptual и motor resources | Между agent executors; human intervals capacity 1 |
| Shared bottleneck | Procedural resource плюс отдельные serial declarative/perceptual/motor resources | Один агрегированный developer resource `H`, умноженный на `gamma(P)` |
| Interference | Event-level collision конкретных resource requests | Aggregate switch multiplier `gamma(P)` и отдельно integration multiplier `C(P)` |
| Scheduling policy | Greedy/polite acquisition, least recently processed procedural thread | Agent assignment, DAG feasibility и explicit non-overlap human windows |
| Learning | Production compilation меняет demand и interference | Параметры `k_i^(r)`, `h_i^(r)` калибруются внешне; learning пока не моделируется динамически |
| Work structure | Process timelines внутри cognitive tasks | Fixed set of indivisible jobs, DAG и critical path `L` |
| Outcomes | Reaction time, tracking error, reading speed, driving performance | Project makespan и speedup относительно no-AI sequential baseline |
| Empirical basis | Simulations against prior laboratory/driver studies | Детерминированная formal model, требующая coding-specific estimates |

Главное содержательное различие для M4: Salvucci и Taatgen моделируют **несколько разделяемых ресурсов и точные моменты их запросов**, тогда как M4 сворачивает человеческую сторону в scalar capacity-1 total `H` и aggregate multiplier `gamma(P)`. Такое свёртывание делает M4 применимой к project scheduling, но теряет возможность предсказать, когда разные виды human processing реально перекрываются и какие именно collisions создают delay.

## Проверенные claims для Related Work

1. Threaded cognition представляет concurrent tasks как goal-related processing threads, координируемые serial procedural resource и распределённые по отдельным declarative, perceptual и motor resources (PDF 2, 4-12 / печ. 102, 104-112).
2. Каждый resource в теории обслуживает один request за раз, но разные resources могут работать параллельно; поэтому interference возникает при resource conflict, а при temporal separation requests возможно perfect time sharing (PDF 8-13 / печ. 108-113).
3. Threads greedily acquire и politely release resources, а procedural conflict разрешается в пользу least recently processed thread; отдельный supervisory executive для routine concurrent execution не требуется (PDF 10-12 / печ. 110-112).
4. Production compilation снижает dependence на declarative instructions и тем самым уменьшает declarative и procedural interference с practice (PDF 7, 10, 12-15 / печ. 107, 110, 112-115).
5. Simulations охватывают dual choice, tracking-choice, reading-dictation и driving secondary tasks и воспроизводят как interference, так и его отсутствие; reported fits варьируются от `R^2=.74` до `.99` для outcomes, где `R^2` приведён (PDF 13-26 / печ. 113-126).
6. Driving-sentence-span model воспроизводит magnitude дополнительной brake delay (`.54 s` против `.56 s` в data), но не absolute reaction times, что ограничивает интерпретацию fit (PDF 25 / печ. 125).
7. Авторы ограничивают основную theory nondeliberative concurrent multitasking на subsecond-second scale и не относят к ней long-project switching или последовательное alternating task switching (PDF 27-28 / печ. 127-128).
8. Для M0-M4 источник поддерживает serial human decision/interleaving mechanism, но не numerical `h`, `H`, `gamma(P)`, coding-agent `P` или fixed-workload makespan.

## Вариант встраивания в Related Work

> Когнитивный механизм concurrent supervision можно связать с теорией threaded cognition Salvucci и Taatgen (2008). В ней несколько active goals порождают автономные processing threads, которые могут выполняться параллельно на разных perceptual, motor и memory resources, но каждый отдельный resource обслуживает только один request за раз. Центральный procedural resource последовательно обрабатывает результаты и инициирует дальнейшие действия; при одновременной готовности threads применяется least-recently-processed interleaving. Симуляции dual-choice, tracking, reading/dictation и driving tasks воспроизводят как interference, так и near-perfect time sharing, показывая зависимость потерь от temporal overlap, shared resources и practice. Это даёт теоретическую опору для capacity-1 human bottleneck в M4 и для существования context/interference overhead. Однако источник работает на субсекундном и секундном масштабе, прямо отделяет concurrent threading от последовательного task switching и не изучает coding agents. Поэтому он не калибрует `H` или `gamma(P)` и не обосновывает линейную форму `gamma(P)=1+delta(P-1)`; эти параметры должны оцениваться на developer-agent workflows.

### Более короткая вставка

> Salvucci и Taatgen (2008) моделируют concurrent multitasking как interleaving нескольких goal threads через serial procedural resource при возможной параллельной работе distinct perceptual, motor и memory resources. Теория объясняет и interference, и perfect time sharing в зависимости от overlap resource demands и practice, что поддерживает идею общего последовательного человеческого bottleneck. Но она не является численной моделью coding-agent supervision: авторы ограничивают основной scope subsecond-second concurrent behavior и отделяют его от долгих task switches, поэтому значения и форма `gamma(P)` требуют отдельной эмпирической калибровки.

## Таблица опорных страниц

| PDF | Печатная | Раздел / объект | Опорное содержание |
|---:|---:|---|---|
| 1 | 101 | Title; Abstract; Introduction | Библиография, DOI, funding; определение threaded cognition; serial procedural resource; perceptual/motor resources; заявка на interference predictions |
| 2 | 102 | Introduction; Threaded Cognition | Критика domain-specific executives; multiple active goals; ACT-R implementation; no supervisory executive claim |
| 3 | 103 | Cooking analogy | Parallel peripheral processes; conflicts за cook/procedural resource и другие resources; waiting delays |
| 4 | 104 | Single-task assumptions | Cognitive/perceptual/motor resources; modules и buffers; procedural/declarative split; declarative request seriality |
| 5-6 | 105-106 | Resource details; choice example | Visual/auditory/manual resources; production rules; 50-ms procedural firing; alternating procedural/peripheral blocks и slack |
| 7 | 107 | Procedural learning; threaded processing | Production compilation; declarative load у novices; multiple active goals и definition of thread |
| 8 | 108 | Thread examples | Resource conflict versus perfect time sharing; complex task может включать несколько threads |
| 9-10 | 109-110 | Resource Seriality; Resource Usage | Один request на resource; serial procedural bottleneck; distinct resource parallelism; greedy/polite acquisition |
| 11 | 111 | Conflict Resolution | Buffer release; least recently processed policy; fairness, alternation и no starvation |
| 12-13 | 112-113 | Key Claims and Predictions; Model Simulations | Семь claims; predictions interference/no interference/practice; четыре validation domains и Table 1 |
| 14-16 | 114-116 | Dual choice | Novice declarative interference, practice, perfect time sharing, PRP and incongruent mapping fits |
| 16-18 | 116-118 | Tracking and choice | Continuous/discrete dual task; visual/manual conflicts; `R^2=.97/.74`; отсутствие explicit switching rules |
| 18-20 | 118-120 | Reading and dictation | Two participants, 85 days; practice-dependent reading recovery; model speeds и normalized comparison |
| 20-22 | 120-122 | Driving and choice | Imported driver model; PRP-like braking delay; modality effects; `R^2=.97/.95` |
| 22-24 | 122-124 | Driving and dialing | Manual versus voice resource conflict; dialing time and lateral velocity fits `R^2=.99/.96` |
| 24-26 | 124-126 | Driving and sentence span; simulation summary | Procedural cognitive contention; `.56/.54 s` increment; absolute-time mismatch; Table 2 model origins/parameters |
| 27 | 127 | General Discussion | Implications; no executive; procedural/declarative interference; scope subsecond-second; deliberate priorities as extra processing |
| 28 | 128 | Task switching; interruption | Long projects and alternating switches outside direct scope; control-state retrieval; interruption/resumption discussion |
| 30 | 130 | References; publication history | Received, revised и accepted dates |

## Итоговая оценка релевантности

Salvucci и Taatgen - сильный первичный теоретический источник для архитектурной интуиции M4. Он показывает, как несколько concurrent goals могут продвигаться через общий serial procedural channel, почему результаты ждут consuming step, когда parallel slack позволяет interleaving и почему shared memory/perceptual/motor resources создают дополнительные delays. Особенно полезна демонстрация, что interference не является неизбежной константой: она зависит от task representation, совпадения resource requests, timing и practice.

Одновременно этот источник слабее, чем иногда предполагает формулировка «теория переключения контекста». Основная theory не описывает minute-to-hour switching между coding tasks и прямо отделяет concurrent threading от sequential task switching. Она также представляет человека как несколько отдельных resources, а не как один scalar server. Поэтому корректная роль статьи - обосновать serial procedural bottleneck и возможные cognitive interference/resumption mechanisms, но оставить `h`, `H` и `gamma(P)` эмпирическими coding-specific параметрами. Для прямого обоснования switch/resumption costs на длинном масштабе Salvucci и Taatgen следует дополнять отдельной литературой по task switching и interruption, а не выдавать их simulations за такую калибровку.
