const saveButton = document.querySelector('#save');

saveButton.addEventListener('click', (evt) => {
  evt.preventDefault();

  const data = {
    restaurantId: saveButton.value,
  };

  fetch(`/api/save`, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((responseJson) => {
      alert(responseJson.status);
    });

  document.querySelector('.modal-backdrop').style.display = 'none';
  document.querySelector('#favorites-modal').style.display = 'none';
});