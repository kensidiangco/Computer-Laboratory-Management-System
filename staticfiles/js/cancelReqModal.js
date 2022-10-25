let CancelModal = document.getElementById("CancelModal")
let isCancelModalOpen = false

function OpenCancel() {
  if (!isCancelModalOpen) {
    CancelModal.classList.remove("hidden")
    isCancelModalOpen = !isCancelModalOpen
  }
}

function closeCancelModal() {
  if (isCancelModalOpen) {
    CancelModal.classList.add("hidden")
    isCancelModalOpen = !isCancelModalOpen
  }
}