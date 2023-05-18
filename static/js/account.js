document.querySelector('#create-list-btn').addEventListener('click', () => {

  document.querySelector('#new-list-container').insertAdjacentHTML('beforebegin', '<hr class="mt-0 mb-4">');

  document.querySelector('#new-list-form').insertAdjacentHTML('beforeend',
    '<div class="row"><form action="/create-list" method="POST"><label class="form-label mb-3" for="list-name">List Name</label><input type="text" class="form-control mb-3" id="list-name" name="list-name"></form></div>'
  );

  document.querySelector('#create-list-btn').innerHTML = 'Create';
});
