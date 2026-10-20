# NEO Mathematics GreenPrint — Running Design Record entry v2.3 (DRAFT)

**Proposed version:** 2.3 · **Date:** 2026-10-20 · **Controlling record:** builds on Active v1.6, extends entry v2.2
**Status:** Draft entry for filing · Curriculum by Gerry Docherty

*"Connection before curriculum. Always."*

## Decision — Every coordinate graph is numbered and labelled, as we ask learners to do

Every coordinate grid in NEO Mathematics follows the conventions we expect learners to use. This covers interactive lessons, Practice Companions, Learner Guides, Supporting Adult Guidance, Final Task exemplars and diagnostic and assessment materials:

1. **Both axes carry a numbered scale.** Number them at equal intervals: every unit, or every second unit when an axis is long. Use the same spacing along the whole axis. Negative numbers use the true minus sign (−).
2. **Both axes are labelled.** Put an italic *x* and *y* at the positive ends of the axes. In a context graph, use the quantity and its unit instead (for example "Time (s)").
3. **Mark the origin** with O.
4. **Show the positive direction** of each axis, for example with arrowheads.
5. **Keep lines, curves, regions and labels inside the grid.** Nothing runs into the margin, and no label is hidden by a point, a line or shading.
6. **Write variables in italics wherever they appear.** That means *x* and *y* in the text as well as on the diagram, so the words and the picture match.

Number lines follow the same principle: a numbered scale at equal intervals, with true minus signs.

## Why this entry exists

The Inequalities Lesson 4 guidance drew regions on grids with unnumbered axes and no axis labels. *x* was in italics in the text but *y* was not. We would not accept either from a learner. Guidance that leaves them out quietly teaches that they are optional. **Practise what we preach.**

The same gap turned up in six already-published Intermediate guides, which use the same shared diagram code: Equations Lessons 5, 6, 7, 8, 9 and 11.

## What has been done (20 October 2026)

1. **Shared guide template.** A single `_coord_axes` routine now draws every coordinate grid in the guidance PDFs to the standard above. The line, two-line and region diagrams all use it, and their lines are clipped to the grid. The guide text now puts *y* in italics as well as *x*.
2. **Guides regenerated** for Foundations Inequalities Lesson 4 and Intermediate Equations Lessons 5, 6, 7, 8, 9 and 11 (learner and adult guides: 14 PDFs).
3. **Interactive lesson.** Every grid in Inequalities Lesson 4 is numbered on both axes, labels *x* and *y*, and marks O at the origin.

## Consequences

1. **QA gate (visual containment).** Before a lesson ships, check every coordinate grid and number line across all five resources against points 1–6 above. A missing scale, a missing axis label or a hidden label blocks shipping, in the same way as a broken worked-solution unlock.
2. **Audit the remaining graphs.** The parabola diagrams in the Quadratics guides already number and label their axes, but they do not yet mark O. Check the interactive graphs in published lessons (Intermediate Equations Lessons 5–11, Quadratics, and any other lesson with a coordinate grid) against the standard, and fix them at their next version.
3. **Learner-facing models.** Wherever a worked example, Final Task exemplar or rubric shows a graph, it shows a correctly numbered and labelled one, so learners always see the standard modelled.

## Unchanged

The colour palette, visual containment, the reasoning-first rule (v1.5) and precise mathematical vocabulary (v2.0).
