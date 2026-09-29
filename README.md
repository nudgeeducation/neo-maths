# NEO Maths · GreenPrint

**Repository:** nudgeeducation/neo-maths (transferred from TheNovacene/maths, 29 September 2026)

The working curriculum vault and public site for **NEO Maths** — the mathematics curriculum of Nudge Education Online, operated by Nudge Education Ltd.

**Live site:** https://nudgeeducation.github.io/neo-maths/

This is v2 of the NEO Maths repository. Where [neo-maths](https://github.com/TheNovacene/neo-maths) (v1) collected the open lesson library, this repository holds the **GreenPrint** curriculum build: the design records, curriculum maps, production lessons and QA materials — plus the public site that serves each lesson as an interactive webpage, connected to the Six Cornerstones and ready for progress tracking.

## Structure

```
vault/      The curriculum vault, mirrored from the working Drive folder.
            Source of truth for all curriculum materials: GreenPrint design
            records, curriculum maps, lesson packages, guidance PDFs, QA.

docs/       The GitHub Pages site.
  index.html            Curriculum home — units and lesson cards
  cornerstones.html     The Six Cornerstones in mathematics
  lessons/              Interactive lesson pages (built from vault/)
  assets/progress.js    Progress module (local-first, backend-swappable)
  data/curriculum.json  The site's index of units and lessons

scripts/
  build_site.py         Sync vault/ → docs/lessons/ and refresh the index
```

## Updating the site

1. Update or add materials in `vault/` (mirror of the Drive folder).
2. If a lesson has a new version, point `scripts/build_site.py` at the new filename in `SOURCES`.
3. Run `python3 scripts/build_site.py` from the repo root.
4. Commit and push (or commit + push in GitHub Desktop). Pages redeploys automatically.

## Local preview

To preview the built site before pushing, serve `docs/` **from the repo root** — no need to `cd` into it:

```
python3 -m http.server 8000 --directory docs
```

Then open http://localhost:8000. The `--directory` flag (Python 3.7+) keeps you in the repo root, so the same working directory runs both the build and the server.

A two-tab workflow keeps this frictionless: leave the server running in one terminal tab (it serves files live — no restart needed after a rebuild) and use a second tab for `python3 scripts/build_site.py`, then hard-refresh the browser (Cmd+Shift+R) to see the change.

### Preview the *built* lesson, not the raw source file

Several site-wide features are added to every lesson **at build time** by `scripts/build_site.py`, not stored in the lesson source: the shared header/footer, the **Comfort & Access** control, the maths **symbol palette**, the **single-open accordion**, the standard **Practice Companion** card, and the UTF-8 charset. So if you open a lesson file directly from `vault/` (or double-click a `docs/lessons/...` file), those features will appear to be missing — that is expected.

Always review a lesson via the **built** page on `http://localhost:8000` after running `python3 scripts/build_site.py`. Two things are written into each lesson's own source and *do* show even in the raw file: the six Cornerstone panels with their interactives, the Reconnection Routes control, and the worked-solution unlock gate.

## Progress tracking

Every lesson page loads `assets/progress.js` (injected at build time). Today it records opened/completed state in the learner's own browser only — no accounts, no data leaves the device. The module has a single narrow interface (`NEOProgress`), so real-time progress tracking can be added later by implementing a remote backend and calling `NEOProgress.setBackend(...)` — no lesson needs to change.

## Publishing (GitHub Pages)

Repo Settings → Pages → Source: **Deploy from a branch** → Branch: `main`, folder `/docs`.

Note: on standard GitHub plans, a Pages site is publicly viewable even when the repository is private.


## Curriculum rationale

The full statement of curriculum intent, implementation and impact is in
[curriculum-intent-implementation-impact-v0.1.md](curriculum-intent-implementation-impact-v0.1.md)
(carried forward from [neo-maths v1](https://github.com/TheNovacene/neo-maths)).

## Working in this repo with AI

`skills/verse-ality-cowork-starter/` contains the
[Verse-ality Cowork starter skill](https://github.com/TheNovacene/verse-ality-cowork-starter) —
a relational operating protocol for AI agents collaborating in this repository
(identity non-capture, bounded autonomy, consent as protocol, agent-to-agent hygiene).

## Licences

Code and tooling are under the [MIT Licence](LICENSE). Curriculum content —
lessons, guidance, media, the vault — is © Nudge Education Ltd and co-authors under
**CC BY-NC-ND 4.0**; see [CONTENT_LICENSE.md](CONTENT_LICENSE.md).

---


Nudge Education Online · [nudgeeducation.online](https://nudgeeducation.online) · neo@nudgeeducation.online

## Google Classroom sync

`scripts/classroom/classroom_sync.gs` mirrors `docs/data/curriculum.json` into a
Google Classroom course — one Topic per unit, one Material per lesson, each a
link to the lesson page on this site. Git stays canonical; Classroom is derived.
Re-run after any curriculum change; it is idempotent. Setup and the target
course id are at the top of the script. It creates topics and materials only —
no learner data is read or written.
