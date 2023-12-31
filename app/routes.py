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

    # Generate meditation script using OpenAI (simplified example)
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Create a guided meditation script. Mood: {mood}, Music: {music}, Goal: {goal}, Duration: {duration} minutes.",
            max_tokens=1000
        )
        script = response.choices[0].text.strip()

        # Convert the script to speech using Azure Text-to-Speech
        azure_key = os.getenv('AZURE_TTS_KEY')  # Azure TTS Key
        azure_region = os.getenv('AZURE_TTS_REGION')  # Azure TTS Region

        speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        result = synthesizer.speak_text_async(script).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # Stream the audio data
            return Response(result.audio_data, mimetype='audio/wav')
        else:
            return jsonify({"error": "Error synthesizing the script"}), 500


    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
#        return jsonify({"script": script})
#    except Exception as e:
#        return jsonify({"error": str(e)})

