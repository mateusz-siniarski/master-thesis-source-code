function createFormFromSpreadsheet(fileid) {
  var fileid = "13Y50SPFzr1eqdRX0tFPrk5xUa5m4U3kyEwRJfamULDQ"
  var spreadsheet = SpreadsheetApp.openById(fileid);
  var lastRow = spreadsheet.getLastRow();
  var lastRowLimit = 10;
  var lastCol = spreadsheet.getLastColumn();
  var sheet = spreadsheet.getSheets()[0];
  var form = FormApp.create("relevant_docs_test_en");
  
  /*
  if(lastRow > lastRowLimit) {
    lastRow = lastRowLimit; 
  }
  */
  
  for(var row=1; row<=lastRow; row++) {
    var title = sheet.getRange(row,1).getValue();
    var url = sheet.getRange(row,3).getValue();
    var item = form.addMultipleChoiceItem();
    item.setTitle(title+" - "+url);
    item.setChoices([
        item.createChoice('Yes'),
        item.createChoice('Maybe'),
        item.createChoice('No')
    ]);
    Logger.log(title);
    
    if(row%lastRowLimit==0 && row != lastRow) {
      form.addPageBreakItem();
    }
    
  }
  
}

function createForm(modelFolderId,destFolderName) {
  //spreadsheet-simple-forms (0B-yNp8HMNLYVNHVEMmxTQ2NzRGs)
  var form = FormApp.create(DriveApp.getFolderById(modelFolderId).getName())
  form.setProgressBar(true)
  moveFile(form.getId(),destFolderName);
  return form;
  
}

function createMultiPageFormFromSpreadsheetFolderEn(modelFolderId) {
  var spreadsheets = DriveApp.getFolderById(modelFolderId).getFiles();
  var form = createForm(modelFolderId,"spreadsheet-en-forms-auto");
  

  
  
  form.setTitle(DriveApp.getFolderById(modelFolderId).getName())
  form.setDescription("Please evaluate if the following articles are related to the first one.")
  
  while(spreadsheets.hasNext()) {
    var ssFile = spreadsheets.next();
    var ss = SpreadsheetApp.openById(ssFile.getId());
    var sheet = ss.getSheets()[0];
    
    
    
    var title = sheet.getRange(1,1).getValue();
    var pageid = sheet.getRange(1,2).getValue();
    var url = sheet.getRange(1,3).getValue();
    
    
    var textItem = form.addSectionHeaderItem();
    textItem.setTitle(title+" - "+url);
    textItem.setHelpText(getSummaryFromArticleIdLng("en",pageid))
    
    var lastRow = ss.getLastRow();
    var lastRowLimit = 26;
    
    
    
  
    if(lastRow > lastRowLimit) {
      lastRow = lastRowLimit; 
    }
  
  
    for(var row=2; row<=lastRow; row++) {
      var title = sheet.getRange(row,1).getValue();
      var pageid = sheet.getRange(row,2).getValue();
      var url = sheet.getRange(row,3).getValue();
      var item = form.addMultipleChoiceItem();
      item.setTitle(title+" - "+url);
      item.setHelpText(getSummaryFromArticleIdLng("en",pageid))
      item.setChoices([
        item.createChoice('Yes'),
        item.createChoice('Maybe'),
        item.createChoice('No')
      ]);
    }
    
    if(spreadsheets.hasNext()) {
      form.addPageBreakItem();
    }
    
  }
  
  
}

function createMultiPageFormFromSpreadsheetFolder(modelFolderId) {
  var spreadsheets = DriveApp.getFolderById(modelFolderId).getFiles();
  var form = createForm(modelFolderId,"spreadsheet-simple-forms-auto");
  

  
  
  form.setTitle(DriveApp.getFolderById(modelFolderId).getName())
  form.setDescription("Please evaluate if the following articles are related to the first one.")
  
  while(spreadsheets.hasNext()) {
    var ssFile = spreadsheets.next();
    var ss = SpreadsheetApp.openById(ssFile.getId());
    var sheet = ss.getSheets()[0];
    
    
    
    var title = sheet.getRange(1,1).getValue();
    var pageid = sheet.getRange(1,2).getValue();
    var url = sheet.getRange(1,3).getValue();
    
    
    var textItem = form.addSectionHeaderItem();
    textItem.setTitle(title+" - "+url);
    textItem.setHelpText(getSummaryFromArticleID(pageid))
    
    var lastRow = ss.getLastRow();
    var lastRowLimit = 11;
    
    
    
  
    if(lastRow > lastRowLimit) {
      lastRow = lastRowLimit; 
    }
  
  
    for(var row=2; row<=lastRow; row++) {
      var title = sheet.getRange(row,1).getValue();
      var pageid = sheet.getRange(row,2).getValue();
      var url = sheet.getRange(row,3).getValue();
      var item = form.addMultipleChoiceItem();
      item.setTitle(title+" - "+url);
      item.setHelpText(getSummaryFromArticleID(pageid))
      item.setChoices([
        item.createChoice('Yes'),
        item.createChoice('Maybe'),
        item.createChoice('No')
      ]);
    }
    
    if(spreadsheets.hasNext()) {
      form.addPageBreakItem();
    }
    
  }
  
  
}

function createMultiPageFormFromSpreadsheetFolder2(modelFolderId) {
  var spreadsheets = DriveApp.getFolderById(modelFolderId).getFiles();
  var form = createForm(modelFolderId,"spreadsheets-simple-forms-auto");
  

  
  
  form.setTitle(DriveApp.getFolderById(modelFolderId).getName())
  form.setDescription("Please evaluate if the following articles are related to the first one.")
  
  while(spreadsheets.hasNext()) {
    var ssFile = spreadsheets.next();
    var ss = SpreadsheetApp.openById(ssFile.getId());
    var sheet = ss.getSheets()[0];
    
    
    var lastRow = ss.getLastRow();
    var lastCol = ss.getLastColumn();
    var lastRowLimit = 11;
    
    
    
  
    if(lastRow > lastRowLimit) {
      lastRow = lastRowLimit; 
    }
  
    
    
    
    var range = sheet.getRange(1,1,lastRow,lastCol);
    var values = range.getValues();
    
    var title = values[0][0];
    var pageid = values[0][1];
    var url = values[0][2];
    
    
    var textItem = form.addSectionHeaderItem();
    textItem.setTitle(title+" - "+url);
    textItem.setHelpText(getSummaryFromArticleID(pageid))
    
    
  
    for(var row=1; row<lastRow; row++) {
      var title = values[row][0];
      var pageid = values[row][1];
      var url = values[row][2];
      var item = form.addMultipleChoiceItem();
      item.setTitle(title+" - "+url);
      item.setHelpText(getSummaryFromArticleID(pageid))
      item.setChoices([
        item.createChoice('Yes'),
        item.createChoice('Maybe'),
        item.createChoice('No')
      ]);
    }
    
    if(spreadsheets.hasNext()) {
      form.addPageBreakItem();
    }
    
  }
  
  
}

function createMultiPageFormFromSpreadsheetFolderEn2(modelFolderId) {
  var spreadsheets = DriveApp.getFolderById(modelFolderId).getFiles();
  var form = createForm(modelFolderId,"relevant-docs");
  

  
  
  form.setTitle(DriveApp.getFolderById(modelFolderId).getName())
  form.setDescription("Please evaluate if the following articles are related to the first one.")
  
  while(spreadsheets.hasNext()) {
    var ssFile = spreadsheets.next();
    var ss = SpreadsheetApp.openById(ssFile.getId());
    var sheet = ss.getSheets()[0];
    
    
    var lastRow = ss.getLastRow();
    var lastCol = ss.getLastColumn();
    var lastRowLimit = 11;
    
    
    
  
    if(lastRow > lastRowLimit) {
      lastRow = lastRowLimit; 
    }
  
    
    
    
    var range = sheet.getRange(1,1,lastRow,lastCol);
    var values = range.getValues();
    
    var title = values[0][0];
    var pageid = values[0][1];
    var url = values[0][2];
    
    
    var textItem = form.addSectionHeaderItem();
    textItem.setTitle(title+" - "+url);
    textItem.setHelpText(getSummaryFromArticleIdLng('en',pageid))
    
    
  
    for(var row=1; row<lastRow; row++) {
      var title = values[row][0];
      var pageid = values[row][1];
      var url = values[row][2];
      var item = form.addMultipleChoiceItem();
      item.setTitle(title+" - "+url);
      item.setHelpText(getSummaryFromArticleIdLng('en',pageid))
      item.setChoices([
        item.createChoice('Yes'),
        item.createChoice('Maybe'),
        item.createChoice('No')
      ]);
    }
    
    if(spreadsheets.hasNext()) {
      form.addPageBreakItem();
    }
    
  }
  
  
}

function createMultiPageFormFromSpreadsheetEn(spreadsheetId,folder_name) {
  var form = FormApp.create("relevant-docs-normalized")
  form.setProgressBar(true)
  moveFile(form.getId(),folder_name);
  

  
  
  form.setTitle("Evaluation of relevant Wikipedia articles");
  form.setDescription("Dear participant,\n\nWe are building software to help scientist and researchers in marine science, oceanography and related disciplines to search in Wikipedia. As a part of this effort, we have now trained our system to recognize relevant Wikipedia pages (for example, about phytoplankton) and to disregard irrelevant pages (for example, about former US presidents). We now want to evaluate the performance of our system against that of human experts.\n\nBelow you will find a selection of 200 Wikipedia pages with a summary of their content. We ask you to indicate if the page is clearly relevant to marine science/oceanography (yes), possibly of interest (maybe) or definitely irrelevant (no). We are asking for snap judgements; this should not take you more than a couple of seconds per page on average.\n\nWe wish to collect answers from a multitude of users. It will be very helpful for further evaluations if you can fill out your personal information below.\n\nThank you very much for your help!")
  var name_item = form.addTextItem();
  name_item.setTitle('Name');
  
  var item = form.addMultipleChoiceItem();
      item.setTitle('Age');
      item.setChoices([
        item.createChoice('Under 18 years old'),
        item.createChoice('18-24 years old'),
        item.createChoice('25-34 years old'),
        item.createChoice('35-44 years old'),
        item.createChoice('45-54 years old'),
        item.createChoice('55-64 years old'),
        item.createChoice('65-74 years old'),
        item.createChoice('75 years or older')
      ]);
  
  
  
  
  
  
  var item = form.addMultipleChoiceItem();
      item.setTitle('Degree');
      item.setChoices([
        item.createChoice('High school degree'),
        item.createChoice('Bachelor’s degree'),
        item.createChoice('Master’s degree'),
        item.createChoice('Doctorate degree'),
        item.createChoice('Other')
      ]);
    
  var profession_item = form.addTextItem();
  profession_item.setTitle('Profession');







  
  
  
  form.addPageBreakItem();
  
  //while(spreadsheets.hasNext()) {
    //var ssFile = spreadsheets.next();
    var ss = SpreadsheetApp.openById(spreadsheetId);
    var sheet = ss.getSheets()[0];
    
    
    var lastRow = ss.getLastRow();
    var lastCol = ss.getLastColumn();
    var lastRowLimit = 9;
    
    var range = sheet.getRange(1,1,lastRow,lastCol);
    var values = range.getValues();
    
    
    
  
    for(var row=0; row<lastRow; row++) {
      var title = values[row][0];
      var pageid = values[row][1];
      var url = values[row][2];
      var item = form.addMultipleChoiceItem();
      item.setRequired(true)
      item.setTitle(title+" - "+url);
      item.setHelpText(getSummaryFromArticleIdLng('en',pageid))
      item.setChoices([
        item.createChoice('Yes'),
        item.createChoice('Maybe'),
        item.createChoice('No')
      ]);
      
      if(row == lastRowLimit && row != 0) {
        form.addPageBreakItem();
        lastRowLimit += 10;
      }
    }
    
    var item = form.addParagraphTextItem();
    item.setTitle('Thank you very much for your help!');
  item.setHelpText('Please feel free to add any comments in the field below:')
    
  //}
  
  
}


/*

Process finished with exit code 0
response spreadsheet ID 1vpMfw_Fo03SNWQ_19cES8J1cMBZkA3CsMUyo-vC8htk
*/


function runCreateMultiPageFormFromSpreadsheetFolder() {
  
  createMultiPageFormFromSpreadsheetEn("1vpMfw_Fo03SNWQ_19cES8J1cMBZkA3CsMUyo-vC8htk","relevant-docs");
  
}