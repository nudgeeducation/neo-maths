# Adding The Animation Studio to the results service

**For:** Gerry · **Takes:** about 5 minutes · **Prepared:** 24 November 2026

## What changes
The Animation Studio, the diagnostic for the Foundations unit *Geometry: Transformations, Similarity and Scale*, joins the results service. Its outcomes reach the learner passport and the educator dashboard like the other eight expeditions. The passport and dashboard list it automatically; nothing else changes.

## Steps
1. Open the **NEO Maths results service** script project, signed in to your NEO account.
2. **Add the new page.** Next to **Files**, click **+ ▸ HTML**, type **AnimationStudio** (no spaces, without `.html`) and press Enter. Open https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/AnimationStudio.html in a new tab, copy all of it (⌘A, then ⌘C), select everything in the new file (⌘A), paste (⌘V) and save (⌘S).
3. **Update Code.gs.** Open https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/results/Code.gs, copy all of it, click **Code.gs** in the project, select everything, paste and save. Its list of expeditions now ends with a line for 'animationstudio'.
4. **Deploy:** Deploy ▸ Manage deployments ▸ the pencil icon ▸ Version: New version ▸ Deploy. The web address stays the same.
5. **Check:** open the address ending **?page=animationstudio**, step inside and examine the first lock. The bottom of the floor plan should say "Animation Studio v0.1".

The Animation Studio's link is: https://script.google.com/a/macros/nudgeeducation.online/s/AKfycbzZ4_uhLDHULyz8DDRtxjGh9DX0e3ETZqE_i08mv00jUfz2OtowM2giqSnWqx3FiyU/exec?page=animationstudio

If anything looks wrong, Manage deployments lets you switch back to the previous version straight away.
