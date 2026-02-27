// ==============================
// Smooth Page Fade In
// ==============================

document.addEventListener("DOMContentLoaded", function () {
    document.body.classList.add("fade-in");
});

// ==============================
// Confirmation Popup
// ==============================

function confirmAction(message) {
    return confirm(message);
}

// ==============================
// Dynamic Match Score Animation
// ==============================

function animateScore(elementId, finalScore) {
    let element = document.getElementById(elementId);
    let start = 0;
    let duration = 1000;
    let increment = finalScore / (duration / 10);

    let counter = setInterval(function () {
        start += increment;
        if (start >= finalScore) {
            start = finalScore;
            clearInterval(counter);
        }
        element.innerText = Math.floor(start) + "%";
    }, 10);
}

// ==============================
// Dark/Light Toggle (Optional Feature)
// ==============================

function toggleTheme() {
    document.body.classList.toggle("light-mode");
}