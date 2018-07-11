var isShown = true;
var initial = document.querySelector(".page-footer").style.display;

function toggleFooter() {
    document.querySelector(".page-footer").style.display = isShown ? 'none' : initial;
    isShown = !isShown;
}