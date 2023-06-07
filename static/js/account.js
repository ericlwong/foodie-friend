document.querySelector('#create-list-btn').addEventListener('click', () => {

  document.querySelector('#new-list-container').insertAdjacentHTML('beforebegin', '<hr class="mt-0 mb-4">');

  document.querySelector('#form-list').insertAdjacentHTML('beforeend',
    '<label class="form-label mb-3" for="list-name">List Name</label><input type="text" class="form-control mb-3" id="list-name" name="list-name"><button type="submit" class="btn btn-primary">Create</button>'
  );

  document.querySelector('#create-list-btn').style.display = 'none';
});

const deleteListBtns = document.querySelectorAll('#delete-list-btn');

deleteListBtns.forEach(deleteListBtn => {
  deleteListBtn.addEventListener('click', () => {
    const data = {
      listId: deleteListBtn.value,
    };
  
    fetch('/api/delete-list', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((responseJson) => {
        document.querySelector(`#favlist-${responseJson.data.listId}`).remove();
        alert(responseJson.status);
      });
  });
})

let favoriteBtnId = null;
document.querySelector('#delete-favorite-modal').addEventListener('show.bs.modal', (evt) => {
  favoriteBtnId = evt.relatedTarget.dataset.favoriteId;
});

document.querySelector('#confirm-delete-fav-btn').addEventListener('click', () => {
  const data = {
    favoriteId: favoriteBtnId,
  };

  fetch('/api/delete-favorite', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((responseJson) => {
      document.querySelector(`#favorite-${responseJson.data.favoriteId}`).parentElement.parentElement.remove();
      bootstrap.Modal.getInstance(document.querySelector('#delete-favorite-modal')).hide();
      document.getElementById('status').innerHTML = responseJson.status;

      if (responseJson.success === true) {
          document.getElementById('status').classList.add('alert', 'alert-success');
      } else {
        document.getElementById('status').classList.add('alert', 'alert-danger');
      }
    });
});

let listId = null;
document.querySelector('#delete-list-modal').addEventListener('show.bs.modal', (evt) => {
  listId = evt.relatedTarget.value;
  console.log(listId)
});

document.querySelector('#confirm-delete-list-btn').addEventListener('click', () => {
  const data = {
    listId: listId,
  };

  fetch('/api/delete-list', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((responseJson) => {
      document.querySelector(`#favlist-${responseJson.data.listId}`).remove();
      bootstrap.Modal.getInstance(document.querySelector('#delete-list-modal')).hide();
      document.getElementById('status').innerHTML = responseJson.status;

      if (responseJson.success === true) {
          document.getElementById('status').classList.add('alert', 'alert-success');
      } else {
        document.getElementById('status').classList.add('alert', 'alert-danger');
      }
    });
});



