let map, infoWindow;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 18,
  });
  infoWindow = new google.maps.InfoWindow();

  // Call the geolocation function immediately after initializing the map
}

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.watchPosition(
      (position) => {
        console.log(position.coords);
        const pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };

        $("#longitude").val(pos["lng"]);
        $("#latitude").val(pos["lat"]);
        // const posString = JSON.stringify(pos);
        // alert(posString);

        // Set in map
        // infoWindow.setPosition(pos);
        // infoWindow.setContent("You are here.");
        // infoWindow.open(map);
        // map.setCenter(pos);
      },
      () => {
        handleLocationError(true, infoWindow, map.getCenter());
      }
    );
  }
  // else {
  //   handleLocationError(false, infoWindow, map.getCenter());
  // }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );

  infoWindow.open(map);
}

$(document).ready(function () {
  getLocation();
});

// window.initMap = initMap;

$("#locationCheck").on("change", function () {
  if ($(this).prop("checked") == true) {
    $(".fileUpload").removeClass("d-none");
    $('.fileUpload input[type="file"]').attr("required", true);
  } else {
    $(".fileUpload").addClass("d-none");
    $('.fileUpload input[type="file"]').removeAttr("required");
  }
});

$('#mapForm').submit(function(e){
  setTime("time");
  setDate("date");
});

getLocation();
setTime("time");
setDate("date");


function locationGetFun(){
  event.preventDefault();
  getLocation()
  var endLon= $("#longitude").val();
  var endLat= $("#latitude").val();
  if (!endLon || !endLat) {
    $('.endLocationImg').removeClass('d-none');
    $('#endLocationImg').attr('required', true);
    alert('We can not get location  information please add location image');
    return false
  }
  else{
    $('#docketsForm').submit()
  }
}
