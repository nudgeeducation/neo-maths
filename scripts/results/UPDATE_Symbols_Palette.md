# Updating the four diagnostics: the symbols palette

**For:** Gerry · **Takes:** about 10 minutes · **Prepared:** 3 November 2026

## What changes
The four diagnostic expeditions get the **√ Symbols** palette from the lessons. It appears under every answer box where learners type, with a fraction key and a "Reads as" preview that shows typed fractions with a horizontal bar. Fractions in the questions now have a horizontal bar too.

Nothing else changes. What is saved, the learner passport and the educator dashboard all stay exactly as they are. Code.gs does **not** change.

## Steps
1. Open the **NEO Maths results service** script project (NEO Drive › Diagnostic Assessments, or script.google.com), signed in to your NEO account.
2. For each of the four files below:
   - open its link in a new tab, select all (⌘A) and copy (⌘C);
   - back in the project, click the file of the same name, select all (⌘A), paste (⌘V) and save (⌘S).

   | File in the project | Copy from |
   |---|---|
   | Observatory | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/Observatory.html |
   | WalledGarden | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/WalledGarden.html |
   | Workshop | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/Workshop.html |
   | Lighthouse | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/Lighthouse.html |

3. Click **Deploy ▸ Manage deployments**, then the pencil icon. Under **Version**, choose **New version**, then **Deploy**. The web links stay the same.
4. **Check:** open the Lighthouse link (`…/exec?page=lighthouse`), step inside, and examine the first lock. A **√ Symbols** button should sit under the answer box. The bottom of the floor plan should say "Lighthouse v0.2".

If anything looks wrong, Manage deployments lets you switch back to the previous version straight away.
