from flask import Blueprint, request, jsonify, render_template, Response
import openai  # Assuming you're using the OpenAI Python client
import azure.cognitiveservices.speech as speechsdk
import os
import io

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

        debug = 'line 31'
        
        # Azure TTS SDK setup
        azure_key = os.getenv('AZURE_TTS_KEY')  # Azure TTS Key from environment variable
        azure_region = os.getenv('AZURE_TTS_REGION')  # Azure TTS Region from environment variable
        speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)

        debug = 'line 38'
        
        # Use an in-memory stream
        stream = speechsdk.audio.AudioOutputStream.create_pull_stream()
        audio_config = speechsdk.audio.AudioConfig(stream=stream)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        debug = 'line 45'
        
        # Synthesize the speech
        ssml_string = f"<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='en-US-JennyNeural'>{script}</voice></speak>"
        synthesizer.speak_ssml_async(ssml_string).get()

        debug = 'line 51'
        
        # Get the synthesized audio data
        stream.seek(0)
        audio_data = stream.read()

        debug = 'line 57'

        return Response(audio_data, mimetype='audio/wav')

    
    except Exception as e:
        return jsonify({"error": debug}), 500

