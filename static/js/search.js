document.querySelector('#search-btn').addEventListener('click', () => {
  document.querySelector('#search-input').readonly = true;
  document.querySelector('#location-input').readonly = true;
  document.querySelector('#search-ctn').classList.add('visually-hidden');
  document.querySelector('#loader-ctn').classList.remove('visually-hidden');
});