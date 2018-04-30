setTimeout(function(){
    document.body.classList.add("bg");
    document.body.style.cursor = "initial";
    document.querySelector(".title-container").style.overflow = 'visible'
    document.querySelector(".title-container").style.top = '15vh'
    document.querySelector("h1").innerHTML = 'All-NBA Teams Stats'
    document.querySelector("h1").style.fontStyle = 'normal'
}, 2000)
setTimeout(function(){
    document.querySelector("h1").classList.add("title");
    document.querySelector(".container_author").style.display = 'flex';
    document.querySelector("button").style.display = 'initial';
    document.querySelector("svg.corner").style.display = 'initial';
}, 3800)