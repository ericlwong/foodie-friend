document.querySelector('#create-list-btn').addEventListener('click', () => {

  document.querySelector('#new-list-container').insertAdjacentHTML('beforebegin', '<hr class="mt-0 mb-4">');

  document.querySelector('#form-list').insertAdjacentHTML('beforeend',
    '<label class="form-label mb-3" for="list-name">List Name</label><input type="text" class="form-control mb-3" id="list-name" name="list-name"><button type="submit" class="btn btn-primary">Create</button>'
  );

  document.querySelector('#create-list-btn').style.display = 'none';
});
