function initMap() {
    const target = document.getElementById('map');
    if(document.getElementById("id_gym").tagName == 'INPUT'){
        var inputGym = document.getElementById("id_gym").value
        var inputAddress = document.getElementById("id_address").value
    }else{
        var inputGym = document.getElementById("id_gym").textContent
        var inputAddress = document.getElementById("id_address").textContent
    }
    const title = inputGym
    const geocoder = new google.maps.Geocoder();

    geocoder.geocode({ address: inputAddress }, function(results, status){
        if (status === 'OK' && results[0]){
            const map = new google.maps.Map(target, {
                center: results[0].geometry.location,
                zoom: 15,
            });
            const marker = new google.maps.Marker({
                position: results[0].geometry.location,
                map: map,
            });
            const latlng = new google.maps.LatLng(results[0].geometry.location.lat(), results[0].geometry.location.lng());
            const content = '<div id="map_content"><p>' + title + '<br/>' + inputAddress + '<br/><a href="https://maps.google.co.jp/maps?q=' + latlng + '&iwloc=J" target="_blank" rel="noopener noreferrer">Open Google Map</a></p></div>';
            var infowindow = new google.maps.InfoWindow({
                content: content,
            });
            infowindow.open(map, marker);

            google.maps.event.addListener(marker, 'click', function() {
                infowindow.open(map, marker);
            });
        } else {
            alert("Not Found: " + status);
            return;
        }
    });
}

function initAutocomplete() {   
    var map = new google.maps.Map(document.getElementById("map"), initMap());
    const input = document.getElementById("pac-input");
    const searchBox = new google.maps.places.SearchBox(input);
    map.addListener("bounds_changed", () => {
        searchBox.setBounds(map.getBounds());
    });
    let markers = [];
    searchBox.addListener("places_changed", () => {
        map = new google.maps.Map(document.getElementById("map"), {
            center: {},
            zoom: 13,
            mapTypeId: "roadmap",
        });
        const places = searchBox.getPlaces();
        if (places.length == 0) {
            return;
        }
        markers.forEach((marker) => {
            marker.setMap(null);
        });
        markers = [];
        const bounds = new google.maps.LatLngBounds();
        var prev_infowindow =false;

        places.forEach((place) => {
            if (!place.geometry || !place.geometry.location) {
                console.log("Returned place contains no geometry");
                return;
            }
            const icon = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25),
            };
            var marker = new google.maps.Marker({
                map,
                icon,
                title: place.name,
                position: place.geometry.location,
            })
            var infowindow = new google.maps.InfoWindow({
                content: place.name +'<br>'+ place.formatted_address
            });
            markers.push(marker);
            
            google.maps.event.addListener(marker, "click", function(e) {
                if( prev_infowindow ) {
                    prev_infowindow.close();
                }
                prev_infowindow = infowindow;
                infowindow.open(map, this);
            });

            if (place.geometry.viewport) {
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });
}