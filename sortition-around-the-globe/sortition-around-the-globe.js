/**
 * Brett Hennig - map data and code (google map callback) for sortition around the world map
 * Modifications by David Western to pull data from Google Sheets.
 */

function initMap() {

        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 2,
          center: {lat: 23.451065, lng: 0.949395}
        });

        var infowindow = new google.maps.InfoWindow({
          maxWidth: 300
        });

        // Pull locations2 from spreadsheet:
        var url = "https://sheets.googleapis.com/v4/spreadsheets/1kwgOpxMX4pwR3Myu4pXku4gjcnOS53bPOKwOGjZNxyI/values/OECD!A2:BL?majorDimension=ROWS&valueRenderOption=FORMULA"
        var API_KEY = "INSERT KEY HERE. ASK DAVID OR SOMEONE ELSE WHO KNOWS."
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

        var markers2 = [];

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

       for (i = 0; i < locations2.length; i++) {
         if (isNaN(locations2[i].lat)) {continue;}
         var mylabel = locations2[i].year.toString().substring(2);
         var myicon = "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + mylabel + "|" + yearToColour(locations2[i].year);
         var mark = new google.maps.Marker({
           position: { lat: locations2[i].lat, lng: locations2[i].lng },
           title: locations2[i].title,
           icon: myicon
          });
         var content = "<h3>" + locations2[i].title + "</h3>" + "<b>" + locations2[i].year + ", " + locations2[i].loc + ".</b> " +
             locations2[i].desc;
         if (locations2[i].link) {
           content = content + " Read more: <a href=" + locations2[i].link + "><b>" + locations2[i].link + "</b></a>";
         }
         google.maps.event.addListener(mark,'click', (function(mark, content, infowindow){
                 return function() {
                 infowindow.setContent(content);
                 infowindow.open(map,mark);
                };
         })(mark,content,infowindow));

         markers2.push ( mark  );
       }

        // Add a marker clusterer to manage the markers.
        var markerCluster = new MarkerClusterer(map, markers2,  {imagePath: 'https://raw.githubusercontent.com/googlemaps/js-marker-clusterer/gh-pages/images/m'});
        //google.maps.event.trigger(map, 'resize');
}
