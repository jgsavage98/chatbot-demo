function createSession() {
    var mood = document.getElementById('mood').value;
    var music = document.getElementById('music').value;
    var goal = document.getElementById('goal').value;
    var duration = document.getElementById('duration').value;

    // Optionally, display a loading indicator here

    fetch('/create_meditation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mood, music, goal, duration }),
    })
    .then(response => {
        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('Meditation script:', data.script);
        // Display the script to the user
        document.getElementById('scriptOutput').textContent = data.script;
        // Additional processing can be done here if needed
    })
    .catch(error => {
        console.error('Error:', error);
        // Update the UI to show the error, for example:
        document.getElementById('errorOutput').textContent = 'An error occurred: ' + error.message;
    })
    .finally(() => {
        // Hide the loading indicator here, if used
    });
}
