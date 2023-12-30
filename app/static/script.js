function createSession() {
    var mood = document.getElementById('mood').value;
    var music = document.getElementById('music').value;
    var goal = document.getElementById('goal').value;
    var duration = document.getElementById('duration').value;

    // Example fetch call - Replace with your actual API call
    fetch('/create_meditation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mood, music, goal, duration }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('scriptOutput').textContent = data.script;
    })
    .catch(error => {
        document.getElementById('errorOutput').textContent = 'An error occurred: ' + error.message;
    });
}

