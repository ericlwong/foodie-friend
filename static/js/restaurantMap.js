function initMap() {
  const bounds = new google.maps.LatLngBounds();
  const restaurantInfo = new google.maps.InfoWindow();
  const restaurantMarkers = {};

  // Data to send in payload for AJAX
  const data = { restaurants: [], };

  const map = new google.maps.Map(document.querySelector('#map'));

  document.querySelectorAll('.restaurant').forEach(restaurant => {
    const restaurantId = restaurant.dataset.restaurantId;
    data.restaurants.push({ restaurantId: restaurantId });
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

        marker.addListener('mouseover', () => {
          document.getElementById(`${marker.restaurantId}`).style.backgroundColor = '#f8f9fa';
        });

        marker.addListener('mouseout', () => {
          document.getElementById(`${marker.restaurantId}`).removeAttribute('style');
        });

        map.fitBounds(bounds);
        map.panToBounds(bounds);
  
        map.addListener('click', () => {
          if (restaurantInfo) restaurantInfo.close();
        });
      });
    });
}