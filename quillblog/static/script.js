// Get the modal, open button, and close button elements
let modal = document.getElementById('deleteModal')
let deleteIcon = document.getElementById('delete-icon')
let closeBtn = document.getElementsByClassName('close')[0]
let cancelBtn = document.getElementsByClassName('cancel-btn')[0]

// When the user clicks the delete icon, open the modal
deleteIcon.onclick = function (event) {
  event.preventDefault() // Prevent default action of link
  modal.style.display = 'block'
}

// When the user clicks on the (x) close button, close the modal
closeBtn.onclick = function () {
  modal.style.display = 'none'
}

// When the user clicks on the cancel button, close the modal
cancelBtn.onclick = function () {
  modal.style.display = 'none'
}

// When the user clicks anywhere outside of the modal content, close the modal
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = 'none'
  }
}
