# Cummings, Mitchell (2008) — Predicting Controller Capacity in Supervisory Control of Multiple UAVs

## Проверенная версия

- M. L. Cummings, P. J. Mitchell.
- *IEEE Transactions on Systems, Man, and Cybernetics—Part A*, 38(2),
  451--460, DOI `10.1109/TSMCA.2007.914757`; 11-page manuscript/PDF.
- Локальный файл: `../literature/cummings2008_capacity.pdf`.

## Почему включён

Работа расширяет простое отношение neglect/interaction time явными источниками
ожидания: очередью нескольких UAV к оператору, потерей situation awareness и
cognitive reorientation. Это прямое эмпирическое основание для конечности
полезного fan-out и переключения одного capacity-1 operator, но не для численной
калибровки coding agents.

## Дизайн и количественные claims

- **Population:** 12 участников (10 мужчин, 2 женщины), возраст 20--42,
  mean 26.3; девять с ROTC/active-duty background, девять с pilot experience,
  никто без UAV experience; 90--120 минут training.
- **Intervention/conditions:** две 30-минутные randomized/counterbalanced
  sessions с low и high replanning workload (7 против 13 replanning events),
  уровни automation; supervisory-control simulation MAUVE.
- **Comparator:** original fan-out prediction без wait-time components против
  revised prediction с WTI/WTQ/WTSA; within-subject workload/automation contrasts.
- **Outcomes:** interaction wait time WTI, queue wait WTQ, situation-awareness
  wait WTSA и predicted maximum number of UAVs.
- **Estimator:** reported means/SD and repeated-measures mixed-model analysis;
  capacity is model-derived upper-bound prediction, не наблюдаемое число
  успешно завершённых software tasks.
- **Результат:** WTI mean 81.5 s (SD 57.6), WTQ 35.0 s (SD 43.4), WTSA
  263.7 s (SD 239.7). Включение wait times снижает predicted capacity на
  36--67%; даже super-active management-by-exception condition теряет 36% из-за
  wait связанных с situation awareness.
- **Inclusion:** участники, завершившие training и обе simulation conditions;
  детали контекста и workload существенно влияют на оценку.
- **Ограничения переноса:** малая специализированная выборка, homogeneous
  independent UAVs, short simulation, model-derived capacity; авторы прямо
  предупреждают о task/context dependence. Результат нельзя переносить
  количественно на software work.

## Отображение на M4

Поддерживает структурную аналогию: один оператор обслуживает запросы
последовательно, ожидание и переориентация уменьшают полезный fan-out, а
автономность не устраняет потребность в обслуживании. Не поддерживает конкретную
форму `gamma(P)`, software task-DAG, local agent-slot hold, `k`, `a/h` или
accepted-result makespan.

## Постраничная карта PDF

- p. 1 — abstract; wait-time taxonomy and up-to-67% capacity reduction.
- p. 2 — original fan-out model and supervisory-control background.
- p. 3 — revised capacity equation with interaction, queue and SA wait times.
- p. 4 — MAUVE simulation and levels of automation.
- p. 5 — decision support, task environment and measures.
- p. 6 — experimental procedure, workload conditions and hypotheses.
- p. 7 — participant population/design; WTI results.
- p. 8 — WTQ and WTSA results and wait-time proportions.
- p. 9 — Figure 9 capacity drop, context dependence and cognitive reorientation.
- p. 10 — conclusion, limitations and references.
- p. 11 — references continuation and author biographies.

## Допустимый claim

В конкретном UAV simulation учёт очереди, потери situation awareness и
переориентации существенно снизил модельную верхнюю оценку числа систем на
оператора. Это поддерживает capacity-1/finite-fan-out механизм только как
структурную аналогию, не как численную оценку `P` для разработки.
