const saveButton = document.querySelector('#save') || null;

if (saveButton !== null) {
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
        document.getElementById('status').innerHTML = responseJson.status;

        if (responseJson.success === true) {
          document.getElementById('status').classList.add('alert', 'alert-success');
        } else {
          document.getElementById('status').classList.add('alert', 'alert-danger');
        }
        
        bootstrap.Modal.getInstance(document.querySelector('#favorites-modal')).hide();
      });
  });
}