function createMeditationSession() {
    var mood = document.getElementById('mood').value;
    var music = document.getElementById('music').value;
    var goal = document.getElementById('goal').value;
    var duration = document.getElementById('duration').value;

    var responseText = "Creating a meditation session with your preferences: \nMood: " + mood + "\nMusic: " + music + "\nGoal: " + goal + "\nDuration: " + duration + " minutes.";
    
    document.getElementById('chatbotResponse').innerText = responseText;
}
