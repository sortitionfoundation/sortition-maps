var url = "https://sheets.googleapis.com/v4/spreadsheets/1kwgOpxMX4pwR3Myu4pXku4gjcnOS53bPOKwOGjZNxyI/values/OECD!A2:BL?majorDimension=ROWS&valueRenderOption=FORMULA"
// N.B. API_KEY will be loaded from api-key.js if you run test.html.
url = url.concat("&key=").concat(API_KEY);

// Properties of the locations objects, and the numerical indices of the columns
// in which they appear in the OECD database.
var colDict = {"title": 0, "year": 12, "city": 16, "country": 13, "desc": 7,
              "link": 11, "lat": 62, "lng": 63}

// Fetch spreadsheet data as JSON.
var p = new XMLHttpRequest();
p.open("GET",url,false);
p.send(null);
// document.write(p.responseText);
var data = JSON.parse(p.responseText);

// Iterate over spreadsheet rows, populating the locations objects.
var locations2 = []
var prevRow = 0;
var newEntry = new Object();
for (i = 0; i < data.values.length; i++) {
  for (var colName in colDict) {
    switch (colName) {
      case "lat":
      case "lng":
      case "year":
        // Parse numerical fields
        newEntry[colName] = parseFloat(data.values[i][colDict[colName]]);
        break;
      default:
        newEntry[colName] = data.values[i][colDict[colName]];
    }
  }
  // Combine city and country to a single 'place' property.
  newEntry.loc = newEntry.city.concat(", ",newEntry.country);

  locations2.push(Object.assign({}, newEntry));
}

function rgbToHex(r, g, b) {
  return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

function yearToColour(year) {
  var age = Math.abs(new Date() - new Date(year,1));
  var maxAge = 1.6e12;
  var r = Math.max(0, Math.min(255, Math.ceil(255*age/maxAge)));
  var g = Math.max(0, Math.min(255, Math.floor(255*(maxAge-age)/maxAge)));
  document.write("year: " + year + ", maxAge: " + maxAge + ", age: " + age);
  return rgbToHex(r, g, 0);
}

// Test output
var content;
for (i = 0; i < locations2.length; i++) {
  document.write("<h3 style='color:" + yearToColour(locations2[i].year) + "';>" + locations2[i].year + "</h3>");
  if (isNaN(locations2[i].lat)) {continue;}
  content = "<h3>" + locations2[i].title + "</h3>" + "<b>" + locations2[i].year + ", " + locations2[i].loc + ".</b> " +
      locations2[i].desc;
  if (locations2[i].link) {
    content = content + " Read more: <a href=" + locations2[i].link + "><b>" + locations2[i].link + "</b></a>";
  }
  content = content + " Lat: "+locations2[i].lat;
  document.write(content);
}
