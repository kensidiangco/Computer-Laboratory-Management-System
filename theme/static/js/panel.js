var openM = document.getElementById("openM")
var sideB = document.getElementById("sideB")
var navB = document.getElementById("navB")

function openMenu() {
    openM.classList.add("md:hidden")
    navB.classList.add("md:ml-60")
    sideB.classList.remove("w-0")
    sideB.classList.add("md:w-60")
}

function closeMenu() {
    openM.classList.remove("md:hidden")
    navB.classList.remove("md:ml-60")
    sideB.classList.add("w-0")
    sideB.classList.remove("md:w-60")
}