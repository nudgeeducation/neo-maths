/**
 * NEO Maths results service (Google Apps Script web app)
 *
 * Serves the diagnostic expeditions, the learner passport and the educator dashboard
 * from inside NEO's Google Workspace, and saves diagnostic results to one spreadsheet
 * in the shared "Diagnostic Assessments" folder on the NEO Drive.
 *
 * Who is who: the web app is deployed "Execute as: Me" and "Who has access: anyone
 * within nudgeeducation.online", so every visitor is signed in with their NEO account
 * and Session.getActiveUser() gives their email. Educators are the email addresses
 * listed on the spreadsheet's "Staff" tab (and, optionally, members of STAFF_GROUP).
 *
 * What is saved (and nothing else): the date, the learner's NEO email, and for each room
 * of a diagnostic: how the lock looked to the learner, the outcome, what a common mistake
 * might suggest, and the suggested Reconnection Route. An optional comment is saved only
 * when the learner chooses to share it. No timings, attempt counts, clicks or field-kit use.
 *
 * Install: see INSTALL.md in this folder. Keep the installed copy identical to this file.
 */

const CONFIG = {
  FOLDER_ID: '1vVzl3xDrs3e2J9f-WTXgY38ifrv8T9Ko',   // NEO Drive · Diagnostic Assessments
  SHEET_NAME: 'NEO Maths Results',
  DOMAIN: 'nudgeeducation.online',
  STAFF_GROUP: '',                                     // optional, e.g. 'maths-staff@nudgeeducation.online'
  // One entry per diagnostic expedition: ?page=<key> opens it. Add a line here for each new unit.
  DIAGNOSTICS: {
    'observatory': { file: 'Observatory', title: 'The Observatory · Number Systems', short: 'The Observatory' },
    'garden': { file: 'WalledGarden', title: 'The Walled Garden · Inequalities', short: 'The Walled Garden' },
    'workshop': { file: 'Workshop', title: 'The Inventor\u2019s Workshop · Formulae and Rearranging', short: 'The Inventor\u2019s Workshop' },
    'lighthouse': { file: 'Lighthouse', title: 'The Lighthouse · Algebraic Expressions', short: 'The Lighthouse' }
  }
};

const TABS = {
  Diagnostics: ['Saved', 'Learner', 'Unit', 'Unit ID', 'Expedition', 'Room', 'Lesson', 'How the lock looked', 'Outcome', 'What it might suggest', 'Suggested route'],
  Comments: ['Saved', 'Learner', 'Unit', 'Unit ID', 'Expedition', 'Comment'],
  Staff: ['Email (educators who may see the educator dashboard)']
};

/* ---------------- Setup (run once from the editor) ---------------- */

function setup() {
  const ss = spreadsheet_();
  Object.keys(TABS).forEach(name => {
    let sh = ss.getSheetByName(name);
    if (!sh) sh = ss.insertSheet(name);
    if (sh.getLastRow() === 0) {
      sh.appendRow(TABS[name]);
      sh.setFrozenRows(1);
      sh.getRange(1, 1, 1, TABS[name].length).setFontWeight('bold');
    }
  });
  const blank = ss.getSheetByName('Sheet1');
  if (blank && ss.getSheets().length > 1) ss.deleteSheet(blank);
  const me = Session.getActiveUser().getEmail();
  const staff = ss.getSheetByName('Staff');
  if (me && staff.getLastRow() === 1) staff.appendRow([me]);
  Logger.log('Results spreadsheet ready: ' + ss.getUrl());
}

function spreadsheet_() {
  const props = PropertiesService.getScriptProperties();
  const id = props.getProperty('SHEET_ID');
  if (id) {
    try { return SpreadsheetApp.openById(id); } catch (e) { /* recreated below */ }
  }
  const folder = DriveApp.getFolderById(CONFIG.FOLDER_ID);
  const found = folder.getFilesByName(CONFIG.SHEET_NAME);
  const ss = found.hasNext() ? SpreadsheetApp.open(found.next()) : SpreadsheetApp.create(CONFIG.SHEET_NAME);
  if (!found.hasNext()) DriveApp.getFileById(ss.getId()).moveTo(folder);
  props.setProperty('SHEET_ID', ss.getId());
  return ss;
}

/* ---------------- Pages ---------------- */

function doGet(e) {
  const page = (e && e.parameter && e.parameter.page) || 'home';
  const email = me_();
  if (!email) return message_('Please sign in with your NEO Google account (@' + CONFIG.DOMAIN + ') to continue.');
  const url = ScriptApp.getService().getUrl();
  let name;
  if (CONFIG.DIAGNOSTICS[page]) name = CONFIG.DIAGNOSTICS[page].file;
  else if (page === 'passport') name = 'Passport';
  else if (page === 'educator') {
    if (!isStaff_(email)) return message_('The educator dashboard is for NEO maths staff. Your own learner passport is here: <a href="' + url + '?page=passport" target="_top">open my passport</a>.');
    name = 'Educator';
  } else name = 'Passport';
  const t = HtmlService.createTemplateFromFile(name);
  t.appUrl = url;
  t.isStaff = isStaff_(email);
  t.expeditions = Object.keys(CONFIG.DIAGNOSTICS).map(k => ({ page: k, name: CONFIG.DIAGNOSTICS[k].short }));
  return t.evaluate()
    .setTitle(CONFIG.DIAGNOSTICS[page] ? CONFIG.DIAGNOSTICS[page].title : name === 'Educator' ? 'NEO Maths · Educator dashboard' : 'NEO Maths · My learner passport')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function message_(html) {
  return HtmlService.createHtmlOutput('<div style="font-family:Arial,sans-serif;max-width:640px;margin:40px auto;padding:24px;background:#f7f3ea;border-radius:16px;color:#2f3429;line-height:1.6">' + html + '</div>').setTitle('NEO Maths');
}

/* ---------------- Identity ---------------- */

function me_() {
  const email = (Session.getActiveUser().getEmail() || '').toLowerCase();
  return email.endsWith('@' + CONFIG.DOMAIN) ? email : '';
}

function isStaff_(email) {
  if (!email) return false;
  const rows = spreadsheet_().getSheetByName('Staff').getDataRange().getValues().slice(1);
  if (rows.some(r => String(r[0]).trim().toLowerCase() === email)) return true;
  if (CONFIG.STAFF_GROUP) {
    try { return GroupsApp.getGroupByEmail(CONFIG.STAFF_GROUP).hasUser(email); } catch (e) { return false; }
  }
  return false;
}

/* ---------------- Saving (called from the expedition page) ---------------- */

/** payload = {unit, unitId, expedition, rooms:[{room, lesson, felt, outcome, suggests, route}]} */
function saveDiagnostic(payload) {
  const email = me_();
  if (!email) throw new Error('Not signed in with a NEO account.');
  const lock = LockService.getScriptLock(); lock.waitLock(20000);
  try {
    const sh = spreadsheet_().getSheetByName('Diagnostics');
    const done = sh.getLastRow() > 1 && sh.getRange(2, 5, sh.getLastRow() - 1, 1).getValues().some(r => r[0] === payload.expedition);
    if (done) return { saved: true, already: true };       // the same expedition is never saved twice
    const now = new Date();
    const rows = (payload.rooms || []).map(r => [now, email, clip_(payload.unit), clip_(payload.unitId), clip_(payload.expedition),
      clip_(r.room), clip_(r.lesson), clip_(r.felt), clip_(r.outcome), clip_(r.suggests), clip_(r.route)]);
    if (rows.length) sh.getRange(sh.getLastRow() + 1, 1, rows.length, rows[0].length).setValues(rows);
    return { saved: true, rooms: rows.length };
  } finally { lock.releaseLock(); }
}

/** Saved only when the learner presses "Share this with my supporting adult". */
function saveComment(payload) {
  const email = me_();
  if (!email) throw new Error('Not signed in with a NEO account.');
  const text = clip_(payload.comment, 1000);
  if (!text) return { saved: false };
  spreadsheet_().getSheetByName('Comments').appendRow([new Date(), email, clip_(payload.unit), clip_(payload.unitId), clip_(payload.expedition), text]);
  return { saved: true };
}

function clip_(v, n) { return String(v == null ? '' : v).slice(0, n || 300); }

/* ---------------- Reading (learner passport, educator dashboard) ---------------- */

function rows_() {
  const v = spreadsheet_().getSheetByName('Diagnostics').getDataRange().getValues();
  return v.slice(1).map(r => ({ saved: r[0] instanceof Date ? r[0].toISOString() : String(r[0]), learner: r[1], unit: r[2], unitId: r[3], expedition: r[4],
    room: r[5], lesson: r[6], felt: r[7], outcome: r[8], suggests: r[9], route: r[10] }));
}

function comments_() {
  const v = spreadsheet_().getSheetByName('Comments').getDataRange().getValues();
  return v.slice(1).map(r => ({ saved: r[0] instanceof Date ? r[0].toISOString() : String(r[0]), learner: r[1], unit: r[2], unitId: r[3], expedition: r[4], comment: r[5] }));
}

/** The signed-in learner's own record, newest expedition per unit first. Learners only ever get their own rows. */
function getMyPassport() {
  const email = me_();
  if (!email) throw new Error('Not signed in with a NEO account.');
  return { learner: email, rows: rows_().filter(r => String(r.learner).toLowerCase() === email),
           comments: comments_().filter(c => String(c.learner).toLowerCase() === email) };
}

/** Every learner's rows, for NEO maths staff only. */
function getEducatorData() {
  const email = me_();
  if (!isStaff_(email)) throw new Error('The educator dashboard is for NEO maths staff.');
  return { educator: email, rows: rows_(), comments: comments_() };
}

/** For an educator opening one learner's passport from the dashboard. */
function getLearnerPassport(learner) {
  const email = me_();
  if (!isStaff_(email)) throw new Error('Only NEO maths staff can open another learner’s passport.');
  const who = String(learner).toLowerCase();
  return { learner: who, rows: rows_().filter(r => String(r.learner).toLowerCase() === who),
           comments: comments_().filter(c => String(c.learner).toLowerCase() === who) };
}
