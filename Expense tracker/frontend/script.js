const button = document.getElementById("btn");
const message = document.getElementById("message");

button.addEventListener("click", function() {
    message.textContent = "🎉 Button Clicked Successfully!";
});
