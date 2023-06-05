const deleteReviewBtn = document.querySelector('#delete-review-btn') || null;

if (deleteReviewBtn !== null) {
  deleteReviewBtn.addEventListener('click', () => {
    fetch('/api/delete-review', {
      method: 'POST',
      body: JSON.stringify({ userReviewId: deleteReviewBtn.value, }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((responseJson) => {
        deleteReviewBtn.parentElement.remove();
        alert(responseJson.status);
      });
  });
}