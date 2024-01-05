function createSession() {
    var mood = document.getElementById('mood').value;
    // var music = document.getElementById('music').value;
    var goal = document.getElementById('goal').value;
    // var duration = document.getElementById('duration').value;
    var createSessionButton = document.getElementById('createSessionButton');
    var progressBar = document.getElementById('progressBar');
    var audioContainer = document.getElementById('audioContainer'); // Add an element to hold the audio player

    // Clear the previous audio and hide scriptOutput
    audioContainer.innerHTML = '';
    //document.getElementById('scriptOutput').style.display = 'none';

    // Disable the button and show the progress bar
    createSessionButton.disabled = true;
    progressBar.style.display = 'block';
    
    fetch('/create_meditation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mood, goal}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.blob();
    })
    .then(blob => {
        var url = window.URL.createObjectURL(blob);
        var audio = document.createElement('audio');
        audio.src = url;
        audio.controls = true;
        audioContainer.appendChild(audio);
        audio.play();
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

