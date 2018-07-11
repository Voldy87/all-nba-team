var toggle = true;

function toggleH2() {
    console.log(6666);
    var x = document.querySelectorAll("h2");
    for (let i = 0; i < x.length; i++)
        x[i].style.display = toggle ? "none" : "inherit";
    toggle = !toggle;
}



function hoverEvent() {
    console.log("hover");
    //document.querySelector(".container .item.left").style.flexGrow=1;
  //  document.querySelector(".container .item.left .index").style.visibility="hidden";
}