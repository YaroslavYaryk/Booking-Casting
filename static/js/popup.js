// Initialize Variables
var closePopup = document.getElementById("popupclose");
var overlay = document.getElementById("overlay");
var popup = document.getElementById("popup");
var button = document.getElementById("button");
console.log(button)
    // Close Popup Event
closePopup.onclick = function() {
    overlay.style.display = 'none';
    popup.style.display = 'none';
};
// Show Overlay and Popup
button.onclick = function() {
    console.log("popup")
    overlay.style.display = 'block';
    popup.style.display = 'block';
}