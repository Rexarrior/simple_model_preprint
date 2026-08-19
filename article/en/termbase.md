# Translation termbase

American English is used throughout. Terms in the right-hand column are
normative unless a translation query explicitly records an exception.

| Russian / concept | Canonical English |
|---|---|
| человеко-агентная ячейка | human--agent cell |
| фиксированный объём работ | fixed workload |
| принятый результат | accepted result |
| критерий приёмки | acceptance criterion |
| исходный сценарий без ИИ | no-AI baseline |
| трудоёмкость | effort |
| календарное время | elapsed time |
| активное время | active time |
| время завершения всех работ | makespan |
| задача | task |
| сложность задачи $Z_i$ | task size $Z_i$ |
| режим работы | operating mode |
| интерактивный режим | interactive mode |
| делегированный режим | delegated mode |
| полностью автономный режим | fully autonomous mode |
| автономная агентная фаза | autonomous agent phase |
| человеческая фаза | human-attention phase; human phase after first definition |
| агентная составляющая | agent component |
| человеческая составляющая | human component |
| агентный поток | agent stream in process descriptions |
| агентный слот | agent slot in the formal resource model |
| управляемый / настроенный параллелизм | configured parallelism |
| доступная мощность | available capacity |
| граф зависимостей задач | task-dependency DAG; task-DAG after first definition |
| граф фаз | phase graph |
| ресурсно-дополненный фазовый граф | resource-augmented phase graph |
| ресурсно-дополненный критический путь | resource-augmented critical path |
| критический путь | critical path |
| нижняя граница | lower bound |
| структурная нижняя граница | structural lower bound |
| допустимое расписание | feasible schedule |
| доказанный оптимум | certified optimum |
| точный решатель | exact solver |
| локальная блокировка | local blocking |
| удержание слота | slot retention |
| очередь к разработчику | queue for developer attention |
| межагентные интеграционные издержки | cross-stream integration overhead |
| издержки переключения внимания | attention-switching overhead |
| декомпозиция | decomposition |
| гранулярность | granularity |
| оценочная величина эксперимента | estimand |
| фиксированная политика | fixed policy |
| вычислительная верификация | computational verification |
| эмпирическая калибровка | empirical calibration |
| анализ чувствительности | sensitivity analysis |

## Required distinctions

- $B_j$ is a lower bound; $T(\pi)$ is the makespan of a particular schedule or
  policy; $T^*$ is the optimum only when optimality is certified.
- $k_i^{(r)}$ is a normalized duration relative to an estimated baseline, not a
  causal effect of AI. $\hat{k}_i^{(r)}$ is its prospective estimate.
- $a_i^{(r)}$ and $h_i^{(r)}$ are normalized components, not necessarily
  proportions or shares.
- A fully autonomous mode is not an autonomous agent phase within a delegated
  task.
- Available capacity is not the same as configured parallelism.
- Computational verification on synthetic scenarios is not empirical
  validation or a population estimate.
- `OPTIMAL` and `FEASIBLE` retain their literal solver meanings.
- Use `resource-augmented critical path`, never `critical chain`.
