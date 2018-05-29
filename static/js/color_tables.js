// HTMLCollection.prototype[Symbol.iterator] = Array.prototype.values;
var cells = document.getElementsByTagName("td");
for (var i = 0; i < cells.length; i++) {
    var val = cells[i].innerHTML;
    if (val < 50) {
        var opacity = 1 - val/55;
        cells[i].style.backgroundColor = "rgba(255,0,15," + opacity + ")";
    } else {
        var opacity = (val-50) / 50;
        cells[i].style.backgroundColor = "rgba(0,255,15," + opacity + ")";
    }
}
