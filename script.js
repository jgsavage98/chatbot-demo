function createSession() {
    var mood = document.getElementById('mood').value;
    var music = document.getElementById('music').value;
    var goal = document.getElementById('goal').value;
    var duration = document.getElementById('duration').value;

    fetch('/create_meditation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mood, music, goal, duration }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Meditation script:', data.script);
        // TODO:
