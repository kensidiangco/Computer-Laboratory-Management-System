let modal = document.getElementById('modal')
let isOpen = false
function OpenModal() {
  if (!isOpen) {
    modal.classList.remove('hidden')
    isOpen = !isOpen
  } else {
    modal.classList.add('hidden')
    isOpen = !isOpen
  }
}