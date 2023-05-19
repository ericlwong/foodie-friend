document.querySelector('#create-list-btn').addEventListener('click', () => {

  document.querySelector('#new-list-container').insertAdjacentHTML('beforebegin', '<hr class="mt-0 mb-4">');

  document.querySelector('#form-list').insertAdjacentHTML('beforeend',
    '<label class="form-label mb-3" for="list-name">List Name</label><input type="text" class="form-control mb-3" id="list-name" name="list-name"><button type="submit" class="btn btn-primary">Create</button>'
  );

  document.querySelector('#create-list-btn').style.display = 'none';
});

const deleteListBtn = document.querySelector('#delete-list-btn');

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
