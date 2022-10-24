let RejectModal = document.getElementById("RejectModal")
let isRejectModalOpen = false

function OpenReject() {
  if (!isRejectModalOpen) {
    RejectModal.classList.remove("hidden")
    isRejectModalOpen = !isRejectModalOpen
  }
}

function closeRejectModal() {
  if (isRejectModalOpen) {
    RejectModal.classList.add("hidden")
    isRejectModalOpen = !isRejectModalOpen
  }
}