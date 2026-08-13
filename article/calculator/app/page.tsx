"use client";

import { useEffect, useState } from "react";
import { calculateM4, validateConfig, type M4Result, type ProjectConfig } from "./lib/m4";
import {
  CONFIG_PROMPTS,
  DEMO_CONFIGS,
  UI,
  interpolate,
  localizeDiagnostic,
  localizeValidationErrors,
  type Locale,
  type ThemePreference,
} from "./lib/ui";

declare global {
  interface Window {
    siteTheme?: {
      getPreference(): ThemePreference;
      getResolvedTheme(): "light" | "dark";
      setPreference(preference: ThemePreference): ThemePreference;
      cyclePreference(): ThemePreference;
      preferences: ThemePreference[];
    };
  }
}

function cloneConfig(config: ProjectConfig): ProjectConfig {
  return JSON.parse(JSON.stringify(config)) as ProjectConfig;
}

function sameConfig(left: ProjectConfig, right: ProjectConfig) {
  return JSON.stringify(left) === JSON.stringify(right);
}

export default function Home() {
  const initialConfig = DEMO_CONFIGS.en;
  const [locale, setLocale] = useState<Locale>("en");
  const [themePreference, setThemePreference] = useState<ThemePreference>("auto");
  const [config, setConfig] = useState<ProjectConfig>(() => cloneConfig(initialConfig));
  const [jsonInput, setJsonInput] = useState(() => JSON.stringify(initialConfig, null, 2));
  const [result, setResult] = useState<M4Result>(() => calculateM4(initialConfig));
  const [errors, setErrors] = useState<string[]>([]);
  const [consent, setConsent] = useState(false);
  const [saveStatus, setSaveStatus] = useState("");
  const [promptCopied, setPromptCopied] = useState(false);
  const [activeEditor, setActiveEditor] = useState<"classes" | "tasks">("tasks");

  const text = UI[locale];
  const unit = text.units[config.timeUnit];
  const numberFormat = new Intl.NumberFormat(locale === "ru" ? "ru-RU" : "en-US", { maximumFractionDigits: 2 });
  const format = (value: number) => Number.isFinite(value) ? numberFormat.format(value) : "—";
  const themeLabel = text.theme[themePreference];
  const themeIcon = { auto: "◐", light: "☀", dark: "☾" }[themePreference];

  useEffect(() => {
    let savedLocale: Locale = "en";
    try {
      const saved = window.localStorage.getItem("lang");
      if (saved === "ru" || saved === "en") savedLocale = saved;
    } catch {
      // Language still falls back to English when browser storage is blocked.
    }
    document.documentElement.lang = savedLocale;
    const initialTheme = window.siteTheme?.getPreference() ?? "auto";
    queueMicrotask(() => {
      if (savedLocale !== "en") {
        const next = cloneConfig(DEMO_CONFIGS[savedLocale]);
        setLocale(savedLocale);
        setConfig(next);
        setJsonInput(JSON.stringify(next, null, 2));
        setResult(calculateM4(next));
      }
      setThemePreference(initialTheme);
    });
    const onThemeChange = (event: Event) => {
      setThemePreference((event as CustomEvent<{ preference: ThemePreference }>).detail.preference);
    };
    window.addEventListener("site-theme-change", onThemeChange);
    return () => window.removeEventListener("site-theme-change", onThemeChange);
  }, []);

  useEffect(() => {
    const titles = {
      en: {
        title: "M4 Workbench — human–agent planning calculator",
        description: "Estimate development speedup, the critical path, and human-attention load locally with the M4 model.",
      },
      ru: {
        title: "M4 Workbench — калькулятор человеко-агентной работы",
        description: "Локально оцените потенциальное ускорение разработки, критический путь и нагрузку на человеческое внимание по модели M4.",
      },
    }[locale];
    document.documentElement.lang = locale;
    document.title = titles.title;
    document.querySelector('meta[name="description"]')?.setAttribute("content", titles.description);
  }, [locale]);

  const dagLayers = (() => {
    const layers = new Map<number, typeof config.tasks>();
    for (const task of config.tasks) {
      const depth = result.dagDepths[task.id] ?? 0;
      layers.set(depth, [...(layers.get(depth) ?? []), task]);
    }
    return [...layers.entries()].sort(([a], [b]) => a - b);
  })();

  const loadExample = (targetLocale = locale) => {
    const next = cloneConfig(DEMO_CONFIGS[targetLocale]);
    setConfig(next);
    setJsonInput(JSON.stringify(next, null, 2));
    setResult(calculateM4(next));
    setErrors([]);
    setSaveStatus("");
  };

  const changeLocale = (nextLocale: Locale) => {
    if (nextLocale === locale) return;
    const currentIsDemo = sameConfig(config, DEMO_CONFIGS[locale]);
    setLocale(nextLocale);
    try {
      window.localStorage.setItem("lang", nextLocale);
    } catch {
      // The language switch remains active for the current session.
    }
    setErrors([]);
    setSaveStatus("");
    if (currentIsDemo) loadExample(nextLocale);
  };

  const copyPrompt = async () => {
    await navigator.clipboard.writeText(CONFIG_PROMPTS[locale]);
    setPromptCopied(true);
    window.setTimeout(() => setPromptCopied(false), 1800);
  };

  const importJson = () => {
    try {
      const parsed = JSON.parse(jsonInput) as ProjectConfig;
      const validation = localizeValidationErrors(validateConfig(parsed), locale);
      if (validation.length) {
        setErrors(validation);
        return;
      }
      setConfig(parsed);
      setResult(calculateM4(parsed));
      setErrors([]);
      setSaveStatus(text.status.imported);
    } catch {
      setErrors([text.status.invalidJson]);
    }
  };

  const exportJson = () => {
    const blob = new Blob([JSON.stringify(config, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `${config.projectName.toLowerCase().replace(/[^a-zа-я0-9]+/gi, "-") || "m4-project"}.json`;
    anchor.click();
    URL.revokeObjectURL(url);
  };

  const runCalculation = async () => {
    const validation = localizeValidationErrors(validateConfig(config), locale);
    if (validation.length) {
      setErrors(validation);
      return;
    }
    const next = calculateM4(config);
    setResult(next);
    setJsonInput(JSON.stringify(config, null, 2));
    setErrors([]);
    if (!consent) {
      setSaveStatus(text.status.localDone);
      return;
    }
    setSaveStatus(text.status.saving);
    try {
      const response = await fetch("/api/share", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ consent: true, consentVersion: "v1", config, result: next }),
      });
      if (!response.ok) throw new Error("save_failed");
      const payload = (await response.json()) as { id: string };
      setSaveStatus(interpolate(text.status.saved, { id: payload.id.slice(0, 8) }));
    } catch {
      setSaveStatus(text.status.failed);
    }
  };

  const updateClass = (index: number, field: string, value: string | number) => {
    const next = cloneConfig(config);
    next.taskClasses[index] = { ...next.taskClasses[index], [field]: value };
    setConfig(next);
  };

  const updateTask = (index: number, field: string, value: string | number | string[]) => {
    const next = cloneConfig(config);
    next.tasks[index] = { ...next.tasks[index], [field]: value };
    setConfig(next);
  };

  const addClass = () => {
    const next = cloneConfig(config);
    const id = `class-${next.taskClasses.length + 1}`;
    next.taskClasses.push({ id, name: text.status.newClass, aiCycleMultiplier: 0.75, humanFraction: 0.25 });
    setConfig(next);
  };

  const addTask = () => {
    const next = cloneConfig(config);
    const id = `task-${next.tasks.length + 1}`;
    next.tasks.push({ id, classId: next.taskClasses[0]?.id ?? "", name: text.status.newTask, description: "", baselineEffort: 8, predecessors: [] });
    setConfig(next);
  };

  const maxSweep = Math.max(...result.pSweep.map((item) => item.makespan));
  const constraintLabel = text.constraints[result.activeConstraint];
  const evidenceLabels = text.evidence;

  return (
    <main>
      <header className="topbar">
        <a className="brand" href="#top" aria-label={text.brandAria}>
          <span className="brand-mark">M4</span>
          <span>Human–Agent Workbench</span>
        </a>
        <div className="topbar-right">
          <nav aria-label={text.nav.aria}>
            <a href="#import">{text.nav.import}</a>
            <a href="#model">{text.nav.model}</a>
            <a href="#results">{text.nav.results}</a>
          </nav>
          <div className="site-controls">
            <button className="theme-button" type="button" aria-label={`${text.theme.label}: ${themeLabel}`} title={`${text.theme.label}: ${themeLabel}`} onClick={() => window.siteTheme?.cyclePreference()}>
              <span aria-hidden="true">{themeIcon}</span><b>{themeLabel}</b>
            </button>
            <div className="language-switch" role="group" aria-label="Language">
              {(["en", "ru"] as Locale[]).map((item) => <button type="button" className={locale === item ? "active" : ""} aria-pressed={locale === item} onClick={() => changeLocale(item)} key={item}>{item}</button>)}
            </div>
          </div>
        </div>
      </header>

      <section className="hero" id="top">
        <div className="eyebrow"><span className="live-dot" /> {text.hero.eyebrow}</div>
        <h1>{text.hero.title}<br /><em>{text.hero.emphasis}</em></h1>
        <p className="hero-copy">{text.hero.copy}</p>
        <div className="hero-actions">
          <a className="button primary" href="#import">{text.hero.start} <span>↓</span></a>
          <button className="button ghost" onClick={() => loadExample()}>{text.hero.demo}</button>
        </div>
        <div className="hero-stats" aria-label={text.hero.aria}>
          <div><span>{text.hero.speedup}</span><strong>{format(result.demonstratedSpeedup)}×</strong></div>
          <div><span>{text.hero.ceiling}</span><strong>{format(result.speedupCeiling)}×</strong></div>
          <div><span>{text.hero.constraint}</span><strong className="textual">{constraintLabel}</strong></div>
        </div>
      </section>

      <section className="privacy-strip">
        <span className="privacy-icon">◎</span>
        <div><strong>Private by default.</strong> {text.privacy}</div>
      </section>

      <section className="section import-section" id="import">
        <div className="section-heading"><span className="section-index">01</span><div><h2>{text.import.title}</h2><p>{text.import.copy}</p></div></div>
        <div className="import-grid">
          <article className="prompt-card">
            <div className="card-head"><div><span className="micro-label">PROMPT · v1</span><h3>{text.import.promptTitle}</h3></div><button className="copy-button" onClick={copyPrompt}>{promptCopied ? text.import.copied : text.import.copyButton}</button></div>
            <pre>{CONFIG_PROMPTS[locale]}</pre>
            <div className="card-note">{text.import.note}</div>
          </article>
          <article className="json-card">
            <div className="card-head"><div><span className="micro-label">JSON IMPORT</span><h3>{text.import.jsonTitle}</h3></div><button className="text-button" onClick={() => setJsonInput(JSON.stringify(config, null, 2))}>{text.import.current}</button></div>
            <textarea aria-label={text.import.textareaAria} value={jsonInput} onChange={(event) => setJsonInput(event.target.value)} spellCheck={false} />
            {errors.length > 0 && <div className="error-box"><strong>{text.import.check}</strong><ul>{errors.map((error) => <li key={error}>{error}</li>)}</ul></div>}
            <div className="json-actions"><button className="button primary compact" onClick={importJson}>{text.import.importButton}</button><button className="button ghost compact" onClick={exportJson}>{text.import.download}</button></div>
          </article>
        </div>
      </section>

      <section className="section model-section" id="model">
        <div className="section-heading"><span className="section-index">02</span><div><h2>{text.model.title}</h2><p>{text.model.copy}</p></div></div>
        <div className="global-controls">
          <label><span>{text.model.project}</span><input value={config.projectName} onChange={(event) => setConfig({ ...config, projectName: event.target.value })} /><small>{text.model.projectHelp}</small></label>
          <label><span>{text.model.streams}</span><input type="number" min="1" max="12" value={config.p} onChange={(event) => setConfig({ ...config, p: Number(event.target.value) })} /><small>{text.model.streamsHelp}</small></label>
          <label><span>{text.model.agentOverhead}</span><input type="number" min="1" step="0.01" value={config.c} onChange={(event) => setConfig({ ...config, c: Number(event.target.value) })} /><small>{text.model.agentOverheadHelp}</small></label>
          <label><span>{text.model.humanOverhead}</span><input type="number" min="1" step="0.01" value={config.gamma} onChange={(event) => setConfig({ ...config, gamma: Number(event.target.value) })} /><small>{text.model.humanOverheadHelp}</small></label>
        </div>

        <aside className="parameter-guide" aria-label={text.model.guideAria}>
          <div><span className="guide-symbol">k</span><p><strong>{text.model.fullCycle}</strong>{text.model.fullCycleHelp}</p></div>
          <div><span className="guide-symbol">q</span><p><strong>{text.model.humanShare}</strong>{text.model.humanShareHelp}</p></div>
          <div><span className="guide-symbol">Tₕ</span><p><strong>{text.model.baseline}</strong>{text.model.baselineHelp}</p></div>
          <div><span className="guide-symbol">P</span><p><strong>{text.model.parallel}</strong>{text.model.parallelHelp}</p></div>
        </aside>

        <p className="research-disclaimer"><strong>{text.model.researchStrong}</strong> {text.model.research}</p>

        <details className="research-sources">
          <summary><span><strong>{text.model.sources}</strong><small>{text.model.sourcesMeta}</small></span><i aria-hidden="true">＋</i></summary>
          <div className="sources-body">
            <article><span className="source-index">01 · 2026-06</span><div><h3>Generative AI and labour productivity: A quasi experiment on coding</h3><p>{text.model.source1}</p><code>k₀ = 1 / (1 + {locale === "ru" ? "0,22" : "0.22"}) ≈ {locale === "ru" ? "0,82" : "0.82"}</code><a href="https://doi.org/10.1016/j.jfs.2026.101543" target="_blank" rel="noreferrer">Gambacorta, Qiu, Shan & Rees · Journal of Financial Stability ↗</a></div></article>
            <article><span className="source-index">02 · 2026-07</span><div><h3>When Code Authors Are Agents</h3><p>{text.model.source2a}</p><code>docs: 0.82 × 0.779 / 0.838 ≈ 0.76<br />feature: 0.82 × 0.774 / 0.687 ≈ 0.93<br />infra: 0.82 × 0.770 / 0.729 ≈ 0.87</code><p>{text.model.source2b}</p><a href="https://doi.org/10.1145/3805760.3814909" target="_blank" rel="noreferrer">Njoku, Sharafi & Khomh · AIware ’26 ↗</a></div></article>
            <article><span className="source-index">03 · 2026-07</span><div><h3>Does Working with AI Agents Change How Developers Code, Test, and Review?</h3><p>{text.model.source3}</p><code>review & verification: k = 1.00</code><a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6996078" target="_blank" rel="noreferrer">Hamza, Siemon & Awan · SSRN ↗</a></div></article>
            <p className="sources-caveat"><strong>{text.model.caveatStrong}</strong> {text.model.caveat}</p>
          </div>
        </details>

        <div className="editor-tabs" role="tablist">
          <button className={activeEditor === "tasks" ? "active" : ""} onClick={() => setActiveEditor("tasks")}>{text.model.tasks} <span>{config.tasks.length}</span></button>
          <button className={activeEditor === "classes" ? "active" : ""} onClick={() => setActiveEditor("classes")}>{text.model.classes} <span>{config.taskClasses.length}</span></button>
        </div>

        {activeEditor === "classes" ? (
          <div className="class-list">
            {config.taskClasses.map((item, index) => (
              <article className="class-row" key={`${item.id}-${index}`}>
                <label className="wide"><span>{text.model.name}</span><input value={item.name} onChange={(event) => updateClass(index, "name", event.target.value)} /></label>
                <label><span>ID</span><input value={item.id} onChange={(event) => updateClass(index, "id", event.target.value)} /></label>
                <label><span>{text.model.aiCycle}</span><input type="number" min="0.01" step="0.01" value={item.aiCycleMultiplier} onChange={(event) => updateClass(index, "aiCycleMultiplier", Number(event.target.value))} /></label>
                <label><span>{text.model.humanFraction}</span><input type="number" min="0" max="1" step="0.01" value={item.humanFraction} onChange={(event) => updateClass(index, "humanFraction", Number(event.target.value))} /></label>
                <button className="remove-button" aria-label={interpolate(text.model.removeClass, { name: item.name })} onClick={() => setConfig({ ...config, taskClasses: config.taskClasses.filter((_, itemIndex) => itemIndex !== index) })}>×</button>
                <div className="class-breakdown">
                  <p><strong>{interpolate(text.model.perBaseline, { unit })}</strong> {interpolate(text.model.fullCycleShort, { value: format(item.aiCycleMultiplier), unit, human: format(item.aiCycleMultiplier * item.humanFraction), agent: format(item.aiCycleMultiplier * (1 - item.humanFraction)) })}</p>
                  {item.evidence && <div className="evidence-note"><span className={`evidence-kind ${item.evidence.kind}`}>{evidenceLabels[item.evidence.kind]}{item.evidence.publishedAt ? ` · ${item.evidence.publishedAt}` : ""}</span><p>{item.evidence.note} {item.evidence.url ? <a href={item.evidence.url} target="_blank" rel="noreferrer">{item.evidence.label} ↗</a> : <strong>{item.evidence.label}</strong>}{item.evidence.secondaryUrl && item.evidence.secondaryLabel ? <> · <a href={item.evidence.secondaryUrl} target="_blank" rel="noreferrer">{item.evidence.secondaryLabel} ↗</a></> : null}</p></div>}
                  {item.humanFractionBasis && <p className="assumption-note"><strong>{interpolate(text.model.whyQ, { value: format(item.humanFraction) })}</strong> {item.humanFractionBasis}</p>}
                </div>
              </article>
            ))}
            <button className="add-button" onClick={addClass}>{text.model.addClass}</button>
          </div>
        ) : (
          <div className="task-list">
            {config.tasks.map((task, index) => (
              <article className="task-row" key={`${task.id}-${index}`}>
                <div className="task-number">{String(index + 1).padStart(2, "0")}</div>
                <div className="task-fields">
                  <label className="task-name"><span>{text.model.name}</span><input value={task.name ?? ""} placeholder={text.model.optional} onChange={(event) => updateTask(index, "name", event.target.value)} /></label>
                  <label><span>ID</span><input value={task.id} onChange={(event) => updateTask(index, "id", event.target.value)} /></label>
                  <label><span>{text.model.taskClass}</span><select value={task.classId} onChange={(event) => updateTask(index, "classId", event.target.value)}>{config.taskClasses.map((item) => <option value={item.id} key={item.id}>{item.name}</option>)}</select></label>
                  <label><span>{interpolate(text.model.baselineLabel, { unit })}</span><input type="number" min="0.1" step="0.5" value={task.baselineEffort} onChange={(event) => updateTask(index, "baselineEffort", Number(event.target.value))} /><small className="task-field-help">{text.model.sameResult}</small></label>
                  <label className="predecessors"><span>{text.model.predecessors}</span><input value={task.predecessors.join(", ")} placeholder="contract, storage" onChange={(event) => updateTask(index, "predecessors", event.target.value.split(",").map((item) => item.trim()).filter(Boolean))} /></label>
                  <label className="description"><span>{text.model.description}</span><input value={task.description ?? ""} placeholder={text.model.descriptionPlaceholder} onChange={(event) => updateTask(index, "description", event.target.value)} /></label>
                </div>
                <button className="remove-button" aria-label={interpolate(text.model.removeTask, { name: task.name ?? task.id })} onClick={() => setConfig({ ...config, tasks: config.tasks.filter((_, itemIndex) => itemIndex !== index) })}>×</button>
              </article>
            ))}
            <button className="add-button" onClick={addTask}>{text.model.addTask}</button>
          </div>
        )}

        <div className="consent-panel">
          <div className="consent-label">
            <input id="share-consent" type="checkbox" checked={consent} onChange={(event) => { setConsent(event.target.checked); setSaveStatus(""); }} />
            <label htmlFor="share-consent" aria-label={text.model.consentAria}><span className="custom-check" aria-hidden="true" /><span><strong>{text.model.consentTitle}</strong><small>{text.model.consentHelp}</small></span></label>
          </div>
          <div className={`data-route ${consent ? "shared" : "local"}`}><span />{consent ? text.model.routeShared : text.model.routeLocal}</div>
        </div>
        <button className="calculate-button" onClick={runCalculation}><span>{text.model.calculate}</span><span className="calculate-arrow">↗</span></button>
        {saveStatus && <p className="save-status" role="status">{saveStatus}</p>}
      </section>

      <section className="results-section" id="results">
        <div className="results-intro"><span className="section-index light">03</span><div><h2>{text.results.title}</h2><p>{text.results.copy}</p></div></div>
        <div className="metrics-grid">
          <article><span>{text.results.manual}</span><strong>{format(result.tHuman)} <small>{unit}</small></strong><p>{text.results.manualHelp}</p></article>
          <article className="accent"><span>{text.results.schedule}</span><strong>{format(result.schedule.makespan)} <small>{unit}</small></strong><p>{text.results.scheduleHelp}</p></article>
          <article><span>{text.results.bound}</span><strong>{format(result.b4)} <small>{unit}</small></strong><p>{text.results.boundHelp}</p></article>
          <article><span>{text.results.speedup}</span><strong>{format(result.demonstratedSpeedup)}× <small>→ {format(result.speedupCeiling)}×</small></strong><p>{text.results.speedupHelp}</p></article>
        </div>

        <div className="analysis-grid">
          <article className="constraint-card">
            <div className="card-head dark"><div><span className="micro-label">ACTIVE CONSTRAINT</span><h3>{constraintLabel}</h3></div><div className="constraint-orbit"><i /><i /><i /></div></div>
            <div className="branch-row"><span>W₄ / P <small>{text.results.load}</small></span><div><i style={{ width: `${(result.workBranch / result.b4) * 100}%` }} /></div><strong>{format(result.workBranch)}</strong></div>
            <div className="branch-row"><span>L₄ <small>{text.results.critical}</small></span><div><i style={{ width: `${(result.l4 / result.b4) * 100}%` }} /></div><strong>{format(result.l4)}</strong></div>
            <div className="branch-row"><span>γH <small>{text.results.human}</small></span><div><i style={{ width: `${(result.humanBranch / result.b4) * 100}%` }} /></div><strong>{format(result.humanBranch)}</strong></div>
            <p className="constraint-note">{text.results.gap} <strong>{format(result.gapToBound)} {unit}</strong>. {text.results.queue} <strong>{format(result.schedule.queueTime)} {unit}</strong>.</p>
          </article>
          <article className="sweep-card">
            <div className="card-head"><div><span className="micro-label">PARALLELISM SWEEP</span><h3>{text.results.sweep}</h3></div><span className="legend-dot">T(π)</span></div>
            <div className="sweep-chart">{result.pSweep.map((point) => <div className={point.p === config.p ? "active" : ""} key={point.p}><span className="bar-value">{format(point.makespan)}</span><i style={{ height: `${Math.max(12, (point.makespan / maxSweep) * 100)}%` }} /><small>P={point.p}</small></div>)}</div>
          </article>
        </div>

        <article className="dag-card">
          <div className="card-head"><div><span className="micro-label">TASK DAG</span><h3>{text.results.dag}</h3></div><span className="critical-legend">{text.results.criticalLegend}</span></div>
          <div className="dag-canvas">{dagLayers.map(([depth, tasks], layerIndex) => <div className="dag-layer" key={depth}><span className="layer-label">L{depth}</span>{tasks.map((task) => <div className={`dag-node ${result.criticalPath.includes(task.id) ? "critical" : ""}`} key={task.id}><strong>{task.name || task.id}</strong><small>{task.id} · {format(task.baselineEffort)} {unit}</small>{task.predecessors.length > 0 && <span>← {task.predecessors.join(", ")}</span>}</div>)}{layerIndex < dagLayers.length - 1 && <div className="layer-arrow">→</div>}</div>)}</div>
        </article>

        <article className="gantt-card">
          <div className="card-head"><div><span className="micro-label">RESOURCE-FEASIBLE SCHEDULE</span><h3>{text.results.gantt}</h3></div><span>{format(result.schedule.makespan)} {unit}</span></div>
          <div className="gantt">
            {[locale === "ru" ? "Человек" : "Human", ...Array.from({ length: config.p }, (_, index) => `${locale === "ru" ? "Агент" : "Agent"} ${index + 1}`)].map((lane, laneIndex) => <div className="gantt-row" key={lane}><strong>{lane}</strong><div className="gantt-track">{result.schedule.intervals.filter((interval) => laneIndex === 0 ? interval.resource === "human" : interval.agent === laneIndex).map((interval, index) => { const isHold = laneIndex > 0 && interval.resource === "human"; return <span className={`gantt-bar ${interval.resource} ${isHold ? "hold" : ""}`} title={`${interval.taskName}: ${text.phases[interval.phase]}, ${format(interval.start)}–${format(interval.end)}`} key={`${interval.taskId}-${interval.phase}-${index}`} style={{ left: `${(interval.start / result.schedule.makespan) * 100}%`, width: `${Math.max(0.8, ((interval.end - interval.start) / result.schedule.makespan) * 100)}%` }}>{!isHold && interval.taskId}</span>; })}</div></div>)}
          </div>
          <div className="gantt-legend"><span><i className="human" /> {text.results.humanPhase}</span><span><i className="agent" /> {text.results.agentPhase}</span><span><i className="hold" /> {text.results.held}</span></div>
        </article>

        <div className="diagnostics"><div><span className="micro-label">MODEL DIAGNOSTICS</span><h3>{text.results.next}</h3></div><ol>{result.diagnostics.map((item, index) => <li key={item}><span>{String(index + 1).padStart(2, "0")}</span>{localizeDiagnostic(item, locale)}</li>)}</ol></div>
      </section>

      <footer>
        <div><span className="brand-mark">M4</span><strong>Phase-Based Planning Model</strong></div>
        <p>{text.footer}</p>
        <a href="#top">{text.top}</a>
      </footer>
    </main>
  );
}
