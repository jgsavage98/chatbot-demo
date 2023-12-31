function createSession() {
    var mood = document.getElementById('mood').value;
    var music = document.getElementById('music').value;
    var goal = document.getElementById('goal').value;
    var duration = document.getElementById('duration').value;
    var createSessionButton = document.getElementById('createSessionButton');
    var progressBar = document.getElementById('progressBar');

    // Disable the button and show the progress bar
    createSessionButton.disabled = true;
    progressBar.style.display = 'block';
    
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
    })
    .finally(() => {
        // Re-enable the button and hide the progress bar
        createSessionButton.disabled = false;
        progressBar.style.display = 'none';
    });
}

