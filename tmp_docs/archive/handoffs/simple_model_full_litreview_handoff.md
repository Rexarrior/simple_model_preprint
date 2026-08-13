# Handoff: литобзор для `simple_model_full`

Дата фиксации: 2026-08-04.

> **Обновление после выполнения handoff:** основной корпус из 25 работ отобран,
> evidence matrix пересобрана, Related Work написан и подключён, библиография
> обновлена, статья собрана в `simple_model_full/build/main.pdf`. Актуальный
> статус и следующие шаги находятся в
> `tmp_docs/simple_model_full_source_review_report.md`; план ниже сохранён как
> история постановки.

## Актуальный статус после анализа корпуса

- Анализ всех 34 локальных PDF завершён.
- Для каждого PDF создан отдельный постранично проверенный обзор в `simple_model_full/literature_reviews/`.
- Единый краткий отчёт: `tmp_docs/simple_model_full_source_review_report.md`.
- При расхождении этого handoff с индивидуальным обзором каноническим считается индивидуальный обзор.
- Related Work, `references.bib` и формальная модель на этом этапе не редактировались.

## Задача

Подготовить проверенный раздел `Related Work` для статьи `simple_model_full` о формальной модели производительности одной человеко-агентной ячейки: один разработчик управляет несколькими ИИ-агентами, агентная работа параллелится, человеческое внимание остаётся последовательным ресурсом.

Нужно скачать доступные полные тексты, проанализировать их, собрать evidence matrix, дополнить `simple_model_full/references.bib` и написать обзор в `simple_model_full/simple_litreview.tex` с последующим подключением к `main.tex`.

## Состояние статьи

- `simple_model_full/main.tex`: раздел `Related Work` пуст.
- `simple_model_full/simple_litreview.tex`: пустая заготовка.
- `simple_model_full/references.bib`: пока только Peng et al. (2023), Becker et al. (2025) и заметка METR (2026).
- `simple_model_full/Базовая модель.tex`: уже использует без ссылок Амдала, Грэма, Брукса и Universal Scalability Law Гантера.
- `simple_model_full/bad_litreview/`: архивный некачественный обзор. Его текст и `.bib` нельзя переносить без повторной проверки: там есть LinkedIn, GeeksForGeeks, Zhihu, неточные метаданные и потенциально недостоверные утверждения.
- По запросу пользователя обзор и статья пока не редактируются: `main.tex`, `simple_litreview.tex`, `references.bib` и `Базовая модель.tex` не менялись в рамках продолжения 2026-08-04.
- Рабочие материалы сохранены в `tmp_docs/simple_model_full_evidence_matrix.md` и `tmp_docs/simple_model_full_source_notes.md`.

## Обязательный корпус

### 1. Масштабирование и параллельные вычисления

1. Amdahl, G. M. (1967). *Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities*. AFIPS Spring Joint Computer Conference, 483-485. DOI: https://doi.org/10.1145/1465482.1465560
   - Зачем: источник потолка ускорения; в модели последовательная доля заменена средневзвешенной долей человеческого внимания `h`.

2. Gustafson, J. L. (1988). *Reevaluating Amdahl's Law*. Communications of the ACM, 31(5). DOI: https://doi.org/10.1145/42411.42415
   - Зачем: scaled-workload альтернатива Амдалу.
   - Важно: нынешняя статья рассматривает фиксированный объём работ и makespan, поэтому закон Густавсона-Барсиса надо подавать как соседнюю постановку/направление расширения на throughput, а не как прямой источник текущего результата.

3. Gunther, N. J. (2008). *A General Theory of Computational Scalability Based on Rational Functions*. arXiv:0808.1431. PDF: https://arxiv.org/pdf/0808.1431
   - Зачем: формула `1 + alpha(P-1) + beta P(P-1)` уже фактически используется в `C(P)`; источник Universal Scalability Law и связи с machine-repairman queue.

4. Brooks, F. P., Jr. (1975; anniversary ed. 1995). *The Mythical Man-Month: Essays on Software Engineering*. Addison-Wesley. Anniversary ISBN: 978-0-201-83595-3. Связанная запись Crossref: https://doi.org/10.1145/390016.808439
   - Зачем: коммуникационные и интеграционные издержки масштабирования команды.
   - Важно: не писать, что Брукс «полностью неприменим». Не применима конкретная оценка попарных человеческих каналов `P(P-1)/2` к звезде без прямого общения агентов. Косвенная связанность через общие артефакты, merge conflicts и интерфейсы сохраняется.

### 2. Теория расписаний

5. Graham, R. L. (1966). *Bounds for Certain Multiprocessing Anomalies*. Bell System Technical Journal, 45(9), 1563-1581. DOI: https://doi.org/10.1002/j.1538-7305.1966.tb01709.x
   - Зачем: list scheduling bound для задач с precedence constraints; прямо используется в модели.

6. Graham, R. L. (1969). *Bounds on Multiprocessing Timing Anomalies*. SIAM Journal on Applied Mathematics, 17(2), 416-429. DOI: https://doi.org/10.1137/0117039
   - Зачем: LPT guarantee; прямо используется в модели.

7. Pinedo, M. L. (2022). *Scheduling: Theory, Algorithms, and Systems* (6th ed.). Springer. DOI: https://doi.org/10.1007/978-3-031-05921-6
   - Зачем: учебниковый источник для notation, makespan, parallel machines, deterministic/stochastic scheduling.
   - Локально доступна и проанализирована только 3-я редакция 2008 года: `pinedo2008.pdf`. Метаданные и утверждения 6-й редакции нельзя приписывать этому файлу.

8. Hall, N. G., Potts, C. N., & Sriskandarajah, C. (2000). *Parallel Machine Scheduling with a Common Server*. Discrete Applied Mathematics. DOI: https://doi.org/10.1016/S0166-218X(99)00206-1
   - Зачем: один общий последовательный server обслуживает несколько параллельных машин. Это один из ближайших формальных аналогов уровня M4.

9. Kravchenko, S. A., & Werner, F. (1997). *Parallel Machine Scheduling Problems with a Single Server*. Mathematical and Computer Modelling. DOI: https://doi.org/10.1016/S0895-7177(97)00236-7
   - Зачем: второй ближайший аналог схемы «несколько исполнителей плюс один общий обслуживающий ресурс».

10. Brucker, P., Drexl, A., Möhring, R., Neumann, K., & Pesch, E. (1999). *Resource-Constrained Project Scheduling: Notation, Classification, Models, and Methods*. European Journal of Operational Research. DOI: https://doi.org/10.1016/S0377-2217(98)00204-5
    - Зачем: человеческое внимание можно представить возобновляемым ресурсом мощности 1. Нельзя утверждать, что классическая scheduling literature вообще не учитывает общий человеческий ресурс.

### 3. Оценка трудозатрат разработки

11. Boehm, B. W. (1981). *Software Engineering Economics*. Prentice Hall.
    - Зачем: исходная COCOMO как effort/cost model.
    - Важно: локальный `boehm1981.pdf` оказался обзором Bryant и Kirkham (1983), а не книгой Boehm. Первичный текст книги остаётся непроверенным.

12. Boehm, B. W., et al. (2000). *Software Cost Estimation with COCOMO II*. Prentice Hall.
    - Зачем: современная относительно COCOMO-81 параметрическая модель; сравнить оценку effort с моделью процесса/makespan.

13. Boehm, B., Abts, C., & Chulani, S. (2000). *Software Development Cost Estimation Approaches: A Survey*. Annals of Software Engineering. DOI: https://doi.org/10.1023/A:1018991717352
    - Зачем: компактный рецензируемый источник вместо пересказа COCOMO по учебным сайтам.

14. Jørgensen, M., & Shepperd, M. (2007). *A Systematic Review of Software Development Cost Estimation Studies*. IEEE Transactions on Software Engineering, 33(1), 33-53. DOI: https://doi.org/10.1109/TSE.2007.256943
    - Зачем: карта формальных и judgement-based подходов к software effort estimation.

15. Jørgensen, M. (2007). *Forecasting of Software Development Work Effort: Evidence on Expert Judgement and Formal Models*. International Journal of Forecasting, 23(3), 449-462. DOI: https://doi.org/10.1016/j.ijforecast.2007.05.008
    - Зачем: границы формальных cost models и роль экспертной оценки; связано с калибровкой `k_i` до проекта.

### 4. Эмпирика LLM и производительности

16. Peng, S., Kalliamvakou, E., Cihon, P., & Demirer, M. (2023). *The Impact of AI on Developer Productivity: Evidence from GitHub Copilot*. arXiv:2302.06590. DOI/PDF: https://doi.org/10.48550/arXiv.2302.06590
    - Зачем: controlled experiment, одна ограниченная задача, Copilot, 55.8% сокращение времени; приблизительно наблюдение `k` при `P=1`, а не оценка многоагентного параллелизма.

17. Vaithilingam, P., Zhang, T., & Glassman, E. L. (2022). *Expectation vs. Experience: Evaluating the Usability of Code Generation Tools Powered by Large Language Models*. CHI EA. DOI: https://doi.org/10.1145/3491101.3519665
    - Author PDF: https://tianyi-zhang.github.io/files/chi2022-lbw-copilot.pdf
    - Зачем: 24 участника; Copilot не обязательно улучшил completion time/success rate, а понимание, редактирование и отладка генераций мешали работе. Прямая опора для человеческой доли `h`.

18. Brynjolfsson, E., Li, D., & Raymond, L. (2025). *Generative AI at Work*. Quarterly Journal of Economics. DOI: https://doi.org/10.1093/qje/qjae044
    - Это финальная peer-reviewed версия working paper 2023: https://doi.org/10.3386/w31161
    - Зачем: field evidence из customer support, гетерогенность эффекта по опыту и типу работы. В библиографии лучше цитировать финальную версию, а 2023 упомянуть только как историю публикации.
    - Важно: локальный `brynjolfsson2025.pdf` содержит NBER working paper 2023, а не финальную QJE-версию. Детальные числа и страницы локального PDF относятся только к working paper.

19. Becker, J., Rush, N., Barnes, E., & Rein, D. (2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*. arXiv:2507.09089. PDF: https://arxiv.org/pdf/2507.09089
    - Зачем: RCT на опытных разработчиках в знакомых репозиториях, наблюдаемое замедление; уже есть в `references.bib`.

20. Barke, S., James, M. B., & Polikarpova, N. (2023). *Grounded Copilot: How Programmers Interact with Code-Generating Models*. Proceedings of the ACM on Programming Languages. DOI/PDF: https://doi.org/10.1145/3586030
    - Зачем: режимы взаимодействия programmer-Copilot; полезно для операционализации параметра режима `r`, а не только среднего `k`.

21. Noy, S., & Zhang, W. (2023). *Experimental Evidence on the Productivity Effects of Generative Artificial Intelligence*. Science, 381(6654), 187-192. DOI: https://doi.org/10.1126/science.adh2586
    - Зачем: внешний контрольный пример для knowledge work: время и качество меняются одновременно; показывает зависимость результата от класса задач.

22. METR (2026). *We Are Changing Our Developer Productivity Experiment Design*. https://metr.org/blog/2026-02-24-uplift-update/
    - Зачем: selection effects и параллельная работа с несколькими агентами делают per-task duration недостаточной метрикой; уже есть в `references.bib`.
    - Статус: gray literature, использовать только для дизайна измерений и оговорок, не как основное доказательство эффекта.

### 5. Один человек и несколько автономных исполнителей

23. Olsen, D. R., Jr., & Wood, S. B. (2004). *Fan-out: Measuring Human Control of Multiple Robots*. CHI 2004, 231-238. DOI: https://doi.org/10.1145/985692.985722
    - Зачем: fan-out как число роботов, которыми может одновременно управлять один человек; зависит от neglect tolerance и interaction time. Ближайший концептуальный предшественник ограниченного человеческого внимания.

24. Crandall, J. W., Goodrich, M. A., Olsen, D. R., & Nielsen, C. W. (2005). *Validating Human-Robot Interaction Schemes in Multitasking Environments*. IEEE Transactions on Systems, Man, and Cybernetics Part A. DOI: https://doi.org/10.1109/TSMCA.2005.850587
    - Зачем: эмпирическая/формальная проверка multitasking и взаимодействия одного оператора с несколькими роботами.

25. Crandall, J. W., Cummings, M. L., Della Penna, M., & de Jong, P. M. A. (online 2010 / issue publication to verify). *Computing the Effects of Operator Attention Allocation in Human Control of Multiple Robots*. DOI: https://doi.org/10.1109/TSMCA.2010.2084082
    - OA PDF: https://dspace.mit.edu/bitstreams/393dd377-43db-4709-8447-7104010375cf/download
    - Зачем: распределение внимания оператора между несколькими полуавтономными задачами; почти прямой аналог `H` и расписания окон верификации.

26. Salvucci, D. D., & Taatgen, N. A. (2008). *Threaded Cognition: An Integrated Theory of Concurrent Multitasking*. Psychological Review, 115(1), 101-130. DOI: https://doi.org/10.1037/0033-295X.115.1.101
    - Зачем: несколько когнитивных потоков координируются последовательным procedural resource; теоретическая опора для штрафа переключения `gamma(P)`.

## Современный источник по масштабированию агентов

27. Kim, Y., Gu, K., Park, C., et al. (2025). *Towards a Science of Scaling Agent Systems*. arXiv:2512.08296. PDF: https://arxiv.org/pdf/2512.08296
    - Зачем: 260 конфигураций, сравнение independent/centralized/decentralized/hybrid architectures, diminishing returns, overhead на tool-heavy tasks, сильная зависимость от decomposability и sequentiality.
    - Статус: свежий preprint, пока без peer review; использовать как современную эмпирику второго уровня, не как фундаментальную опору.

## Опциональные источники

28. Vaccaro, M., Almaatouq, A., & Malone, T. (2024). *When Combinations of Humans and AI Are Useful: A Systematic Review and Meta-Analysis*. Nature Human Behaviour, 8, 2293-2303. DOI: https://doi.org/10.1038/s41562-024-02024-1
    - OA PDF: https://www.nature.com/articles/s41562-024-02024-1.pdf
    - Зачем: качественная метааналитическая рамка complementarity. Опционально, потому что outcome преимущественно качество/accuracy, а не время и cost.

29. Monsell, S. (2003). *Task Switching*. Trends in Cognitive Sciences. DOI: https://doi.org/10.1016/S1364-6613(03)00028-7
    - Зачем: обзор switch cost; можно использовать вместо или вместе с Salvucci, если понадобится обосновать `gamma(P)`.

30. Bird, C., Ford, D., Zimmermann, T., et al. (2023). *Taking Flight with Copilot*. Communications of the ACM. DOI/PDF: https://doi.org/10.1145/3589996
    - Зачем: ранние наблюдения о pair-programming workflow; ниже по приоритету, чем Peng, Vaithilingam и Barke.

31. Forsgren, N., Storey, M.-A., Maddila, C., et al. (2021). *The SPACE of Developer Productivity*. DOI: https://doi.org/10.1145/3454122.3454124
    - Зачем: предостережение от сведения developer productivity к одной временной метрике. Полезно для limitations и обсуждения измерений.

## Локальный корпус

В `simple_model_full/literature/` находятся 34 PDF. Все они
обработаны; каждому соответствует одноимённый Markdown-файл в
`simple_model_full/literature_reviews/`. Полный статус и обнаруженные
несовпадения версий перечислены в
`tmp_docs/simple_model_full_source_review_report.md`.

## Ключевые выводы поиска

1. Самый опасный пробел текущего позиционирования не COCOMO, а литература `human supervisory control of multiple robots` и `parallel machines with a common/single server`. Они структурно ближе к M4, чем закон Брукса.
2. Новизну нельзя формулировать как «впервые человек введён как общий последовательный ресурс». Корректнее: синтез task-specific AI effect `k`, режима взаимодействия `r`, DAG/makespan, координационных издержек и человеческой доли `h` применительно к software-engineering agents.
3. Модель не выводит точные эмпирические 55.8%, 14% или -19%. Она позволяет привести разнородные результаты к конфигурационно-зависимому `k` и объяснить, почему один средний процент нельзя переносить между задачами, пользователями и режимами. Без внешнего оценщика `k` модель постфактумна.
4. Метрики исследований несопоставимы напрямую: fixed-task completion time, issues/hour, success rate, quality и self-reported productivity. Для каждой работы надо фиксировать outcome и не переводить его в `k` без оговорок.
5. Gustafson относится к scaled workload/throughput; текущая статья относится к fixed workload/makespan.
6. Brooks не описывает звёздную топологию буквально, но интеграционные издержки через общий код и интерфейсы остаются.
7. Утверждение в текущей модели, что классическая scheduling постановка не учитывает общий человеческий ресурс, надо сузить до конкретной постановки Graham `P|prec|Cmax`; RCPSP и common-server scheduling такие ограничения учитывают.

## Выполненный план анализа корпуса

Для каждого источника в индивидуальном обзоре зафиксированы:

- полная проверенная ссылка и версия публикации;
- статус: peer-reviewed / book / preprint / gray literature;
- исследовательский вопрос;
- объект и выборка;
- topology: one-human-one-agent, one-human-many-agents, communicating agents и т.д.;
- task structure: independent / DAG / sequential / decomposable;
- outcome: time / throughput / effort / quality / success;
- основной результат и uncertainty;
- mapping в параметры модели: `Z`, `k`, `r`, `P`, `C(P)`, `h`, `gamma(P)`, `L`;
- что источник поддерживает;
- что он не позволяет утверждать;
- ближайшее отличие от предлагаемой модели.

## Предлагаемая структура `Related Work`

1. **Empirical effects of generative AI on work productivity**: Peng, Vaithilingam, Brynjolfsson, Becker, Barke, Noy, METR. Синтезировать гетерогенность, а не перечислять проценты.
2. **Software effort and cost estimation**: COCOMO/COCOMO II и Jørgensen. Развести прогноз effort/cost и оптимизацию makespan заданного набора задач.
3. **Scalability laws and coordination overhead**: Amdahl, Gustafson, Gunther, Brooks, Kim et al. Показать fixed vs scaled workload и topology-dependent overhead.
4. **Scheduling with precedence and a shared server**: Graham, Pinedo, common-server scheduling, RCPSP. Явно позиционировать M0-M4 в стандартной notation.
5. **Human attention in supervisory control**: fan-out, Crandall, threaded cognition. Это теоретическое обоснование `h`, `H` и `gamma(P)`.
6. **Synthesis and gap**: существующие ветви по отдельности покрывают effort, parallelism, scheduling, supervision или empirical AI effects; статья объединяет их для фиксированной one-human-many-code-agents topology.

Ориентир объёма: 1,800-2,500 слов, 5-6 тематических подразделов, около 20-25 источников в итоговом тексте. Не пытаться включить все опциональные работы.

## Следующий запуск

1. Начать с `tmp_docs/simple_model_full_source_review_report.md` и каталога `simple_model_full/literature_reviews/`.
2. Отобрать основной корпус из примерно 20--25 источников и распределить по тематическим подразделам Related Work.
3. Синтезировать индивидуальные обзоры в актуальную evidence matrix, сохраняя различия outcomes, версий и исследовательских дизайнов.
4. Согласовать позиционирование вклада и спорные места модели, особенно границу `W/P` после разложения `k=a+h`.
5. Затем обновить `references.bib`, написать `simple_litreview.tex`, подключить его через `\input{simple_litreview.tex}` в `main.tex` и собрать LaTeX.
