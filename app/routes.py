from flask import Blueprint, request, jsonify, render_template, Response, current_app
import openai
import azure.cognitiveservices.speech as speechsdk
import os
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
    data = request.json
    mood = data.get('mood')
    music = data.get('music')
    goal = data.get('goal')
    duration = data.get('duration')

    try:
        # Generate meditation script using OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Create a guided meditation script. Mood: {mood}, Music: {music}, Goal: {goal}, Duration: {duration} minutes.",
            max_tokens=1000
        )
        script = response.choices[0].text.strip()
        logger.info('********* Start of Script ********\n')
        logger.info(script)
        logger.info('********* End of Script ********\n')
        
        # Set up Azure Speech SDK
        azure_key = os.getenv('AZURE_TTS_KEY')
        azure_region = os.getenv('AZURE_TTS_REGION')
        speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)

        logger.info('********* Set up Azure Speech SDK')

        # Synthesize the speech
        audio_config = speechsdk.audio.AudioConfig()
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)        
        ssml_string = f"<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='en-US-JennyNeural'>{script}</voice></speak>"
        result = synthesizer.speak_ssml_async(ssml_string).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logger.info("Speech synthesized for text.")
            audio_data = result.audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            logger.error(f"Speech synthesis canceled: {cancellation.reason}. Error details: {cancellation.error_details}")
            raise Exception(f"Speech synthesis canceled: {cancellation.reason}")

        logger.info('********* Synthesized the speech')
        
        return Response(audio_data, mimetype='audio/mpeg')


    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


