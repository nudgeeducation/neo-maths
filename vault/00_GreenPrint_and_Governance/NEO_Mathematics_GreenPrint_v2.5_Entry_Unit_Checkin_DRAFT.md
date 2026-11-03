# NEO Mathematics GreenPrint — Running Design Record entry v2.5 (DRAFT)

**Proposed version:** 2.5 · **Date:** 2026-11-03 · **Controlling record:** builds on Active v1.6, extends entry v2.4
**Status:** Draft for discussion with the Director. Not yet agreed. · Curriculum by Gerry Docherty

*"Connection before curriculum. Always."*

## Proposed decision: every unit closes with a Unit Check-in

Each unit opens with its diagnostic expedition (entry v2.4) and closes with a **Unit Check-in**, the NEO end-of-unit assessment. The check-in shows **where the learner started and where they are now**, without scores, and gives every stakeholder the same picture.

A Unit Check-in has five parts:

1. **The Return Expedition.** The learner returns to the unit's expedition world: same floors or rooms, same field kit, same comfort modes. Each lock now asks about that lesson's own idea, where the diagnostic asked about what the lesson builds on. It is untimed, can be paused, and is taken within a window the learner chooses. A learner may come back and try a floor again after a Reconnection Route.
2. **The learner's reflection.** Before each lock: "How does this idea feel to you now?" (I've got this · Getting there · Not yet sure). At the end there is an optional "looking back" comment, saved only if the learner chooses to share it.
3. **Outcomes in the learner's words.** Secure; Secure: a hidden strength; Getting there; Worth a second look; Not yet. Each is shown beside that floor's start-of-unit outcome from the diagnostic.
4. **The adult's confirmation.** The supporting adult chooses one of the four labels for the unit: Approaching Proficiency, Developing Proficiency, Proficiency or Refining Proficiency. The choice is informed by the check-in and the Final Tasks, and may be supported by a short **maths conversation** using the unit's conversation cards. The adult may add a one-line note. The learner sees both.
5. **The Unit Summary.** One page, the same for the learner, the adult and the family, with a one-page family version in plain language. Commissioners receive a **termly** one-page summary per learner, drawn from the unit summaries, with International GCSE coverage.

**The Exam Corner (Intermediate).** After the check-in, an optional room of two or three exam-style questions with model answers, labelled as practice for later. It is untimed and **never recorded**.

## Why this entry exists

The November milestone asks for end-of-unit assessments. Learners, supporting adults, families and commissioners need different things. The Unit Check-in meets all four without introducing scores, timers or comparison. It reuses each unit's diagnostic, so it is quick to build. It gives commissioners a consistent baseline and endpoint for every learner.

## What has been done (3 November 2026)

1. **Prototype:** Return to the Lighthouse (Intermediate, Algebraic Expressions and Identities): eight floors, start-to-now floor plan, adult view and confirmation, Exam Corner. In `vault/99_Working/Assessment_Prototypes`, made by `make_return.py` from the Lighthouse; QA harness `qa_lighthouse_return.js` (99 checks).
2. **Exemplars** using a fictional learner, in `Assessment_Prototypes/Unit_Checkin_Pack`: the Unit Summary, the family summary, the maths conversation cards and the termly commissioner summary.

## Consequences, if agreed

1. **Blueprints** list the Unit Check-in as the session after the last lesson, alongside the diagnostic before Lesson 1.
2. **The build order for a unit** becomes: blueprint, diagnostic, lessons, then check-in.
3. **The results service** gains a check-in page per unit, and the passport and dashboard show start and end side by side.
4. **Classroom** gains a "Finish here" post at the end of each unit topic.
5. **Existing units** with a diagnostic (Inequalities, Formulae and Rearranging, Number Systems, Algebraic Expressions) get their check-ins first.

## Unchanged

The four principles: no scores, timers, lives or leaderboards; learners see what adults see; record the minimum; data stays in NEO's Workspace.
