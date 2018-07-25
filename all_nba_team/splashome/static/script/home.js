// var svgDoc = document.querySelector("object").contentDocument;
// var styleElement = svgDoc.createElementNS("http://www.w3.org/2000/svg", "style");
// styleElement.textContent = "svg { fill: green }"; // add whatever you need here
// svgDoc.firstChild.appendChild(styleElement);

/* ------------------ enlarge left column --------- */
function clickItem(event) {
    var el = event.target;
    el.classList.add("clickStat");
    while (el.firstChild) {
        el.removeChild(el.firstChild);
    }
}
document.querySelectorAll(".menu-item").forEach(function(elem) { //better way is to use Event Delegation attaching Listener to .menu (when can accept it has the list is static and only 5 anchors are present)
    elem.addEventListener("click",clickItem)
});

/* --------- slideshow ------------ */
var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("demo");
  var captionText = document.getElementById("caption");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
  captionText.innerHTML = dots[slideIndex-1].alt;
} 



