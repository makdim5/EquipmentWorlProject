const menuArea = document.querySelector("tbody");
const menu = document.querySelector(".right-click-menu");

menuArea.addEventListener("contextmenu", event => {

    if (event.target.closest('tr')) {
        window.tr = event.target.closest('tr');
    }
    event.preventDefault();

    menu.style.top = `${event.clientY}px`;
    menu.style.left = `${event.clientX}px`;
    menu.classList.add("active");
}, false);

document.addEventListener("click", event => {
    if (event.button !== 2) {
        menu.classList.remove("active");
    }
}, false);

menu.addEventListener("click", event => {
    event.stopPropagation();
}, false);

