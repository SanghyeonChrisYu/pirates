function calculateFontSize(textLayer, targetWidth, targetHeight) {
  var sourceText = textLayer.property("Source Text");
  var textValue = sourceText.value;

  // Temporarily set the font size to a large value to measure the text dimensions
  textValue.fontSize = 500;
  sourceText.setValue(textValue);

  var textSize = textLayer.sourceRectAtTime(0, false);
  var scaleX = targetWidth / textSize.width;
  var scaleY = targetHeight / textSize.height;

  // Calculate the new font size based on the scaling factors
  var newFontSize = textValue.fontSize * Math.min(scaleX, scaleY);
  textValue.fontSize = newFontSize;
  sourceText.setValue(textValue);
}

var file = new File("./output/list.txt");

var videoNameList = [];
var topTextList = [];
var bottomTextList = [];

if (file.open("r")) {

  file.readln(); // Skip the header line

  while (!file.eof) {
    var line = file.readln();
    var fields = line.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/).map(function(item) { return item.replace(/\\r/g, "\r"); });

    videoNameList.push(fields[0]);
    topTextList.push(fields[1]);
    bottomTextList.push(fields[2]);
  }

  file.close();
} else {
  alert("Error opening the file.");
}

for (var i = 0; i < videoNameList.length; i++) {
  var videoName = videoNameList[i];
  var topText = topTextList[i];
  var bottomText = bottomTextList[i];

  // Perform any operations you need with the current elements here
  var io = new ImportOptions(File("./output/" + videoName));
  var importedVideo = app.project.importFile(io);

  // Get the properties of the imported video
  var videoWidth = importedVideo.width;
  var videoHeight = importedVideo.height;
  var pixelAspectRatio = importedVideo.pixelAspect;
  var duration = importedVideo.duration;
  var frameRate = importedVideo.frameRate;

  // Calculate the dimensions for the 9:16 composition
  var compWidth = Math.min(videoWidth, videoHeight);
  var compHeight = Math.round( compWidth * (16 / 9));

  var comp = app.project.items.addComp("Comp_" + videoName, compWidth, compHeight, pixelAspectRatio, duration, frameRate);
  var videoLayer = comp.layers.add(importedVideo);

  // Calculate the scale and position for the 1:1 aspect ratio video
  var videoScale = 100;
  var videoPosition = [compWidth / 2, compHeight / 2];

  videoLayer.property("Transform").property("Scale").setValue([videoScale, videoScale]);
  videoLayer.property("Transform").property("Position").setValue(videoPosition);

  var textLayerHeight = ((compHeight * (1 - 0.31)) - videoHeight) / 2;
  var textLayerWidth = compWidth * 0.8;

  var topTextLayer = comp.layers.addText(topText);
  calculateFontSize(topTextLayer, textLayerWidth, textLayerHeight);

  // Set font size, bold, color, and stroke
  var topTextProp = topTextLayer.property("Source Text");
  var topTextValue = topTextProp.value;
  topTextValue.font = "Arial-BoldMT";
  topTextValue.fillColor = [1, 1, 1];
  topTextValue.strokeColor = [0, 0, 0];
  topTextValue.strokeWidth = 3;
  topTextValue.justification = ParagraphJustification.CENTER_JUSTIFY;
  topTextProp.setValue(topTextValue);
  // topTextLayer.property("Transform").property("Position").setValue([compWidth / 2, textLayerHeight / 2]);

  var bottomTextLayer = comp.layers.addText(bottomText);
  calculateFontSize(bottomTextLayer, textLayerWidth, textLayerHeight);

  // Set font size, bold, color, and stroke
  var bottomTextProp = bottomTextLayer.property("Source Text");
  var bottomTextValue = bottomTextProp.value;
  bottomTextValue.font = "Arial-BoldMT";
  bottomTextValue.fillColor = [1, 1, 1];
  bottomTextValue.strokeColor = [0, 0, 0];
  bottomTextValue.strokeWidth = 3;
  bottomTextValue.justification = ParagraphJustification.CENTER_JUSTIFY;
  bottomTextProp.setValue(bottomTextValue);
  // bottomTextLayer.property("Transform").property("Position").setValue([compWidth / 2, compHeight - (textLayerHeight / 2)]);

  var topTextLayerY = compHeight * 0.155 + textLayerHeight / 2;
var bottomTextLayerY = compHeight * (1 - 0.155) - textLayerHeight / 2;

topTextLayer.property("Transform").property("Position").setValue([compWidth / 2, topTextLayerY]);
bottomTextLayer.property("Transform").property("Position").setValue([compWidth / 2, bottomTextLayerY]);


}