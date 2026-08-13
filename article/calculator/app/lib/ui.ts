import { CONFIG_PROMPT, DEMO_CONFIG, type ProjectConfig } from "./m4";

export type Locale = "en" | "ru";
export type ThemePreference = "auto" | "light" | "dark";

const ENGLISH_PROMPT = `You are helping describe a software project for the M4 calculator, a phase-based model of one person working with several AI agents.

First ask clarifying questions if any of these are undefined: a shared acceptance criterion for the manual and AI-assisted scenarios, task dependencies, baseline effort without AI, how AI will be used, and mandatory human checks. Keep uncertainty explicit and do not present an estimate as a forecast.

For external calibration, use only empirical studies published in 2026; prefer June–August 2026 when available. Do not use coefficients from older experiments as defaults. If a recent source measures commits, merge rate, or time to merge rather than end-to-end time to an accepted result, mark the estimate as a proxy and explain the conversion.

Then:
1. Decompose the project into verifiable tasks with independent outcomes wherever that is substantively possible.
2. Do not add dependencies merely to impose an order: predecessors must reflect a real inability to start the task earlier.
3. Group similar tasks into classes. For each class, estimate aiCycleMultiplier = end-to-end time to an accepted result with AI / manual baseline. A value of 0.7 means a cycle 30% shorter than manual work; 1.2 means 20% longer.
4. Estimate humanFraction = the share of active human time inside the AI cycle, not a share of the manual baseline. For example, with k=0.7 and humanFraction=0.4, the human is active for 0.28 of the manual baseline and the agent for 0.42. Do not derive humanFraction automatically from k: it is a separate assumption.
5. Add evidence for every class and set kind to measured for directly comparable timing measurements, proxy for indirect metrics such as throughput, or assumption for expert judgment. Add publishedAt in YYYY-MM format for an external source; omit it for an unpublished assumption. If no reliable 2026 source exists, explicitly use assumption. Briefly explain the human share in humanFractionBasis.
6. Parameters c and gamma cannot be below 1. If coordination overhead is unknown, use 1 and explicitly warn that this is optimistic.
7. Return exactly one JSON object without Markdown or comments. IDs must be unique ASCII identifiers. Every predecessor must reference an existing ID, and the graph must be acyclic.

Result schema:
{
  "schemaVersion": "m4-calculator/v1",
  "projectName": "Project name",
  "timeUnit": "hours",
  "p": 3,
  "c": 1.0,
  "gamma": 1.0,
  "taskClasses": [
    {
      "id": "feature",
      "name": "Convenient class name",
      "aiCycleMultiplier": 0.7,
      "humanFraction": 0.4,
      "evidence": {
        "kind": "assumption",
        "label": "Expert estimate for this project",
        "note": "Why this coefficient was selected"
      },
      "humanFractionBasis": "Human work that remains inside the cycle"
    }
  ],
  "tasks": [
    {
      "id": "task-1",
      "classId": "feature",
      "name": "Optional short name",
      "description": "Optional description and acceptance criterion",
      "baselineEffort": 16,
      "predecessors": []
    }
  ]
}`;

const englishClassCopy: Record<string, Pick<ProjectConfig["taskClasses"][number], "name" | "humanFractionBasis"> & { note: string }> = {
  "docs-style": {
    name: "Documentation, specifications, and small configuration changes",
    note: "Model proxy: baseline k=1/1.22≈0.82 is adjusted by the human/agent merge-rate ratio 77.9%/83.8%, resulting in k≈0.76. This is not a direct full-cycle measurement.",
    humanFractionBasis: "Demo assumption: the agent prepares the artifact autonomously; the human defines constraints and accepts the result.",
  },
  "routine-assisted": {
    name: "Routine task with an interactive AI assistant",
    note: "In the CodeFuse quasi-experiment, completed tasks increased by about 22%; inverting throughput gives the proxy k≈1/1.22=0.82.",
    humanFractionBasis: "Demo assumption: the assistant works inside the developer session, so framing, navigation, and verification remain active human time.",
  },
  "feature-behavior": {
    name: "Features and behavior changes",
    note: "Model proxy: baseline k≈0.82 is adjusted by the merge-rate ratio 77.4%/68.7%, resulting in k≈0.93. Agent-authored feature PRs were merged less often than human-authored ones.",
    humanFractionBasis: "Demo assumption: architecture decisions, semantic verification, and edge-case correction require human involvement.",
  },
  "infrastructure-quality": {
    name: "Infrastructure, testing, and internal quality",
    note: "Model proxy: baseline k≈0.82 is adjusted by the merge-rate ratio 77.0%/72.9%, resulting in k≈0.87. The study did not measure authoring time.",
    humanFractionBasis: "Demo assumption: the agent performs the mechanical work; the human verifies CI, environment behavior, and the resilience of the changes.",
  },
  "review-verification": {
    name: "Review and final verification",
    note: "Conservative k=1: reviews became faster and less detailed, but similar changes appeared in control repositories, so no causal agent speedup was demonstrated.",
    humanFractionBasis: "Demo assumption: final accountability and the acceptance decision remain human.",
  },
};

const englishTaskCopy: Record<string, { name: string; description?: string }> = {
  contract: { name: "API contract", description: "Request and response schemas plus validation criteria" },
  storage: { name: "Storage layer" },
  logic: { name: "Business logic" },
  tests: { name: "Automated tests" },
  review: { name: "Change review", description: "Architecture, code, tests, and acceptance-criteria verification" },
  release: { name: "Build and release" },
};

const DEMO_CONFIG_EN: ProjectConfig = {
  ...DEMO_CONFIG,
  projectName: "Order-processing API",
  taskClasses: DEMO_CONFIG.taskClasses.map((item) => ({
    ...item,
    name: englishClassCopy[item.id]?.name ?? item.name,
    humanFractionBasis: englishClassCopy[item.id]?.humanFractionBasis ?? item.humanFractionBasis,
    evidence: item.evidence ? { ...item.evidence, note: englishClassCopy[item.id]?.note ?? item.evidence.note } : undefined,
  })),
  tasks: DEMO_CONFIG.tasks.map((item) => ({ ...item, ...(englishTaskCopy[item.id] ?? {}) })),
};

export const DEMO_CONFIGS: Record<Locale, ProjectConfig> = { en: DEMO_CONFIG_EN, ru: DEMO_CONFIG };
export const CONFIG_PROMPTS: Record<Locale, string> = { en: ENGLISH_PROMPT, ru: CONFIG_PROMPT };

export const UI = {
  en: {
    nav: { aria: "Page navigation", import: "Import", model: "Model", results: "Results" },
    theme: { label: "Theme", auto: "Auto", light: "Light", dark: "Dark" },
    brandAria: "M4 Workbench — back to top",
    hero: {
      eyebrow: "M4 planning calculator · runs entirely in your browser",
      title: "Stress-test your development plan",
      emphasis: "before launching agents.",
      copy: "Describe tasks, dependencies, and human checks. The calculator will show a feasible schedule, the speedup ceiling, and where more parallelism stops helping.",
      start: "Start with the prompt",
      demo: "Load example",
      aria: "Current example",
      speedup: "Scenario speedup",
      ceiling: "Model ceiling",
      constraint: "Active constraint",
    },
    privacy: "Unless you opt in to sharing, your configuration and results never leave your browser. All calculations run locally; no API request is made.",
    import: {
      title: "Let AI draft your model",
      copy: "Send this prompt and your project description to any AI assistant. It will ask clarifying questions and return JSON ready to import.",
      promptTitle: "Decomposition for M4",
      copied: "Copied ✓",
      copyButton: "Copy",
      note: "The prompt asks the AI to state its assumptions explicitly and not present parameter estimates as measured forecasts.",
      jsonTitle: "Paste the configuration",
      current: "Current",
      textareaAria: "JSON configuration",
      check: "Check the configuration:",
      importButton: "Validate and import",
      download: "Download JSON",
    },
    model: {
      title: "Review and refine the plan",
      copy: "Use the editor to review the AI-generated draft. Class parameters apply to every task of that type.",
      project: "Project",
      projectHelp: "Scenario label; does not affect the calculation.",
      streams: "Agent streams P",
      streamsHelp: "Maximum number of tasks AI agents can work on concurrently.",
      agentOverhead: "C(P) · agent overhead",
      agentOverheadHelp: "1.05 means agent work takes 5% longer due to coordination.",
      humanOverhead: "γ(P) · human overhead",
      humanOverheadHelp: "1.10 means 10% more human time due to switching and queues.",
      guideAria: "How to read model parameters",
      fullCycle: "End-to-end AI-assisted cycle",
      fullCycleHelp: "End-to-end time to an accepted result with AI, divided by the manual baseline. 0.7 is 30% faster; 1.2 is 20% slower.",
      humanShare: "Human share",
      humanShareHelp: "The fraction of the AI-assisted cycle during which a human actively frames, checks, or fixes the work—not a fraction of the manual baseline.",
      baseline: "Manual baseline",
      baselineHelp: "Time to the same accepted result without AI. Both scenarios need the same definition of done.",
      parallel: "Parallel streams",
      parallelHelp: "Maximum number of agent tasks that can run concurrently. A stream remains occupied until human acceptance.",
      researchStrong: "Research snapshot: 2026 · June–July prioritized.",
      research: "The k values are reference estimates derived from recent empirical studies, not universal coefficients. q, C(P), and γ(P) remain explicit assumptions.",
      sources: "Calibration sources and method",
      sourcesMeta: "3 publications · conversion formulas · limitations",
      source1: "Quasi-experiment with 1,219 developers: the M4-relevant result is an increase of roughly 22% in completed tasks. We use it as a proxy for end-to-end cycle time:",
      source2a: "Analysis of 40,214 PRs. We adjust k using merge rates: docs/style, 83.8% for agents vs 77.9% for humans; feature/behavior, 68.7% vs 77.4%; infrastructure, 72.9% vs 77.0%. This gives:",
      source2b: "Agents had a shorter overall time to merge, but we do not use it directly in k because it excludes framing, generation, and retries.",
      source3: "Longitudinal difference-in-differences study with 669 developers and 228 controls. Reviews became faster and less detailed, but a similar shift appeared in control repositories. We therefore do not attribute a causal speedup to agents:",
      caveatStrong: "Limitations.",
      caveat: "All coefficients are based on 2026 publications, but combining throughput and merge-rate evidence is a modeling choice. Project-specific measurements should take precedence over this example.",
      tasks: "Tasks",
      classes: "Classes",
      name: "Name",
      aiCycle: "AI cycle k",
      humanFraction: "Human share q",
      perBaseline: "For a manual baseline of 1 {unit}:",
      fullCycleShort: "the end-to-end AI-assisted cycle takes {value} {unit}, with the human active for {human} {unit} and the agent working for {agent} {unit}.",
      whyQ: "Why q={value}:",
      addClass: "＋ Add task class",
      optional: "Optional",
      taskClass: "Class",
      baselineLabel: "Manual baseline, {unit}",
      sameResult: "Same accepted result without AI",
      predecessors: "Comma-separated predecessors",
      description: "Description / acceptance criterion",
      descriptionPlaceholder: "Optional, but useful for AI",
      addTask: "＋ Add task",
      removeClass: "Remove class {name}",
      removeTask: "Remove task {name}",
      consentAria: "Consent to sharing this calculation",
      consentTitle: "Share this calculation to help improve the model",
      consentHelp: "When enabled, clicking Calculate saves the configuration and result to help improve the model. This option is off by default.",
      routeShared: "Local calculation → opt-in saving",
      routeLocal: "Local JavaScript only · no API request",
      calculate: "Calculate scenario",
    },
    results: {
      title: "What limits the speedup",
      copy: "This is a scenario estimate for the entered parameters, not a delivery-date forecast.",
      manual: "Manual baseline · Tₕ",
      manualHelp: "The same accepted scope without AI",
      schedule: "Schedule · T(π)",
      scheduleHelp: "Feasible schedule duration",
      bound: "Lower bound · B₄",
      boundHelp: "The model rules out a shorter duration",
      speedup: "Speedup",
      speedupHelp: "Scenario estimate → theoretical ceiling",
      load: "load",
      critical: "critical path",
      human: "human",
      gap: "Schedule gap to the bound:",
      queue: "Human queue:",
      sweep: "Duration at different P",
      dag: "Critical path and dependencies",
      criticalLegend: "● critical path",
      gantt: "Phases, queues, and occupied slots",
      humanPhase: "Human phase",
      agentPhase: "Agent phase",
      held: "Agent slot reserved",
      next: "What to try next",
    },
    footer: "Every conclusion is conditional on the entered k, h, C(P), γ(P), DAG, and acceptance criterion. The calculator helps compare ways of organizing the work; it does not replace local calibration.",
    top: "Back to top ↑",
    status: {
      imported: "Configuration imported. Calculation completed locally.",
      invalidJson: "Could not parse the JSON.",
      localDone: "Done. The configuration and result were not sent to the server.",
      saving: "Saving the calculation you chose to share…",
      saved: "Calculation saved. ID: {id}…",
      failed: "The local calculation is ready, but it could not be saved.",
      newClass: "New class",
      newTask: "New task",
    },
    units: { hours: "h", days: "d" },
    constraints: { work: "Agent capacity", critical: "Critical path", human: "Human attention" },
    evidence: { measured: "Direct measurement", proxy: "Proxy", assumption: "Assumption" },
    phases: { specification: "specification", execution: "execution", review: "review" },
  },
  ru: {
    nav: { aria: "Навигация по странице", import: "Импорт", model: "Модель", results: "Результат" },
    theme: { label: "Тема", auto: "Авто", light: "Светлая", dark: "Тёмная" },
    brandAria: "M4 Workbench — наверх",
    hero: {
      eyebrow: "Исследовательский калькулятор M4 · всё считается в браузере",
      title: "Обкатайте план разработки",
      emphasis: "до запуска агентов.",
      copy: "Опишите задачи, зависимости и человеческие проверки. Калькулятор покажет достижимое расписание, потолок ускорения и место, где параллелизм перестаёт помогать.",
      start: "Начать с промпта",
      demo: "Загрузить пример",
      aria: "Текущий пример",
      speedup: "Предъявленное ускорение",
      ceiling: "Потолок модели",
      constraint: "Активное ограничение",
    },
    privacy: "Пока согласие не включено, конфигурация и результаты не покидают браузер. Никакого серверного расчёта.",
    import: {
      title: "Пусть ИИ подготовит черновик модели",
      copy: "Передайте промпт любому ИИ вместе с описанием проекта. Он задаст вопросы и вернёт JSON для импорта.",
      promptTitle: "Декомпозиция для M4",
      copied: "Скопировано ✓",
      copyButton: "Копировать",
      note: "Промпт просит ИИ не скрывать предположения и не выдавать оценку параметров за измеренный прогноз.",
      jsonTitle: "Вставьте конфигурацию",
      current: "Текущая",
      textareaAria: "JSON конфигурация",
      check: "Проверьте конфигурацию:",
      importButton: "Проверить и импортировать",
      download: "Скачать JSON",
    },
    model: {
      title: "Подправьте план вручную",
      copy: "Редактор нужен для проверки AI-черновика. Параметры класса применяются ко всем задачам этого типа.",
      project: "Проект", projectHelp: "Подпись сценария; на расчёт не влияет.",
      streams: "Агентных потоков P", streamsHelp: "Сколько задач ИИ может вести параллельно.",
      agentOverhead: "C(P) · издержки агентов", agentOverheadHelp: "1,05 = агентная работа на 5% дольше из-за координации.",
      humanOverhead: "γ(P) · издержки человека", humanOverheadHelp: "1,10 = на 10% больше времени из-за переключений и очередей.",
      guideAria: "Как читать параметры модели",
      fullCycle: "Полный AI-цикл", fullCycleHelp: "Отношение срока принятого результата с ИИ к ручному baseline. 0,7 — на 30% быстрее; 1,2 — на 20% медленнее.",
      humanShare: "Доля человека", humanShareHelp: "Часть именно AI-цикла, когда человек активно ставит, проверяет или исправляет. Это не доля ручного baseline.",
      baseline: "Ручной baseline", baselineHelp: "Сколько занял бы тот же принятый результат без ИИ. Нужен одинаковый критерий готовности в обоих сценариях.",
      parallel: "Параллельные потоки", parallelHelp: "Лимит одновременно запущенных агентных задач. Поток занят до человеческой приёмки результата.",
      researchStrong: "Срез исследований: 2026 год · приоритет июнь–июль.",
      research: "Значения k — модельные ориентиры из свежих эмпирических работ, а не универсальные коэффициенты. q, C(P) и γ(P) остаются явными допущениями.",
      sources: "Источники и методика калибровки", sourcesMeta: "3 публикации · формулы пересчёта · ограничения",
      source1: "Квазиэксперимент с 1 219 разработчиками: наиболее содержательная для M4 метрика — рост числа завершённых задач примерно на 22%. Используем её как throughput-proxy полного цикла:",
      source2a: "Анализ 40 214 PR. Для поправок использованы merge-rate: docs/style — 83,8% у агентов против 77,9% у людей; feature/behavior — 68,7% против 77,4%; infrastructure — 72,9% против 77,0%. Получаются:",
      source2b: "Общее time-to-merge агентов было короче, но в k его напрямую не подставляем: оно не включает постановку, генерацию и повторные попытки.",
      source3: "Longitudinal DiD: 669 разработчиков и 228 участников контрольной группы. Ревью стало быстрее и менее подробным, но похожая динамика была и в control-репозиториях. Поэтому агентного причинного ускорения не заявляем:",
      caveatStrong: "Граница применимости.", caveat: "Все коэффициенты относятся к публикациям 2026 года, но соединение throughput и merge-rate — наше модельное допущение. Собственные замеры проекта должны иметь приоритет над этим демо.",
      tasks: "Задачи", classes: "Классы", name: "Название", aiCycle: "AI-цикл k", humanFraction: "Доля человека q",
      perBaseline: "На 1 {unit} ручного baseline:", fullCycleShort: "весь AI-цикл — {value} {unit}, из них человек активен {human} {unit}, агент работает {agent} {unit}.", whyQ: "Почему q={value}:",
      addClass: "＋ Добавить класс задач", optional: "Необязательно", taskClass: "Класс", baselineLabel: "Ручной baseline, {unit}", sameResult: "Тот же результат без ИИ",
      predecessors: "Предшественники через запятую", description: "Описание / критерий приёмки", descriptionPlaceholder: "Необязательно, но полезно для ИИ", addTask: "＋ Добавить задачу",
      removeClass: "Удалить класс {name}", removeTask: "Удалить задачу {name}",
      consentAria: "Не против поделиться расчётами", consentTitle: "Не против поделиться расчётами", consentHelp: "Если включить, после нажатия кнопки сохраним конфигурацию и результат для развития модели. По умолчанию выключено.",
      routeShared: "Локальный расчёт → добровольное сохранение", routeLocal: "Только локальный JavaScript · без API-запроса", calculate: "Рассчитать сценарий",
    },
    results: {
      title: "Что ограничивает ускорение", copy: "Это оценка сценария при заданных параметрах, а не прогноз календарного срока.",
      manual: "Ручной baseline · Tₕ", manualHelp: "Тот же принятый объём без ИИ", schedule: "Расписание · T(π)", scheduleHelp: "Предъявленный достижимый срок",
      bound: "Нижняя граница · B₄", boundHelp: "Быстрее этого модель не допускает", speedup: "Ускорение", speedupHelp: "Расписание → теоретический потолок",
      load: "загрузка", critical: "критический путь", human: "человек", gap: "Разрыв расписания к границе:", queue: "Очередь к человеку:", sweep: "Срок при разном P",
      dag: "Критический путь и зависимости", criticalLegend: "● критический путь", gantt: "Фазы, очередь и удержание слотов", humanPhase: "Human-фаза", agentPhase: "Agent-фаза", held: "Слот удерживается", next: "Что попробовать следующим",
    },
    footer: "Все выводы условны относительно введённых k, h, C(P), γ(P), DAG и критерия приёмки. Калькулятор помогает сравнивать организацию работы, но не заменяет локальную калибровку.",
    top: "Наверх ↑",
    status: {
      imported: "Конфигурация импортирована. Расчёт выполнен локально.", invalidJson: "Не удалось разобрать JSON.", localDone: "Готово. Конфигурация и результат не отправлялись на сервер.",
      saving: "Сохраняем обезличенный расчёт…", saved: "Расчёт сохранён. Идентификатор: {id}…", failed: "Локальный расчёт готов, но сохранить его не удалось.", newClass: "Новый класс", newTask: "Новая задача",
    },
    units: { hours: "ч", days: "дн" },
    constraints: { work: "Загрузка потоков", critical: "Критический путь", human: "Внимание человека" },
    evidence: { measured: "Прямой замер", proxy: "Прокси", assumption: "Допущение" },
    phases: { specification: "постановка", execution: "выполнение", review: "проверка" },
  },
} as const;

const diagnosticEnglish = new Map<string, string>([
  ["Ограничивает суммарная загрузка потоков: проверьте большее P и цену координации.", "Agent capacity is the binding constraint: test a larger P and account for coordination costs."],
  ["Ограничивает критический путь: в первую очередь дробите или ускоряйте задачи на нём.", "The critical path is binding: split or accelerate its tasks first."],
  ["Ограничивает человеческое внимание: сокращайте постановку, ревью и число обязательных проверок.", "Human attention is binding: reduce framing, review effort, and mandatory checks."],
  ["Фазовая очередь создаёт заметный разрыв к нижней границе: улучшайте порядок запуска и human-checkpoints.", "Phase queues create a material gap to the lower bound: improve launch order and human checkpoints."],
  ["Учтены издержки параллелизма; сравните несколько P, а не максимальное число агентов.", "Parallelism overhead is included; compare several P values instead of choosing the maximum number of agents."],
  ["C(P)=γ(P)=1 — оптимистичное предположение. Проверьте чувствительность к координационным издержкам.", "C(P)=γ(P)=1 is optimistic. Test sensitivity to coordination overhead."],
]);

export function localizeDiagnostic(value: string, locale: Locale) {
  return locale === "en" ? diagnosticEnglish.get(value) ?? value : value;
}

export function localizeValidationErrors(errors: string[], locale: Locale) {
  if (locale === "ru") return errors;
  return errors.map((error) => {
    const exact: Record<string, string> = {
      "Неподдерживаемая версия схемы.": "Unsupported schema version.",
      "Укажите название проекта.": "Enter a project name.",
      "Число агентных потоков P должно быть целым от 1 до 12.": "Agent streams P must be an integer from 1 to 12.",
      "C(P) должно быть не меньше 1.": "C(P) must be at least 1.",
      "γ(P) должно быть не меньше 1.": "γ(P) must be at least 1.",
      "У каждого класса должен быть id.": "Every class must have an ID.",
      "Добавьте хотя бы один класс задач.": "Add at least one task class.",
      "У каждой задачи должен быть id.": "Every task must have an ID.",
      "Добавьте хотя бы одну задачу.": "Add at least one task.",
      "Граф задач содержит цикл.": "The task graph contains a cycle.",
    };
    if (exact[error]) return exact[error];
    return error
      .replace(/^Повторяющийся id класса: (.+)\.$/, "Duplicate class ID: $1.")
      .replace(/^У класса (.+) нет названия\.$/, "Class $1 has no name.")
      .replace(/^Коэффициент k класса (.+) должен быть положительным\.$/, "Class $1 must have a positive k coefficient.")
      .replace(/^Доля человека класса (.+) должна лежать от 0 до 1\.$/, "Class $1 must have a human share between 0 and 1.")
      .replace(/^Класс (.+): evidence\.kind должен быть measured, proxy или assumption\.$/, "Class $1: evidence.kind must be measured, proxy, or assumption.")
      .replace(/^Класс (.+): у evidence нужны label и note\.$/, "Class $1: evidence requires label and note.")
      .replace(/^Класс (.+): ссылка evidence должна начинаться с http:\/\/ или https:\/\/\.$/, "Class $1: the evidence URL must start with http:// or https://.")
      .replace(/^Класс (.+): дополнительная ссылка evidence должна начинаться с http:\/\/ или https:\/\/\.$/, "Class $1: the secondary evidence URL must start with http:// or https://.")
      .replace(/^Класс (.+): для дополнительной ссылки нужен secondaryLabel\.$/, "Class $1: a secondary URL requires secondaryLabel.")
      .replace(/^Класс (.+): publishedAt должен быть месяцем 2026 года в формате YYYY-MM\.$/, "Class $1: publishedAt must identify a month in 2026 in YYYY-MM format.")
      .replace(/^Повторяющийся id задачи: (.+)\.$/, "Duplicate task ID: $1.")
      .replace(/^Задача (.+) ссылается на неизвестный класс\.$/, "Task $1 references an unknown class.")
      .replace(/^Ручная трудоёмкость задачи (.+) должна быть положительной\.$/, "Task $1 must have a positive manual-baseline effort.")
      .replace(/^Задача (.+): неизвестный предшественник (.+)\.$/, "Task $1: unknown predecessor $2.")
      .replace(/^Задача (.+) не может зависеть от себя\.$/, "Task $1 cannot depend on itself.");
  });
}

export function interpolate(template: string, values: Record<string, string>) {
  return Object.entries(values).reduce((result, [key, value]) => result.replaceAll(`{${key}}`, value), template);
}
