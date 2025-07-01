let modal = document.getElementById('deleteModal')
let deleteIcon = document.getElementById('delete-icon')
let closeBtn = document.getElementsByClassName('close')[0]
let cancelBtn = document.getElementsByClassName('cancel-btn')[0]

deleteIcon.onclick = function (event) {
  event.preventDefault()
  modal.style.display = 'block'
}

closeBtn.onclick = function () {
  modal.style.display = 'none'
}

cancelBtn.onclick = function () {
  modal.style.display = 'none'
}

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = 'none'
  }
}
