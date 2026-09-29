/**
 * NEO Maths → Google Classroom sync (Apps Script)
 *
 * Reads docs/data/curriculum.json from the neo-maths repo and mirrors it into
 * one Google Classroom course: one Topic per unit, one Material per lesson,
 * each Material a link to the lesson page on the published site.
 *
 * Git is canonical; Classroom is derived. Re-run after any curriculum change —
 * the script is idempotent (lessons are matched on the marker `neo-maths:<lesson id>`
 * in each Material's description).
 *
 * Setup (once):
 *   1. script.google.com, signed in as a nudgeeducation.online account that is a
 *      teacher on the target course (or a domain admin).
 *   2. New project → paste this file → Services (+) → add "Google Classroom API".
 *   3. Set COURSE_ID below (the number in the Classroom URL, decoded from the
 *      /c/<base64> segment) and run syncClassroom(). Approve the scopes on first run.
 *
 * Nothing here touches learner data: it creates topics and materials only.
 */

const CONFIG = {
  MANIFEST_URL: 'https://raw.githubusercontent.com/nudgeeducation/neo-maths/main/docs/data/curriculum.json',
  SITE_BASE: 'https://nudgeeducation.github.io/neo-maths/',
  COURSE_ID: '869529966246',
  MARKER: 'neo-maths:',            // description marker used for idempotent matching
  ONLY_LIVE: true,                  // skip lessons whose status is not "live"
};

function syncClassroom() {
  const manifest = JSON.parse(UrlFetchApp.fetch(CONFIG.MANIFEST_URL).getContentText());
  const courseId = CONFIG.COURSE_ID;
  const topics = topicsByName_(courseId);
  const existing = materialsByMarker_(courseId);
  const log = { topicsCreated: 0, created: 0, updated: 0, unchanged: 0 };

  // Classroom lists newest-first within a topic, so walk units and lessons in
  // reverse: Lesson 01 ends up at the top of its topic.
  const units = manifest.units.slice().reverse();
  units.forEach(function (unit) {
    const topicName = unit.title;
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
      const title = lesson.num + ' · ' + lesson.title;
      const url = CONFIG.SITE_BASE + lesson.file;
      const description = [
        unit.title + ' · ' + unit.stage + (unit.strand ? ' · ' + unit.strand : ''),
        'Interactive lesson page on the NEO Maths site.',
        marker,
      ].join('\n');

      const found = existing[marker];
      if (found) {
        const sameLink = found.materials && found.materials[0] && found.materials[0].link &&
                         found.materials[0].link.url === url;
        if (found.title === title && found.topicId === topic.topicId && sameLink && found.description === description) {
          log.unchanged++;
          return;
        }
        if (!sameLink) {
          // materials are not patchable — replace the post
          Classroom.Courses.CourseWorkMaterials.remove(courseId, found.id);
          Classroom.Courses.CourseWorkMaterials.create(material_(title, description, url, topic.topicId), courseId);
        } else {
          Classroom.Courses.CourseWorkMaterials.patch(
            { title: title, description: description, topicId: topic.topicId },
            courseId, found.id, { updateMask: 'title,description,topicId' });
        }
        log.updated++;
      } else {
        Classroom.Courses.CourseWorkMaterials.create(material_(title, description, url, topic.topicId), courseId);
        log.created++;
      }
    });
  });

  Logger.log(JSON.stringify(log));
  return log;
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

/** Dry run: lists what syncClassroom() would create, without writing. */
function previewSync() {
  const manifest = JSON.parse(UrlFetchApp.fetch(CONFIG.MANIFEST_URL).getContentText());
  manifest.units.forEach(function (u) {
    Logger.log('TOPIC ' + u.title + ' (' + u.lessons.length + ' lessons)');
    u.lessons.forEach(function (l) { Logger.log('   ' + l.num + ' · ' + l.title + ' → ' + CONFIG.SITE_BASE + l.file); });
  });
}
