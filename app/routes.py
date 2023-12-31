from flask import Blueprint, request, jsonify, render_template, Response
import openai  # Assuming you're using the OpenAI Python client
import azure.cognitiveservices.speech as speechsdk
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create_meditation', methods=['POST'])
def create_meditation():
    # Extract meditation preferences from the request
    data = request.json
    mood = data.get('mood')
    music = data.get('music')
    goal = data.get('goal')
    duration = data.get('duration')

    # Generate meditation script using OpenAI
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Create a guided meditation script. Mood: {mood}, Music: {music}, Goal: {goal}, Duration: {duration} minutes.",
            max_tokens=1000
        )
        script = response.choices[0].text.strip()

        # Azure TTS SDK setup
        azure_key = os.getenv('AZURE_TTS_KEY')  # Azure TTS Key from environment variable
        azure_region = os.getenv('AZURE_TTS_REGION')  # Azure TTS Region from environment variable
        speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)

        # Convert the script to speech using Azure Text-to-Speech SDK
        audio_config = speechsdk.audio.AudioOutputConfig(filename="path/to/temp/audiofile.wav")
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        ssml_string = f"<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='en-US-JennyNeural'>{script}</voice></speak>"
        synthesizer.speak_ssml_async(ssml_string).get()

        # Read the audio file and send as response
        with open("path/to/temp/audiofile.wav", "rb") as audio_file:
            audio_data = audio_file.read()
        return Response(audio_data, mimetype='audio/wav')

    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred: {str(e)}")
        # Return a more detailed error message to the client
        return jsonify({"error": str(e)}), 500

    
    #except Exception as e:
    #    return jsonify({"error": str(e)}), 500

