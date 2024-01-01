from flask import Blueprint, request, jsonify, render_template, Response
import openai  # Assuming you're using the OpenAI Python client
import azure.cognitiveservices.speech as speechsdk
#from azure.cognitiveservices.speech.audio import MemoryStream
import os
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

        # Set up Azure Speech SDK
        azure_key = os.getenv('AZURE_TTS_KEY')
        azure_region = os.getenv('AZURE_TTS_REGION')
        speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)


        class CustomStreamCallback(speechsdk.audio.PullAudioOutputStreamCallback):
            def __init__(self):
                super().__init__()
                self._stream = io.BytesIO()

            def write(self, data):
                self._stream.write(data)

            def close(self):
                pass

            def get_audio_data(self):
                return self._stream.getvalue()

        # Create the custom callback
        callback = CustomStreamCallback()

        # Use the custom callback with PullAudioOutputStream
        stream = speechsdk.audio.PullAudioOutputStream(callback)


        audio_config = speechsdk.audio.AudioConfig(stream=stream)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Synthesize the speech
        ssml_string = f"<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='en-US-JennyNeural'>{script}</voice></speak>"
        result = synthesizer.speak_ssml_async(ssml_string).get()

        # Check result status
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            logger.error("Speech synthesis failed.")
            return jsonify({"error": "Speech synthesis failed"}), 500

        # Get the synthesized audio data
        audio_data = callback.get_audio_data()

        return Response(audio_data, mimetype='audio/wav')

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

