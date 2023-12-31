from flask import Blueprint, request, jsonify, render_template, Response
import requests
import openai  # Assuming you're using the OpenAI Python client
import azure.cognitiveservices.speech as speechsdk
import xml.etree.ElementTree as ET
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
        # Azure endpoint and key
        #azure_endpoint = "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1"
        azure_endpoint = "https://eastus.customvoice.api.speech.microsoft.com"
        azure_key = os.getenv('AZURE_TTS_KEY')  # Store your key in an environment variable

        headers = {
            'Ocp-Apim-Subscription-Key': azure_key,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-16khz-128kbitrate-mono-mp3'
        }

        # Construct the SSML
        ssml = f"<speak version='1.0' xml:lang='en-US'> <voice xml:lang='en-US' xml:gender='Female' name='en-US-JennyNeural'>{script}</voice> </speak>"

        
        response = requests.post(azure_endpoint, headers=headers, data=ssml)

        if response.status_code == 200:
            # Stream the audio data directly in the response
            return Response(response.content, mimetype='audio/mpeg')
        else:
            return jsonify({"error": "Error from Azure TTS service"}), response.status_code

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Azure TTS Request failed: {e.response.text}")
        return jsonify({"error": f"Azure TTS Request failed: {e.response.text}"}), e.response.status_code


    #except Exception as e:
    #    return jsonify({"error": str(e)}), 500

