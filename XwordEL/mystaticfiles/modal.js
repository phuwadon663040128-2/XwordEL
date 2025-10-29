
let modal = document.getElementById("XwordModal");
let btn = document.getElementById("XwordModalBtn");
let span = document.getElementsByClassName("close")[0];



btn.onclick = function () {
    modal.style.display = "block";
}

span.onclick = function () {
    
    modal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


