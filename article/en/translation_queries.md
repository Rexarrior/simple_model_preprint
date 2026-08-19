# Translation query ledger

Issues found while translating the Russian source are recorded here. The
resolution column documents the explicit editorial decision used in the
integrated English manuscript.

| ID | Source | Issue | Translation treatment |
|---|---|---|---|
| Q01 | `main.tex:79--82` | The language note becomes obsolete in a fully English manuscript. | Resolved: omitted from `main_en.tex`. |
| Q02 | TeX preambles | `T2A` and `babel[russian]` are incompatible with an English-only build. | Resolved: `main_en.tex` uses T1 encoding and English babel. |
| Q03 | `Термины и обозначения.tex:3--5` | Appendix text says definitions follow in the next section. | Resolved: the appendix now points to the labeled Formal Model section. |
| Q04 | `Примеры базовой модели.tex:288` | Hard-coded `Определении~1` instead of a label reference. | Resolved: replaced with `Definition~\\ref{def:params}`. |
| Q05 | `Базовая модель.tex` proofs | Manual `Ч.Т.Д.` duplicates the QED marker supplied by `amsthm`. | Resolved: the duplicate manual marker is omitted in English. |
| Q06 | `Примеры базовой модели.tex:491--499` | Mode is said to belong to tasks, then described as tied to streams. | Resolved: mode assignment to tasks is distinguished from stream assignment. |
| Q07 | full glossary vs Introduction | Fully autonomous mode includes task discovery and automatic acceptance, while the Introduction says they are not modeled. | Resolved: the mode is defined only as the zero-mandatory-human-work limiting case for a prespecified task; discovery and automatic acceptance remain outside scope. |
| Q08 | `Введение.tex:29` | `измеренным эффектом ИИ` may imply a causal estimate. | Resolved: translated as a descriptive task-level AI-assisted duration, with an explicit noncausal caveat. |
| Q09 | `simple_litreview.tex:17` | `измеренное участие человека` may overstate current calibration. | Resolved: translated as operationally defined human involvement. |
