# Noy и Zhang (2023): время, качество и неоднородность эффекта ChatGPT в профессиональном письме

## Назначение и границы обзора

Этот документ разбирает один локальный PDF применительно к модели M0-M4 для fixed-workload makespan ячейки «один разработчик - `P` кодовых ИИ-агентов». Noy и Zhang нужны здесь как внешний контрольный пример из knowledge work: доступ к генеративному ИИ может одновременно менять время, качество, распределение результатов между пользователями и саму структуру работы.

Главная граница переноса: исследование посвящено коротким профессиональным письменным заданиям и интерактивному ChatGPT. Оно не изучает разработку ПО, автономных кодовых агентов, несколько одновременных потоков, общий репозиторий, граф зависимостей или проектный makespan. Ни одно число из этой работы нельзя напрямую подставлять в coding-specific `k`, `h`, `C(P)` или `gamma(P)`.

Локальный PDF содержит 15 страниц. PDF-страница 1 - ненумерованный титульный лист; PDF-страницы 2-13 соответствуют печатным страницам 1-12; PDF-страницы 14-15 содержат список литературы. Все ссылки ниже даны на PDF-страницы локальной копии.

## Библиография, статус и версия

**Финальная библиографическая запись:** Shakked Noy and Whitney Zhang. “Experimental Evidence on the Productivity Effects of Generative Artificial Intelligence.” *Science*, 381(6654), 187-192, 2023. DOI: [10.1126/science.adh2586](https://doi.org/10.1126/science.adh2586).

**Статус финальной записи:** журнальная статья в *Science*, опубликована 14 июля 2023 года. DOI и выходные данные проверяются по записи издателя/Crossref.

**Фактически проверенная версия:** локальный файл `noy_zhang2023.pdf`, SHA-256 `3102ba08edbba0adbcd04c759e5f2adf0aa39a9c01b0afd5d0a80a1598b9300b`. На титульном листе указаны дата `March 2, 2023` и статус `Working Paper (not peer reviewed)` (PDF с. 1).

Локальный PDF является доработанной до журнальной публикации рабочей версией, а не version of record. В частности, он сообщает `444` участника и результаты `37%` по времени и `0.45 SD` по качеству. Поэтому эти числа в настоящем обзоре относятся только к проверенному working paper. Их нельзя атрибутировать финальной версии *Science* без отдельной проверки финального PDF.

Предлагаемая запись для `references.bib`, если в статье цитируется финальная публикация:

```bibtex
@article{noy2023experimental,
  author  = {Noy, Shakked and Zhang, Whitney},
  title   = {Experimental Evidence on the Productivity Effects of Generative Artificial Intelligence},
  journal = {Science},
  year    = {2023},
  volume  = {381},
  number  = {6654},
  pages   = {187--192},
  doi     = {10.1126/science.adh2586},
  url     = {https://doi.org/10.1126/science.adh2586}
}
```

## Исследовательские вопросы и тип доказательства

Работа спрашивает, как доступ к генеративному ИИ влияет на производительность в существующих профессиональных задачах, замещает ли он усилия работника или дополняет его навыки, различается ли эффект между работниками с разным исходным уровнем и профилем навыков и меняются ли удовлетворённость работой и отношение к автоматизации (PDF с. 2-3).

Тип доказательства - пререгистрированный рандомизированный онлайн-эксперимент с двумя последовательными occupation-specific writing tasks. Первая задача выполняется до treatment и служит индивидуальным baseline; между первой и второй задачами случайно выбранной половине участников открывают доступ к ChatGPT. Такая схема сочетает between-person randomization с within-person изменением результата (PDF с. 1, 3).

Исследование зарегистрировано в AEA RCT Registry как `AEARCTR-0010882`; титульный лист также сообщает об одобрении MIT Committee on the Use of Humans as Experimental Subjects и перечисляет источники финансирования (PDF с. 1).

## Метод, выборка и задания

### Выборка

В working paper сообщается о **444 опытных специалистах с высшим образованием**. Они представляли шесть профессиональных групп:

- marketers;
- grant writers;
- consultants;
- data analysts;
- human resource professionals;
- managers (PDF с. 1, 3).

Локальный основной текст не сообщает платформу рекрутинга, подробную демографию, распределение участников по профессиям или точное число наблюдений в каждой аналитической модели. Эти сведения авторы относят к Online Appendix и Table 1, которых в локальном PDF нет. Поэтому добавлять такие характеристики по памяти или из другой версии нельзя.

Авторы сообщают attrition около `5%` в control и `10%` в treatment. Среди 13 pretreatment characteristics различия обнаружены для employment status и принадлежности к HR profession. В тексте сказано, что Online Appendix содержит Lee bounds и спецификации с контролем этих различий, но сам appendix не входит в локальный файл, поэтому численно проверить robustness estimates по нему невозможно (PDF с. 3).

### Задания

Каждый участник выполнял два коротких задания, подобранных под профессию. Примеры включают press release, short report, analysis plan и delicate email. Задания рассчитаны примерно на 20-30 минут и должны имитировать реальные рабочие задачи; по словам авторов, большинство участников ранее выполняли сходную работу и считали задания реалистичными (PDF с. 3).

Это фиксированные assignments, но не fixed-quality jobs в строгом смысле M0-M4. Finish не задаётся единым порогом приёмки: качество оценивается непрерывно после сдачи и само меняется под воздействием treatment. Поэтому сокращение времени нельзя интерпретировать как выполнение буквально одинакового quality-adjusted объёма работы.

### Treatment и control

После первой задачи случайно выбранные `50%` участников должны были зарегистрироваться в ChatGPT, пройти краткое знакомство с инструментом и получали разрешение использовать его на второй задаче, если сочтут полезным. Control вместо этого регистрировался в редакторе Overleaf (PDF с. 3).

Treatment является **предложением доступа и инструкцией**, а не принудительным использованием:

- `92%` treatment group успешно зарегистрировались;
- `81%` использовали ChatGPT на второй задаче;
- средняя самооценка полезности составила `4.4/5`;
- до эксперимента около `70%` слышали о ChatGPT и `30%` уже использовали его;
- self-report и минутные snapshots указывают, что `10-20%` control также использовали ChatGPT (PDF с. 4).

Следовательно, основной эффект является intention-to-treat эффектом назначения доступа при неполном take-up и contamination control. Авторы оценивают experimentally induced gap в фактическом использовании как минимум в 60 percentage points и считают ITT нижней границей эффекта usage, но локальный текст не даёт инструментальной variable estimate эффекта фактического использования (PDF с. 4).

Для M0-M4 это интерактивный режим одного человека с assistive chatbot. ChatGPT генерирует текст по запросу, после чего пользователь решает, вставлять, редактировать или заменять ответ. Это не автономный исполнитель, которому делегируют coding task с фоновыми тестами и отдельным окном верификации.

### Стимулы и дополнительные arms

Участники получали бонусы за качество. Две основные схемы охватывали `80%` респондентов: linear incentive давал `$1` за каждый балл каждой работы по шкале 1-7, а convex incentive дополнительно давал `$3` за оценку 6 или 7 (PDF с. 4-5).

В отдельном arm с `20%` участников время каждой задачи принудительно фиксировалось на 15 минутах. Ещё `30%` treatment group после второй задачи могли вернуться к тексту первой задачи и отредактировать или заменить его с ChatGPT (PDF с. 5-6).

## Outcomes и статистическая модель

### Время

Основная временная метрика - self-reported total time. Дополнительно система делала snapshot текста каждую минуту, чтобы построить objective measure of active time и обнаруживать использование ChatGPT в control и до treatment. В подписи к Figure 1 сказано, что objective active-time results сходны с self-report, но подробные результаты вынесены в Supplementary Materials, отсутствующие в локальном PDF (PDF с. 3, 5).

Авторы определяют productivity как earnings per minute. Для нашей модели важнее не этот агрегат, а отдельно опубликованные time и quality outcomes: минутная длительность ближе к `k`, тогда как grade показывает, изменился ли результат по качеству одновременно со временем (PDF с. 4-5).

### Качество

Каждый текст оценивали три blinded evaluators с опытом в той же профессии. Они выставляли общую оценку, а также оценки writing quality, content quality и originality по шкале 1-7. Средняя межэкспертная корреляция внутри одного essay составляла `0.44`, то есть измерение качества содержит заметный evaluator noise (PDF с. 3).

### Основная спецификация

Figure 1 показывает коэффициент treatment dummy из person-evaluator-level OLS, где outcome является within-person difference между второй и первой задачами. Спецификация включает evaluator fixed effects, incentive-arm fixed effects и occupation-by-task-order fixed effects; стандартные ошибки кластеризуются по worker. Коэффициенты и standard errors нормированы на pretreatment standard deviation соответствующего outcome в relevant incentive groups (PDF с. 5).

Это не простой post-treatment ratio средних. Raw means удобны для описания величины различия, но причинная оценка авторов опирается на рандомизацию, baseline task и указанную regression specification.

## Результаты и неопределённость

### Время выполнения

На второй задаче control тратил в среднем `27` минут, treatment - `17` минут. Raw difference равна 10 минутам, а raw ratio:

\[
\frac{17}{27} \approx 0.630,
\qquad
1 - \frac{17}{27} \approx 37.0\%.
\]

То есть working paper сообщает **37% сокращение времени**, а reciprocal ratio соответствует примерно `1.59x` по скорости. Стандартизированный regression effect равен `-0.83 SD`; Figure 1 печатает 95% CI в обратном порядке `[-0.63, -1.03]`, что в обычном возрастающем порядке записывается как `[-1.03, -0.63]`. В тексте `p` напечатано как `0.000`, что корректно передавать как `p < 0.001` при показанной точности (PDF с. 4-5).

В abstract эффект округлён до снижения времени на `0.8 SD` (PDF с. 1). Для M0-M4 raw ratio `0.630` можно считать только внешним контекстным аналогом однопоточного duration factor для этих writing tasks. Это не coding-specific `k`, и даже здесь он не является fixed-quality ratio, потому что treatment одновременно повысил оценки качества.

### Качество результата

На второй задаче raw mean grade составил `3.789` в control и `4.54` в treatment, то есть разность равна `0.751` балла по шкале 1-7. Стандартизированный regression effect равен `+0.45 SD`, 95% CI `[0.27, 0.63]`; `p` в тексте указан как `0.000`, то есть `p < 0.001` при показанной точности. Сходный рост наблюдался для overall, writing, content и originality grades (PDF с. 4-5).

В abstract эффект округлён до `0.4 SD` (PDF с. 1). Ключевой вывод для нашей статьи не в конкретном числе, а в совместном направлении outcomes: treatment group работала быстрее и получила более высокие оценки. Поэтому time-only метрика не описывает весь эффект и не должна автоматически трактоваться как экономия при неизменном качестве.

### Fixed-time arm

При принудительно одинаковых 15 минутах treatment повысил grade на `0.39 SD`, но оценка была неточной: `p = 0.13`. Авторы также отмечают небольшое pretreatment imbalance; confidence interval в основном тексте не приведён (PDF с. 5).

Этот arm полезен как попытка отделить productive capacity от решения потратить меньше времени. Однако отсутствие статистической точности не позволяет утверждать, что fixed-time quality effect надёжно отличен от нуля в этой подвыборке.

### Замещение усилий и редактирование

Среди treatment participants:

- `68%` сообщили, что отправили первый output ChatGPT без редактирования;
- после первого наблюдаемого paste крупного блока текста пользователь оставался активен в среднем только 3 минуты;
- время активности после paste не коррелировало с итоговой оценкой;
- human-edited treatment outputs в среднем не получили более высокие оценки, чем raw ChatGPT outputs, отдельно переданные оценщикам (PDF с. 6-7).

В дополнительном arm после второй задачи `23%` заменили исходный ответ на первую задачу output ChatGPT, а `25%` использовали ChatGPT для редактирования исходного ответа (PDF с. 6).

На этом основании авторы интерпретируют механизм преимущественно как substitution for worker effort, а не skill complementarity. Граница вывода узкая: отсутствие обнаруженного value added от редактирования относится к коротким writing tasks, конкретному интерфейсу, стимулам и измерению качества. Оно не доказывает отсутствие human-AI complementarity в программировании или других видах knowledge work.

### Неравенство по исходному результату

В control связь оценки первой и второй задач остаётся высокой: текст называет корреляции `0.49` и `0.25` для control и treatment. Figure 2 показывает соответствующие regression slopes `0.491` (`SE=0.053`) и `0.248` (`SE=0.065`). Разность slopes равна `-0.243`; figure печатает CI в обратном порядке `[-0.08, -0.41]`, то есть в возрастающем порядке `[-0.41, -0.08]`. Текст сообщает `p = 0.004` для difference in slopes (PDF с. 6-7).

Это означает compression распределения **оценок**: участники с низким baseline grade сильнее улучшили качество, тогда как участники с высоким baseline grade главным образом сохранили качество при меньшем времени. Baseline grade здесь является экспериментальным proxy исходной performance/ability, а не общей квалификацией человека или профессиональным уровнем.

Для time outcome Figure 2 показывает slopes `0.802` (`SE=0.600`) в control и `-0.198` (`SE=0.564`) в treatment. Разность приблизительно `-1.000`, но отдельные CI и `p` для этого contrast в figure и основном тексте не приведены. Поэтому безопасный вывод - время сокращалось по всему baseline-grade distribution, но точную статистическую неоднородность time effect по ability локальный PDF не устанавливает (PDF с. 7).

### Профиль навыков и task structure

До treatment участники сообщали, что тратят примерно `25%` времени на brainstorming, `50%` на rough drafting и `25%` на editing. После treatment доля rough drafting упала более чем вдвое, а доля editing выросла более чем вдвое (PDF с. 8-9). Это показывает изменение структуры человеческой работы, но доли self-reported и не дают двухканального хронометража `a+h`.

Авторы проверяют, получают ли больший выигрыш люди со сравнительно слабыми writing/communication skills. Они используют self-ranked communication skill и разность между overall и writing grade первой задачи. Ясной неоднородности не обнаружено: willingness to pay остаётся около `0.5%` месячной зарплаты, а grade gain примерно плосок по группам relative writing skill. Confidence intervals и формальные тесты для этих сравнений в основном тексте не приведены (PDF с. 8-9).

Это важное различие: работа обнаруживает compression по **исходному overall grade**, но не обнаруживает ясного differential benefit по **относительному writing skill**. Нельзя сводить оба результата к общему тезису «ИИ всегда больше помогает менее квалифицированным».

### Adoption и использование после эксперимента

В незавершённом на дату working paper follow-up response rate составлял `82%` среди `423` уже приглашённых участников, без обнаруженной differential response по treatment status. Через две недели ChatGPT в реальной работе использовали `33%` бывших treatment participants и `18%` control. Среди тех, кто не использовал ChatGPT до эксперимента, показатели составляли `26%` и `9%`; `p = 0.048` для разности. Средняя usefulness среди пользователей была `3.65/5`, ниже экспериментальных `4.4/5` (PDF с. 11-12).

Неиспользовавшие инструмент часто ссылались на отсутствие context-specific knowledge о клиентах, текущей информации и продуктах компании. Авторы прямо связывают более низкую полевую полезность с большей длиной, сложностью и контекстностью реальных задач (PDF с. 12).

Follow-up поддерживает вывод о том, что краткое exposure влияет на adoption, но не является рандомизированной оценкой производительности в реальной работе: actual usage после эксперимента self-selected, задачи неоднородны, время и качество реальных outputs не измеряются.

### Субъективные outcomes

Текст сообщает рост job satisfaction примерно на `0.40 SD` с `p < 0.001`, тогда как Figure 4 печатает treatment effect `0.5 SD`, 95% CI `[0.32, 0.68]`. Это внутреннее расхождение округления/спецификации в working paper следует сохранять как оговорку, а не выбирать одно число без комментария (PDF с. 10-11).

Self-efficacy выросла на `0.20 SD`, 95% CI `[-0.02, 0.42]`, `p = 0.060`, то есть estimate неточна и interval включает ноль. Worry about replacement выросла на `0.264 SD` (`p = 0.006`), excitement about enhancement - на `0.389 SD` (`p < 0.001`), overall optimism - на `0.20 SD` (`p = 0.037`) (PDF с. 10-11).

Эти показатели полезны для adoption и организационного контекста, но не являются duration, quality или makespan и не должны входить в `k`.

## Ограничения и внешняя применимость

### Ограничения, признанные авторами

1. Задачи короткие, self-contained и почти не требуют context-specific knowledge, что может завышать полезность ChatGPT.
2. Удовлетворённость отдельной короткой задачей не равна общей job satisfaction; через две недели различий общей удовлетворённости работой не было.
3. Эксперимент измеряет только прямые краткосрочные эффекты и не охватывает general-equilibrium adaptation рынков труда и производственных систем.
4. Эффекты, вероятно, различаются по occupation, task и skill level (PDF с. 12-13).

### Дополнительные ограничения для нашей модели

1. **Несовпадение версий.** Проверенный PDF предшествует финальной статье; его sample size и headline effects нельзя смешивать с version of record.
2. **Нет локального Online Appendix.** Нельзя независимо проверить questionnaires, Table 1, Lee bounds, objective active-time figures и robustness specifications, на которые ссылается основной текст.
3. **Treatment non-use и control contamination.** ITT не равен эффекту фактического использования; take-up определяется доступностью и выбором пользователя.
4. **Качество не фиксировано.** Время снижается одновременно с ростом grade, поэтому raw time ratio не является чистой оценкой изменения времени при строго одинаковом output.
5. **Качество шумно.** Межэкспертная корреляция `0.44` показывает заметную вариативность оценщиков.
6. **Self-report time.** Основной результат использует self-reported time; objective snapshots названы подтверждением, но их подробности находятся вне локального PDF.
7. **Короткий горизонт.** Нет learning curve, накопленного rework, долгосрочной проверки качества, ответственности за ошибки или стоимости поддержки результата.
8. **Нет coding outcomes.** Не измерены correctness, tests, maintainability, security, integration, deployment или работа в репозитории.
9. **Нет параллелизма.** Один пользователь решает одну активную задачу; несколько concurrent agents и очереди внимания отсутствуют.
10. **Ограниченная heterogeneity evidence.** Compression по baseline grade установлена, но task- и occupation-specific effect sizes в локальном основном тексте не опубликованы, а relative-writing-skill heterogeneity ясного сигнала не дала.

## Полный mapping к M0-M4

Здесь **contextual** означает допустимый внешний аналог при другой предметной области; **trivialized** - параметр формально схлопывается из-за одной активной задачи и `P=1`; **absent** - объект не измерялся.

| Поле модели | Статус | Соответствие в Noy и Zhang | Точная граница |
|---|---|---|---|
| baseline `X` и `Z_i X` | **contextual, неразделимый** | Control mean 27 минут на второй writing task даёт group-level baseline duration | Нет универсальной единицы `X`; сложность `Z_i` не отделена от задания, профессии и пользователя |
| `Z_i` | **absent как численная шкала** | Задания различаются по профессии и содержанию | Нет нормированной сложности, task weights или сопоставимых `Z_i`; main text не даёт task-specific effects |
| `k_i^(r)` | **contextual при `P=1`** | Raw post-task time ratio `17/27≈0.630` для assignment to ChatGPT access | Не coding `k`; ITT при non-use/contamination; качество меняется; ratio не является индивидуальным paired coefficient и не переносится между задачами |
| режим `r` | **описан один широкий режим** | Интерактивный chatbot для генерации и редактирования текста; пользователь решает, применять ли output | Фактические стратегии неоднородны; нет сравнения interactive/delegated/autonomous coding modes и точной версии модели |
| fixed workload / `N` | **partial** | Каждый participant получает две заданные writing tasks, main effect относится ко второй | Это две последовательные экспериментальные попытки, не фиксированный проектный набор работ; output quality не фиксировано |
| `W = X sum Z_i k_i` | **absent** | Есть длительность отдельной post-treatment task | Нет суммирования AI-weighted работ, project work или единого workload, который надо распределить по исполнителям |
| `P` | **фиксирован концептуально как `P=1`** | Один человек может использовать один интерактивный ChatGPT в одной активной задаче | Число агентов не варьируется; отсутствуют concurrent streams и effective parallelism |
| неделимость / `M_N` (M1) | **trivialized** | Assignment сдаётся как единый текст | Нет раскладки нескольких неделимых jobs по исполнителям, longest-job bound или scheduling comparison |
| DAG / `L` (M2) | **absent** | Brainstorming, drafting и editing описаны как компоненты процесса | Нет вершин, precedence edges, weighted paths или critical-path estimate; последовательность стадий не является оценённым project DAG |
| `C(P)` (M3) | **неидентифицируем** | Однопоточные prompting/editing costs входят в observed task time | Нет `P>1`, shared artifacts, merge conflicts, interface inconsistency или agent-agent integration overhead |
| `a_i^(r)` и `h_i^(r)` | **conceptual/partial** | Time allocation, 68% unedited initial output и 3 минуты активности после paste указывают на substitution of human effort | Интервалы human-active и agent-autonomous time не размечены в конвенции M0-M4; self-reported shares нельзя преобразовать в численные `a` и `h` |
| `H = X sum Z_i h_i` (M4) | **absent** | Исследование обсуждает объём человеческих усилий на одной задаче | Нет набора параллельных задач, capacity-1 human schedule или суммы непересекающихся intervention windows |
| `gamma(P)` (M4) | **absent** | Изменяется баланс brainstorming/drafting/editing | Нет переключения между `P` агентными контекстами, зависимости от `P` или оценки switching penalty |
| makespan | **partial только для одной задачи** | Total time второй задачи является single-job elapsed duration | Это не makespan фиксированного DAG workload на `P` agents и не resource-feasible schedule; finish quality не зафиксировано единым acceptance gate |

### Допустимая контекстная запись

Только как описание raw second-task means рабочей версии можно записать:

\[
\hat{k}_{\text{professional writing, ChatGPT access, interactive, WP-2023}}
\approx
\frac{17}{27}
=0.630.
\]

Индекс обязан сохранять domain, task class, treatment, режим и версию источника. Даже внутри knowledge work это не чистый structural parameter: assignment to access отличается от actual use, а treatment одновременно изменяет quality. Для coding M0-M4 это число является внешним примером неоднородного time effect, а не калибровкой.

## Что источник поддерживает для M0-M4

1. **Time и quality нужно измерять раздельно и совместно.** В working paper время уменьшилось, а blinded grade вырос; time-only productivity claim был бы неполным (PDF с. 4-5).
2. **`k` не является свойством инструмента вне контекста.** Эффект относится к коротким self-contained professional writing tasks, конкретному режиму доступа и конкретной выборке; сами авторы ожидают вариацию по task, occupation и skill (PDF с. 3, 12-13).
3. **User heterogeneity важна.** Quality gains были больше у участников с низким baseline grade, что сжало распределение оценок (PDF с. 6-7).
4. **Разные определения skill дают разные выводы.** Compression по baseline performance не сопровождается ясной heterogeneity по relative writing skill (PDF с. 8-9).
5. **Режим меняет состав человеческой работы.** Rough drafting сокращается, editing растёт, а многие пользователи принимают initial output без правок; полный эффект включает не только generation speed, но и выбор, проверку и редактирование (PDF с. 6-9).
6. **Adoption является отдельным outcome.** Доступ и краткий опыт повысили последующее использование, но actual use не равен автоматически измеренному productivity gain в полевой работе (PDF с. 11-12).
7. **Контекстность задач ограничивает перенос.** Пользователи реже применяли ChatGPT там, где требовались специфические знания о компании, продукте, клиентах и текущей информации (PDF с. 12).
8. **Для калибровки нужны versioned estimates и uncertainty.** Даже headline estimates зависят от версии paper; внутри working paper основные standardized effects сопровождаются CI, а часть subgroup и supplementary claims не имеет доступной численной проверки.

Пункты 2, 5 и 8 являются интерпретацией результатов в терминах M0-M4, а не формулировками авторов.

## Что источник не позволяет утверждать

1. Что ChatGPT сокращает время любой knowledge-work task на 37%.
2. Что `17/27≈0.630` можно переносить на software development или подставлять как coding-specific `k_i^(r)`.
3. Что числа working paper являются числами финальной статьи *Science*.
4. Что эффект относится к автономному agentic workflow: изучался assistive chatbot, используемый по выбору человека.
5. Что добавление агентов даёт линейное или иное масштабирование: `P` не варьируется.
6. Что источник оценивает неделимость, DAG/`L`, `C(P)`, `H`, `gamma(P)` или multi-agent makespan.
7. Что из time-allocation shares, 68% unedited submissions или трёх минут после paste можно вычислить численное `h`.
8. Что более низкая исходная квалификация вообще всегда означает больший выигрыш: установлен gradient по baseline grade, но не ясный gradient по relative writing skill.
9. Что эффекты однородны по профессиям и типам задач: локальный main text не публикует соответствующие subgroup estimates.
10. Что human editing бесполезно в других domains: отсутствие обнаруженного value added относится только к этому дизайну.
11. Что повышение качества гарантировано при фиксированном времени: fixed-15-minute estimate `0.39 SD` имеет `p=0.13`.
12. Что follow-up usage доказывает полевой productivity effect: usage self-selected, а performance outcomes реальной работы не измерялись.
13. Что снижение inequality в экспериментальных grades означает снижение wage, employment или wealth inequality.
14. Что self-reported satisfaction, willingness to pay или automation beliefs являются параметрами makespan.

## Отличие от M0-M4

| Измерение | Noy и Zhang, working paper | M0-M4 |
|---|---|---|
| Центральный вопрос | Причинный эффект доступа к ChatGPT на время, качество, усилия и perceptions в professional writing | Makespan fixed workload при одном разработчике и `P` кодовых агентах |
| Domain | Короткие occupation-specific writing tasks | Software engineering tasks |
| Топология | Один человек, одна активная задача, один assistive chatbot | Один общий разработчик и до `P` параллельных agent streams |
| Treatment | Разрешение и обучение использованию ChatGPT; usage необязательно | Полная process configuration `(P,r)` с task-specific assignment режимов |
| Baseline | Первая задача до treatment и randomized control на второй задаче | Последовательный no-AI baseline `T_h = X sum Z_i` |
| Outcomes | Self-reported/active time, blinded grades, task structure, satisfaction, beliefs, follow-up use | Makespan и speedup; качество входит только через время проверки и исправления |
| Workload | Две последовательные короткие задачи, main result по второй | Набор неоднородных задач с `Z_i`, `W`, неделимостью и fixed total work |
| Зависимости | Не формализованы | DAG и critical path `L` |
| Масштабирование | Не исследуется | `P`, integration multiplier `C(P)` и effective parallelism |
| Человеческий ресурс | Effort и стадии работы измерены частично и self-reported | Явные `h_i`, capacity-1 сумма `H`, допустимые intervention windows и `gamma(P)` |
| Неопределённость | RCT estimates, clustered regression, CI для основных outcomes, но отсутствующий appendix | Детерминированное ядро, параметры которого требуют внешней task/mode-specific калибровки |

Noy и Zhang находятся перед scheduling layer M0-M4. Они показывают, почему внешний оценщик эффекта ИИ должен хранить как минимум domain, task, user population, mode, outcome и version, а также почему duration нельзя интерпретировать без quality. M0-M4 решает следующий, отсутствующий у них вопрос: как task-level durations складываются в resource-feasible makespan при `P>1`, неделимости, DAG, integration overhead и одном последовательном человеческом ресурсе.

## Проверенные claims для Related Work

1. В локальной working-paper версии пререгистрированного RCT 444 college-educated professionals из шести occupation groups выполняли две occupation-specific writing tasks; половине между задачами случайно открывали доступ к ChatGPT (PDF с. 1, 3).
2. На второй задаче raw mean time составил 17 против 27 минут, то есть на 37% меньше; стандартизированный effect равен `-0.83 SD`, 95% CI `[-1.03,-0.63]`, `p<0.001` при опубликованной точности (PDF с. 4-5).
3. Одновременно raw mean grade вырос с 3.789 до 4.54, а standardized effect составил `+0.45 SD`, 95% CI `[0.27,0.63]`, `p<0.001` (PDF с. 4-5).
4. В fixed-15-minute arm grade effect составил `+0.39 SD`, но был неточным (`p=0.13`); этот результат не устанавливает надёжное улучшение качества при фиксированном времени (PDF с. 5).
5. Связь baseline и post-treatment grades ослабла: slopes равны `0.491` и `0.248`, difference `-0.243`, 95% CI `[-0.41,-0.08]`, `p=0.004`, что поддерживает compression распределения качества по исходной performance (PDF с. 6-7).
6. Ясной heterogeneity по relative writing skill не обнаружено, поэтому результат о compression нельзя обобщать до тезиса о преимуществе для любого менее квалифицированного пользователя (PDF с. 8-9).
7. Take-up был неполным (`81%` treatment использовали ChatGPT), а `10-20%` control также использовали его; основной результат относится к randomized access, а не к чистому сравнению users и non-users (PDF с. 4).
8. Через две недели usage в работе составил 33% против 18%; среди ранее не использовавших ChatGPT - 26% против 9% (`p=0.048`), но follow-up не измерял полевую производительность (PDF с. 11-12).
9. Работа не содержит evidence о software agents, `P>1`, scheduling или makespan; её корректная роль - внешний knowledge-work пример совместного изменения time, quality, task structure и распределения эффектов.

## Встраивание в статью

### Рекомендуемое место

Источник лучше поставить в подраздел эмпирики AI productivity после coding-specific Peng et al. и Vaithilingam et al., но до синтеза о неоднородности результатов. Он выполняет роль внешней проверки: даже в domain, где найден положительный средний эффект, необходимо одновременно фиксировать outcome quality, baseline ability, actual use и task context.

### Безопасный короткий вариант для `Related Work`

> Внешний контрольный пример из профессионального письма показывает, что эффект генеративного ИИ нельзя описывать только одной временной метрикой. В рандомизированном эксперименте Noy и Zhang доступ к ChatGPT одновременно сокращал время выполнения коротких occupation-specific assignments и повышал blinded quality grades; рост качества был больше у участников с низким исходным результатом, тогда как ясной неоднородности по относительному writing skill авторы не обнаружили. Исследование также фиксирует неполный take-up, использование ChatGPT частью control group и более низкую полезность на контекстно насыщенных реальных задачах. Для нашей модели это поддерживает task-, user- и mode-specific калибровку `k` и раздельный контроль time и quality, но не даёт чисел для coding: работа не рассматривает разработку ПО, автономных агентов, `P>1`, DAG, `C(P)`, `h`, `H` или `gamma(P)`.

Этот вариант намеренно не переносит exact numbers working paper в цитату финальной статьи *Science*. Если в тексте нужны численные эффекты, сначала следует получить и проверить final version of record; иначе нужно явно писать «в рабочей версии от 2 марта 2023 года».

### Формулировка для limitations модели

> Параметр `k_i^(r)` описывает время, но не заменяет отдельную метрику качества. Эксперименты в knowledge work показывают, что time и quality способны изменяться одновременно и неодинаково по исходному уровню пользователя. Поэтому эмпирическая калибровка модели должна фиксировать acceptance criterion и последующий rework; перенос среднего duration ratio между domains, задачами и версиями инструмента недопустим.

## Таблица доказательных страниц

| PDF-страница | Раздел / объект | Опорное содержание |
|---:|---|---|
| 1 | Title; Abstract; disclosure | Working paper от 2 марта 2023, `not peer reviewed`, 444 participants, rounded effects `-0.8 SD` по времени и `+0.4 SD` по качеству, preregistration, ethics, funding |
| 2 | Introduction | Automation versus complementarity, возможное влияние на inequality, постановка исследовательских вопросов |
| 3 | Design overview | Шесть occupations, две 20-30-минутные задачи, blinded professional evaluators, три оценки на output, correlation `0.44`, random 50% treatment, Overleaf control, snapshots, attrition и ссылки на отсутствующий Online Appendix |
| 4 | Takeup; Productivity | Signup `92%`, usage `81%`, usefulness `4.4/5`, prior awareness/use, control contamination `10-20%`, raw time effect 10 минут/37%, grade effect `0.45 SD`, `p` values |
| 5 | Figure 1; regression note | Raw means 27/17 минут и grades 3.789/4.54; time effect `-0.83 SD`, CI; grade effect `+0.45 SD`, CI; OLS specification; fixed-15-minute arm `+0.39 SD`, `p=0.13` |
| 6 | Editing arm; Inequality; Complementarity | 23% replace и 25% edit; baseline-grade compression; control/treatment relation; 68% initial output без редактирования; 3 минуты активности после paste |
| 7 | Figure 2 | Grade slopes `0.491` и `0.248`, SE, difference `-0.243` и CI; time slopes `0.802` и `-0.198`; отсутствие higher grades у human-edited output против raw ChatGPT output |
| 8 | Task Structure; Skill Demand | До treatment 25/50/25% brainstorming/drafting/editing, сдвиг от rough drafting к editing; определения relative writing skill; willingness-to-pay и grade-gain tests |
| 9 | Figure 3 | Визуализация task-structure shift и отсутствия ясной heterogeneity по relative writing skill; willingness to pay около 0.5% salary |
| 10 | Job Satisfaction; Self-Efficacy; Beliefs | Текстовые estimates satisfaction/self-efficacy и `p`; определения automation-belief outcomes |
| 11 | Figure 4; Follow-up start | Figure-level effect и CI для satisfaction/self-efficacy; belief effects; follow-up response rate `82%` среди 423 приглашённых |
| 12 | Follow-up; Discussion | Usage 33/18%, среди prior non-users 26/9% (`p=0.048`), usefulness `3.65/5`, барьер context-specific knowledge, отсутствие overall job-satisfaction difference |
| 13 | Discussion; Limitations | Short/self-contained tasks, отсутствие context-specific knowledge, краткосрочность, general-equilibrium boundary, ожидаемая вариация по occupation/task/skill |
| 14-15 | References | Список литературы; дополнительных methods/results или Online Appendix в локальном PDF нет |

## Итоговая оценка источника

Сильная сторона Noy и Zhang - рандомизация, pretreatment task, blinded occupational evaluators, совместное измерение времени и качества и явный анализ распределения результатов. Для M0-M4 работа полезна как внешний пример того, что средний AI effect зависит от outcome и пользователя: положительный time effect не обязан сопровождаться неизменным качеством, а compression по baseline performance не равна универсальному преимуществу для любой low-skill группы.

Доказательная граница проходит до software-agent scheduling. Локальный PDF является непрошедшей рецензирование рабочей версией, отличается от финальной публикации и не содержит Online Appendix. Эксперимент не рассматривает код, несколько агентов, зависимости, общий человеческий ресурс или проектный makespan. Поэтому корректное использование источника - обосновать раздельное измерение time/quality, task/user/mode specificity и осторожность переноса, но не калибровать ни один многоагентный параметр и не переносить его effect sizes на coding.
