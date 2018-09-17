var i = 0;

function toggler() { console.log("TOGGLEFOOTER");
    i++;
    if (i==2) {
        i=0;
        document.querySelector(".page-content-container").classList.toggle("adapt");
    }
}
function afterDOMload() { 
    const mq = window.matchMedia( "(max-width: 768px)" );
    if (mq.matches) {
        var transitionEnd = transitionEndEventName();
        element.addEventListener(transitionEnd, toggler, false);
        document.querySelector(".page-footer").classList.add("adapt");
      } 
}
document.addEventListener('DOMContentLoaded', afterDOMload );