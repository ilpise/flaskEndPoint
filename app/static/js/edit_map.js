
console.log(lat)
console.log(lng)
console.log(dabName)

    // Verify if lat lng are settled
    if(lat === 'None' && lng === 'None' ){
        var center = [45.46794553816529, 9.132749306484605]
    } else {
        var center = [lat, lng]
    }

// The first parameter are the coordinates of the center of the map
  // The second parameter is the zoom level
  var map = L.map('dashmap').setView(center, 11);

  // {s}, {z}, {x} and {y} are placeholders for map tiles
  // {x} and {y} are the x/y of where you are on the map
  // {z} is the zoom level
  // {s} is the subdomain of cartodb
  var layer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
  });

  // Now add the layer onto the map
  layer.addTo(map);

var myMarker = L.marker(center, {title: dabName, alt: dabName, draggable: true})
		.addTo(map)
		.on('dragend', function() {
			var coord = String(myMarker.getLatLng()).split(',');
			var lat = coord[0].split('(');
			var lng = coord[1].split(')');
            console.log(lat[1])
            console.log(lng[0])
            $.ajax({
              url : "/setlatlng",
              type : "POST",
              contentType: "application/json",
              dataType: 'json',
              data : JSON.stringify({'dabId':dabId, 'lat':lat[1], 'lng':lng[0]}),
              success: function(result) {
                console.log("Result:");
                console.log(result);
              }
            });
		});
