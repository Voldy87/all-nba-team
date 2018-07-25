var isShown = true;
var initial = document.querySelector(".page-footer").style.display;
var j = 0;
var element = document.querySelector(".item.left");

function toggleFooter() {
    var style = element.currentStyle || window.getComputedStyle(element);
    var grow = style.flexGrow;
    if (grow==30) {
        document.querySelector(".page-footer").style.opacity =  0 ;
        document.querySelector(".page-content-container").style.height = '80%';
        document.querySelector(".item.right").classList.add("reduced");
        document.querySelector(".item.left").style.width="100%";
    }
    else {
        document.querySelector(".page-footer").style.opacity =   initial;
        document.querySelector(".page-content-container").style.height =  initial;
        document.querySelector(".item.right").classList.remove("reduced");
        document.querySelector(".item.left").style.width="10vw";
    }
    //isShown = !isShown;
}

function transitionEndEventName () {
    var i,
        undefined,
        transitions = {
            'transition':'transitionend',
            'OTransition':'otransitionend',  // oTransitionEnd in very old Opera
            'MozTransition':'transitionend',
            'WebkitTransition':'webkitTransitionEnd'
        };

    for (i in transitions) {
        if (transitions.hasOwnProperty(i) && element.style[i] !== undefined) {
            return transitions[i];
        }
    }

    //TODO: throw 'TransitionEnd event is not supported in this browser'; 
}

function afterDOMload() {
    const mq = window.matchMedia( "(max-width: 768px)" );
    if (mq.matches) {
        var transitionEnd = transitionEndEventName();
        element.addEventListener(transitionEnd, toggleFooter, false);
        document.querySelector(".item.left").style.width="10vw";
      } 
      else {
        
      }
    
}
document.addEventListener('DOMContentLoaded', afterDOMload );