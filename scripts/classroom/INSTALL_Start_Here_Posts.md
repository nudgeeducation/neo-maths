# Installing the "Start here" diagnostic posts in Google Classroom

**For:** Kirstin Stevens · **Takes:** about 5 minutes · **Prepared:** 3 November 2026

## What this does
Each NEO Maths unit that has a diagnostic expedition gets one new post at the top of its Classroom topic, above Lesson 01. The post is titled **Start here · [expedition name]** and links to the diagnostic on the NEO Maths results service. Learners take it before the first lesson; it has no scores and suggests where to begin.

Four posts will be added, two in each master course:

**Mathematics | Foundation | Master**
- Inequalities: Start here · The Walled Garden
- Formulae and Rearranging: Start here · The Inventor's Workshop

**Mathematics | Intermediate | Master**
- Number Systems and Calculator Judgement: Start here · The Observatory
- Algebraic Expressions and Identities: Start here · The Lighthouse

Nothing else changes. Every existing lesson post stays exactly as it is, and the script never reads or touches learner data.

## Steps
1. Go to **script.google.com**, signed in as **kirstin.stevens@nudgeeducation.online**, and open the project **NEO Maths Classroom sync**.
2. Open the new version of the script in another tab: https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/scripts/classroom/classroom_sync.gs and copy all of it (⌘A, then ⌘C).
3. Back in the project, click the code file, select all of it (⌘A), paste the new version (⌘V) and save (⌘S).
4. **Check first.** In the function menu at the top, choose **previewSync** and click **Run**. Nothing is posted. The Execution log should show four lines that begin "Start here", one under each unit above.
5. **Install.** Choose **syncClassroom** and click **Run**. The log should report "created":2 for each course, with every other post unchanged.
6. Open each master course in Classroom › Classwork. The four units now show the "Start here" post at the top.

## Good to know
- From now on, whenever a new unit gets a diagnostic, running **syncClassroom** adds its "Start here" post automatically.
- If a "Start here" post ever sits below a lesson, drag it back to the top of the topic in Classwork.
- The diagnostic opens on the results service, so learners must be signed in with their NEO Google account (as they always are in Classroom).
- Questions or anything unexpected in the log: contact Gerry before running it again.
