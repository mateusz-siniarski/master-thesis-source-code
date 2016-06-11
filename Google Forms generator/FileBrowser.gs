function logAllFiles() {
  // Log the name of every file in the user's Drive.
  var files = DriveApp.getFiles();
  
  while (files.hasNext()) {
    var file = files.next()
    //Logger.log(file.getName());
    parents = file.getParents()
    while(parents.hasNext()) {
      Logger.log(parents.next()) 
    }
  }
}

function getFolderIdByName(name) {
  Logger.log("getFolderIdByName")
  var folders = DriveApp.getFolders();
  while (folders.hasNext()) {
    var folder = folders.next();
    if (folder.getName() == name) {
      print = folder.getName() + " " + folder.getId()
      Logger.log(print);
      return folder.getId()
    }
  }
}


function getChildFolderIdByParentAndChildFolderName(parentName,childName) {
  Logger.log("getChildFolderIdByParentAndChildFolderName")
  var folders = DriveApp.getFolders();
  while (folders.hasNext()) {
    var parentFolder = folders.next();
    if (parentFolder.getName() == parentName) {
      childFolders = parentFolder.getFolders();
      while (childFolders.hasNext()) {
        var childFolder = childFolders.next();
        if (childFolder.getName() == childName) {
          print = parentFolder.getName() + "-" +parentFolder.getId()+" "+childFolder.getName() + "-" + childFolder.getId()
          Logger.log(print);
          return childFolder.getId()
        }
      }
    }
  }
}

function getChildrenFolderIdByParentAndChildFolderName(parentName,childName) {
  Logger.log("getChildFolderIdByParentAndChildFolderName")
  var folders = DriveApp.getFolders();
  while (folders.hasNext()) {
    var parentFolder = folders.next();
    if (parentFolder.getName() == parentName) {
      childFolders = parentFolder.getFolders();
      files = [];
      while (childFolders.hasNext()) {
        var childFolder = childFolders.next();
        if (childFolder.getName() == childName) {
          childFolderFiles = childFolder.getFiles()
          while(childFolderFiles.hasNext()) {
             childFolderFile = childFolderFiles.next()
             print = childFolderFile.getName() + " " + childFolderFile.getId()
             Logger.log(print);
             files.push(childFolderFile.getId());
          }
          
        }
      }
      return files;
    }
  }
}

function getChildFoldersFromParentFolderName(parentName) {
  Logger.log("getChildFoldersFromParentFolderName "+parentName)
  var folders = DriveApp.getFolders();
  while (folders.hasNext()) {
    var parentFolder = folders.next();
    if (parentFolder.getName() == parentName) {
      childFolders = parentFolder.getFolders();
      folders = [];
      while(childFolders.hasNext()) {
             childFolder = childFolders.next();
             print = childFolder.getName() + " " + childFolder.getId()
             Logger.log(print);
             folders.push(childFolder.getId());
      }
      return folders;
    }
  }
}

function getChildFoldersFromParentFolderId(parentId) {
  Logger.log("getChildFoldersFromParentFolderId "+parentId)
  var folders = DriveApp.getFolders();
  while (folders.hasNext()) {
    var parentFolder = folders.next();
    if (parentFolder.getId() == parentId) {
      childFolders = parentFolder.getFolders();
      folders = [];
      while(childFolders.hasNext()) {
             childFolder = childFolders.next();
             print = childFolder.getName() + " " + childFolder.getId()
             Logger.log(print);
             folders.push(childFolder.getId());
      }
      return folders;
    }
  }
}


function moveFiles(source_folder, dest_folder) {
   
  var files = source_folder.getFiles();
 
  while (files.hasNext()) {
 
    var file = files.next();
    dest_folder.addFile(file);
    source_folder.removeFile(file);
 
  }
}

function moveFile(fileId, destFolderName) {
  var file = DriveApp.getFileById(fileId); 
  var folder = file.getParents().next();
  var destFolder = DriveApp.getFolderById(getFolderIdByName(destFolderName));
  
 
  destFolder.addFile(file);
  folder.removeFile(file);
  
}
  
 
function testMoveFiles2() {
  fileId = "0B-yNp8HMNLYVZjV1VnYxdEJ6WFU";
  moveFiles2(fileId);
}
    