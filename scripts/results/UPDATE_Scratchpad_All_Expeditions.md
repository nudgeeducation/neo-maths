# The Unit Check-ins, the Scratchpad and the calculator, and the newer expeditions, in one update

**For:** Gerry · **Takes:** about 35 minutes · **Prepared:** 27 November 2026 · **Updated:** 28 November 2026 (Unit Check-ins)

## What changes
Every diagnostic expedition now has the **NEO Maths Scratchpad**, the same one as in the lessons. There is a **✏️ Scratchpad** button in every lock and in the top bar. Each room opens its own page with a suggested background (for example a coordinate grid for rotations, a ratio table for sharing). Nothing drawn on it is saved or sent, and the "What is saved?" box says so.

Every expedition also has the lessons' **🧮 Calculator**, in each lock and in the top bar. It is never recorded. In the few locks that test working without a calculator (order of operations, estimating, fractions and negatives by hand, index laws, surds, and the Year 7 number and angle expeditions) it rests, with a short friendly note. Results are saved exactly as before.

This one update also installs the four newer expeditions, if they are not in the service yet: **The Architect's Studio**, **The Market Hall**, **The Sorting Office** and **The Animation Studio**. If you have already added some of them, the steps below simply replace them with the new version.

**The seven Unit Check-ins join the service.** Each "Return to …" check-in is saved to the learner record when the learner reaches the end, on a new **CheckIns** tab. "Start" in each room comes from the learner's own saved diagnostic for that unit, so it no longer needs to have been taken on the same device. The **learner passport** shows each unit's diagnostic and then the check-in, start → now. The **educator dashboard** has a new section, *Unit Check-ins*, where staff **confirm one label for the unit** (Approaching / Developing / Proficiency / Refining Proficiency) with an optional note. The label is saved on a new **Labels** tab with the email of the adult who confirmed it, and the learner sees it in the check-in and the passport. Learners cannot set a label themselves. Both new tabs are created automatically the first time they are needed.

## Steps
1. Open the **NEO Maths results service** script project, signed in to your NEO account.
2. **Replace (or add) the nine expedition pages.** For each file in the table: if it is not in the project yet, click **+ ▸ HTML** next to **Files** and type the name exactly as shown (no `.html`). Then open its link in a new tab, copy all of it (⌘A, then ⌘C), click the file in the project, select everything (⌘A), paste (⌘V) and save (⌘S).

| File in the project | Copy from |
|---|---|
| Lighthouse | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/Lighthouse.html |
| Observatory | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/Observatory.html |
| WalledGarden | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/WalledGarden.html |
| Workshop | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/Workshop.html |
| CountingHouse | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/CountingHouse.html |
| Studio | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/Studio.html |
| MarketHall | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/MarketHall.html |
| SortingOffice | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/SortingOffice.html |
| AnimationStudio | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/AnimationStudio.html |

3. **Add the seven Unit Check-in pages**, in the same way (each is a new HTML file: **+ ▸ HTML**, type the name, paste, save):

| File in the project | Copy from |
|---|---|
| ObservatoryReturn | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/ObservatoryReturn.html |
| WalledGardenReturn | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/WalledGardenReturn.html |
| WorkshopReturn | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/WorkshopReturn.html |
| LighthouseReturn | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/LighthouseReturn.html |
| MarketHallReturn | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/MarketHallReturn.html |
| SortingOfficeReturn | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/SortingOfficeReturn.html |
| AnimationStudioReturn | https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/AnimationStudioReturn.html |

4. **Replace Passport and Educator** in the same way: Passport from https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/Passport.html and Educator from https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/Educator.html.
5. **Update Code.gs** (so all nine expeditions and seven check-ins are listed, and check-ins and labels are saved): open https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/Code.gs, copy all of it, click **Code.gs** in the project, select everything, paste and save.
6. **Deploy:** Deploy ▸ Manage deployments ▸ the pencil icon ▸ Version: New version ▸ Deploy. The web address stays the same.
7. **Check one expedition:** open the address ending **?page=animationstudio**, step inside, examine the first lock and press **✏️ Scratchpad**. A coordinate grid should open, titled "The Storyboard Wall". Close it and press **🧮 Calculator**: the calculator should open. The bottom of the floor plan should say "Animation Studio v0.2".
8. **Check one check-in:** open the address ending **?page=return-animationstudio** and walk through it. At the end, the floor plan should say **Saved to your learner record ✓**. Your passport (**?page=passport**) should show the check-in, and the educator dashboard (**?page=educator**) should show it under *Unit Check-ins*, with a label to confirm. If you test with your own account, confirm and then **Clear** the label, or delete your test rows from the CheckIns and Labels tabs.

The check-in addresses: **?page=** return-observatory, return-garden, return-workshop, return-lighthouse, return-markethall, return-sortingoffice, return-animationstudio. Learners only need these at the end of each unit; the links will go in the Classroom posts alongside the diagnostics.

| Expedition | New version |
|---|---|
| The Lighthouse | v0.3 |
| The Observatory | v0.5 |
| The Walled Garden | v0.5 |
| The Inventor's Workshop | v0.3 |
| The Counting House | v0.2 |
| The Architect's Studio | v0.2 |
| The Market Hall | v0.2 |
| The Sorting Office | v0.2 |
| The Animation Studio | v0.2 |

If anything looks wrong, Manage deployments lets you switch back to the previous version straight away.
