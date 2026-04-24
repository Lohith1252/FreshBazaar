// ================= CART POPUP =================
function toggleCart() {
    let popup = document.getElementById("cartPopup");
    popup.classList.toggle("show");
}


// ================= QTY CONTROL =================
function changeQty(btn, val) {
    let input = btn.parentElement.querySelector("input");
    let q = parseInt(input.value) + val;

    if (q < 1) q = 1;

    input.value = q;
}


// ================= BUTTON ANIMATION =================
function animateBtn(btn) {
    btn.innerHTML = "✔ ADDED";
    btn.style.background = "#ff6f00";

    setTimeout(() => {
        btn.innerHTML = "ADD TO CART";
        btn.style.background = "green";
    }, 800);
}


// ================= SEARCH FILTER =================
document.addEventListener("DOMContentLoaded", function () {

    let search = document.getElementById("search");

    if (search) {
        search.addEventListener("keyup", function () {
            let val = this.value.toLowerCase();

            document.querySelectorAll(".card").forEach(card => {
                let text = card.innerText.toLowerCase();
                card.style.display = text.includes(val) ? "block" : "none";
            });
        });
    }

});