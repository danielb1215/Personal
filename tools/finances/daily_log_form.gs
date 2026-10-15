/**
 * Creates the "Daily spend" Google Form and wires it to the Daily log tab of finances_unified.
 *
 * One-time setup:
 *   1. Go to script.google.com, New project, paste this file.
 *   2. Run createDailySpendForm and accept the permissions prompt.
 *   3. Open View > Logs (or Execution log) and copy the form URL.
 *   4. On your phone, open the URL and add it to the home screen.
 *
 * Each submission appends one row to 'Daily log' (columns A to E). Columns F and G
 * are formulas in the Sheet, so this script never writes to them.
 */

const SHEET_ID = '1YeZ1p34fgsvv1sDIuNFrausv0FE0lFLG86AVsfwrdd8';
const LOG_TAB = 'Daily log';
const DATE_TITLE = 'Date (leave empty for today)';

// Must match Budget!A13:A22 exactly.
const CATEGORIES = [
  'Food at home',
  'Restaurants & delivery',
  'Shopping',
  'Entertainment',
  'Transport & fuel',
  'Cycling & sport',
  'Payouts to people',
  'Travel & big purchases',
  'Fixed bills',
  'Other',
];

function createDailySpendForm() {
  const form = FormApp.create('Daily spend');
  form.setConfirmationMessage('Saved. The Budget tab shows what is left.');
  form.setShowLinkToRespondAgain(true);

  form.addTextItem()
    .setTitle('Amount')
    .setHelpText('Numbers only, as paid.')
    .setRequired(true)
    .setValidation(FormApp.createTextValidation().requireNumberGreaterThan(0).build());

  form.addListItem()
    .setTitle('Category')
    .setChoiceValues(CATEGORIES)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Currency')
    .setChoiceValues(['COP', 'USD', 'EUR'])
    .setRequired(true);

  form.addTextItem().setTitle('Note (optional)');

  form.addDateItem().setTitle(DATE_TITLE);

  ScriptApp.newTrigger('onFormSubmit').forForm(form).onFormSubmit().create();

  Logger.log('Form to fill: ' + form.getPublishedUrl());
  Logger.log('Form to edit: ' + form.getEditUrl());
}

function onFormSubmit(e) {
  const answers = {};
  e.response.getItemResponses().forEach(function (item) {
    answers[item.getItem().getTitle()] = item.getResponse();
  });

  const amount = parseFloat(String(answers['Amount']).replace(/,/g, ''));
  if (!isFinite(amount)) throw new Error('Amount is not a number: ' + answers['Amount']);

  let when = new Date();
  const picked = answers[DATE_TITLE];
  if (picked) {
    const p = String(picked).split('-');
    when = new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
  }
  when = new Date(when.getFullYear(), when.getMonth(), when.getDate());

  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(LOG_TAB);
  // First empty row in column A. getLastRow() would count the notes in column I.
  const used = sheet.getRange('A:A').getValues().filter(function (r) { return r[0] !== ''; }).length;
  sheet.getRange(used + 1, 1, 1, 5).setValues([[
    when,
    amount,
    answers['Currency'],
    answers['Category'],
    answers['Note (optional)'] || '',
  ]]);
}
