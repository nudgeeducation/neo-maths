# NEO Mathematics GreenPrint — Running Design Record entry v2.4 (DRAFT)

**Proposed version:** 2.4 · **Date:** 2026-10-20 · **Controlling record:** builds on Active v1.6, extends entry v2.3
**Status:** Draft entry for filing · Curriculum by Gerry Docherty

*"Connection before curriculum. Always."*

## Decision: every new unit opens with a diagnostic expedition

From Spring 2027 onwards, each unit is planned with a **diagnostic expedition**, built before its first lesson. The expedition is a gamified check of what the unit builds on, with no surveillance. It is part of the unit's blueprint, listed as the session before Lesson 1, and it is built and reviewed before the lessons.

Every expedition follows the format the Director approved for the Observatory and the Walled Garden:

1. **One room per lesson.** Each room has one lock, which checks the prerequisite that lesson builds on, so the outcome for a room says how ready the learner is for that lesson.
2. **No scores, timers, lives or leaderboards, ever.** The right answer is the key. A wrong key gives a gentle hint, and "Show me how" is always available.
3. **A side passage in every room**, which leads on just the same. Taking it is a positive choice: "I'd like to learn this in the unit."
4. **The learner's own sense of each lock** ("I've got this", "Not sure", "This is new to me"), asked before trying a key.
5. **A field kit:** one reference tool per room, collected once the lock is resolved. Looking things up in it is encouraged and never recorded.
6. **A "Did you know?" note** in each room, just for interest.
7. **Still mode, Flat view, Comfort text and Read aloud**, honouring reduced-motion settings.
8. **Learners see what adults see.** The end-of-expedition plan and the adult table are the same information. Outcomes use the learner's words and never a score: Ready, Hidden strength, Got there with a nudge, Worth a second look, New ground.
9. **Record the minimum.** Save only how each lock looked, the outcome, what a common mistake might suggest, and the suggested Reconnection Route. A comment is saved only if the learner chooses to share it. No timings, attempt counts, clicks or field-kit use.
10. **Answers are checked by value** (QA gate 6a), including algebraic answers, which are evaluated at test values rather than matched as text.
11. **Every expedition is connected to the NEO results service** (`?page=<name>`), so its outcomes reach the learner passport and the educator dashboard.

Each expedition has its own theme, chosen to fit the unit's mathematics.

## Why this entry exists

The Director welcomed the Observatory and Walled Garden prototypes. One expedition per unit gives every learner a calm start to each unit and gives the team the same kind of evidence across the curriculum. Building the expedition first also tells us which Reconnection Routes the unit's lessons need.

## What has been done (20 October 2026)

1. **The Inventor's Workshop** (Year 9, Formulae and Rearranging) has six rooms, one per lesson:
   - The Drawing Office: order of operations.
   - The Cold Store: multiplying negatives.
   - The Order Book: writing an expression.
   - The Pattern Loom: the *n*th term of a linear sequence.
   - The Machine Hall: reversing a function machine.
   - The Measuring Room: converting units.

   The prototype is in `vault/99_Working/Assessment_Prototypes`.
2. **Results service:** the Walled Garden and the Inventor's Workshop now have results-service pages (`?page=garden`, `?page=workshop`), made by a reusable converter that reproduces the live Observatory exactly. The passport and dashboard top bars list every expedition automatically. They go live when the new files are added to the script project and a new version is deployed.

## Consequences

1. **Blueprints** list the diagnostic as the session before Lesson 1, with its theme and its rooms.
2. **The build order for a unit** is: blueprint, then diagnostic, then lessons one at a time.
3. **Units already built** (Year 9 Autumn units, Year 10 units) can be given expeditions later, as capacity allows. The Observatory already covers Year 10 Number Systems.
4. **End-of-unit assessments** are a separate decision, still to be agreed.

## Unchanged

The four principles: no scores, timers, lives or leaderboards; learners see what adults see; record the minimum; data stays in NEO's Workspace.
