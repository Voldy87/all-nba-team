var sideMenuOpened = true;

function toggleH2() {
    if (document.querySelector(".item.left").style.flexGrow==30) //the side mnenu is opened
        sideMenuOpened = false;
    console.log("hover");
    var x = document.querySelectorAll("h2");
    var i;
    for (i = 0; i < x.length; i++) {
        x[i].style.display = sideMenuOpened ? "none" : "inherit";
    }
    sideMenuOpened = !sideMenuOpened;
    //document.querySelector(".container .item.left .index").style.visibility="hidden";
}

function hoverEvent() {
    console.log("hover");
    //document.querySelector(".container .item.left").style.flexGrow=1;
  //  document.querySelector(".container .item.left .index").style.visibility="hidden";
}