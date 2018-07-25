document.querySelector("#lang-switch").style.display = 'none';
setTimeout(function(){
    document.body.classList.add("bg");
    document.body.style.cursor = "initial";
    document.querySelector(".title-container").style.overflow = 'visible';
    document.querySelector(".title-container").style.top = '5vh';
    document.querySelector("h1").innerHTML = 'All-NBA Teams';
    document.querySelector(".subtitle").style.display = 'initial';
    document.querySelector("h1").style.fontStyle = 'normal';
    document.querySelector("#lang-switch").style.display = 'initial';
}, 2000)
setTimeout(function(){
    document.querySelector("h1").classList.add("title");
    document.querySelector(".container_author").style.display = 'flex';
    document.querySelector("button").style.display = 'initial';
    document.querySelector("svg.corner").style.display = 'initial';
    document.querySelector("#tracker").classList.add("dis");
}, 3800)