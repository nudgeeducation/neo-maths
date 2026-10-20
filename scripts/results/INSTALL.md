# Installing the NEO Maths results service

About 15 minutes, once. Done by someone with a NEO Google account (`@nudgeeducation.online`) who can edit the **Diagnostic Assessments** folder on the NEO Drive. The service then belongs to NEO and runs under that account.

**What you will end up with**
- A spreadsheet called **NEO Maths Results** in the Diagnostic Assessments folder, with three tabs: **Diagnostics**, **Comments** and **Staff**.
- One web address that opens every diagnostic expedition, the learner passport and the educator dashboard.

## 1. Create the project

1. In Chrome, make sure you are signed in to Google with your **NEO** account.
2. Open the **Diagnostic Assessments** folder on the NEO Drive.
3. Click **New ▸ More ▸ Google Apps Script**. A new tab opens with the script editor.
4. Click **Untitled project** at the top and rename it **NEO Maths results service**.

## 2. Add the four files

The files are in the maths folder at `scripts/results/`. Claude can put each one on your clipboard in turn.

1. **Code.gs:** in the editor, click `Code.gs`, select everything in it, and paste the contents of `Code.gs` over it.
2. **Observatory:** next to **Files**, click **+ ▸ HTML**, type `Observatory` (without `.html`), press Enter, select everything in the new file and paste the contents of `Observatory.html`.
3. **Passport:** the same way, an HTML file named `Passport`.
4. **Educator:** the same way, an HTML file named `Educator`.
5. Click the **Save** icon (or press ⌘S).

## 3. Run the setup once

1. In the toolbar, choose the function **setup** from the drop-down, then click **Run**.
2. Google asks for permission: **Review permissions ▸** choose your NEO account **▸ Allow**. (It needs to create the spreadsheet in the folder and recognise who is signed in.)
3. Check the Diagnostic Assessments folder: **NEO Maths Results** should now be there.
4. Open it, go to the **Staff** tab, and add the NEO email address of every educator who should see the educator dashboard, one per row. Your own address is already there.

## 4. Publish it as a web app

1. Click **Deploy ▸ New deployment**.
2. Click the cog next to **Select type** and choose **Web app**.
3. Description: `First version`.
4. **Execute as:** Me. **Who has access:** Anyone within Nudge Education (the NEO domain).
5. Click **Deploy**, then copy the **Web app URL**.

## 5. Try it

Add these endings to the Web app URL:

| Ending | Opens |
| --- | --- |
| `?page=observatory` | The Observatory diagnostic (Year 10, Number Systems) |
| `?page=garden` | The Walled Garden diagnostic (Year 9, Inequalities) |
| `?page=workshop` | The Inventor's Workshop diagnostic (Year 9, Formulae and Rearranging) |
| `?page=passport` | The learner passport: the signed-in person's own record |
| `?page=educator` | The educator dashboard (Staff tab only) |

Complete the Observatory once with a test learner account, then check that seven rows appear on the **Diagnostics** tab and that the passport and dashboard show them.

## Updating later

When Claude changes a file: paste the new contents over the old in the editor, save, then **Deploy ▸ Manage deployments ▸** the pencil icon **▸ Version: New version ▸ Deploy**. The web address stays the same.

## Adding a new expedition

Each new unit's diagnostic is one more HTML file, plus one line in `Code.gs`. Claude prepares both.

1. Next to **Files**, click **+ ▸ HTML** and give the new file the name Claude gives you, for example `Workshop` (without `.html`). Paste its contents.
2. Paste the updated `Code.gs` over the old one. Its `DIAGNOSTICS` list now has a line for the new expedition.
3. Paste the updated `Passport.html` and `Educator.html` if Claude has changed them. Their top bars list every expedition automatically.
4. Save, then **Deploy ▸ Manage deployments ▸** the pencil icon **▸ Version: New version ▸ Deploy**.

The new expedition opens at the same web address with its own ending, for example `?page=workshop`.

## What is saved

Only the date, the learner's NEO email, and for each room: how the lock looked to the learner, the outcome, what a common mistake might suggest, and the suggested Reconnection Route. A comment is saved only when the learner presses **Share this with my supporting adult**. No timings, attempt counts, clicks or field-kit use. Learners can only ever see their own record; staff see everyone's.
