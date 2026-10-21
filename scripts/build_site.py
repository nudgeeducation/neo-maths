#!/usr/bin/env python3
"""NEO Maths GreenPrint — site build script.

Copies the canonical interactive lessons from vault/ into docs/lessons/,
injects the progress-tracking snippet, and flips each lesson's status to
"live" in docs/data/curriculum.json.

Run from the repo root:  python3 scripts/build_site.py
Safe to re-run any time the vault changes.
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"
DOCS = ROOT / "docs"
CURRICULUM = DOCS / "data" / "curriculum.json"

# lesson id -> newest source file in the vault (update when versions move on)
SOURCES = {
    "aps-01-rounding-to-significant-figures":
        "02_Foundations/Accuracy, Powers and Scale/Lesson 01 - Rounding to Significant Figures/Lesson_01_Rounding_to_Significant_Figures_v0.3.html",
    "aps-02-estimation":
        "02_Foundations/Accuracy, Powers and Scale/Lesson 02 - Estimation/Lesson_02_Estimation_v0.1.html",
    "aps-03-using-index-laws":
        "02_Foundations/Accuracy, Powers and Scale/Lesson 03 - Using Index Laws/Lesson_03_Using_Index_Laws_v0.2.html",
    "aps-04-write-and-order-standard-form":
        "02_Foundations/Accuracy, Powers and Scale/Lesson 04 - Write and Order Standard Form/Lesson_04_Write_and_Order_Standard_Form_v0.3.html",
    "aps-05-calculating-with-standard-form":
        "02_Foundations/Accuracy, Powers and Scale/Lesson 05 - Calculating with Standard Form/Lesson_05_Calculating_with_Standard_Form_v0.4.html",
    "pyth-01-right-triangles-and-hidden-squares":
        "02_Foundations/01_Lessons/Pythagorean_Theorem/Lesson_01_Right_Triangles_and_Hidden_Squares/NEO_Maths_Y9_Pythagoras_Lesson_01_Hidden_Squares_v0.5.html",
    "pyth-02-finding-the-hypotenuse":
        "02_Foundations/01_Lessons/Pythagorean_Theorem/Lesson_02_Finding_the_Hypotenuse/NEO_Maths_Y9_Pythagoras_Lesson_02_Finding_the_Hypotenuse_v1.0.html",
    "pyth-03-finding-a-shorter-side":
        "02_Foundations/01_Lessons/Pythagorean_Theorem/Lesson_03_Finding_a_Shorter_Side/NEO_Maths_Y9_Pythagoras_Lesson_03_Finding_a_Shorter_Side_v0.3.html",
    "pyth-04-geometrical-problems":
        "02_Foundations/01_Lessons/Pythagorean_Theorem/Lesson_04_Geometrical_Problems/NEO_Maths_Y9_Pythagoras_Lesson_04_Geometrical_Problems_v0.5.html",
    "shapes-01-analysing-properties":
        "02_Foundations/01_Lessons/2D_and_3D_Shapes/Lesson_01_Analysing_2D_and_3D_Properties/NEO_Maths_Y9_Shapes_Lesson_01_Analysing_Properties_v0.1.html",
    "shapes-02-angles-in-polygons":
        "02_Foundations/01_Lessons/2D_and_3D_Shapes/Lesson_02_Angles_in_Polygons/NEO_Maths_Y9_Shapes_Lesson_02_Angles_in_Polygons_v0.1.html",
    "shapes-03-circumference-of-a-circle":
        "02_Foundations/01_Lessons/2D_and_3D_Shapes/Lesson_03_Circumference_of_a_Circle/NEO_Maths_Y9_Shapes_Lesson_03_Circumference_of_a_Circle_v0.1.html",
    "shapes-04-area-of-a-circle":
        "02_Foundations/01_Lessons/2D_and_3D_Shapes/Lesson_04_Area_of_a_Circle/NEO_Maths_Y9_Shapes_Lesson_04_Area_of_a_Circle_v0.1.html",
    "shapes-05-reasoning-from-nets":
        "02_Foundations/01_Lessons/2D_and_3D_Shapes/Lesson_05_Reasoning_from_Nets/NEO_Maths_Y9_Shapes_Lesson_05_Reasoning_from_Nets_v0.1.html",
    "quad-01-growing-patterns":
        "02_Foundations/01_Lessons/Quadratics/Lesson_01_Growing_Patterns/NEO_Maths_Y9_Quadratics_Lesson_01_Growing_Patterns_v0.1.html",
    "quad-02-the-second-difference":
        "02_Foundations/01_Lessons/Quadratics/Lesson_02_The_Second_Difference/NEO_Maths_Y9_Quadratics_Lesson_02_The_Second_Difference_v0.1.html",
    "quad-03-the-rule-behind-the-sequence":
        "02_Foundations/01_Lessons/Quadratics/Lesson_03_The_Rule_Behind_the_Sequence/NEO_Maths_Y9_Quadratics_Lesson_03_The_Rule_Behind_the_Sequence_v0.1.html",
    "quad-04-the-expression-behind-it":
        "02_Foundations/01_Lessons/Quadratics/Lesson_04_The_Expression_Behind_It/NEO_Maths_Y9_Quadratics_Lesson_04_The_Expression_Behind_It_v0.1.html",
    "quad-05-meet-the-parabola":
        "02_Foundations/01_Lessons/Quadratics/Lesson_05_Meet_the_Parabola/NEO_Maths_Y9_Quadratics_Lesson_05_Meet_the_Parabola_v0.1.html",
    "quad-06-stretch-and-reflect":
        "02_Foundations/01_Lessons/Quadratics/Lesson_06_Stretch_and_Reflect/NEO_Maths_Y9_Quadratics_Lesson_06_Stretch_and_Reflect_v0.1.html",
    "quad-07-slide-it-across":
        "02_Foundations/01_Lessons/Quadratics/Lesson_07_Slide_it_Across/NEO_Maths_Y9_Quadratics_Lesson_07_Slide_it_Across_v0.1.html",
    "quad-08-reading-real-parabolas":
        "02_Foundations/01_Lessons/Quadratics/Lesson_08_Reading_Real_Parabolas/NEO_Maths_Y9_Quadratics_Lesson_08_Reading_Real_Parabolas_v0.1.html",
    "constructions-01-the-compass-and-the-circle":
        "02_Foundations/01_Lessons/Constructions/Lesson_01_The_Compass_and_the_Circle/NEO_Maths_Y9_Constructions_Lesson_01_The_Compass_and_the_Circle_v0.1.html",
    "constructions-02-shapes-that-hold-their-form":
        "02_Foundations/01_Lessons/Constructions/Lesson_02_Shapes_That_Hold_Their_Form/NEO_Maths_Y9_Constructions_Lesson_02_Shapes_That_Hold_Their_Form_v0.1.html",
    "constructions-03-the-perpendicular-bisector":
        "02_Foundations/01_Lessons/Constructions/Lesson_03_The_Perpendicular_Bisector/NEO_Maths_Y9_Constructions_Lesson_03_The_Perpendicular_Bisector_v0.1.html",
    "constructions-04-the-angle-bisector":
        "02_Foundations/01_Lessons/Constructions/Lesson_04_The_Angle_Bisector/NEO_Maths_Y9_Constructions_Lesson_04_The_Angle_Bisector_v0.1.html",
    "constructions-05-loci":
        "02_Foundations/01_Lessons/Constructions/Lesson_05_Loci/NEO_Maths_Y9_Constructions_Lesson_05_Loci_v0.1.html",
    "constructions-06-bearings":
        "02_Foundations/01_Lessons/Constructions/Lesson_06_Bearings/NEO_Maths_Y9_Constructions_Lesson_06_Bearings_v0.1.html",
    "constructions-07-putting-it-together":
        "02_Foundations/01_Lessons/Constructions/Lesson_07_Putting_It_Together/NEO_Maths_Y9_Constructions_Lesson_07_Putting_It_Together_v0.1.html",
    "ineq-01-inequality-symbols":
        "02_Foundations/01_Lessons/Inequalities/Lesson_01_Inequality_Symbols/NEO_Maths_Y9_Inequalities_Lesson_01_Inequality_Symbols_v0.1.html",
    "ineq-02-solving-linear-inequalities":
        "02_Foundations/01_Lessons/Inequalities/Lesson_02_Solving_Linear_Inequalities/NEO_Maths_Y9_Inequalities_Lesson_02_Solving_Linear_Inequalities_v0.1.html",
    "ineq-03-solutions-on-a-number-line":
        "02_Foundations/01_Lessons/Inequalities/Lesson_03_Showing_Solutions_on_a_Number_Line/NEO_Maths_Y9_Inequalities_Lesson_03_Showing_Solutions_on_a_Number_Line_v0.1.html",
    "ineq-04-regions-on-a-graph":
        "02_Foundations/01_Lessons/Inequalities/Lesson_04_Inequalities_as_Regions/NEO_Maths_Y9_Inequalities_Lesson_04_Inequalities_as_Regions_v0.1.html",
    "formulae-01-letters-unknowns-variables":
        "02_Foundations/01_Lessons/Formulae_and_Rearranging/Lesson_01_Letters_as_Unknowns_and_Variables/NEO_Maths_Y9_Formulae_Lesson_01_Letters_as_Unknowns_and_Variables_v0.1.html",
    "formulae-02-substituting-values":
        "02_Foundations/01_Lessons/Formulae_and_Rearranging/Lesson_02_Substituting_Values/NEO_Maths_Y9_Formulae_Lesson_02_Substituting_Values_v0.1.html",
    "formulae-03-words-and-diagrams":
        "02_Foundations/01_Lessons/Formulae_and_Rearranging/Lesson_03_Formulae_from_Words_and_Diagrams/NEO_Maths_Y9_Formulae_Lesson_03_Formulae_from_Words_and_Diagrams_v0.1.html",
    "shapes-06-platonic-solids":
        "02_Foundations/01_Lessons/2D_and_3D_Shapes/Lesson_06_Platonic_Solids/NEO_Maths_Y9_Shapes_Lesson_06_Platonic_Solids_v0.1.html",
    "shapes-07-surface-area":
        "02_Foundations/01_Lessons/2D_and_3D_Shapes/Lesson_07_Surface_Area/NEO_Maths_Y9_Shapes_Lesson_07_Surface_Area_v0.1.html",
    "shapes-08-cross-sections":
        "02_Foundations/01_Lessons/2D_and_3D_Shapes/Lesson_08_Cross_Sections/NEO_Maths_Y9_Shapes_Lesson_08_Cross_Sections_v0.1.html",
    "shapes-09-volume":
        "02_Foundations/01_Lessons/2D_and_3D_Shapes/Lesson_09_Volume/NEO_Maths_Y9_Shapes_Lesson_09_Volume_v0.1.html",
    "shapes-10-converting-units":
        "02_Foundations/01_Lessons/2D_and_3D_Shapes/Lesson_10_Converting_Units/NEO_Maths_Y9_Shapes_Lesson_10_Converting_Units_v0.1.html",
    "straight-lines-01-a-line-as-a-relationship":
        "03_Intermediate/01_Lessons/Straight_Lines/Lesson_01_A_Line_as_a_Relationship/NEO_Maths_Y10_Straight_Lines_Lesson_01_A_Line_as_a_Relationship_v0.1.html",
    "straight-lines-02-a-table-can-predict-a-line":
        "03_Intermediate/01_Lessons/Straight_Lines/Lesson_02_A_Table_Can_Predict_a_Line/NEO_Maths_Y10_Straight_Lines_Lesson_02_A_Table_Can_Predict_a_Line_v0.1.html",
    "straight-lines-03-where-does-the-line-start":
        "03_Intermediate/01_Lessons/Straight_Lines/Lesson_03_Where_Does_the_Line_Start/NEO_Maths_Y10_Straight_Lines_Lesson_03_Where_Does_the_Line_Start_v0.1.html",
    "straight-lines-04-how-fast-is-the-line-changing":
        "03_Intermediate/01_Lessons/Straight_Lines/Lesson_04_How_Fast_Is_the_Line_Changing/NEO_Maths_Y10_Straight_Lines_Lesson_04_How_Fast_Is_the_Line_Changing_v0.1.html",
    "straight-lines-05-rise-run-and-two-points":
        "03_Intermediate/01_Lessons/Straight_Lines/Lesson_05_Rise_Run_and_Two_Points/NEO_Maths_Y10_Straight_Lines_Lesson_05_Rise_Run_and_Two_Points_v0.1.html",
    "straight-lines-06-can-i-write-the-line":
        "03_Intermediate/01_Lessons/Straight_Lines/Lesson_06_Can_I_Write_the_Line/NEO_Maths_Y10_Straight_Lines_Lesson_06_Can_I_Write_the_Line_v0.1.html",
    "straight-lines-07-parallel-stories-of-change":
        "03_Intermediate/01_Lessons/Straight_Lines/Lesson_07_Parallel_Lines/NEO_Maths_Y10_Straight_Lines_Lesson_07_Parallel_Lines_v0.1.html",
    "straight-lines-08-when-two-lines-meet":
        "03_Intermediate/01_Lessons/Straight_Lines/Lesson_08_When_Two_Lines_Meet/NEO_Maths_Y10_Straight_Lines_Lesson_08_When_Two_Lines_Meet_v0.1.html",
    "straight-lines-09-conversion-graphs-as-models":
        "03_Intermediate/01_Lessons/Straight_Lines/Lesson_09_Conversion_Graphs/NEO_Maths_Y10_Straight_Lines_Lesson_09_Conversion_Graphs_v0.1.html",
    "straight-lines-10-what-can-i-explain":
        "03_Intermediate/01_Lessons/Straight_Lines/Lesson_10_What_Can_I_Explain/NEO_Maths_Y10_Straight_Lines_Lesson_10_What_Can_I_Explain_v0.1.html",
    "equations-01-keeping-the-balance":
        "03_Intermediate/01_Lessons/Equations_Inequalities_Simultaneous/Lesson_01_Keeping_the_Balance/NEO_Maths_Y10_Equations_Lesson_01_Keeping_the_Balance_v0.1.html",
    "equations-02-both-sides-and-brackets":
        "03_Intermediate/01_Lessons/Equations_Inequalities_Simultaneous/Lesson_02_Both_Sides_and_Brackets/NEO_Maths_Y10_Equations_Lesson_02_Both_Sides_and_Brackets_v0.1.html",
    "equations-03-equations-with-fractions":
        "03_Intermediate/01_Lessons/Equations_Inequalities_Simultaneous/Lesson_03_Equations_with_Fractions/NEO_Maths_Y10_Equations_Lesson_03_Equations_with_Fractions_v0.1.html",
    "equations-04-forming-an-equation":
        "03_Intermediate/01_Lessons/Equations_Inequalities_Simultaneous/Lesson_04_Forming_an_Equation/NEO_Maths_Y10_Equations_Lesson_04_Forming_an_Equation_v0.1.html",
    "equations-05-a-line-is-a-set-of-solutions":
        "03_Intermediate/01_Lessons/Equations_Inequalities_Simultaneous/Lesson_05_A_Line_is_a_Set_of_Solutions/NEO_Maths_Y10_Equations_Lesson_05_A_Line_is_a_Set_of_Solutions_v0.1.html",
    "equations-06-where-two-lines-meet":
        "03_Intermediate/01_Lessons/Equations_Inequalities_Simultaneous/Lesson_06_Where_Two_Lines_Meet/NEO_Maths_Y10_Equations_Lesson_06_Where_Two_Lines_Meet_v0.1.html",
    "equations-07-solving-by-substitution":
        "03_Intermediate/01_Lessons/Equations_Inequalities_Simultaneous/Lesson_07_Solving_by_Substitution/NEO_Maths_Y10_Equations_Lesson_07_Solving_by_Substitution_v0.1.html",
    "equations-08-solving-by-elimination":
        "03_Intermediate/01_Lessons/Equations_Inequalities_Simultaneous/Lesson_08_Solving_by_Elimination/NEO_Maths_Y10_Equations_Lesson_08_Solving_by_Elimination_v0.1.html",
    "equations-09-forming-and-solving-a-pair":
        "03_Intermediate/01_Lessons/Equations_Inequalities_Simultaneous/Lesson_09_Forming_and_Solving_a_Pair/NEO_Maths_Y10_Equations_Lesson_09_Forming_and_Solving_a_Pair_v0.1.html",
    "equations-10-inequalities-on-a-number-line":
        "03_Intermediate/01_Lessons/Equations_Inequalities_Simultaneous/Lesson_10_Inequalities_on_a_Number_Line/NEO_Maths_Y10_Equations_Lesson_10_Inequalities_on_a_Number_Line_v0.1.html",
    "equations-11-inequalities-as-regions":
        "03_Intermediate/01_Lessons/Equations_Inequalities_Simultaneous/Lesson_11_Inequalities_as_Regions/NEO_Maths_Y10_Equations_Lesson_11_Inequalities_as_Regions_v0.1.html",
    "circle-theorems-01-the-circle-and-its-parts":
        "03_Intermediate/01_Lessons/Circle_Theorems/Lesson_01_The_Circle_and_its_Parts/NEO_Maths_Y10_Circle_Theorems_Lesson_01_The_Circle_and_its_Parts_v0.1.html",
    "circle-theorems-02-the-angle-at-the-centre":
        "03_Intermediate/01_Lessons/Circle_Theorems/Lesson_02_The_Angle_at_the_Centre/NEO_Maths_Y10_Circle_Theorems_Lesson_02_The_Angle_at_the_Centre_v0.1.html",
    "circle-theorems-03-the-angle-in-a-semicircle":
        "03_Intermediate/01_Lessons/Circle_Theorems/Lesson_03_The_Angle_in_a_Semicircle/NEO_Maths_Y10_Circle_Theorems_Lesson_03_The_Angle_in_a_Semicircle_v0.1.html",
    "circle-theorems-04-angles-in-the-same-segment":
        "03_Intermediate/01_Lessons/Circle_Theorems/Lesson_04_Angles_in_the_Same_Segment/NEO_Maths_Y10_Circle_Theorems_Lesson_04_Angles_in_the_Same_Segment_v0.1.html",
    "circle-theorems-05-cyclic-quadrilaterals":
        "03_Intermediate/01_Lessons/Circle_Theorems/Lesson_05_Cyclic_Quadrilaterals/NEO_Maths_Y10_Circle_Theorems_Lesson_05_Cyclic_Quadrilaterals_v0.1.html",
    "circle-theorems-06-tangents":
        "03_Intermediate/01_Lessons/Circle_Theorems/Lesson_06_Tangents/NEO_Maths_Y10_Circle_Theorems_Lesson_06_Tangents_v0.1.html",
    "circle-theorems-07-the-alternate-segment-theorem":
        "03_Intermediate/01_Lessons/Circle_Theorems/Lesson_07_The_Alternate_Segment_Theorem/NEO_Maths_Y10_Circle_Theorems_Lesson_07_The_Alternate_Segment_Theorem_v0.1.html",
    "circle-theorems-08-the-perpendicular-from-the-centre-to-a-chord":
        "03_Intermediate/01_Lessons/Circle_Theorems/Lesson_08_The_Perpendicular_from_the_Centre_to_a_Chord/NEO_Maths_Y10_Circle_Theorems_Lesson_08_The_Perpendicular_from_the_Centre_to_a_Chord_v0.1.html",
    "circle-theorems-09-combining-the-theorems":
        "03_Intermediate/01_Lessons/Circle_Theorems/Lesson_09_Combining_the_Theorems/NEO_Maths_Y10_Circle_Theorems_Lesson_09_Combining_the_Theorems_v0.1.html",
    "circle-theorems-10-proof-and-problem-solving":
        "03_Intermediate/01_Lessons/Circle_Theorems/Lesson_10_Proof_and_Problem_Solving/NEO_Maths_Y10_Circle_Theorems_Lesson_10_Proof_and_Problem_Solving_v0.1.html",
    "trigonometry-01-the-constant-ratio":
        "03_Intermediate/01_Lessons/Introduction_to_Trigonometry/Lesson_01_The_Constant_Ratio/NEO_Maths_Y10_Trigonometry_Lesson_01_The_Constant_Ratio_v0.1.html",
    "trigonometry-02-naming-the-sides":
        "03_Intermediate/01_Lessons/Introduction_to_Trigonometry/Lesson_02_Naming_the_Sides/NEO_Maths_Y10_Trigonometry_Lesson_02_Naming_the_Sides_v0.1.html",
    "trigonometry-03-the-tangent-ratio":
        "03_Intermediate/01_Lessons/Introduction_to_Trigonometry/Lesson_03_The_Tangent_Ratio/NEO_Maths_Y10_Trigonometry_Lesson_03_The_Tangent_Ratio_v0.1.html",
    "trigonometry-04-sine-and-cosine":
        "03_Intermediate/01_Lessons/Introduction_to_Trigonometry/Lesson_04_Sine_and_Cosine/NEO_Maths_Y10_Trigonometry_Lesson_04_Sine_and_Cosine_v0.1.html",
    "trigonometry-05-finding-a-side":
        "03_Intermediate/01_Lessons/Introduction_to_Trigonometry/Lesson_05_Finding_a_Side/NEO_Maths_Y10_Trigonometry_Lesson_05_Finding_a_Side_v0.1.html",
    "trigonometry-06-finding-a-side-rearranging":
        "03_Intermediate/01_Lessons/Introduction_to_Trigonometry/Lesson_06_Finding_a_Side_Rearranging/NEO_Maths_Y10_Trigonometry_Lesson_06_Finding_a_Side_Rearranging_v0.1.html",
    "trigonometry-07-finding-an-angle":
        "03_Intermediate/01_Lessons/Introduction_to_Trigonometry/Lesson_07_Finding_an_Angle/NEO_Maths_Y10_Trigonometry_Lesson_07_Finding_an_Angle_v0.1.html",
    "trigonometry-08-putting-it-together":
        "03_Intermediate/01_Lessons/Introduction_to_Trigonometry/Lesson_08_Putting_It_Together/NEO_Maths_Y10_Trigonometry_Lesson_08_Putting_It_Together_v0.1.html",
    "ks3-ratio-and-proportion":
        "KS3 (1)/ratio (1)/NEO_Maths_KS3_Ratio_Proportion_Interactive_v6.html",
    "ks3-place-value":
        "KS3 (1)/place-value-recycled/NEO_Maths_Y7_Place_Value_Interactive_v0.2.html",
}

SNIPPET = (
    '\n<script src="{rel}assets/progress.js"></script>'
    '\n<script>NEOProgress.autoTrack({lesson_id!r});</script>\n'
)

CHROME_STYLE = """
<style>
  .neo-chrome, .neo-chrome * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif; }
  .neo-chrome-header { background: #1A2E3B; color: #F7F7F5; padding: 0.6rem 1.2rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
  .neo-chrome-header a.neo-home { color: #2AB3A0; text-decoration: none; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; white-space: nowrap; }
  .neo-chrome-header a.neo-home:hover { text-decoration: underline; }
  .neo-chrome-header .neo-crumb { font-size: 0.8rem; color: rgba(247,247,245,0.85); text-align: right; }
  .neo-chrome-header .neo-crumb strong { color: #FFFFFF; font-weight: 600; }
  .neo-chrome-footer { background: #1A2E3B; color: rgba(247,247,245,0.85); padding: 1.1rem 1.2rem; text-align: center; font-size: 0.8rem; margin-top: 2rem; }
  .neo-chrome-footer a { color: #2AB3A0; text-decoration: none; margin: 0 0.6rem; }
  .neo-chrome-footer a:hover { text-decoration: underline; }
  .neo-chrome-footer .neo-mark { font-size: 0.95rem; color: #FFFFFF; letter-spacing: 0.06em; margin-bottom: 0.3rem; }
  .neo-chrome-footer .neo-mark span { color: #2AB3A0; }
  /* On a phone, a wide table (e.g. the Final Task rubric) scrolls inside its own box instead of widening the whole page. */
  @media (max-width: 700px) { .neo-lesson-root table { display: block; max-width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; } }
  /* --- Comfort & Access --- */
  .neo-comfort-btn{background:#2AB3A0;color:#08312b;border:none;border-radius:8px;padding:0.35rem 0.7rem;font-weight:700;font-size:0.72rem;letter-spacing:0.06em;cursor:pointer;white-space:nowrap}
  .neo-comfort-btn:hover{filter:brightness(1.06)}
  .neo-comfort-panel{background:#12242e;color:#F7F7F5;padding:0.85rem 1.2rem;display:flex;flex-wrap:wrap;gap:1.4rem;align-items:flex-end;border-top:1px solid rgba(255,255,255,0.12);font-family:'Inter',-apple-system,'Segoe UI',sans-serif}
  .neo-comfort-panel[hidden]{display:none}
  .neo-comfort-group{display:flex;flex-direction:column;gap:0.35rem}
  .neo-comfort-group>span{font-size:0.62rem;text-transform:uppercase;letter-spacing:0.14em;color:rgba(247,247,245,0.65)}
  .neo-comfort-row{display:flex;gap:0.4rem}
  .neo-comfort-panel button.opt{background:rgba(255,255,255,0.10);color:#F7F7F5;border:1px solid rgba(255,255,255,0.25);border-radius:7px;padding:0.35rem 0.7rem;cursor:pointer;font-size:0.8rem}
  .neo-comfort-panel button.opt[aria-pressed="true"]{background:#2AB3A0;color:#08312b;border-color:#2AB3A0;font-weight:700}
  .neo-comfort-reset{margin-left:auto;align-self:center;background:none;border:1px solid rgba(255,255,255,0.3);color:rgba(247,247,245,0.85);border-radius:7px;padding:0.35rem 0.7rem;cursor:pointer;font-size:0.75rem}
  html[data-neo-text="large"]{font-size:112.5%}
  html[data-neo-text="larger"]{font-size:125%}
  html[data-neo-spacing="on"] .neo-lesson-root{letter-spacing:0.012em}
  html[data-neo-spacing="on"] .neo-lesson-root p,html[data-neo-spacing="on"] .neo-lesson-root li,html[data-neo-spacing="on"] .neo-lesson-root summary,html[data-neo-spacing="on"] .neo-lesson-root h2,html[data-neo-spacing="on"] .neo-lesson-root h3,html[data-neo-spacing="on"] .neo-lesson-root label{line-height:1.9!important;margin-bottom:0.7em!important}
  html[data-neo-calm="on"]{filter:saturate(0.82) brightness(1.02)}
  html[data-neo-motion="reduced"] *,html[data-neo-motion="reduced"] *::before,html[data-neo-motion="reduced"] *::after{animation-duration:0.001ms!important;animation-iteration-count:1!important;transition-duration:0.001ms!important;scroll-behavior:auto!important}
  @media (prefers-reduced-motion: reduce){*,*::before,*::after{animation-duration:0.001ms!important;transition-duration:0.001ms!important;scroll-behavior:auto!important}}
  .mathpalette{margin:6px 0}
  .palette-toggle{background:#365a68;color:#fff;border:none;padding:7px 12px;border-radius:8px;cursor:pointer;font-weight:600}
  .palette-keys{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
  .palette-keys[hidden]{display:none}
  .palette-keys button{min-width:42px;padding:8px 10px;font-size:1.05em;background:#fff;border:1px solid #bcae98;border-radius:8px;cursor:pointer;color:#2f3429}
  .frac{display:inline-flex;flex-direction:column;text-align:center;vertical-align:middle;margin:0 .18em;line-height:1.05}
  .frac .fnum{padding:0 .25em .5px}
  .frac .fden{padding:.5px .25em 0;border-top:1.6px solid currentColor}
  .fracpreview{margin-top:6px;font-size:1.05em;color:#2f3429}
  .fracpreview[hidden]{display:none}
  .fracpreview .flabel{font-size:.85em;color:#5c6b4f;margin-right:.4em}
</style>
"""

CHROME_HEADER = (
    '<div class="neo-chrome neo-chrome-header">'
    '<a class="neo-home" href="{rel}index.html">&larr; NEO Maths home</a>'
    '<div class="neo-crumb">{unit} &middot; <strong>{num} &mdash; {title}</strong></div>'
    '<button class="neo-comfort-btn" type="button" onclick="neoComfortToggle()" aria-expanded="false" aria-controls="neoComfortPanel" title="Comfort and access settings">Aa&nbsp;Comfort</button>'
    '</div>'
)

CHROME_FOOTER = (
    '<div class="neo-chrome neo-chrome-footer">'
    '<div class="neo-mark">NE<span>O</span> by Nudge Education</div>'
    '<div>'
    '<a href="{rel}index.html">All lessons</a>'
    '<a href="{rel}cornerstones.html">The Six Cornerstones</a>'
    '<a href="{rel}curriculum.html">Our curriculum</a>'
    '<a href="{rel}tools/geometry-studio.html">Geometry Studio</a>'
    '</div>'
    '</div>'
)

COMFORT_PANEL = (
    '<div id="neoComfortPanel" class="neo-comfort neo-comfort-panel" hidden aria-label="Comfort and access settings">'
    '<div class="neo-comfort-group"><span>Text size</span><div class="neo-comfort-row">'
    '<button class="opt" data-k="text" data-v="normal" onclick="neoComfortSet(&#39;text&#39;,&#39;normal&#39;)">A</button>'
    '<button class="opt" data-k="text" data-v="large" onclick="neoComfortSet(&#39;text&#39;,&#39;large&#39;)">A+</button>'
    '<button class="opt" data-k="text" data-v="larger" onclick="neoComfortSet(&#39;text&#39;,&#39;larger&#39;)">A++</button>'
    '</div></div>'
    '<div class="neo-comfort-group"><span>Comfort</span><div class="neo-comfort-row">'
    '<button class="opt" data-k="spacing" onclick="neoComfortToggleOpt(&#39;spacing&#39;)">More spacing</button>'
    '<button class="opt" data-k="calm" onclick="neoComfortToggleOpt(&#39;calm&#39;)">Calmer colours</button>'
    '<button class="opt" data-k="motion" onclick="neoComfortToggleOpt(&#39;motion&#39;)">Reduce motion</button>'
    '</div></div>'
    '<button class="neo-comfort-reset" type="button" onclick="neoComfortReset()">Reset</button>'
    '</div>'
)


PALETTE_SCRIPT = """
<script>
/* Maths symbol palette on every answer field (design push). Per-lesson override: window.NEO_PALETTE_SYMBOLS */
(function(){
  if(window.__neoPaletteInstalled)return; window.__neoPaletteInstalled=true;
  var DEFAULT=["a","b","c","x","y","\u00b2","\u00b3","\u221a","\u03c0","+","-","\u00d7","\u00f7","=","\u2248","\u00b0"];
  function syms(){ return (window.NEO_PALETTE_SYMBOLS&&window.NEO_PALETTE_SYMBOLS.length)?window.NEO_PALETTE_SYMBOLS:DEFAULT; }
  function esc(t){ return String(t).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
  /* render any a/b in a plain string as a stacked fraction (numerator over denominator) */
  function renderFractions(t){ var re=new RegExp("([A-Za-z0-9.\u00b2\u00b3]+) */ *([A-Za-z0-9.\u00b2\u00b3]+)","g"); return esc(t).replace(re, function(_,n,d){ return '<span class="frac"><span class="fnum">'+n+'</span><span class="fden">'+d+'</span></span>'; }); }
  function insert(f,s){ f.focus(); var a=f.selectionStart,b=f.selectionEnd; if(a==null){a=b=f.value.length;} f.value=f.value.slice(0,a)+s+f.value.slice(b); var p=a+s.length; try{f.selectionStart=f.selectionEnd=p;}catch(e){} f.focus(); }
  function updatePreview(f,pv){ var v=f.value||""; if(v.indexOf("/")>=0){ pv.hidden=false; pv.innerHTML='<span class="flabel">Reads as:</span> '+renderFractions(v); } else { pv.hidden=true; pv.innerHTML=""; } }
  function attach(f){ if(f.dataset.paletteReady)return; f.dataset.paletteReady="1";
    var w=document.createElement("div"); w.className="mathpalette";
    var t=document.createElement("button"); t.type="button"; t.className="palette-toggle"; t.textContent="\u221a Symbols";
    var k=document.createElement("div"); k.className="palette-keys"; k.hidden=true;
    var pv=document.createElement("div"); pv.className="fracpreview"; pv.hidden=true; pv.setAttribute("aria-live","polite");
    syms().forEach(function(s){ var b=document.createElement("button"); b.type="button"; b.textContent=s; b.addEventListener("click",function(){insert(f,s);updatePreview(f,pv);}); k.appendChild(b); });
    var fr=document.createElement("button"); fr.type="button"; fr.title="Insert a fraction (numerator / denominator)"; fr.innerHTML='<span class="frac"><span class="fnum">a</span><span class="fden">b</span></span>';
    fr.addEventListener("click",function(){ insert(f,"/"); updatePreview(f,pv); }); k.appendChild(fr);
    t.addEventListener("click",function(){ k.hidden=!k.hidden; });
    f.addEventListener("input",function(){ updatePreview(f,pv); });
    w.appendChild(t); w.appendChild(k); f.insertAdjacentElement("afterend",w); w.insertAdjacentElement("afterend",pv);
  }
  function init(){ document.querySelectorAll('input[id$="Answer"], .neo-mathfield').forEach(attach); }
  if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",init);}else{init();}
})();
</script>
"""

ACCORDION_SCRIPT = """
<script>
/* Single-open accordion: opening one panel closes the others (data-keep-open opts out). */
(function(){
  if(window.__neoAccordionInstalled)return; window.__neoAccordionInstalled=true;
  function closeOthers(cur){
    var scope=cur.closest("#lessonView")||document;
    scope.querySelectorAll("details").forEach(function(d){
      if(d!==cur && !d.contains(cur) && d.dataset.keepOpen!=="true") d.open=false;
    });
  }
  document.addEventListener("toggle",function(e){
    var d=e.target;
    if(d && d.tagName==="DETAILS" && d.open && (d.closest("#lessonView")||d.closest(".neo-lesson-root"))) closeOthers(d);
  },true);
})();
</script>
"""

CALCULATOR = r"""
<style>
#neoCalcWrap{position:fixed;right:16px;bottom:16px;z-index:9990;font-family:Arial,sans-serif}
#neoCalcToggle{background:#365a68;color:#fff;border:none;border-radius:24px;padding:11px 16px;font-weight:700;font-size:1em;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.25)}
#neoCalcPanel{position:absolute;right:0;bottom:56px;width:246px;background:#f7f3ea;border:1px solid #cdbfa9;border-radius:14px;box-shadow:0 12px 34px rgba(0,0,0,.30);padding:12px}
#neoCalcPanel[hidden]{display:none}
.neoCalcHead{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.neoCalcHead b{color:#3f5f45}
.neoCalcDeg{font-size:.72em;font-weight:700;color:#fff;background:#5c6b4f;border-radius:6px;padding:2px 7px;letter-spacing:.05em}
#neoCalcExpr{min-height:22px;background:#fff;border:1px solid #cdbfa9;border-radius:8px;padding:7px 9px;font-size:1.05em;text-align:right;word-break:break-all;color:#2f3429}
#neoCalcResult{min-height:20px;text-align:right;font-size:1.15em;font-weight:700;color:#2f6b46;padding:3px 4px 8px}
.neoCalcGrid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.neoCalcGrid button{padding:11px 0;font-size:1em;border:1px solid #bcae98;border-radius:9px;background:#fff;cursor:pointer;color:#2f3429;font-weight:600}
.neoCalcGrid button:hover{background:#f0ebe0}
.neoCalcGrid button.fn{background:#e5eef2;border-color:#7d97a6;font-size:.92em}
.neoCalcGrid button.op{background:#eef3e8}
.neoCalcGrid button.eq{background:#2f6b46;color:#fff;border:none}
.neoCalcGrid button.clr{background:#f6e6de;border-color:#c69}
@media print{#neoCalcWrap{display:none}}
</style>
<div id="neoCalcWrap">
  <button id="neoCalcToggle" type="button" onclick="neoCalcToggle()" aria-expanded="false" aria-controls="neoCalcPanel">&#129518; Calculator</button>
  <div id="neoCalcPanel" hidden role="dialog" aria-label="Scientific calculator, degrees">
    <div class="neoCalcHead"><b>Calculator</b><span class="neoCalcDeg">DEG</span></div>
    <div id="neoCalcExpr" aria-live="polite">0</div>
    <div id="neoCalcResult" aria-live="polite"></div>
    <div class="neoCalcGrid">
      <button type="button" class="fn" onclick="neoCalcFn('sin')">sin</button>
      <button type="button" class="fn" onclick="neoCalcFn('cos')">cos</button>
      <button type="button" class="fn" onclick="neoCalcFn('tan')">tan</button>
      <button type="button" class="clr" onclick="neoCalcBack()">&#9003;</button>
      <button type="button" class="fn" onclick="neoCalcFn('asin')">sin&#8315;&#185;</button>
      <button type="button" class="fn" onclick="neoCalcFn('acos')">cos&#8315;&#185;</button>
      <button type="button" class="fn" onclick="neoCalcFn('atan')">tan&#8315;&#185;</button>
      <button type="button" class="fn" onclick="neoCalcFn('sqrt')">&#8730;</button>
      <button type="button" class="fn" onclick="neoCalcKey('(')">(</button>
      <button type="button" class="fn" onclick="neoCalcKey(')')">)</button>
      <button type="button" class="clr" onclick="neoCalcClear()">C</button>
      <button type="button" class="op" onclick="neoCalcKey('÷')">&#247;</button>
      <button type="button" onclick="neoCalcKey('7')">7</button>
      <button type="button" onclick="neoCalcKey('8')">8</button>
      <button type="button" onclick="neoCalcKey('9')">9</button>
      <button type="button" class="op" onclick="neoCalcKey('×')">&#215;</button>
      <button type="button" onclick="neoCalcKey('4')">4</button>
      <button type="button" onclick="neoCalcKey('5')">5</button>
      <button type="button" onclick="neoCalcKey('6')">6</button>
      <button type="button" class="op" onclick="neoCalcKey('-')">&#8722;</button>
      <button type="button" onclick="neoCalcKey('1')">1</button>
      <button type="button" onclick="neoCalcKey('2')">2</button>
      <button type="button" onclick="neoCalcKey('3')">3</button>
      <button type="button" class="op" onclick="neoCalcKey('+')">+</button>
      <button type="button" onclick="neoCalcKey('0')">0</button>
      <button type="button" onclick="neoCalcKey('.')">.</button>
      <button type="button" class="eq" style="grid-column:span 2" onclick="neoCalcEq()">=</button>
    </div>
    <p style="font-size:.78em;color:#5c6b4f;margin:8px 2px 0">Angles are in <b>degrees</b>. Examples: 9 &#215; sin(37) = 5.42; &nbsp;sin&#8315;&#185;(0.5) = 30</p>
  </div>
</div>
<script>
(function(){
  if(window.__neoCalcInstalled)return; window.__neoCalcInstalled=true;
  var expr="";
  function isFn(x){return x==="sin"||x==="cos"||x==="tan"||x==="sqrt"||x==="asin"||x==="acos"||x==="atan";}
  function evalExpr(input){
    var s=String(input).replace(/×/g,"*").replace(/÷/g,"/").replace(/−/g,"-").replace(/°/g,"");
    var toks=s.match(/\d+\.?\d*|\.\d+|asin|acos|atan|sin|cos|tan|sqrt|√|[()+\-*/]/g);
    if(!toks) return NaN;
    var out=[], ops=[], prec={"+":1,"-":1,"*":2,"/":2,"u":4}, prev=null;
    for(var i=0;i<toks.length;i++){ var t=toks[i]; if(t==="√")t="sqrt";
      if(/^[\d.]/.test(t)){ out.push(parseFloat(t)); prev="n"; }
      else if(isFn(t)){ ops.push(t); prev="f"; }
      else if(t==="("){ ops.push("("); prev="("; }
      else if(t===")"){ while(ops.length&&ops[ops.length-1]!=="(") out.push(ops.pop()); if(ops.length) ops.pop(); if(ops.length&&isFn(ops[ops.length-1])) out.push(ops.pop()); prev="n"; }
      else { var op=t; if(op==="-"&&(prev===null||prev==="("||prev==="o"||prev==="f")) op="u";
        while(ops.length){ var tp=ops[ops.length-1]; if(tp!=="(" && (isFn(tp) || (prec[tp] && prec[tp]>=prec[op]))) out.push(ops.pop()); else break; }
        ops.push(op); prev="o"; }
    }
    while(ops.length){ var o=ops.pop(); if(o!=="(") out.push(o); }
    var st=[];
    for(var j=0;j<out.length;j++){ var x=out[j];
      if(typeof x==="number"){ st.push(x); }
      else if(x==="u"){ if(!st.length)return NaN; st.push(-st.pop()); }
      else if(isFn(x)){ if(!st.length)return NaN; var a=st.pop(), r;
        if(x==="sin")r=Math.sin(a*Math.PI/180); else if(x==="cos")r=Math.cos(a*Math.PI/180); else if(x==="tan")r=Math.tan(a*Math.PI/180);
        else if(x==="sqrt")r=Math.sqrt(a);
        else if(x==="asin")r=(a<-1||a>1)?NaN:Math.asin(a)*180/Math.PI; else if(x==="acos")r=(a<-1||a>1)?NaN:Math.acos(a)*180/Math.PI; else if(x==="atan")r=Math.atan(a)*180/Math.PI;
        st.push(r); }
      else { if(st.length<2)return NaN; var b=st.pop(), a2=st.pop(); st.push(x==="+"?a2+b:x==="-"?a2-b:x==="*"?a2*b:a2/b); }
    }
    return st.length===1?st[0]:NaN;
  }
  function render(){
    document.getElementById("neoCalcExpr").textContent = (expr||"0").replace(/asin/g,"sin⁻¹").replace(/acos/g,"cos⁻¹").replace(/atan/g,"tan⁻¹");
    var v=evalExpr(expr);
    document.getElementById("neoCalcResult").textContent = (expr && isFinite(v)) ? "= "+(Math.round(v*1e6)/1e6) : "";
  }
  window.neoCalcEval=evalExpr;
  window.neoCalcToggle=function(){ var p=document.getElementById("neoCalcPanel"); p.hidden=!p.hidden; document.getElementById("neoCalcToggle").setAttribute("aria-expanded", String(!p.hidden)); };
  window.neoCalcKey=function(s){ expr+=s; render(); };
  window.neoCalcFn=function(f){ expr+=(f==="sqrt"?"√":f)+"("; render(); };
  window.neoCalcClear=function(){ expr=""; render(); };
  window.neoCalcBack=function(){ var m=expr.match(/(asin\(|acos\(|atan\(|sin\(|cos\(|tan\(|√\()$/); expr=m?expr.slice(0,-m[0].length):expr.slice(0,-1); render(); };
  window.neoCalcEq=function(){ var v=evalExpr(expr); document.getElementById("neoCalcResult").textContent = isFinite(v) ? "= "+(Math.round(v*1e6)/1e6) : "= —"; };
  render();
})();
</script>
"""

COMFORT_SCRIPT = """
<script>
(function(){
 var KEY="neoComfort",d=document.documentElement,st={text:"normal",spacing:false,calm:false,motion:false};
 try{var sv=JSON.parse(localStorage.getItem(KEY)||"null");if(sv)st=Object.assign(st,sv);}catch(e){}
 function apply(){d.setAttribute("data-neo-text",st.text);st.spacing?d.setAttribute("data-neo-spacing","on"):d.removeAttribute("data-neo-spacing");st.calm?d.setAttribute("data-neo-calm","on"):d.removeAttribute("data-neo-calm");st.motion?d.setAttribute("data-neo-motion","reduced"):d.removeAttribute("data-neo-motion");}
 function save(){try{localStorage.setItem(KEY,JSON.stringify(st));}catch(e){}}
 function sync(){var ps=document.querySelectorAll("#neoComfortPanel .opt");for(var i=0;i<ps.length;i++){var b=ps[i],k=b.getAttribute("data-k");if(k==="text"){b.setAttribute("aria-pressed",st.text===b.getAttribute("data-v")?"true":"false");}else{b.setAttribute("aria-pressed",st[k]?"true":"false");}}}
 window.neoComfortToggle=function(){var p=document.getElementById("neoComfortPanel"),btn=document.querySelector(".neo-comfort-btn"),willOpen=p.hasAttribute("hidden");willOpen?p.removeAttribute("hidden"):p.setAttribute("hidden","");if(btn)btn.setAttribute("aria-expanded",willOpen?"true":"false");};
 window.neoComfortSet=function(k,v){st[k]=v;apply();save();sync();};
 window.neoComfortToggleOpt=function(k){st[k]=!st[k];apply();save();sync();};
 window.neoComfortReset=function(){st={text:"normal",spacing:false,calm:false,motion:false};apply();save();sync();};
 apply();
 if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",sync);}else{sync();}
})();
</script>
"""


def inject_chrome(html: str, unit: str, num: str, title: str, depth: int) -> str:
    if "neo-chrome" in html:
        return html
    rel = "../" * depth
    header = CHROME_STYLE + CHROME_HEADER.format(rel=rel, unit=unit, num=num, title=title) + COMFORT_PANEL + COMFORT_SCRIPT + '<div class="neo-lesson-root">'
    footer = PALETTE_SCRIPT + ACCORDION_SCRIPT + "</div>" + CALCULATOR + CHROME_FOOTER.format(rel=rel)
    m = re.search(r"<body[^>]*>", html, re.IGNORECASE)
    if m:
        html = html[: m.end()] + "\n" + header + "\n" + html[m.end() :]
    else:
        html = header + "\n" + html
    if re.search(r"</body>", html, re.IGNORECASE):
        html = re.sub(r"</body>", lambda _m: footer + "\n</body>", html, count=1, flags=re.IGNORECASE)
    else:
        html = html + footer
    return html


def ensure_charset(html: str) -> str:
    """Guarantee a UTF-8 declaration in the first bytes of the page.

    Most lessons are full documents that already declare <meta charset="utf-8">
    in their <head>. A few (e.g. the Straight-Line equation lesson) are bare
    fragments with no <head> at all; without a charset the local server serves
    them with no encoding and the browser falls back to Windows-1252, rendering
    UTF-8 emoji and dashes as mojibake. This is a no-op when a charset is
    already present.
    """
    if re.search(r"<meta[^>]+charset", html, re.IGNORECASE):
        return html
    return '<meta charset="utf-8">\n' + html


PRACTICE_CARD = (
    '\n<div class="neo-practice-cta" style="background:#fffaf0; padding:20px; margin-top:22px;'
    ' border-left:6px solid #5c6b4f; border-radius:14px; text-align:center;">'
    '<h2 style="margin:0 0 14px;">✏️ Ready to strengthen your understanding?</h2>'
    '<button type="button" onclick="{fn}()" style="padding:13px 22px; background:#5c6b4f; color:#fff;'
    ' border:none; border-radius:10px; font-weight:bold; font-size:1.05em; cursor:pointer;">'
    'Open Practice Companion</button></div>\n'
)


def inject_practice_card(html: str) -> str:
    """Standardise the Practice Companion trigger across every lesson.

    Each lesson has exactly one practice trigger — a plain button (near the top in most
    lessons) or an older "Ready to strengthen your skills?" card at the bottom in a few.
    Remove whichever it is and drop one consistent card at the bottom of the lesson view,
    calling that lesson's own open-function. Runs on the raw lesson HTML before the shared
    chrome is added. No-op if it can't find the trigger or the anchor, so a lesson is never
    left in a broken state.
    """
    if "neo-practice-cta" in html:
        return html
    if 'onclick="openPracticeSession()"' in html:
        fn = "openPracticeSession"
    elif 'onclick="openPractice()"' in html:
        fn = "openPractice"
    else:
        return html

    # Remove the existing trigger: an older "Ready to strengthen" card first, else the button.
    card_re = re.compile(
        r"<div\b[^>]*>(?:(?!</div>).)*?Ready to strengthen(?:(?!</div>).)*?"
        r'onclick="openPractice(?:Session)?\(\)"(?:(?!</div>).)*?</div>',
        re.IGNORECASE | re.DOTALL,
    )
    stripped, n = card_re.subn("", html, count=1)
    if n == 0:
        btn_re = re.compile(
            r'<button\b[^>]*onclick="openPractice(?:Session)?\(\)"[^>]*>'
            r"(?:(?!</button>).)*?</button>",
            re.IGNORECASE | re.DOTALL,
        )
        stripped, n = btn_re.subn("", html, count=1)
        if n == 0:
            return html
        # Tidy an empty support box the removed button may have left behind.
        stripped = re.sub(
            r'<div class="guides"><div class="buttonrow">\s*</div></div>', "", stripped
        )

    card = PRACTICE_CARD.format(fn=fn)
    placed, m = re.subn(
        r'(</div>)(\s*(?:<!--(?:(?!-->).)*?-->\s*)?<div id="practiceView")',
        card + r"\1\2",
        stripped,
        count=1,
        flags=re.DOTALL,
    )
    if m == 0:
        return html
    return placed


def inject_progress(html: str, lesson_id: str, depth: int) -> str:
    rel = "../" * depth
    snippet = SNIPPET.format(rel=rel, lesson_id=lesson_id)
    if "NEOProgress.autoTrack" in html:
        return html  # already injected
    if re.search(r"</body>", html, re.IGNORECASE):
        return re.sub(r"</body>", snippet + "</body>", html, count=1, flags=re.IGNORECASE)
    return html + snippet


# Units whose diagnostic expedition gives a field kit (GreenPrint v2.4). Their lessons get a "Field kit"
# button; lesson n of the unit opens with tool n first. Data files: docs/assets/fieldkits/<unit-id>.js,
# made by scripts/fieldkits/make_fieldkits.js. Add a unit here when its expedition is built.
FIELDKIT_UNITS = {"inequalities", "formulae-rearranging"}


def inject_fieldkit(html: str, unit_id: str, index: int, depth: int) -> str:
    if unit_id not in FIELDKIT_UNITS or "NEOFieldKit.mount" in html:
        return html
    rel = "../" * depth
    snippet = (f'\n<script src="{rel}assets/fieldkits/{unit_id}.js"></script>'
               f'\n<script src="{rel}assets/fieldkit.js"></script>'
               f'\n<script>NEOFieldKit.mount({index});</script>\n')
    if re.search(r"</body>", html, re.IGNORECASE):
        return re.sub(r"</body>", lambda _m: snippet + "</body>", html, count=1, flags=re.IGNORECASE)
    return html + snippet


def copy_lesson_assets(html: str, src: Path, dest: Path) -> list:
    """Copy a lesson's guidance PDFs into docs/ next to its built page.

    Lessons link their Learner and Supporting Adult guidance by bare filename (same
    folder as the page), e.g. href="NEO_..._Learner_Guide.pdf". The build otherwise copies
    only the HTML, so those links 404 on the live site. Copy each referenced same-folder
    PDF that exists in the vault lesson folder into the built page's folder. Returns the
    list of guidance filenames the page references but that are still missing.
    """
    missing = []
    for name in sorted(set(re.findall(r'href="([^"/]+\.pdf)"', html))):
        pdf = src.parent / name
        if pdf.exists():
            shutil.copy2(pdf, dest.parent / name)
        else:
            missing.append(name)
    return missing


def publish_tools() -> None:
    """Publish standalone tools (not lessons) from the vault into docs/ so they go live.
    The Dynamic Geometry Studio is versioned in the vault (…_v0.3.html, …_v0.4.html, …);
    always publish the highest version to docs/tools/geometry-studio.html."""
    import re
    studio_dir = VAULT / "05_Lesson_Templates" / "Dynamic_Geometry_Studio"
    versions = sorted(
        studio_dir.glob("NEO_Dynamic_Geometry_Studio_v*.html"),
        key=lambda p: [int(n) for n in re.findall(r"\d+", p.stem.split("_v")[-1])] or [0],
    )
    if not versions:
        print("tools: no Dynamic Geometry Studio version found to publish")
        return
    latest = versions[-1]
    dest = DOCS / "tools" / "geometry-studio.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(latest, dest)
    print(f"tools: published {latest.name} -> docs/tools/geometry-studio.html")


def validate_studio_links() -> list:
    """Guard the Constructions unit pattern: every 'Open in the Geometry Studio' launch
    link in a published lesson must point at the published Studio, name a task id that
    exists in the Studio's task registry, and carry a return path that resolves to a real
    lesson file. Returns a list of problem strings (empty = all good)."""
    import re
    import urllib.parse
    studio = DOCS / "tools" / "geometry-studio.html"
    problems = []
    if not studio.exists():
        return ["Geometry Studio not published"]
    studio_src = studio.read_text(encoding="utf-8", errors="replace")
    task_ids = set(re.findall(r'"([a-z0-9-]+)":\s*\{\s*tag:', studio_src))
    for html_file in DOCS.glob("lessons/**/*.html"):
        html = html_file.read_text(encoding="utf-8", errors="replace")
        for raw in re.findall(r'href="([^"]*geometry-studio\.html\?[^"]*)"', html):
            link = raw.replace("&amp;", "&")
            path, _, query = link.partition("?")
            qs = urllib.parse.parse_qs(query)
            task = (qs.get("task") or [""])[0]
            ret = (qs.get("return") or [""])[0]
            studio_target = (html_file.parent / path).resolve()
            if not studio_target.exists():
                problems.append(f"{html_file.name}: studio link path not found ({path})")
            if task and task not in task_ids:
                problems.append(f"{html_file.name}: task id '{task}' not in Studio registry")
            if ret:
                ret_target = (studio_target.parent / ret).resolve()
                if not ret_target.exists():
                    problems.append(f"{html_file.name}: return path not found ({ret})")
    return problems


def main() -> None:
    data = json.loads(CURRICULUM.read_text(encoding="utf-8"))
    live, missing = [], []
    missing_guides = []

    for unit in data["units"]:
        for index, lesson in enumerate(unit["lessons"]):
            src_rel = SOURCES.get(lesson["id"])
            if not src_rel:
                continue
            src = VAULT / src_rel
            dest = DOCS / lesson["file"]
            if not src.exists():
                missing.append(lesson["id"])
                lesson["status"] = "pending"
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            html = src.read_text(encoding="utf-8", errors="replace")
            depth = len(Path(lesson["file"]).parents) - 1
            html = inject_practice_card(html)
            html = inject_progress(html, lesson["id"], depth)
            html = inject_fieldkit(html, unit["id"], index, depth)
            html = inject_chrome(html, unit["title"], lesson["num"], lesson["title"], depth)
            html = ensure_charset(html)
            dest.write_text(html, encoding="utf-8")
            for gap in copy_lesson_assets(html, src, dest):
                missing_guides.append(f"{lesson['id']}: {gap}")
            lesson["status"] = "live"
            live.append(lesson["id"])

    publish_tools()
    CURRICULUM.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"live: {len(live)}  missing: {len(missing)}")
    if missing_guides:
        print(f"guidance PDFs referenced but not found ({len(missing_guides)}):")
        for g in missing_guides:
            print(f"  {g}")
    for m in missing:
        print(f"  missing source: {m}")

    studio_problems = validate_studio_links()
    if studio_problems:
        print(f"Geometry Studio launch-link problems ({len(studio_problems)}):")
        for p in studio_problems:
            print(f"  {p}")
    else:
        print("studio links: all Geometry Studio launch links valid")


if __name__ == "__main__":
    main()
