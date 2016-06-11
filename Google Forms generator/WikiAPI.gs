function getSummaryFromArticleID(pageId) {
  var url = "https://simple.wikipedia.org/w/api.php?format=xml&action=query&prop=extracts&exintro=&explaintext=&pageids="+pageId;
  var xml = UrlFetchApp.fetch(url).getContentText();
  var document = XmlService.parse(xml);
  var root = document.getRootElement();
  var extract = root.getChild("query").getChild("pages").getChild("page").getChildText("extract");
  Logger.log(extract);
  return extract;
}

function getSummaryFromArticleIdLng(lng,pageId) {
  var url = "https://"+lng+".wikipedia.org/w/api.php?format=xml&action=query&prop=extracts&exintro=&explaintext=&pageids="+pageId;
  var xml = UrlFetchApp.fetch(url).getContentText();
  var document = XmlService.parse(xml);
  var root = document.getRootElement();
  var extract = root.getChild("query").getChild("pages").getChild("page").getChildText("extract");
  Logger.log(extract);
  return extract;
}

function getSummary() {
  getSummaryFromArticleID(136443);
}