document.addEventListener("DOMContentLoaded", function () {
    let emotionText = document.querySelector(".typed-text");
    if (emotionText) {
        let text = emotionText.getAttribute("data-text");
        let i = 0;
        
        function typeEffect() {
            if (i < text.length) {
                emotionText.textContent += text.charAt(i);
                i++;
                setTimeout(typeEffect, 100);
            } else {
                emotionText.style.borderRight = "none"; // Remove cursor
            }
        }

        emotionText.textContent = "";
        typeEffect();
    }
});
