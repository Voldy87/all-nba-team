function showSection(elem, theme) {
    var tabs = document.querySelectorAll(".tab")
    var sections = document.querySelectorAll(".tab-section");
    document.querySelector(".tab-container").style.display = 'block';
    document.querySelector(".tab-container").style.fontSize = 'smaller';
    for (let i = 0; i<tabs.length; i++) {
        console.log(theme);
        tabs[i].style.borderWidth =  "0px" ;
        tabs[i].style.background =  "initial" ;
        sections[i].style.display = (sections[i].id==theme) ? 'block': 'none';
    }
    var tab = elem || tabs[0];
        tab.style.borderWidth = "2px";
        tab.style.borderStyle = "solid";
        tab.style.borderTopColor = "white";
        tab.style.borderRightColor = "white";
        tab.style.borderLeftColor = "white";
        tab.style.background = "none";
        
    //clickedElem.style.color = "green";
    //document.getElementById(section).style.display = "initial" ;
}

if (window.matchMedia( "(max-width: 768px)" ).matches)
    showSection(null,"what");