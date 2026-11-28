# The Scratchpad and the calculator in every expedition, and the newer expeditions, in one update

**For:** Gerry · **Takes:** about 20 minutes · **Prepared:** 27 November 2026

## What changes
Every diagnostic expedition now has the **NEO Maths Scratchpad**, the same one as in the lessons. There is a **✏️ Scratchpad** button in every lock and in the top bar. Each room opens its own page with a suggested background (for example a coordinate grid for rotations, a ratio table for sharing). Nothing drawn on it is saved or sent, and the "What is saved?" box says so.

Every expedition also has the lessons' **🧮 Calculator**, in each lock and in the top bar. It is never recorded. In the few locks that test working without a calculator (order of operations, estimating, fractions and negatives by hand, index laws, surds, and the Year 7 number and angle expeditions) it rests, with a short friendly note. Results are saved exactly as before.

This one update also installs the four newer expeditions, if they are not in the service yet: **The Architect's Studio**, **The Market Hall**, **The Sorting Office** and **The Animation Studio**. If you have already added some of them, the steps below simply replace them with the new version.

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

3. **Update Code.gs** (so all nine expeditions are listed): open https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/Code.gs, copy all of it, click **Code.gs** in the project, select everything, paste and save.
4. **Deploy:** Deploy ▸ Manage deployments ▸ the pencil icon ▸ Version: New version ▸ Deploy. The web address stays the same.
5. **Check one:** open the address ending **?page=animationstudio**, step inside, examine the first lock and press **✏️ Scratchpad**. A coordinate grid should open, titled "The Storyboard Wall". Close it and press **🧮 Calculator**: the calculator should open. The bottom of the floor plan should say "Animation Studio v0.2".

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
