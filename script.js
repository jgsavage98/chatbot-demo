document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.getElementById("textInput");
    document.getElementById("buttonInput").addEventListener("click", function() {
        let userText = inputField.value;
        document.getElementById("chatbox").innerHTML += '<p class="userText"><span>' + userText + '</span></p>';
        inputField.value = "";
        // This is where you would add the logic to send the message to ChatGPT and get a response
    });
});

