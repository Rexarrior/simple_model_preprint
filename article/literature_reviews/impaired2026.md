# Balepur et al. (2026): coding agents, краткосрочная продуктивность и ухудшение понимания кода

## Назначение и границы обзора

Этот документ разбирает Balepur et al. применительно к модели M0-M4 для fixed-workload makespan звезды «один разработчик - `P` coding agents». Работа релевантна прежде всего режиму взаимодействия `r`, составу человеческой работы `h`, совместному измерению времени и качества, а также гетерогенности по пользователю, задаче и способу использования инструмента.

Главная граница переноса: исследование сравнивает одного студента с одним агентом, напрямую редактирующим код, и одного студента с намеренно ограниченным chatbot, который даёт только общие подсказки по синтаксису. Оно не содержит no-AI arm, не варьирует число одновременно работающих агентов и не измеряет двухканально human/agent time. Поэтому работа не даёт численных `k`, `h`, `H`, `C(P)` или `gamma(P)` и не является evidence о масштабировании при `P>1`.

Локальный PDF содержит 39 страниц. Основной текст занимает PDF-страницы 1-9, references - 9-14, appendix - 15-39. Номера ниже относятся к PDF-страницам локальной копии.

## Библиография, статус и версия

**Заголовок:** “(Im)Paired Programming: Coding Agents Improve Productivity but Harm Understanding”.

**Авторы на титульной странице PDF:** Nishant Balepur, Connor Baumler, Valerie Chen, Eunsol Choi, Rachel Rudinger, Jordan Boyd-Graber. Metadata arXiv раскрывает имя последнего автора как `Jordan Lee Boyd-Graber`.

**Аффилиации:** University of Maryland, New York University и Carnegie Mellon University (PDF с. 1).

**Полная ссылка:** Nishant Balepur, Connor Baumler, Valerie Chen, Eunsol Choi, Rachel Rudinger, and Jordan Lee Boyd-Graber. “(Im)Paired Programming: Coding Agents Improve Productivity but Harm Understanding.” arXiv:2607.26375v1 [cs.CL], 2026. DOI: [10.48550/arXiv.2607.26375](https://doi.org/10.48550/arXiv.2607.26375).

**Проверенная версия:** arXiv `2607.26375v1`, подана 29 июля 2026 года. Основная категория - `cs.CL`, дополнительная - `cs.HC`. На 4 августа 2026 года submission history содержит только v1.

**Статус:** arXiv помечает работу как `In-progress Preprint`. В PDF нет сведений о принятии на конференцию или о рецензируемой публикации. Упоминание треков EMNLP 2026 во введении описывает контекст области, а не publication status. Поэтому источник нельзя обозначать как peer-reviewed или accepted.

**Лицензия:** arXiv указывает CC BY 4.0.

**Проверка локальной копии:** SHA-256 локального файла `impaired2026.pdf` равен `774a575510539b7ca3b7b3e91927eccb67fae537e86a23ea455841c3f5ae5e30` и полностью совпадает с SHA-256 PDF `https://arxiv.org/pdf/2607.26375v1`. Следовательно, обзор относится именно к arXiv v1.

## Предмет работы и смысл “(Im)Paired”

Работа изучает не общее «ухудшение программирования» и не замедление coding agents. Её предмет - компромисс между краткосрочным task completion и пониманием пользователем кода, который за него пишет агент.

Слово `(Im)Paired` в названии является игрой с `paired programming` и `impaired`. В доказательной части `impaired` означает прежде всего **более слабое понимание собственного кода** у пользователей агента по сравнению с пользователями ограниченного chatbot. Это проявляется в recall и reasoning questions. Авторы также связывают более слабое понимание с меньшей готовностью расширять код без агента, но общий эффект treatment на extension accuracy статистически не отличался от нуля (PDF с. 1, 5-6, 16, 20-21).

Поэтому некорректны формулировки:

- «агенты ухудшили продуктивность» - в initial task агентная группа была быстрее и точнее;
- «агенты доказанно ухудшили последующее выполнение» - общий extension outcome между группами существенно не различался;
- «понимание снизилось относительно состояния до AI» - pretest понимания собственного будущего кода невозможен и не проводился; causal contrast относится к agent arm против constrained-chatbot arm;
- «пользователи работали без AI в extension task» - агент был убран, но обе группы получили ограниченный chatbot.

## Исследовательские вопросы

Два явных вопроса study design (PDF с. 2):

1. Понимают ли пользователи код, созданный при помощи AI agent?
2. Могут ли пользователи расширить свой первоначальный код без AI agent?

Дополнительные аналитические вопросы:

- как background programming ability связано с initial accuracy, comprehension и extension accuracy;
- объясняют ли initial code accuracy и comprehension последующее extension performance;
- какие prompting и review strategies связаны с comprehension;
- какие свойства сгенерированного кода связаны с comprehension;
- совпадают ли субъективные оценки полезности и понимания с измеренными outcomes;
- какие design interventions могут удержать пользователя активно вовлечённым.

Тип доказательства - randomized between-subjects online user study для основного contrast и exploratory observational analyses внутри agent arm для механизмов.

## Выборка и рекрутинг

Авторы набрали 59 CS students из двух американских университетов: 17 B.S., 31 M.S. и 11 Ph.D. После attention checks из анализа исключили пять человек. Итоговая выборка - 54 участника, по 27 в agent и chatbot arms (PDF с. 2, 5).

Участники сообщали в среднем `5.4 +/- 0.3` года опыта программирования и `16.2 +/- 1.4` месяца использования AI для coding. Course instructors давали extra credit; существовало альтернативное задание той же заявленной длительности. Протокол был одобрен IRB (PDF с. 5, 9).

Репрезентативность ограничена: это студенты CS, а не случайная выборка профессиональных разработчиков. Хотя уровни обучения различались, работа не проверяет production maintainers, длительное владение repository, командный review или эксплуатацию системы.

## Дизайн исследования

### Background quiz

До coding task участники отвечали на 12 multiple-choice questions по HTML, CSS и JavaScript: recall, conceptual knowledge, tracing и implementation. Вопросы взяты из публичных LinkedIn skill quizzes и проверены front-end engineer (PDF с. 3, 17).

Авторы прямо отмечают, что валидированного concept inventory для web development у них не было. Поэтому quiz является pragmatic covariate, а не установленной психометрической шкалой общей programming expertise.

### Initial website task

Все участники в течение не более 50 минут модифицировали три файла - HTML, CSS и JavaScript - и создавали web game `zic-zac-zoe`, вариант tic-tac-toe на поле 5x5. Требовалось (PDF с. 3, 31):

1. Чередовать ходы `A, A, B, B, ...`.
2. Разрешать ход только в пустую клетку.
3. Определять победу по полной строке или столбцу и ничью при заполнении поля.
4. Центрировать страницу через CSS.
5. Показывать status текущего хода и результата игры.

Участникам не сообщали заранее о последующих comprehension questions и extension task. Лишь 16% после эксперимента ответили, что ожидали продолжения или изменения кода (PDF с. 3, 18).

### Treatment A: agent

- Base model: `gpt-4.1-2025-04-14`.
- Agent framework: open-source AIDER.
- Agent имел доступ к пользовательским файлам и предлагал search-and-replace diffs.
- Пользователь мог принять или отклонить изменения по файлам, принять всё, вручную исправить код или попросить новые изменения.
- После execution отдельный prompt формировал краткое summary изменений (PDF с. 3-4, 15, 33).

Это delegated/agentic editing workflow: AI пишет значительную часть project-specific code, а человек преимущественно ставит задачу и review'ит edits.

### Treatment B: constrained chatbot

- Base model тот же: `gpt-4.1-2025-04-14`.
- Chatbot не имел доступа к файлам пользователя.
- Он должен был давать только общую syntax guidance и generic snippets.
- Пользователь вручную писал код с нуля или адаптировал snippets (PDF с. 3-4, 32).

В описании есть внутренняя несогласованность: основной текст говорит о code blocks из пяти или менее строк, а опубликованный Prompt A.1 разрешает максимум три строки. Для интерпретации treatment важнее общий факт: chatbot намеренно ограничен и отказывается писать project-specific implementation.

Контроль не является no-AI condition. Он представляет другой, более требовательный к человеку AI workflow. Поэтому основной causal estimand - эффект **пакета уровня автоматизации и интерфейса** agent editing против constrained syntax chat, а не AI против ручного программирования.

### Initial outcomes

**Code accuracy** - доля выполненных правил из скрытой 15-rule rubric. `Gemini-3.1 Pro` оценивал code submissions. Два автора вручную оценили 20 submissions, по десять из каждой группы: agreement составил 98% правил, а Cohen's `kappa=0.96` между Gemini и Author A (PDF с. 4).

**Time-to-submission** - вторичный outcome. Участник мог сдать работу раньше лимита, даже не выполнив все требования. Поэтому это не fixed-quality completion time: более ранняя submission и более высокая rubric accuracy анализируются как два связанных, но разных показателя.

### Comprehension outcomes

После initial task участники отвечали на 12 tailored questions, не видя свой полный код, кроме показанных snippets (PDF с. 4-5):

- 6 recall questions: распознать элементы/functions/selectors и выбрать собственный snippet из двух логически эквивалентных;
- 6 reasoning questions: определить purpose кода и предсказать эффект изменения snippet;
- по две HTML, CSS и JavaScript questions каждого типа.

`GPT-5.2-2025-12-11` генерировал distractors и заполнял заранее подготовленные templates. Авторы провели pilot validation, ручную проверку templates и дополнительные проверки real-study questions. В appendix reported pass rates были близки между arms; один редкий mismatch выбора функции не делал вопрос неверным (PDF с. 4, 18-19, 34-36).

Метрика в значительной степени проверяет memory/recognition без обычного доступа к IDE. Это осознанная operationalization понимания, но она строже обычного production workflow, где разработчик может перечитать код. Поведенческий extension task частично дополняет этот недостаток.

### Extension task

После comprehension test участники в течение 20 минут должны были (PDF с. 5, 31):

1. Добавить победу по четырём углам.
2. Сделать символы `A` красными, `B` синими через CSS.
3. Добавить reset button.

Все участники использовали constrained chatbot; agent arm перед этим проходил пятиминутный warm-up с chatbot. Следовательно, extension task измеряет перенос после удаления editing agent, но не полностью самостоятельное программирование без AI.

Extension accuracy оценивалась по 12-rule rubric тем же LLM judge. Time-to-submission анализировался отдельно.

### Поведенческие, self-report и качественные данные

Авторы анализировали prompts, accept/reject patterns, ручные edits, code properties, Likert ratings и open-ended feedback. В agent arm было 152 prompts. Стратегии prompts и review interactions размечались сначала авторами, затем LLM classifiers с human validation (PDF с. 6-8, 15-16).

Эти анализы не рандомизируют interaction strategy. Они показывают ассоциации внутри `n=27`, а не причинные эффекты auto-accept, technical prompting или readability.

## Основные результаты

### Initial productivity

Agent users были точнее и быстрее в initial task (PDF с. 1, 5):

| Outcome | Направление agent vs chatbot | Reported statistic |
|---|---|---|
| Initial task accuracy | выше у agent | `d=1.4`; figure печатает `p=0.00` |
| Initial time-to-submission | меньше у agent | `d=1.2`; figure печатает `p=0.00` |

`p=0.00` - округлённая подпись figure, а не вероятность, буквально равная нулю. Figure 1 суммарно описывает сильные contrasts initial completion и comprehension как `p<0.002`, `d>0.80`.

Точные arm means initial accuracy/time в тексте и таблицах не напечатаны; они показаны графически. Поэтому из PDF не следует восстанавливать точный ratio времён или объявлять численное `k`.

### Comprehension

Overall comprehension была ниже у agent users: Figure 1 сообщает `d=0.9` и печатает `p=0.00` (PDF с. 1). Разбиение Figure 4 показывает более сильный contrast по code recall (`d=1.3`, округлённое `p=0.00`) и более слабый по code reasoning (`d=0.5`, `p=0.08`; PDF с. 5).

Appendix Table 7 уточняет, что эффект неодинаков по типам questions (PDF с. 20):

| Question type | Agent | Chatbot | Разность agent-chatbot | `p` | Cohen's `d` |
|---|---:|---:|---:|---:|---:|
| Select names and IDs | `0.701 +/- 0.022` | `0.793 +/- 0.037` | `-0.093` | `0.035` | `0.592` |
| Identify own code | `0.593 +/- 0.048` | `0.960 +/- 0.022` | `-0.367` | reported `0.000` | `1.873` |
| Purpose | `0.630 +/- 0.057` | `0.860 +/- 0.052` | `-0.230` | `0.004` | `0.826` |
| Change | `0.741 +/- 0.054` | `0.750 +/- 0.069` | `-0.009` | `0.916` | `0.030` |

Таким образом, наиболее сильное различие относится к распознаванию собственного кода и его purpose. Вопросы о наблюдаемом поведении website после изменения кода практически не различали groups. Claim «агенты ухудшают понимание» поэтому поддержан не всеми subdimensions одинаково.

### Extension performance

Для всей выборки agent arm не получил статистически различимого преимущества в extension task (PDF с. 1, 5):

| Outcome | Reported contrast |
|---|---|
| Extension accuracy, all users | `p=0.45`, `d=0.2` |
| Extension time-to-submission | `p=0.69`, `d=0.1` |
| Extension accuracy при initial accuracy `>0.50` | направление меняется в пользу chatbot, но `p=0.18`, `d=0.5` |

Следовательно, работа показывает отсутствие переноса сильного initial advantage, но не устанавливает общий отрицательный treatment effect на extension accuracy или time.

### Opposing pathways

Авторы интерпретируют сходный extension outcome как баланс двух путей: agent arm получает более качественный initial scaffold, но хуже понимает его. В simplified saturated path model (PDF с. 16, 21):

- indirect effect group через initial accuracy: `0.177`, 95% CI `[0.050, 0.304]`, `p=0.006`;
- indirect effect group через comprehension: `-0.204`, 95% CI `[-0.340, -0.069]`, `p=0.003`;
- total indirect effect: `-0.027`, 95% CI `[-0.250, 0.196]`, `p=0.810`;
- direct effect на extension accuracy: `0.065`, 95% CI `[-0.184, 0.314]`, `p=0.608`;
- total effect: `0.038`, 95% CI `[-0.163, 0.239]`, `p=0.712`.

Модель использует robust maximum likelihood, но она saturated, упрощает primary regressions и не устанавливает causal mediation без дополнительных предпосылок. Это согласующаяся с данными decomposition, а не доказательство, что comprehension причинно полностью медиирует extension outcome.

### Background ability и user heterogeneity

Background score между groups существенно не различался (`p=0.12`, `d=0.4`; PDF с. 5). Regression analyses показывают:

- в agent arm initial accuracy была высокой независимо от background ability;
- background ability положительно связан с comprehension в обеих groups;
- background слабо объяснял extension accuracy в исходной модели (`adjusted R^2=0.05`);
- initial accuracy и comprehension вместе заметно лучше объясняли extension accuracy (`adjusted R^2=0.34`; PDF с. 5-6).

Это поддерживает user-specific heterogeneity: одинаковый initial output не означает одинакового понимания, а agent assistance может маскировать differences in background skill по task-completion metric.

### Prompting и review mechanisms

В agent arm низкоусильные interaction patterns были связаны с более слабым comprehension (PDF с. 6-7):

| Prompt strategy | Mean comprehension | Mean BG | Users |
|---|---:|---:|---:|
| Asking agent to explain codebase | `0.635` | `0.692` | 6 |
| Copying task criteria | `0.654` | `0.668` | 25 |
| Iterative debugging | `0.692` | `0.662` | 5 |
| Turning criteria into syntax | `0.743` | `0.684` | 9 |

| Review interaction | Mean comprehension | Mean BG | Users |
|---|---:|---:|---:|
| Auto-accept | `0.615` | `0.603` | 6 |
| Override changes | `0.661` | `0.682` | 15 |
| Accept all | `0.664` | `0.669` | 20 |
| Accept each file | `0.777` | `0.714` | 7 |

Один пользователь мог применять несколько strategies. Малые и пересекающиеся группы, различия BG и self-selection не позволяют заключить, что запрет copy-paste или обязательный file-by-file review причинно даст указанный прирост comprehension. Результаты полезны как mechanism hypotheses и как design variables для `r`.

### Code properties

Agent arm создавал более длинный и объёмный JavaScript: initial task means составляли 124.89 против 83.08 LOC и 3929.71 против 2786.78 volume units; также у agent code было немного больше functions, entropy и comment-line proportion (PDF с. 20).

В четырёх отдельных regressions внутри agent arm меньше LOC, volume и proportion of comments были связаны с более высоким comprehension; intervals для entropy включали широкий диапазон (PDF с. 7). Эти results exploratory:

- `n=27`;
- metrics collinear, поэтому fit проводился отдельно;
- code length одновременно отражает объём выполненных требований;
- assignment code properties не рандомизированы;
- qualitative feedback некоторых пользователей, напротив, называл comments и modular structure полезными для extension (PDF с. 8).

Источник не устанавливает универсальный causal rule «комментарии вредят пониманию».

### Subjective outcomes

Agent users сообщали более высокую helpfulness и меньший mental effort, но более слабое ownership и understanding (PDF с. 7-8):

| Rating 1-5 | Agent | Chatbot |
|---|---:|---:|
| Helpful | `4.7 +/- 0.2` | `3.3 +/- 0.2` |
| Took mental effort | `1.9 +/- 0.2` | `3.7 +/- 0.2` |
| Reviewed responses | `3.2 +/- 0.3` | `4.0 +/- 0.2` |
| Code feels like my own | `2.5 +/- 0.2` | `3.7 +/- 0.2` |
| Understand how code works | `3.3 +/- 0.3` | `4.2 +/- 0.2` |
| Could easily extend code | `3.1 +/- 0.3` | `3.2 +/- 0.2` |
| Prefer agent in new tasks | `4.2 +/- 0.2` | `3.9 +/- 0.2` |
| Prefer ability to switch modes | `4.6 +/- 0.2` | `4.1 +/- 0.3` |

Пользователи частично осознавали более слабое понимание, но всё равно предпочитали agent. Это повторяет важный measurement-design вывод: preference, low effort и perceived helpfulness не являются заменой objective time, quality или comprehension outcomes.

## Качество, время и граница понятия productivity

Работа намеренно показывает, что `productivity` многомерна:

1. **Initial code accuracy** улучшилась с agent.
2. **Initial time-to-submission** сократилось с agent.
3. **Comprehension** ухудшилось с agent.
4. **Extension accuracy/time после удаления agent** существенно не улучшились.
5. **Preference/helpfulness** были выше для agent, несмотря на weaker understanding.

Для M0-M4 особенно важно, что initial time не измеряется при одинаковом обязательном acceptance gate. Участник мог сдать неполный task, а quality учитывалась отдельной rubric score. Поэтому observation нельзя свести к одному duration ratio без выбора способа quality adjustment.

Code comprehension также не является временем. В current M0-M4 она попадает в objective только косвенно, если более слабое понимание увеличивает будущие verification, debugging, handoff или extension times. Balepur et al. показывают правдоподобность такого канала, но общий extension effect за один короткий follow-up не отличался от нуля.

## Ограничения и угрозы валидности

### Ограничения, признанные авторами

1. Population ограничена CS students в двух университетах (PDF с. 9).
2. Domain ограничен двумя web-development tasks вокруг одной game codebase (PDF с. 9).
3. Study UI поддерживает меньше workflow customization, чем реальные IDE и выбранные пользователем agents (PDF с. 9).
4. Rubric scoring и personalized questions зависят от imperfect LLM tools, несмотря на manual validation (PDF с. 9, 18-19).
5. Краткосрочная productivity иногда может быть достаточной целью, например для личного disposable project; ценность понимания зависит от контекста (PDF с. 9).
6. Longitudinal learning, другие programming domains и современные interaction modes остаются future work (PDF с. 8-9).

### Дополнительные ограничения для переноса в M0-M4

1. **Нет no-AI baseline.** Chatbot arm тоже использует GPT-4.1 и внешнюю AI guidance.
2. **Treatment является package intervention.** Одновременно меняются code access, ability to edit, specificity ответа, объём разрешённого code, review UI и human authorship. Нельзя приписать эффект одному компоненту.
3. **Нет фиксированного quality gate для time outcome.** Submission time и rubric accuracy разделены; точный M0 `k` не идентифицируется.
4. **Один task family.** Greenfield HTML/CSS/JS game не покрывает unfamiliar production repository, bug fixing, tests, architecture, security или operations.
5. **Короткий горизонт.** Initial 50 минут и extension 20 минут не измеряют накопление mental model, technical debt, повторный review или handoff.
6. **Нет concurrent agents.** Один участник не supervises несколько simultaneous tasks или contexts.
7. **Нет двухканального timing.** Mental effort, prompt count и accept actions не дают длительность human intervals `h`.
8. **Comprehension task искусственно закрывает код.** Recall без IDE измеряет важный memory construct, но не полностью совпадает с practical ability перечитать и объяснить codebase.
9. **Extension condition не полностью без AI.** Обе groups используют constrained chatbot; agent group получает отдельный warm-up.
10. **Exploratory mechanism analyses.** Prompt/review/readability patterns основаны на `n=27`, self-selection и множественных связанных comparisons.
11. **Неполная статистическая отчётность.** Для основных group contrasts не опубликованы точные means, confidence intervals effect sizes и точные `p`; figures округляют некоторые `p` до `0.00`.
12. **Randomization details.** PDF говорит о random assignment, но не описывает sequence generation, allocation concealment, preregistration или power calculation.
13. **Post-enrollment exclusions.** Пять из 59 participants удалены по attention checks; arm-specific flow до итоговых `27+27` подробно не показан.
14. **Multiple outcomes.** Accuracy, time, четыре question types, file types, regressions, interactions, subjective ratings и exploratory mechanisms образуют большой family analyses; correction for multiplicity не описана.
15. **Internal reporting ambiguities.** Main text и Prompt A.1 расходятся по максимуму строк chatbot snippet. Figure 6 печатает `adjusted R^2=0.15`, тогда как caption упоминает `0.40 -> 0.42`; это не позволяет без source data однозначно цитировать данный промежуточный fit.

## Mapping к M0-M4

Здесь **direct descriptive support** означает прямое наблюдение механизма без численной идентификации коэффициента; **contextual only** - частичное соответствие при иной operationalization; **absent** - параметр не измеряется.

| Поле модели | Статус | Что можно сопоставить | Точная граница |
|---|---|---|---|
| `Z` / `Z_i` | **contextual only** | У всех одна initial website task и одна extension task; background и subrequirements описывают task/user difficulty | Нет no-AI baseline effort scale `Z_i X`, story points или набора неоднородных project jobs |
| `k_i^(r)` | **направление relative outcome, численно absent** | Agent arm быстрее в initial submission и точнее по rubric; effect зависит от task stage и mode | Comparator - constrained chatbot, не no-AI; quality не фиксирована; exact time means не опубликованы. Нельзя получить M0 `k` |
| `r` | **direct support** | `r_agent-edit`: AIDER/GPT-4.1 edits с diff review; `r_chat-manual`: GPT-4.1 syntax guidance без file access и ручная адаптация | Это два bundled experimental workflows; внутри arm strategy выбирается пользователем и не рандомизируется |
| `W = X sum Z_i k_i` | **absent** | Есть одна общая task specification и follow-up | Нет fixed multi-job workload, общей scale `X`, task weights или суммируемой AI work quantity |
| `P` | **фиксирован концептуально как `P=1`** | Один participant работает с одной agent/chat instance над одной активной task | Не изучены concurrent agents, effective parallelism, fan-out или scaling curve |
| `L` / DAG | **absent** | Initial task имеет несколько requirements, extension зависит от initial code | Нет формального precedence graph, weights, critical path или scheduling variation |
| `C(P)` | **absent** | Agent иногда делал unexpected/extraneous edits и создавал rework внутри одного stream | Эти one-stream costs должны входить в mode-specific `k`; agent-agent integration overhead при росте `P` не измерен |
| `a_i^(r)` | **conceptual only** | Agent autonomously generates/applies edits; chatbot generation is brief | Длительность autonomous periods не отделена от participant activity и не нормирована на baseline |
| `h_i^(r)` | **direct support состава, численно absent** | Prompting, specification, diff review, accept/reject, manual override, comprehension, debugging и extension; review effort различается по strategy | Prompt counts, Likert mental effort и comprehension scores не являются human time share; численное `h` неизвестно |
| `H = X sum Z_i h_i` | **absent** | Study показывает, что human understanding может переноситься между stages | Нет набора parallel jobs и полного event log capacity-1 human intervals; `H` вычислить нельзя |
| `gamma(P)` | **absent** | Есть cognitive switching между prompting, reviewing и coding внутри одной task | Нет переключения между `P` concurrent agent contexts, switch count, recovery time или зависимости от `P` |
| Makespan | **contextual single-task proxy** | Initial и extension time-to-submission являются elapsed durations отдельных stages | Нет project completion boundary, fixed quality gate, resource-feasible multi-agent schedule или common workload makespan |
| Quality/understanding | **direct outcome вне текущего objective** | Rubric accuracy, code comprehension, extension ability, ownership и perceived understanding | M0-M4 включает качество только через дополнительное время verification/rework; самостоятельный quality state в модели отсутствует |

## Что источник поддерживает для M0-M4

1. **Режим `r` меняет не только speed, но и человеческую роль.** При одном base model direct editing переносит человека от написания к prompting/review и даёт иной набор outcomes, чем syntax-only chat (PDF с. 2-5, 15).
2. **Нельзя оценивать coding productivity только initial completion.** Agent одновременно повысил initial accuracy/скорость и снизил comprehension; initial advantage не перешёл в установленный extension advantage (PDF с. 1, 5-6).
3. **`h` имеет содержательную, а не только количественную сторону.** File-by-file review, technical prompting и active writing связаны с более высоким comprehension, а auto-accept и copying criteria - с более низким; эти actions следует различать в definition режима и event logging (PDF с. 6-7, 15-16).
4. **Минимизация human time не является безусловной целью.** Более низкий self-reported mental effort в agent arm соседствует с более слабым understanding. Если acceptance criteria включают oversight, maintainability, learning или независимую extension ability, часть `h` может быть продуктивной инвестицией, а не чистым overhead (PDF с. 7-9).
5. **Нужна task-stage heterogeneity.** Initial implementation и later extension дали разные contrasts; один `k` на весь lifecycle может скрыть перенос стоимости из creation в comprehension/rework (PDF с. 5-6, 16, 21).
6. **Нужна user heterogeneity.** Background skill продолжает предсказывать comprehension, даже когда agent сглаживает differences в initial task accuracy (PDF с. 5-6).
7. **Preference не равна productivity.** Пользователи предпочитают agent и считают его helpful, хотя сами сообщают weaker understanding и объективно хуже отвечают на comprehension questions (PDF с. 7-8, 20).
8. **Measurement design должен связывать time, quality и downstream transfer.** Полезный protocol включает initial output, acceptance rubric, comprehension/oversight и follow-up без full agent support, а не только time до первой submission (PDF с. 2-5).

## Что источник не позволяет утверждать

1. Что coding agents универсально повышают developer productivity.
2. Что coding agents универсально ухудшают все формы понимания: change-reasoning questions почти не различались.
3. Что agent arm ухудшил общий extension outcome: total effect на extension accuracy статистически не отличался от нуля.
4. Что users продолжали extension полностью без AI: constrained chatbot оставался доступен.
5. Что exact initial time ratio можно использовать как `k`: arm means не опубликованы численно, comparator не no-AI, quality gate не фиксирован.
6. Что `k<1` при `P=1` установлен для production coding, professional developers или modern repository tasks.
7. Что lower mental effort численно означает меньшее `h`: Likert rating не является долей времени.
8. Что comprehension score можно прибавить к `H` или напрямую перевести во время.
9. Что copy-paste prompting или auto-accept причинно снижают comprehension: strategy analyses observational и малы.
10. Что comments причинно вредят comprehension: readability regressions exploratory и расходятся с частью qualitative feedback.
11. Что source валидирует decomposition, DAG/`L`, неделимость, `C(P)`, `H`, `gamma(P)` или оптимальный `P`.
12. Что agent-generated code имел одинаковое содержание/complexity с chatbot code: agent submissions были длиннее и полнее.
13. Что study оценивает concurrent-agent supervision. Agentic editing одной task не означает `P>1`.
14. Что title `impaired` означает ухудшение time productivity; ухудшено прежде всего measured comprehension.

## Отличие от M0-M4

| Измерение | Balepur et al. (2026) | M0-M4 |
|---|---|---|
| Центральный вопрос | Как direct-editing agent влияет на initial completion, понимание и extension по сравнению с constrained chatbot | Когда `P>1` agents сокращают fixed-workload makespan |
| Топология | Один user - одна active task - один agent или chatbot | Один developer - `P` concurrent coding agents |
| Population | 54 CS students | Абстрактный developer с externally calibrated parameters |
| Workload | Одна greenfield web game и короткое extension | Набор jobs с `Z_i`, fixed total `W` и optional DAG |
| Baseline | Chatbot, требующий ручного writing/adaptation | Последовательная работа без AI, `T_h=X sum Z_i` |
| Режим | Randomized agent editing против constrained syntax chat | Явный task-specific `r`/`rho(i)`, включая interactive/delegated/autonomous |
| Outcome | Accuracy, submission time, comprehension, extension, preference | Makespan и speedup; quality только через time consequences |
| Human work | Behavioral actions и subjective effort, без timing split | `k=a+h`, capacity-1 `H`, non-overlapping human windows |
| Dependencies | Initial code становится scaffold для extension | Formal precedence DAG и critical path `L` |
| Scaling | Не исследуется, `P` концептуально равен 1 | `P`, `C(P)`, `gamma(P)`, diminishing returns и finite optimum |

Balepur et al. находятся перед scheduling layer M0-M4 и одновременно указывают на отсутствующее измерение. Они помогают определить режим `r` и наблюдаемые действия внутри `h`, но добавляют самостоятельный outcome - понимание кода. M0-M4 может использовать источник двумя способами: узко, включая последствия слабого понимания в future verification/rework time; или как основание для будущего multi-objective extension, где makespan оптимизируется при constraint на comprehension/quality.

## Проверенные claims для Related Work

1. В randomized between-subjects study 54 CS students были распределены поровну между GPT-4.1/AIDER agent, напрямую редактирующим project files, и GPT-4.1 chatbot без file access, ограниченным общей syntax guidance; обе groups создавали одну web game, после чего отвечали на tailored comprehension questions и расширяли codebase без editing agent (PDF с. 2-5, 15, 32-33).
2. Agent arm показал более высокую initial accuracy (`d=1.4`) и меньшее initial submission time (`d=1.2`), но более низкую overall comprehension (`d=0.9`); figures округляют соответствующие `p` до `0.00`, а caption суммарно сообщает `p<0.002`, `d>0.80` (PDF с. 1, 5).
3. Сильнейшие comprehension differences относились к identification собственного code (`0.593` против `0.960`, `d=1.873`) и purpose questions (`0.630` против `0.860`, `d=0.826`), тогда как change-reasoning почти не различался (`0.741` против `0.750`, `p=0.916`; PDF с. 20).
4. Initial advantage не дал установленного общего extension advantage: extension accuracy `p=0.45`, `d=0.2`, extension time `p=0.69`, `d=0.1`; simplified path model показывает противоположные indirect paths через initial accuracy и comprehension и near-zero total effect (PDF с. 1, 5-6, 16, 21).
5. Внутри agent arm copy-like prompts и auto-accept были связаны с более низким comprehension, а technical prompts и file-by-file review - с более высоким, но эти comparisons observational, основаны на малых пересекающихся subsets и не идентифицируют causal effect (PDF с. 6-7, 15-16).
6. Agent users сообщали большую helpfulness (`4.7` против `3.3`) и меньший mental effort (`1.9` против `3.7`), но меньшее ownership (`2.5` против `3.7`) и понимание (`3.3` против `4.2`); при этом preference for agent оставалась высокой (PDF с. 7-8).
7. Для M0-M4 работа подтверждает mode- и user-dependent composition человеческого участия, но не даёт duration factor относительно no-AI, human-time share или multi-agent scaling: `P>1`, `C(P)`, `H` и `gamma(P)` отсутствуют.

## Предлагаемое место в статье

Источник лучше вставить в подраздел empirical effects / human-AI interaction сразу после Vaithilingam et al. и Barke et al. Он усиливает переход от раннего Copilot usability к direct-editing coding agents и даёт отдельный аргумент для measurement design.

Не использовать его как источник для раздела multi-agent scaling или как численную калибровку `k`.

### Короткий вариант встраивания

> Balepur et al. (2026) в randomized between-subjects исследовании 54 CS students сравнили GPT-4.1/AIDER agent, напрямую редактировавший project files, с ограниченным GPT-4.1 chatbot, при котором пользователи писали и адаптировали код сами. Agent arm был точнее и быстрее в initial web-development task (`d=1.4` и `d=1.2`), но хуже отвечал на вопросы о собственном коде (overall `d=0.9`); общего преимущества по accuracy или времени последующего extension task без editing agent обнаружено не было (`p=0.45` и `p=0.69`). Наблюдаемые связи auto-accept и low-effort prompts с более слабым comprehension показывают, что режим `r` определяет не только task duration, но и состав человеческого review. Вместе с тем работа рассматривает одного пользователя и одного agent, не имеет no-AI arm и не разделяет human/agent time, поэтому не калибрует `k`, `h` и scaling при `P>1`.

### Вариант для discussion/limitations модели

> Снижение человеческой доли не всегда является безусловным улучшением. Balepur et al. обнаружили, что direct-editing agent уменьшал subjective mental effort и улучшал initial completion, но одновременно снижал comprehension собственного code. Поэтому потолок `1/h` следует интерпретировать только для time objective при заданном acceptance standard: если oversight, maintainability или независимая последующая работа входят в требования, active human engagement может быть не устраняемым overhead, а quality constraint.

## Таблица доказательных страниц

| PDF-страница | Раздел / объект | Опорное содержание |
|---:|---|---|
| 1 | Title; Abstract; Figure 1 | Заголовок, авторы, affiliations, 54 users, initial/comprehension/extension contrasts, `d` и `p`, смысл основного claim |
| 2 | Introduction; Figure 2; Related Work | Два RQ, between-subjects design, agent vs chatbot, understanding vs learning, contributions |
| 3 | Study Design 3.1-3.2 | Background quiz, zic-zac-zoe requirements, 50-minute limit, random assignment, AIDER agent |
| 4 | AI Groups; Productivity; Comprehension | Constrained chatbot, 15-rule rubric, Gemini judge validation, recall/reasoning design и GPT-5.2 questions |
| 5 | Extension; Recruitment; Figure 4 | Extension requirements и 20-minute limit, all-users chatbot, 59 recruited/54 analyzed, experience, initial/time/comprehension/extension effects |
| 6 | Regressions; Path interpretation; Prompt coding | Background heterogeneity, distinction completion/comprehension, predictors extension, exploratory nature mechanisms |
| 7 | Tables 1-2; Review; Readability; Self-report | Prompt/review strategies, code readability regressions, helpfulness/effort/understanding/preference |
| 8 | Table 3; Qualitative themes; Conclusion | Точные self-report ratings, low mental effort, control problems, code quality, polarized value of understanding |
| 9 | Limitations; Ethics | Student/web-task generalizability, constrained workflow, LLM measurement, IRB, alternative credit task |
| 15 | Appendix A.2-A.4 | Exact model checkpoints, AIDER implementation, question/judge models, interaction regressions |
| 16 | Appendix A.4-A.6 | Regression coefficients, simplified mediation interpretation, perceived vs measured outcomes |
| 17-18 | Appendix A.8 | Background pool, exact comprehension templates, qualitative questions, only 16% anticipated extension |
| 18-19 | Appendix A.9 | Validation of generated comprehension questions и comparison across groups |
| 20 | Tables 4-8 | Chatbot strategies, code-property means, question-type means/effects, perceived-measured relationships |
| 21 | Figure 9 | Path coefficients, direct/indirect/total effects, CIs и p-values |
| 31 | Rubrics A.1-A.2 | Exact 15-rule initial и 12-rule extension quality criteria |
| 32-39 | Prompts A.1-A.8 | Operational details chatbot restriction, summaries, question generation, LLM judge и interaction classifiers |

## Итоговая оценка источника

Balepur et al. - сильный современный preprint для аргумента, что initial task completion недостаточен как measure coding-agent productivity. Random assignment, единая task, одинаковый base model в двух arms, отдельные time/accuracy/comprehension/extension outcomes и проверки LLM-based measurement делают основной contrast содержательно полезным. Особенно ценен opposing-path result: agent создаёт лучший scaffold, но более слабый mental model пользователя компенсирует этот выигрыш в последующей работе.

Доказательная сила заканчивается до уровня многоагентного расписания. Comparator является намеренно ограниченным chatbot, time не привязан к общему quality gate, participants - студенты, mechanism analyses exploratory, а concurrent agents отсутствуют. Корректная роль источника в M0-M4 - уточнить `r`, перечень и ценность действий внутри `h`, показать необходимость lifecycle measurement и поставить quality/comprehension caveat к минимизации human effort. Использовать его как численную оценку `k`, `h`, `gamma(P)` или эффекта `P>1` нельзя.
