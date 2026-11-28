# Installing the diagnostic and Unit Check-in posts in Google Classroom

**For:** Kirstin Stevens · **Takes:** about 10 minutes · **Prepared:** 3 November 2026, updated 28 November 2026

## What this does
Each NEO Maths unit with a diagnostic gets a post at the top of its Classroom topic, above Lesson 01. It is titled **Start here · [diagnostic name]**. Learners take it before the first lesson. It has no scores, and it suggests where to begin.

Each complete unit with a Unit Check-in also gets a post for the end of the unit, titled **Unit Check-in · Return to [name]**. Learners take it after the last lesson. It goes back to the world of the diagnostic and shows where they started and where they are now. There are no scores and no timers. The supporting adult confirms the unit label afterwards from the NEO educator dashboard.

Both kinds of post link to the NEO Maths results service.

**Mathematics | Foundation | Master** (9 new posts)

| Unit | Start here | Unit Check-in |
|---|---|---|
| Inequalities | The Walled Garden | Return to the Walled Garden |
| Formulae and Rearranging | The Inventor's Workshop | Return to the Inventor's Workshop |
| Transformations, Similarity and Scale | The Animation Studio | Return to the Animation Studio |
| Place Value | The Counting House | (to come) |
| Angles | The Architect's Studio | (to come) |
| Perimeter and Area | The Architect's Studio | (to come) |

**Mathematics | Intermediate | Master** (8 new posts)

| Unit | Start here | Unit Check-in |
|---|---|---|
| Number Systems and Calculator Judgement | The Observatory | Return to the Observatory |
| Algebraic Expressions and Identities | The Lighthouse | Return to the Lighthouse |
| Percentages, Ratio, Growth and Bounds | The Market Hall | Return to the Market Hall |
| Sets and Venn Diagrams | The Sorting Office | Return to the Sorting Office |

Nothing else changes. Every existing lesson post stays exactly as it is, and the script never reads or touches learner data.

## Steps
1. Go to **script.google.com**, signed in as **kirstin.stevens@nudgeeducation.online**, and open the project **NEO Maths Classroom sync**.
2. Open the new version of the script in another tab: https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/classroom/classroom_sync.gs and copy all of it (⌘A, then ⌘C).
3. Back in the project, click the code file, select all of it (⌘A), paste the new version (⌘V) and save (⌘S).
4. **Check first.** In the function menu at the top, choose **previewSync** and click **Run**. Nothing is posted. The Execution log should show ten lines beginning "Start here" and seven beginning "Unit Check-in", each under its unit.
5. **Install.** Choose **syncClassroom** and click **Run**. The log should report "created":9 for the Foundation course and "created":8 for the Intermediate course, with every other post "unchanged".
6. **Move the check-ins to the end.** Open each master course in Classroom › Classwork. Classroom puts new posts near the top, so each "Unit Check-in" post sits just below "Start here". Drag each of the seven check-in posts down to the bottom of its topic, below the last lesson. This only needs doing once.

## Good to know
- From now on, running **syncClassroom** adds the posts automatically whenever a new unit gets a diagnostic or a check-in. A check-in is only posted once every lesson in its unit is live.
- If a "Start here" post ever sits below a lesson, drag it back to the top of the topic.
- The posts open on the results service, so learners must be signed in with their NEO Google account (as they always are in Classroom).
- Questions or anything unexpected in the log: contact Gerry before running it again.
