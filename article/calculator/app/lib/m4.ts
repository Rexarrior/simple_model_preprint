export type Resource = "human" | "agent";

export interface TaskClass {
  id: string;
  name: string;
  aiCycleMultiplier: number;
  humanFraction: number;
  evidence?: {
    kind: "measured" | "proxy" | "assumption";
    label: string;
    url?: string;
    secondaryLabel?: string;
    secondaryUrl?: string;
    publishedAt?: string;
    note: string;
  };
  humanFractionBasis?: string;
}

export interface ProjectTask {
  id: string;
  classId: string;
  name?: string;
  description?: string;
  baselineEffort: number;
  predecessors: string[];
}

export interface ProjectConfig {
  schemaVersion: "m4-calculator/v1";
  projectName: string;
  timeUnit: "hours" | "days";
  p: number;
  c: number;
  gamma: number;
  taskClasses: TaskClass[];
  tasks: ProjectTask[];
}

export interface ScheduleInterval {
  taskId: string;
  taskName: string;
  phase: "specification" | "execution" | "review";
  resource: Resource;
  agent: number;
  start: number;
  end: number;
}

export interface M4Result {
  tHuman: number;
  w4: number;
  l4: number;
  humanBranch: number;
  workBranch: number;
  b4: number;
  activeConstraint: "work" | "critical" | "human";
  criticalPath: string[];
  schedule: {
    makespan: number;
    queueTime: number;
    intervals: ScheduleInterval[];
  };
  demonstratedSpeedup: number;
  speedupCeiling: number;
  gapToBound: number;
  diagnostics: string[];
  dagDepths: Record<string, number>;
  pSweep: Array<{ p: number; makespan: number; ceiling: number }>;
}

const EPSILON = 1e-9;

export const DEMO_CONFIG: ProjectConfig = {
  schemaVersion: "m4-calculator/v1",
  projectName: "API для обработки заказов",
  timeUnit: "hours",
  p: 3,
  c: 1.05,
  gamma: 1.1,
  taskClasses: [
    {
      id: "docs-style",
      name: "Документация, спецификации и малые конфиги",
      aiCycleMultiplier: 0.76,
      humanFraction: 0.4,
      evidence: {
        kind: "proxy",
        label: "Njoku, Sharafi & Khomh, AIware ’26",
        url: "https://doi.org/10.1145/3805760.3814909",
        secondaryLabel: "Gambacorta et al., JFS",
        secondaryUrl: "https://doi.org/10.1016/j.jfs.2026.101543",
        publishedAt: "2026-07",
        note: "Модельный proxy: базовые k=1/1,22≈0,82 скорректированы отношением human/agent merge-rate 77,9%/83,8%, итого k≈0,76. Это не прямой замер полного цикла.",
      },
      humanFractionBasis: "Допущение демо: агент готовит артефакт автономно, человек задаёт рамки и принимает результат.",
    },
    {
      id: "routine-assisted",
      name: "Типовая задача с интерактивным AI-assistant",
      aiCycleMultiplier: 0.82,
      humanFraction: 0.55,
      evidence: {
        kind: "proxy",
        label: "Gambacorta et al., Journal of Financial Stability",
        url: "https://doi.org/10.1016/j.jfs.2026.101543",
        publishedAt: "2026-06",
        note: "В квазиэксперименте CodeFuse число завершённых задач выросло примерно на 22%; инверсия throughput даёт proxy k≈1/1,22=0,82.",
      },
      humanFractionBasis: "Допущение демо: assistant работает внутри сессии разработчика, поэтому постановка, навигация и проверка остаются активным человеческим временем.",
    },
    {
      id: "feature-behavior",
      name: "Feature и изменение поведения системы",
      aiCycleMultiplier: 0.93,
      humanFraction: 0.65,
      evidence: {
        kind: "proxy",
        label: "Njoku, Sharafi & Khomh, AIware ’26",
        url: "https://doi.org/10.1145/3805760.3814909",
        publishedAt: "2026-07",
        note: "Модельный proxy: базовые k≈0,82 скорректированы отношением merge-rate 77,4%/68,7%, итого k≈0,93. Агентные feature-PR принимались реже человеческих.",
      },
      humanFractionBasis: "Допущение демо: архитектурные решения, проверка семантики и исправление пограничных случаев требуют участия человека.",
    },
    {
      id: "infrastructure-quality",
      name: "Инфраструктура, тесты и внутреннее качество",
      aiCycleMultiplier: 0.87,
      humanFraction: 0.6,
      evidence: {
        kind: "proxy",
        label: "Njoku, Sharafi & Khomh, AIware ’26",
        url: "https://doi.org/10.1145/3805760.3814909",
        publishedAt: "2026-07",
        note: "Модельный proxy: базовые k≈0,82 скорректированы отношением merge-rate 77,0%/72,9%, итого k≈0,87. Время авторинга исследование не измеряло.",
      },
      humanFractionBasis: "Допущение демо: агент выполняет механическую часть, человек проверяет CI, окружение и устойчивость изменений.",
    },
    {
      id: "review-verification",
      name: "Ревью и финальная верификация",
      aiCycleMultiplier: 1,
      humanFraction: 0.9,
      evidence: {
        kind: "assumption",
        label: "Hamza, Siemon & Awan, longitudinal DiD",
        url: "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6996078",
        publishedAt: "2026-07",
        note: "Консервативно k=1: ревью стало быстрее и менее подробным, но те же изменения наблюдались в control-репозиториях; причинного ускорения от агентов не показано.",
      },
      humanFractionBasis: "Допущение демо: итоговая ответственность и решение о приёмке остаются человеческими.",
    },
  ],
  tasks: [
    {
      id: "contract",
      classId: "docs-style",
      name: "Контракт API",
      description: "Схема запросов, ответов и критерии валидации",
      baselineEffort: 10,
      predecessors: [],
    },
    {
      id: "storage",
      classId: "feature-behavior",
      name: "Слой хранения",
      baselineEffort: 18,
      predecessors: ["contract"],
    },
    {
      id: "logic",
      classId: "feature-behavior",
      name: "Бизнес-логика",
      baselineEffort: 24,
      predecessors: ["contract"],
    },
    {
      id: "tests",
      classId: "infrastructure-quality",
      name: "Автотесты",
      baselineEffort: 16,
      predecessors: ["storage", "logic"],
    },
    {
      id: "review",
      classId: "review-verification",
      name: "Ревью изменений",
      description: "Проверка архитектуры, кода, тестов и критериев приёмки",
      baselineEffort: 10,
      predecessors: ["tests"],
    },
    {
      id: "release",
      classId: "infrastructure-quality",
      name: "Сборка и выпуск",
      baselineEffort: 8,
      predecessors: ["review"],
    },
  ],
};

export const CONFIG_PROMPT = `Ты помогаешь описать программный проект для калькулятора M4 — фазовой модели работы одного человека с несколькими ИИ-агентами.

Сначала задай уточняющие вопросы, если не определены: одинаковый критерий принятого результата для ручного и AI-сценария, зависимости задач, ручная трудоёмкость, режим использования ИИ и обязательные человеческие проверки. Не скрывай неопределённость и не называй оценку прогнозом.

Для внешней калибровки используй только эмпирические исследования, опубликованные в 2026 году; при наличии выбирай июнь–август 2026. Не переноси коэффициенты из более старых экспериментов в default. Если свежий источник измеряет commits, merge-rate или time-to-merge, а не полный срок принятого результата, пометь оценку как proxy и объясни преобразование.

Затем:
1. Декомпозируй проект на проверяемые задачи с независимыми результатами там, где это содержательно возможно.
2. Не добавляй зависимости только ради порядка: predecessors должны отражать реальную невозможность начать задачу раньше.
3. Объедини похожие задачи в классы. Для каждого класса оцени aiCycleMultiplier = полный срок принятого результата с ИИ / ручной baseline. Значение 0.7 означает цикл на 30% короче ручного, 1.2 — на 20% длиннее.
4. Оцени humanFraction = доля активного человеческого времени именно внутри AI-цикла, а не доля ручного baseline. Например, при k=0.7 и humanFraction=0.4 человек занят 0.28 ручного baseline, агент — 0.42. Не выводи humanFraction автоматически из k: это отдельное допущение.
5. Для каждого класса добавь evidence: measured — прямой замер сопоставимого времени, proxy — косвенная метрика вроде throughput, assumption — экспертное допущение. Для внешнего источника добавь publishedAt в формате YYYY-MM; для assumption без публикации поле пропусти. Если надёжного источника 2026 года нет, честно поставь assumption. В humanFractionBasis кратко объясни оценку доли человека.
6. Параметры c и gamma не могут быть меньше 1. Если нет данных о координационных издержках, поставь 1 и явно предупреди об оптимистичности.
7. Верни только один JSON без markdown и комментариев. Идентификаторы — латиницей, уникальные. Все predecessors должны ссылаться на существующие id, граф обязан быть ацикличным.

Схема результата:
{
  "schemaVersion": "m4-calculator/v1",
  "projectName": "Название проекта",
  "timeUnit": "hours",
  "p": 3,
  "c": 1.0,
  "gamma": 1.0,
  "taskClasses": [
    {
      "id": "feature",
      "name": "Класс для удобства",
      "aiCycleMultiplier": 0.7,
      "humanFraction": 0.4,
      "evidence": {
        "kind": "assumption",
        "label": "Экспертная оценка для этого проекта",
        "note": "Почему выбран такой коэффициент"
      },
      "humanFractionBasis": "Какая работа человека остаётся в цикле"
    }
  ],
  "tasks": [
    {
      "id": "task-1",
      "classId": "feature",
      "name": "Необязательное короткое имя",
      "description": "Необязательное описание и критерий приёмки",
      "baselineEffort": 16,
      "predecessors": []
    }
  ]
}`;

export function validateConfig(config: ProjectConfig): string[] {
  const errors: string[] = [];
  if (config.schemaVersion !== "m4-calculator/v1") {
    errors.push("Неподдерживаемая версия схемы.");
  }
  if (!config.projectName?.trim()) errors.push("Укажите название проекта.");
  if (!Number.isInteger(config.p) || config.p < 1 || config.p > 12) {
    errors.push("Число агентных потоков P должно быть целым от 1 до 12.");
  }
  if (!Number.isFinite(config.c) || config.c < 1) errors.push("C(P) должно быть не меньше 1.");
  if (!Number.isFinite(config.gamma) || config.gamma < 1) {
    errors.push("γ(P) должно быть не меньше 1.");
  }

  const classIds = new Set<string>();
  for (const item of config.taskClasses ?? []) {
    if (!item.id?.trim()) errors.push("У каждого класса должен быть id.");
    if (classIds.has(item.id)) errors.push(`Повторяющийся id класса: ${item.id}.`);
    classIds.add(item.id);
    if (!item.name?.trim()) errors.push(`У класса ${item.id || "без id"} нет названия.`);
    if (!Number.isFinite(item.aiCycleMultiplier) || item.aiCycleMultiplier <= 0) {
      errors.push(`Коэффициент k класса ${item.id} должен быть положительным.`);
    }
    if (!Number.isFinite(item.humanFraction) || item.humanFraction < 0 || item.humanFraction > 1) {
      errors.push(`Доля человека класса ${item.id} должна лежать от 0 до 1.`);
    }
    if (item.evidence) {
      if (!["measured", "proxy", "assumption"].includes(item.evidence.kind)) {
        errors.push(`Класс ${item.id}: evidence.kind должен быть measured, proxy или assumption.`);
      }
      if (!item.evidence.label?.trim() || !item.evidence.note?.trim()) {
        errors.push(`Класс ${item.id}: у evidence нужны label и note.`);
      }
      if (item.evidence.url && !/^https?:\/\//i.test(item.evidence.url)) {
        errors.push(`Класс ${item.id}: ссылка evidence должна начинаться с http:// или https://.`);
      }
      if (item.evidence.secondaryUrl && !/^https?:\/\//i.test(item.evidence.secondaryUrl)) {
        errors.push(`Класс ${item.id}: дополнительная ссылка evidence должна начинаться с http:// или https://.`);
      }
      if (item.evidence.secondaryUrl && !item.evidence.secondaryLabel?.trim()) {
        errors.push(`Класс ${item.id}: для дополнительной ссылки нужен secondaryLabel.`);
      }
      if (item.evidence.publishedAt && !/^2026-(0[1-9]|1[0-2])$/.test(item.evidence.publishedAt)) {
        errors.push(`Класс ${item.id}: publishedAt должен быть месяцем 2026 года в формате YYYY-MM.`);
      }
    }
  }
  if (!config.taskClasses?.length) errors.push("Добавьте хотя бы один класс задач.");

  const taskIds = new Set<string>();
  for (const task of config.tasks ?? []) {
    if (!task.id?.trim()) errors.push("У каждой задачи должен быть id.");
    if (taskIds.has(task.id)) errors.push(`Повторяющийся id задачи: ${task.id}.`);
    taskIds.add(task.id);
    if (!classIds.has(task.classId)) errors.push(`Задача ${task.id} ссылается на неизвестный класс.`);
    if (!Number.isFinite(task.baselineEffort) || task.baselineEffort <= 0) {
      errors.push(`Ручная трудоёмкость задачи ${task.id} должна быть положительной.`);
    }
  }
  if (!config.tasks?.length) errors.push("Добавьте хотя бы одну задачу.");
  for (const task of config.tasks ?? []) {
    for (const predecessor of task.predecessors ?? []) {
      if (!taskIds.has(predecessor)) errors.push(`Задача ${task.id}: неизвестный предшественник ${predecessor}.`);
      if (predecessor === task.id) errors.push(`Задача ${task.id} не может зависеть от себя.`);
    }
  }

  if (errors.length === 0) {
    try {
      topologicalOrder(config.tasks);
    } catch {
      errors.push("Граф задач содержит цикл.");
    }
  }
  return errors;
}

function topologicalOrder(tasks: ProjectTask[]): string[] {
  const predecessors = new Map(tasks.map((task) => [task.id, new Set(task.predecessors)]));
  const successors = new Map(tasks.map((task) => [task.id, [] as string[]]));
  for (const task of tasks) {
    for (const predecessor of task.predecessors) successors.get(predecessor)?.push(task.id);
  }
  const ready = tasks.filter((task) => task.predecessors.length === 0).map((task) => task.id).sort();
  const order: string[] = [];
  while (ready.length) {
    const id = ready.shift()!;
    order.push(id);
    for (const successor of (successors.get(id) ?? []).sort()) {
      const incoming = predecessors.get(successor)!;
      incoming.delete(id);
      if (incoming.size === 0) {
        ready.push(successor);
        ready.sort();
      }
    }
  }
  if (order.length !== tasks.length) throw new Error("cycle");
  return order;
}

function taskDurations(config: ProjectConfig, p = config.p) {
  const classes = new Map(config.taskClasses.map((item) => [item.id, item]));
  return new Map(
    config.tasks.map((task) => {
      const taskClass = classes.get(task.classId)!;
      const aiCycle = task.baselineEffort * taskClass.aiCycleMultiplier;
      const humanBase = aiCycle * taskClass.humanFraction;
      const agentBase = aiCycle - humanBase;
      return [
        task.id,
        {
          manual: task.baselineEffort,
          human: humanBase * config.gamma,
          agent: agentBase * config.c,
          total: humanBase * config.gamma + agentBase * config.c,
          p,
        },
      ];
    }),
  );
}

function graphMetrics(config: ProjectConfig, p = config.p) {
  const order = topologicalOrder(config.tasks);
  const tasks = new Map(config.tasks.map((task) => [task.id, task]));
  const durations = taskDurations(config, p);
  const best = new Map<string, number>();
  const parent = new Map<string, string | null>();
  const depths: Record<string, number> = {};
  for (const id of order) {
    const task = tasks.get(id)!;
    const predecessor = task.predecessors.length
      ? [...task.predecessors].sort((a, b) => (best.get(b)! - best.get(a)!) || a.localeCompare(b))[0]
      : null;
    best.set(id, durations.get(id)!.total + (predecessor ? best.get(predecessor)! : 0));
    parent.set(id, predecessor);
    depths[id] = task.predecessors.length
      ? 1 + Math.max(...task.predecessors.map((item) => depths[item]))
      : 0;
  }
  let last = order[0];
  for (const id of order) if ((best.get(id) ?? 0) > (best.get(last) ?? 0)) last = id;
  const path: string[] = [];
  for (let cursor: string | null = last; cursor; cursor = parent.get(cursor) ?? null) path.unshift(cursor);

  const successors = new Map(config.tasks.map((task) => [task.id, [] as string[]]));
  for (const task of config.tasks) for (const predecessor of task.predecessors) successors.get(predecessor)!.push(task.id);
  const bottom = new Map<string, number>();
  for (const id of [...order].reverse()) {
    const tail = Math.max(0, ...(successors.get(id) ?? []).map((item) => bottom.get(item)!));
    bottom.set(id, durations.get(id)!.total + tail);
  }
  return { order, durations, l4: best.get(last)!, path, depths, bottom };
}

function simulate(config: ProjectConfig, p = config.p) {
  const { durations, bottom } = graphMetrics(config, p);
  const tasks = new Map(config.tasks.map((task) => [task.id, task]));
  const taskPhases = new Map(
    config.tasks.map((task) => {
      const duration = durations.get(task.id)!;
      const phases = [
        { phase: "specification" as const, resource: "human" as const, duration: duration.human * 0.4 },
        { phase: "execution" as const, resource: "agent" as const, duration: duration.agent },
        { phase: "review" as const, resource: "human" as const, duration: duration.human * 0.6 },
      ].filter((item) => item.duration > EPSILON);
      return [task.id, phases];
    }),
  );

  const taskKey = (a: string, b: string) =>
    (bottom.get(b)! - bottom.get(a)!) ||
    (durations.get(b)!.total - durations.get(a)!.total) ||
    a.localeCompare(b);
  const assigned = new Map<string, number>();
  const agentTasks: Array<string | null> = Array.from({ length: p }, () => null);
  const completed = new Set<string>();
  const cursor = new Map<string, number>();
  const runningAgent = new Map<string, { phaseIndex: number; end: number }>();
  let runningHuman: { taskId: string; phaseIndex: number; end: number } | null = null;
  const humanQueue: Array<{ requestedAt: number; taskId: string; phaseIndex: number }> = [];
  const intervals: ScheduleInterval[] = [];
  let queueTime = 0;
  let now = 0;

  const offerPhase = (taskId: string, requestedAt: number) => {
    const phaseIndex = cursor.get(taskId)!;
    const phase = taskPhases.get(taskId)![phaseIndex];
    if (phase.resource === "human") {
      humanQueue.push({ requestedAt, taskId, phaseIndex });
    } else {
      const end = requestedAt + phase.duration;
      runningAgent.set(taskId, { phaseIndex, end });
      intervals.push({
        taskId,
        taskName: tasks.get(taskId)!.name || taskId,
        phase: phase.phase,
        resource: phase.resource,
        agent: assigned.get(taskId)!,
        start: requestedAt,
        end,
      });
    }
  };

  const assignReady = (at: number) => {
    const ready = config.tasks
      .filter((task) => !assigned.has(task.id) && task.predecessors.every((item) => completed.has(item)))
      .map((task) => task.id)
      .sort(taskKey);
    const free = agentTasks.map((taskId, index) => (taskId === null ? index : -1)).filter((index) => index >= 0);
    for (let index = 0; index < Math.min(ready.length, free.length); index += 1) {
      const taskId = ready[index];
      const agentIndex = free[index];
      assigned.set(taskId, agentIndex + 1);
      agentTasks[agentIndex] = taskId;
      cursor.set(taskId, 0);
      offerPhase(taskId, at);
    }
  };

  const startHuman = (at: number) => {
    if (runningHuman || humanQueue.length === 0) return;
    humanQueue.sort((a, b) =>
      (a.requestedAt - b.requestedAt) || taskKey(a.taskId, b.taskId) || (a.phaseIndex - b.phaseIndex),
    );
    const request = humanQueue.shift()!;
    const phase = taskPhases.get(request.taskId)![request.phaseIndex];
    queueTime += Math.max(0, at - request.requestedAt);
    runningHuman = { taskId: request.taskId, phaseIndex: request.phaseIndex, end: at + phase.duration };
    intervals.push({
      taskId: request.taskId,
      taskName: tasks.get(request.taskId)!.name || request.taskId,
      phase: phase.phase,
      resource: "human",
      agent: assigned.get(request.taskId)!,
      start: at,
      end: at + phase.duration,
    });
  };

  assignReady(0);
  startHuman(0);
  let guard = 0;
  while (completed.size < config.tasks.length && guard < 10000) {
    guard += 1;
    const eventTimes = [...runningAgent.values()].map((item) => item.end);
    if (runningHuman) eventTimes.push(runningHuman.end);
    if (!eventTimes.length) throw new Error("Расписание заблокировано.");
    now = Math.min(...eventTimes);
    const finished: string[] = [];
    for (const [taskId, running] of [...runningAgent.entries()]) {
      if (Math.abs(running.end - now) > EPSILON) continue;
      runningAgent.delete(taskId);
      cursor.set(taskId, running.phaseIndex + 1);
      finished.push(taskId);
    }
    if (runningHuman && Math.abs(runningHuman.end - now) <= EPSILON) {
      const done = runningHuman;
      runningHuman = null;
      cursor.set(done.taskId, done.phaseIndex + 1);
      finished.push(done.taskId);
    }
    const continuing: string[] = [];
    for (const taskId of finished) {
      if (cursor.get(taskId)! >= taskPhases.get(taskId)!.length) {
        completed.add(taskId);
        agentTasks[assigned.get(taskId)! - 1] = null;
      } else {
        continuing.push(taskId);
      }
    }
    continuing.sort(taskKey).forEach((taskId) => offerPhase(taskId, now));
    assignReady(now);
    startHuman(now);
  }
  if (guard >= 10000) throw new Error("Расписание превысило лимит событий.");
  return { makespan: now, queueTime, intervals: intervals.sort((a, b) => a.start - b.start || a.taskId.localeCompare(b.taskId)) };
}

function calculateAtP(config: ProjectConfig, p: number) {
  const graph = graphMetrics(config, p);
  const schedule = simulate(config, p);
  const tHuman = config.tasks.reduce((sum, task) => sum + task.baselineEffort, 0);
  const w4 = [...graph.durations.values()].reduce((sum, item) => sum + item.total, 0);
  const humanBranch = [...graph.durations.values()].reduce((sum, item) => sum + item.human, 0);
  const workBranch = w4 / p;
  const b4 = Math.max(workBranch, graph.l4, humanBranch);
  return { graph, schedule, tHuman, w4, humanBranch, workBranch, b4 };
}

export function calculateM4(config: ProjectConfig): M4Result {
  const errors = validateConfig(config);
  if (errors.length) throw new Error(errors.join(" "));
  const current = calculateAtP(config, config.p);
  const branches = [
    { name: "work" as const, value: current.workBranch },
    { name: "critical" as const, value: current.graph.l4 },
    { name: "human" as const, value: current.humanBranch },
  ].sort((a, b) => b.value - a.value);
  const gap = Math.max(0, current.schedule.makespan - current.b4);
  const diagnostics: string[] = [];
  if (branches[0].name === "work") diagnostics.push("Ограничивает суммарная загрузка потоков: проверьте большее P и цену координации.");
  if (branches[0].name === "critical") diagnostics.push("Ограничивает критический путь: в первую очередь дробите или ускоряйте задачи на нём.");
  if (branches[0].name === "human") diagnostics.push("Ограничивает человеческое внимание: сокращайте постановку, ревью и число обязательных проверок.");
  if (gap / current.b4 > 0.05) diagnostics.push("Фазовая очередь создаёт заметный разрыв к нижней границе: улучшайте порядок запуска и human-checkpoints.");
  if (config.c > 1 || config.gamma > 1) diagnostics.push("Учтены издержки параллелизма; сравните несколько P, а не максимальное число агентов.");
  if (config.c === 1 && config.gamma === 1) diagnostics.push("C(P)=γ(P)=1 — оптимистичное предположение. Проверьте чувствительность к координационным издержкам.");

  const maxP = Math.max(6, Math.min(8, config.tasks.length));
  const pSweep = Array.from({ length: maxP }, (_, index) => index + 1).map((p) => {
    const point = calculateAtP(config, p);
    return { p, makespan: point.schedule.makespan, ceiling: point.tHuman / point.b4 };
  });
  return {
    tHuman: current.tHuman,
    w4: current.w4,
    l4: current.graph.l4,
    humanBranch: current.humanBranch,
    workBranch: current.workBranch,
    b4: current.b4,
    activeConstraint: branches[0].name,
    criticalPath: current.graph.path,
    schedule: current.schedule,
    demonstratedSpeedup: current.tHuman / current.schedule.makespan,
    speedupCeiling: current.tHuman / current.b4,
    gapToBound: gap,
    diagnostics,
    dagDepths: current.graph.depths,
    pSweep,
  };
}
