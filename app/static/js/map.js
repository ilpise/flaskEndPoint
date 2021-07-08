

  // The first parameter are the coordinates of the center of the map
  // The second parameter is the zoom level
//  var map = L.map('dashmap').setView([45.46794553816529, 9.132749306484605], 11);
    var map = L.map('dashmap');

  // {s}, {z}, {x} and {y} are placeholders for map tiles
  // {x} and {y} are the x/y of where you are on the map
  // {z} is the zoom level
  // {s} is the subdomain of cartodb
  var layer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
  });

  // Now add the layer onto the map
  layer.addTo(map);

//  var marker = L.marker([45.46794553816529, 9.132749306484605]).addTo(map);
//  marker.bindTooltip("Dab 1");
//  marker.bindPopup("Dab 1");

   // Set an empty GeoJson template
   var geojson = {
    type: "FeatureCollection",
    features: [],
   };

   $.getJSON('/dabs', function(data) {
        console.log(data);
        $.each( data, function( key, value ) {
            console.log(value.lon)
            if (value.lon !== null && value.lat !== null) {
                geojson.features.push({
                    "type": "Feature",
                    "geometry": {
                      "type": "Point",
                      "coordinates": [parseFloat(value.lon), parseFloat(value.lat)]
                    },
                    "properties": {
                      "Name": value.Name,
                      "id" : value.primary_key,
                      "HumanName": value.HumanName
                    }
                  });
            }
        });
   }).then(
        function(data){
            console.log(geojson);
            var features = L.geoJSON(geojson, {
                style: function (feature) { return {color: feature.properties.Status}; },
                }).bindPopup(function (layer) {
            //        return layer.feature.properties.Name;
                    var el = document.createElement('div');
                    el.classList.add("my-class");
                    el.innerHTML = '<a href="/dab?dab_id=' + layer.feature.properties.id + '">' + layer.feature.properties.HumanName + '</a>';
            //        el.innerHTML = '<a href="/dab_info?user_id=' + layer.feature.properties.id + '">' + layer.feature.properties.Name + '</a>';

            //        $.getJSON("http://www.example.com/data",function(datapoint){
            //           el.innerHTML = '<h2>' + datapoint[i].intensity + '</h2>';
            //        })
                    return el;
                }).addTo(map);

            map.fitBounds(features.getBounds());
        }
   );