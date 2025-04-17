// List of "Hello" in different languages
const words = ["Hello", "Hola", "Bonjour", "Hallo", "Ciao", "こんにちは", "안녕하세요", "你好", "Привет", "مرحبا",
    "Merhaba", "Sawubona", "नमस्ते", "Salam", "Hei", "Hej", "Kamusta", "Salve", "Γεια σας"];

function createFloatingText() {
const text = document.createElement("div");
text.className = "floating-text";
text.textContent = words[Math.floor(Math.random() * words.length)];
text.style.top = Math.random() * 90 + "%"; // Random Y position
text.style.animationDuration = (Math.random() * 5 + 5) + "s"; // Random speed
document.getElementById("background").appendChild(text);

// Remove text after animation ends
setTimeout(() => text.remove(), 10000);
}

// Generate floating text at intervals
setInterval(createFloatingText, 1000);

// Redirect to Microsoft Login
function redirectToMicrosoftLogin() {
window.location.href = "/auth/login/";
}