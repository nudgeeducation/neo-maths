# NEO Mathematics GreenPrint — Running Design Record entry v2.6 (DRAFT)

**Proposed version:** 2.6 · **Date:** 2026-11-14 · **Controlling record:** builds on Active v1.6, extends entries v2.0–v2.5
**Status:** Draft entry for filing · Curriculum by Gerry Docherty

*"Connection before curriculum. Always."*

## Decision — Division in a formula is written as a stacked fraction

Wherever a division sits inside a formula or a line of working, write it as a **stacked fraction**: the numerator over the denominator, with a horizontal fraction bar. Do not use ÷ read from left to right. For example, write

  percentage change = (change over original) × 100, with *change* above the bar and *original* below it,

not "percentage change = change ÷ original × 100".

This applies to every learner- and adult-facing surface:

1. **Interactive lessons:** idea cards, widget readouts, questions, feedback, proof stretches and "Carry this forward" lines.
2. **Practice Companions:** questions, prompts, hints and worked solutions.
3. **Learner Guides and Supporting Adult Guidance:** working steps in worked examples use the template's stacked fraction. In running prose, say it in words ("divide the change by the original").
4. **Diagnostic expeditions, Final Task exemplars and assessment materials.**

**Where ÷ stays:**
- a single quick calculation in a hint ("24 ÷ 2");
- the symbols palette and keyboard input, since learners may type ÷;
- plain-text prompts that cannot display a fraction, such as the Scratchpad's sticky prompt and feedback set as plain text.

Answer checking is unchanged: learners may type a / b, a ÷ b or a decimal, and every equivalent form is accepted (entry v2.1, QA gate 6a).

## Why this entry exists

Gerry Docherty, reviewing Percentages, Ratio, Growth and Bounds Lesson 4 (14 November 2026): learners are more familiar with a fraction written with a horizontal bar than with ÷ read from left to right. A stacked fraction shows at a glance what is divided by what. In “change ÷ original × 100”, the order of operations has to be read carefully; written as a fraction it cannot be misread. It also matches how learners will see these formulae in examinations and textbooks, and links division to fractions, which the course builds on throughout.

## What has been done (14 November 2026)

1. **Lesson.** Percentages, Ratio, Growth and Bounds Lesson 4 (Percentage change) now shows every division as a stacked fraction: the idea card, the Before-and-After Board's readout (for example −20 over 60 × 100 = −33 1/3%), the multiplier (new over original), questions, the proof stretch's choices, Movement feedback and the Practice Companion. A reusable fraction style (`.fr`) and helper (`FR(n, d)`) are in the lesson's code for later lessons.
2. **Guides.** The Lesson 4 guides use the template's stacked fractions in their working steps; their prose says the division in words.

## Consequences

1. **QA gate.** Before a lesson ships, check that no formula or line of working shows ÷ where a fraction belongs.
2. **Earlier lessons.** Lessons 1–3 of the same unit, and earlier units, still use ÷ in some readouts and solutions. Update them at their next version, or sooner if the curriculum lead asks.
3. **The skill.** Add this rule to the NEO Mathematics skill (wording below), together with the entries it does not yet include (v2.2–v2.5).

## Suggested wording for the NEO Mathematics skill

> **Division as a stacked fraction (GreenPrint v2.6).** In formulae and working — idea cards, readouts, feedback, proof steps, worked solutions and guide working — write division as a stacked fraction (numerator over denominator, horizontal bar), not ÷ read left to right: percentage change = change over original × 100. In HTML use an inline-flex column span with a rule under the numerator; in guidance PDFs use the template's stacked fraction for working and words in prose. Keep ÷ only for a single quick calculation in a hint, in the symbols palette, and in plain-text prompts. Answer checking still accepts a/b, a ÷ b and decimals (QA gate 6a).

## Unchanged

Precise mathematical vocabulary, including numerator and denominator rather than top and bottom (v2.0); equivalent answer forms (v2.1); numbered, labelled axes (v2.3); the reasoning-first rule (v1.5).
