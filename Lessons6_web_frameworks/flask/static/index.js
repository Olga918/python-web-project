document.addEventListener("DOMContentLoaded", function () {
    var btn = document.querySelector("button");
    if (btn) {
        btn.addEventListener("click", function () {
            alert("You pressed the button!");
        });
    }
});
