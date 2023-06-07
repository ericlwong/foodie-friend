let swapTracker = 0; // 0 = swap start/end, 1 = swap end/start

document.querySelector('#swap-btn').addEventListener('click', () => {
  const restaurantName = swapTracker == 0 
    ? document.querySelector('#end-restaurant').textContent 
    : document.querySelector('#start-restaurant').textContent;

  const restaurantAddress = swapTracker == 0 
    ? document.querySelector('#end').value
    : document.querySelector('#start').value;

  const userAddress = swapTracker == 0
    ? document.querySelector('#start').value
    : document.querySelector('#end').value;

  if (swapTracker == 0) {
    document.querySelector('#end-restaurant').innerHTML = '';
    document.querySelector('#start-restaurant').innerHTML = restaurantName;
    document.querySelector('#start').value = restaurantAddress;
    document.querySelector('#start').readOnly = true;
    document.querySelector('#start').classList.add('form-control-plaintext');
    document.querySelector('#start').classList.remove('form-control');
    document.querySelector('#end').value = userAddress;
    document.querySelector('#end').readOnly = false;
    document.querySelector('#end').classList.add('form-control');
    document.querySelector('#end').classList.remove('form-control-plaintext');
    swapTracker = 1;
  } else {
    document.querySelector('#start-restaurant').innerHTML = '';
    document.querySelector('#end-restaurant').innerHTML = restaurantName;
    document.querySelector('#end').value = restaurantAddress;
    document.querySelector('#end').readOnly = true;
    document.querySelector('#end').classList.add('form-control-plaintext');
    document.querySelector('#end').classList.remove('form-control');
    document.querySelector('#start').value = userAddress;
    document.querySelector('#start').readOnly = false;
    document.querySelector('#start').classList.add('form-control');
    document.querySelector('#start').classList.remove('form-control-plaintext');
    swapTracker = 0;
  }
});

function initMap() {
  const bounds = new google.maps.LatLngBounds();
  const restaurantInfo = new google.maps.InfoWindow();
  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer();

  // Data to send in payload for AJAX
  const data = { restaurants: [], };
  const restaurantMarkers = [];

  const map = new google.maps.Map(document.querySelector('#map'), {
    zoom: 14,
    mapTypeControl: false,
    gestureHandling: 'cooperative',
    fullscreenControl: false,
  });

  //map.controls[google.maps.ControlPosition.TOP_LEFT].push(document.getElementById('directions-control'));

  directionsRenderer.setMap(map);
  directionsRenderer.setPanel(document.getElementById('directions'));

  document.querySelectorAll('.restaurant').forEach(restaurant => {
    const restaurantId = restaurant.dataset.restaurantId;
    data.restaurants.push({ restaurantId: restaurantId });
  });

  document.querySelector('#directions-btn').addEventListener('click', () => {
    calculateRoute(directionsService, directionsRenderer, map, restaurantMarkers);
  });

  fetch('/api/restaurants', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((restaurantObj) => {
      restaurantObj.forEach(restaurant => {
        const marker = new google.maps.Marker({
          position: new google.maps.LatLng(restaurant.latitude, restaurant.longitude),
          title: restaurant.name,
          map: map,
          restaurantId: restaurant.restaurantId,
        });

        restaurantMarkers.push(marker);
        bounds.extend(marker.position);

        const restaurantInfoContent = `
          <h5>
            <a href="/restaurants/${restaurant.restaurantId}" class="link-dark link-underline-dark link-underline-opacity-0 link-underline-opacity-75-hover">
              ${marker.title}
            </a>
          </h5>
          <p>Rating: ${restaurant.rating}</p>
          <p class="mb-0">${restaurant.address.street}</p>
          <p>
            ${restaurant.address.city}, ${restaurant.address.state} ${restaurant.address.zipcode}
          </p>
        `;

        marker.addListener('click', () => {
          restaurantInfo.close();
          restaurantInfo.setContent(restaurantInfoContent);
          restaurantInfo.open(map, marker);
        });

        map.setCenter(marker.position);
  
        map.addListener('click', () => {
          if (restaurantInfo) restaurantInfo.close();
        });
      });
    });
}

function calculateRoute(directionsService, directionsRenderer, map, restaurantMarkers) {
  const selectedMode = document.getElementById('travel-mode').value;

  if (document.getElementById('start').value === '' || document.getElementById('end').value === '') {
    document.getElementById('status').innerHTML = 'Please enter a valid address.';
    document.getElementById('status').classList.add('alert', 'alert-danger');
    return;
  }

  directionsService.route({
    origin: {
      query: document.getElementById('start').value,
    },
    destination: {
      query: document.getElementById('end').value,
    },
    travelMode: google.maps.TravelMode[selectedMode],
  })
    .then((response) => {
      directionsRenderer.setDirections(response);
      restaurantMarkers.forEach((marker) => {
        marker.setMap(null);
      });
      map.panTo(response.routes[0].bounds.getCenter());

      document.getElementById('status').innerHTML = '';
      document.getElementById('status').classList.remove('alert', 'alert-danger');
    });
}