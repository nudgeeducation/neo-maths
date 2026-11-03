/**
 * NEO Maths → Google Classroom sync (Apps Script)
 *
 * Reads docs/data/curriculum.json from the neo-maths repo and mirrors it into
 * the Google Classroom master courses, one per stage: one Topic per unit, one
 * Material per lesson, each Material a link to the lesson page on the published site.
 * A unit with a `diagnostic` ({id, title}) also gets a "Start here" Material at the
 * top of its topic, linking to that diagnostic expedition on the NEO Maths results
 * service (GreenPrint v2.4: one diagnostic per unit, taken before Lesson 01).
 *
 * Git is canonical; Classroom is derived. Re-run after any curriculum change —
 * the script is idempotent (lessons are matched on the marker `neo-maths:<lesson id>`
 * in each Material's description).
 *
 * Setup (once):
 *   1. script.google.com, signed in as a nudgeeducation.online account that is a
 *      teacher on the target course (or a domain admin).
 *   2. New project → paste this file → Services (+) → add "Google Classroom API".
 *   3. Set TARGETS below (course id = the number in the Classroom URL, decoded from
 *      the /c/<base64> segment) and run syncClassroom(). Approve the scopes on first run.
 *   The installed copy lives in the NEO Apps Script project "NEO Maths Classroom sync"
 *   (kirstin.stevens@nudgeeducation.online); keep it identical to this file.
 *
 * Nothing here touches learner data: it creates topics and materials only.
 */

const CONFIG = {
  MANIFEST_URL: 'https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/docs/data/curriculum.json',
  SITE_BASE: 'https://nudgeeducation.github.io/neo-maths/',
  // The NEO Maths results service (Apps Script web app). A diagnostic opens at RESULTS_URL?page=<id>.
  RESULTS_URL: 'https://script.google.com/a/macros/nudgeeducation.online/s/AKfycbzZ4_uhLDHULyz8DDRtxjGh9DX0e3ETZqE_i08mv00jUfz2OtowM2giqSnWqx3FiyU/exec',
  // One entry per Classroom. `stages` lists the manifest stage labels that
  // belong in that course; units with any other stage are removed from it.
  TARGETS: [
    { name: 'Mathematics | Foundation | Master',   courseId: '878455913553', stages: ['Foundations', 'Key Stage 3'] },
    { name: 'Mathematics | Intermediate | Master', courseId: '869529966246', stages: ['Intermediate'] },
  ],
  MARKER: 'neo-maths:',            // description marker used for idempotent matching
  ONLY_LIVE: true,                  // skip lessons whose status is not "live"
};

function syncClassroom() {
  const manifest = JSON.parse(UrlFetchApp.fetch(CONFIG.MANIFEST_URL).getContentText());
  const results = {};
  CONFIG.TARGETS.forEach(function (target) {
    results[target.name] = syncCourse_(manifest, target);
  });
  Logger.log(JSON.stringify(results, null, 1));
  return results;
}

function syncCourse_(manifest, target) {
  const courseId = target.courseId;
  const topics = topicsByName_(courseId);
  const existing = materialsByMarker_(courseId);
  const log = { topicsCreated: 0, created: 0, updated: 0, unchanged: 0, removed: 0, topicsRemoved: 0 };
  const wanted = {};   // marker → true, for everything that belongs in this course
  const wantedTopics = {};

  // Classroom lists newest-first within a topic, so walk units and lessons in
  // reverse: Lesson 01 ends up at the top of its topic.
  const units = manifest.units.filter(function (u) { return target.stages.indexOf(u.stage) !== -1; }).reverse();
  units.forEach(function (unit) {
    const topicName = unit.title;
    wantedTopics[topicName] = true;
    let topic = topics[topicName];
    if (!topic) {
      topic = Classroom.Courses.Topics.create({ name: topicName }, courseId);
      topics[topicName] = topic;
      log.topicsCreated++;
    }

    const lessons = unit.lessons.slice().reverse();
    lessons.forEach(function (lesson) {
      if (CONFIG.ONLY_LIVE && lesson.status !== 'live') return;
      const marker = CONFIG.MARKER + lesson.id;
      wanted[marker] = true;
      const title = lesson.num + ' · ' + lesson.title;
      const url = CONFIG.SITE_BASE + lesson.file;
      const description = [
        unit.title + ' · ' + unit.stage + (unit.strand ? ' · ' + unit.strand : ''),
        'Interactive lesson page on the NEO Maths site.',
        marker,
      ].join('\n');

      upsert_(courseId, existing, log, marker, title, description, url, topic.topicId);
    });

    // The diagnostic goes in last, so it sits above Lesson 01 (newest first).
    if (unit.diagnostic) {
      const marker = CONFIG.MARKER + 'diagnostic-' + unit.id;
      wanted[marker] = true;
      upsert_(courseId, existing, log, marker, startTitle_(unit), startDescription_(unit, marker), diagnosticUrl_(unit), topic.topicId);
    }
  });

  // Remove materials this script created that no longer belong in this course
  // (unit moved to another stage, lesson retired). Only marker-bearing posts are
  // ever touched — anything an educator posted by hand is left alone.
  Object.keys(existing).forEach(function (marker) {
    if (!wanted[marker]) {
      Classroom.Courses.CourseWorkMaterials.remove(courseId, existing[marker].id);
      log.removed++;
    }
  });

  // Remove topics named after manifest units that are not wanted here and are now empty.
  const unitTitles = {};
  manifest.units.forEach(function (u) { unitTitles[u.title] = true; });
  const remaining = materialsByMarker_(courseId);
  const topicsInUse = {};
  Object.keys(remaining).forEach(function (m) { topicsInUse[remaining[m].topicId] = true; });
  Object.keys(topics).forEach(function (name) {
    const t = topics[name];
    if (unitTitles[name] && !wantedTopics[name] && !topicsInUse[t.topicId]) {
      Classroom.Courses.Topics.remove(courseId, t.topicId);
      log.topicsRemoved++;
    }
  });

  return log;
}

// Create the post, or bring an existing one (found by its marker) up to date.
function upsert_(courseId, existing, log, marker, title, description, url, topicId) {
  const found = existing[marker];
  if (found) {
    const sameLink = found.materials && found.materials[0] && found.materials[0].link &&
                     found.materials[0].link.url === url;
    if (found.title === title && found.topicId === topicId && sameLink && found.description === description) {
      log.unchanged++;
      return;
    }
    if (!sameLink) {
      // materials are not patchable — replace the post
      Classroom.Courses.CourseWorkMaterials.remove(courseId, found.id);
      Classroom.Courses.CourseWorkMaterials.create(material_(title, description, url, topicId), courseId);
    } else {
      Classroom.Courses.CourseWorkMaterials.patch(
        { title: title, description: description, topicId: topicId },
        courseId, found.id, { updateMask: 'title,description,topicId' });
    }
    log.updated++;
  } else {
    Classroom.Courses.CourseWorkMaterials.create(material_(title, description, url, topicId), courseId);
    log.created++;
  }
}

function startTitle_(unit) { return 'Start here · ' + unit.diagnostic.title; }
function diagnosticUrl_(unit) { return CONFIG.RESULTS_URL + '?page=' + unit.diagnostic.id; }
function startDescription_(unit, marker) {
  return [
    'Begin ' + unit.title + ' here, before Lesson 01.',
    unit.diagnostic.title + ' is a short expedition with no scores. It suggests where to start in this unit and which Reconnection Routes may help. Sign in with your NEO account.',
    marker,
  ].join('\n');
}

function material_(title, description, url, topicId) {
  return {
    title: title,
    description: description,
    materials: [{ link: { url: url } }],
    topicId: topicId,
    state: 'PUBLISHED',
  };
}

function topicsByName_(courseId) {
  const out = {};
  let pageToken;
  do {
    const res = Classroom.Courses.Topics.list(courseId, { pageSize: 100, pageToken: pageToken });
    (res.topic || []).forEach(function (t) { out[t.name] = t; });
    pageToken = res.nextPageToken;
  } while (pageToken);
  return out;
}

function materialsByMarker_(courseId) {
  const out = {};
  let pageToken;
  do {
    const res = Classroom.Courses.CourseWorkMaterials.list(courseId, {
      pageSize: 100, pageToken: pageToken, courseWorkMaterialStates: ['PUBLISHED', 'DRAFT'] });
    (res.courseWorkMaterial || []).forEach(function (m) {
      const match = (m.description || '').match(/neo-maths:[A-Za-z0-9-]+/);
      if (match) out[match[0]] = m;
    });
    pageToken = res.nextPageToken;
  } while (pageToken);
  return out;
}

/** Dry run: lists what syncClassroom() would put in each course, without writing. */
function previewSync() {
  const manifest = JSON.parse(UrlFetchApp.fetch(CONFIG.MANIFEST_URL).getContentText());
  CONFIG.TARGETS.forEach(function (target) {
    Logger.log('COURSE ' + target.name + ' (' + target.courseId + ')');
    manifest.units.filter(function (u) { return target.stages.indexOf(u.stage) !== -1; }).forEach(function (u) {
      Logger.log('  TOPIC ' + u.title + ' · ' + u.stage + ' (' + u.lessons.length + ' lessons)');
      if (u.diagnostic) Logger.log('     ' + startTitle_(u) + ' → ' + diagnosticUrl_(u));
      u.lessons.forEach(function (l) { Logger.log('     ' + l.num + ' · ' + l.title + ' → ' + CONFIG.SITE_BASE + l.file); });
    });
  });
}
