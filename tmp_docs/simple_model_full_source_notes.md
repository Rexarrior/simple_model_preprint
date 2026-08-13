# Source notes for the future literature review

Дата проверки: 2026-08-04. Это конспект, а не готовый текст статьи.

## Статус

Этот файл был подготовлен до полного чтения всех PDF и теперь служит только
тематическим навигатором. Канонические post-source notes находятся в
`simple_model_full/literature_reviews/` -- 34 отдельных Markdown-файла для 34
PDF. Краткий итог с проблемами корпуса и следующим шагом:
`tmp_docs/simple_model_full_source_review_report.md`. При расхождении
использовать индивидуальный обзор.

## Масштабирование

### Amdahl (1967)

G. M. Amdahl, “Validity of the Single Processor Approach to Achieving Large
Scale Computing Capabilities,” AFIPS Spring Joint Computer Conference,
483--485, 1967, DOI `10.1145/1465482.1465560`.

Использовать как классический fixed-workload источник для потолка ускорения,
когда последовательная доля не масштабируется. Аналогия с моделью
структурная: человеческая доля `h` обслуживается последовательно. Не писать,
что закон Амдала сам доказывает модель человеческого внимания.

### Gustafson (1988)

J. L. Gustafson, “Reevaluating Amdahl's Law,” *Communications of the ACM*,
31(5), 532--533, 1988, DOI `10.1145/42411.42415`.

Использовать для разведения fixed workload/makespan и scaled
workload/throughput. Это соседняя постановка и направление расширения, а не
прямой источник текущего критерия.

### Gunther (2008)

Открытый источник: https://arxiv.org/abs/0808.1431; локальный PDF:
`simple_model_full/literature/gunther2008.pdf`.

Аннотация прямо связывает Universal Scalability Law с рациональной функцией
числа исполнителей и machine-repairman queue. Это поддерживает интерпретацию
`alpha` как contention и `beta` как coherency/coordination overhead. Источник
не валидирует эту формулу эмпирически для human-supervised LLM agents.

### Brooks (1995)

F. P. Brooks, Jr., *The Mythical Man-Month: Essays on Software Engineering*,
anniversary ed., Addison-Wesley, 1995, ISBN `978-0-201-83595-3`.

Использовать для мотивации интеграционных и коммуникационных издержек роста
числа участников. Не переносить буквально `P(P-1)/2` прямых человеческих
каналов на звезду без agent-agent communication. Общие артефакты, интерфейсы,
merge conflicts и rework всё равно дают топологически-зависимый `C(P)`.

## Расписания и общие ресурсы

### Graham (1966, 1969)

- R. L. Graham, “Bounds for Certain Multiprocessing Anomalies,” *Bell System
  Technical Journal*, 45(9), 1563--1581, 1966, DOI
  `10.1002/j.1538-7305.1966.tb01709.x`.
- R. L. Graham, “Bounds on Multiprocessing Timing Anomalies,” *SIAM Journal
  on Applied Mathematics*, 17(2), 416--429, 1969, DOI `10.1137/0117039`.

Использовать для upper bound list scheduling с precedence constraints и для
LPT при независимых задачах. Оговорка обязательна: классические гарантии не
учитывают `C(P)` и shared human resource.

### Pinedo (2008, локальная версия)

M. L. Pinedo, *Scheduling: Theory, Algorithms, and Systems*, 3rd ed.,
Springer, 2008, DOI `10.1007/978-0-387-78935-4`.

Учебниковый якорь для makespan, parallel-machine notation и различия между
deterministic и stochastic scheduling. Проанализирован локальный
`simple_model_full/literature/pinedo2008.pdf`; метаданные 6-го издания 2022
года к нему не относятся.

### Common/single server scheduling

- N. G. Hall, C. N. Potts, and C. Sriskandarajah, “Parallel Machine Scheduling
  with a Common Server,” *Discrete Applied Mathematics*, 102(3), 223--243,
  2000, DOI `10.1016/S0166-218X(99)00206-1`.
- S. A. Kravchenko and F. Werner, “Parallel Machine Scheduling Problems with
  a Single Server,” *Mathematical and Computer Modelling*, 26(12), 1--11,
  1997, DOI `10.1016/S0895-7177(97)00236-7`.

Это самые близкие формальные аналоги общего последовательного ресурса. В
обзоре лучше писать “structural analogue”: server operations не равны
интерпретации, спецификации, верификации и context switching разработчика.

### RCPSP

P. Brucker, A. Drexl, R. Möhring, K. Neumann, and E. Pesch,
“Resource-Constrained Project Scheduling: Notation, Classification, Models,
and Methods,” *European Journal of Operational Research*, 112(1), 3--41,
1999, DOI `10.1016/S0377-2217(98)00204-5`.

Важная коррекция позиционирования: классическая scheduling literature не
игнорирует общие ресурсы вообще. RCPSP уже моделирует precedence constraints и
возобновляемые ресурсы с ограниченной мощностью. Специфика статьи --
интерпретация ресурса как человеческого внимания, декомпозиция `a+h` и связь
с эмпирическим эффектом AI.

## Effort и cost estimation

Рекомендуемые источники:

- B. W. Boehm, *Software Engineering Economics*, Prentice Hall, 1981.
- B. W. Boehm et al., *Software Cost Estimation with COCOMO II*, Prentice
  Hall, 2000.
- B. Boehm, C. Abts, and S. Chulani, “Software Development Cost Estimation
  Approaches: A Survey,” *Annals of Software Engineering*, 10, 177--205,
  2000, DOI `10.1023/A:1018991717352`.
- M. Jørgensen and M. Shepperd, “A Systematic Review of Software Development
  Cost Estimation Studies,” *IEEE Transactions on Software Engineering*,
  33(1), 33--53, 2007, DOI `10.1109/TSE.2007.256943`.
- M. Jørgensen, “Forecasting of Software Development Work Effort: Evidence on
  Expert Judgement and Formal Models,” *International Journal of Forecasting*,
  23(3), 449--462, 2007, DOI `10.1016/j.ijforecast.2007.05.008`.

Синтез: эти источники мотивируют внешний оценщик `k_hat` и предупреждают,
что формальные и экспертные оценки имеют контекстную ошибку. Их нужно
использовать для разведения effort/cost forecasting и makespan optimization,
а не как прямое доказательство LLM productivity.

Важно: локальный `boehm1981.pdf` оказался обзором A. Bryant и J. A. Kirkham
(1983), а не первичным текстом книги Boehm. Индивидуальный обзор описывает
фактический файл; книга 1981 года остаётся непроверенной.

## Эмпирика AI productivity

### Peng et al. (2023)

Открытый источник: https://arxiv.org/abs/2302.06590; локальный PDF:
`simple_model_full/literature/peng2023.pdf`.

Контролируемый эксперимент: разработчики реализовывали HTTP server на
JavaScript; среднее время среди completers сократилось на 55.8%. Mapping:
task/mode-specific `k`, примерно при `P=1`; это не оценка многоагентного
параллелизма.

### Vaithilingam, Zhang & Glassman (2022)

Авторский PDF: https://tianyi-zhang.github.io/files/chi2022-lbw-copilot.pdf;
локальный PDF: `simple_model_full/literature/vaithilingam2022.pdf`.

24 участника; работа изучает разрыв между ожиданием и опытом с code
generation. Для статьи важнее не один универсальный effect size, а стоимость
понимания, редактирования и отладки генераций. Источник обосновывает `h` и
режим `r`.

### Brynjolfsson, Li & Raymond (2025)

Финальная peer-reviewed версия: *The Quarterly Journal of Economics*, 140(2),
889--942, DOI `10.1093/qje/qjae044`. Working paper 2023: NBER, DOI
`10.3386/w31161`.

Локальный `brynjolfsson2025.pdf` содержит именно NBER working paper 2023 года,
а не финальную QJE-версию. Детальные локальные числа и страницы нельзя
атрибутировать version of record.

Crossref abstract: 5,172 customer-support agents; AI повышает issues
resolved per hour в среднем на 15%; эффекты неоднородны по опыту, skill и
редкости проблемы. Использовать как evidence for task/user-dependent `k`.
Не называть это экспериментом с coding agents.

### Becker et al. (2025)

Открытый источник: https://arxiv.org/abs/2507.09089; локальный PDF:
`simple_model_full/literature/becker2025.pdf`.

RCT: 16 опытных open-source developers, 246 задач зрелых проектов; разрешение
early-2025 AI увеличило completion time на 19%. Всегда указывать контекст:
это не универсальный отрицательный эффект AI.

### Barke et al. (2023)

S. Barke, M. B. James, and N. Polikarpova, “Grounded Copilot: How Programmers
Interact with Code-Generating Models,” *Proceedings of the ACM on Programming
Languages*, 7(OOPSLA1), Article 78, 78:1--78:27, 2023, DOI
`10.1145/3586030`.

Использовать для режимов interaction и grounding/verification. Это источник
механизма для `r` и `h`, а не для многоагентного makespan.

### Noy & Zhang (2023)

S. Noy and W. Zhang, “Experimental Evidence on the Productivity Effects of
Generative Artificial Intelligence,” *Science*, 381(6654), 187--192, 2023,
DOI `10.1126/science.adh2586`.

Локальный PDF является working paper от 2 марта 2023 года, а не финальной
версией *Science*. Численные результаты локального файла нельзя без сверки
атрибутировать version of record.

Внешний контрольный пример из knowledge work: время и качество меняются
по-разному в разных классах задач. Проценты нельзя напрямую переводить в
software `k`.

### METR (2026)

Открытый HTML: https://metr.org/blog/2026-02-24-uplift-update/.

Пост описывает selection into AI-allowed tasks, отказ разработчиков от задач,
которые не хочется делать без AI, и ненадёжность task-time при одновременной
работе с несколькими агентами. Это gray literature для оговорок о дизайне
измерений, не основное доказательство effect size.

### Kim et al. (2025/2026 v3)

Открытый источник: https://arxiv.org/abs/2512.08296; локальный PDF:
`simple_model_full/literature/kim2025.pdf`.

V3 abstract: 260 configurations, 6 benchmarks, 5 architectures; relative
change от +80.8% на decomposable financial reasoning до -70.0% на sequential
planning. Поддерживает task-architecture alignment, diminishing returns и
overhead, но изучает agent-agent architectures, а не одного человека с
несколькими coding agents.

### Vaccaro, Almaatouq & Malone (2024)

Открытый источник: https://www.nature.com/articles/s41562-024-02024-1.pdf;
локальный PDF: `simple_model_full/literature/vaccaro2024.pdf`.

106 experimental studies, 370 effect sizes. В среднем human-AI combinations
ниже лучшего solo condition: Hedges' `g=-0.23`, 95% CI [-0.39, -0.07]. Это
рамка complementarity и quality caveat; outcomes преимущественно accuracy или
quality, а не fixed-workload completion time.

## Человек и надзор за несколькими исполнителями

Проверенные источники:

- D. R. Olsen Jr. and S. B. Wood, “Fan-out: Measuring Human Control of
  Multiple Robots,” CHI 2004, 231--238, DOI `10.1145/985692.985722`.
- J. W. Crandall, M. A. Goodrich, D. R. Olsen Jr., and C. W. Nielsen,
  “Validating Human-Robot Interaction Schemes in Multitasking Environments,”
  *IEEE Transactions on Systems, Man, and Cybernetics Part A*, 35(4),
  438--449, 2005, DOI `10.1109/TSMCA.2005.850587`.
- J. W. Crandall, M. L. Cummings, M. Della Penna, and P. M. A. de Jong,
  “Computing the Effects of Operator Attention Allocation in Human Control of
  Multiple Robots,” *IEEE Transactions on Systems, Man, and Cybernetics Part
  A*, 41(3), 385--397, 2011, DOI `10.1109/TSMCA.2010.2084082`.
- D. D. Salvucci and N. A. Taatgen, “Threaded Cognition: An Integrated Theory
  of Concurrent Multitasking,” *Psychological Review*, 115(1), 101--130,
  2008, DOI `10.1037/0033-295X.115.1.101`.

Эти источники дают наиболее сильную концептуальную опору для `H`, окон
вмешательства и `gamma(P)`. Они не дают калибровки для coding agents, поэтому
`h_i` и `gamma(P)` следует оставлять эмпирически оцениваемыми параметрами.

## Дополнительно, пока не обязательно включать

- Monsell (2003), “Task Switching,” DOI `10.1016/S1364-6613(03)00028-7`, если
  понадобится отдельный обзор switch cost.
- Forsgren et al. (2021), “The SPACE of Developer Productivity,” DOI
  `10.1145/3454122.3454124`, для ограничения одной временной метрики.
- Bird et al. (2023), “Taking Flight with Copilot,” DOI
  `10.1145/3589996`, как менее приоритетный workflow source.
