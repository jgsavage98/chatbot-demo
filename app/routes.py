from flask import Blueprint, request, jsonify, render_template, Response
from pydub import AudioSegment
import requests
import openai
import os
import logging
from io import BytesIO
from azure.storage.blob import BlobServiceClient

openai.api_key=os.getenv('OPENAI_API_KEY')
CHUNK_SIZE = 1024

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
    client_name = data.get('name')
    gender = data.get('gender')
    struggles = data.get('struggles')
    emotions = data.get('emotions')
    goal = data.get('goal')
    other_info = data.get('other_info')

    try:
        pronouns = "they/them"
        if gender=='male':
            pronouns = "he/him"
        elif gender=='female':
            pronouns = "she/her"

        prompt = f"""
            You are a guided mediation expert. Your client, {client_name}, {pronouns} is struggling with {struggles}. {pronouns} wants to {emotions}.
            {pronouns}'d like to feel {goal}. Some additional information about {client_name} includes {other_info}. Write a 5-minute personalized meditation script (around 650 words) 
            for {client_name} without any introduction, titles, or headings. Use his name in the script to make it more personal. 
            Add in the following string : "<break time=\"1.0s\" />" after every sentence, and this string: "<break time=\"3.0s\" />" 
            wherever you think a 3 second pause is appropriate, and this string: "<break time=\"3.0s\" /> <break time=\"3.0s\" /> <break time=\"3.0s\" />" 
            wherever you need a long 10 second pause. Make the whole meditation 5 minutes long. Do not include any titles or headings.
        """
        # Generate meditation script using OpenAI
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=1000
        )
        script = response.choices[0].text.strip()
        logger.info('********* Start of Script ********\n')
        logger.info(script)
        logger.info('********* End of Script ********\n')

        # This is the path to Fiona's voice on ElevenLabs
        url = "https://api.elevenlabs.io/v1/text-to-speech/7L2F0M8ojXkZ6StuH3Zr/stream?optimize_streaming_latency=4"

        # This is the header to access Fiona's voice on ElevenLabs
        headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.getenv('XI_API_KEY')
        }
        script = response.choices[0].text.strip()

        # Set up the API call to ElevenLabs for TTS
        data = {
        "text": script,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.43,
            "similarity_boost": 0.28,
            "style": 0.23,
            "use_speaker_boost": 0
            }
        }

        # Fetch and store the main audio in memory
        response = requests.post(url, json=data, headers=headers)
        main_audio_buffer = BytesIO()

        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                main_audio_buffer.write(chunk)

        # Reset buffer position to the start
        main_audio_buffer.seek(0)

        # Load the main audio for processing
        sound1 = AudioSegment.from_file(main_audio_buffer, format="mp3")
        sound1.export(f"sound1.mp3", format='mp3')

        # Now get the background music from the Azure Storage Account
        # Azure setup for background audio
        connect_str = 'DefaultEndpointsProtocol=https;AccountName=backgroundaudio;AccountKey=JghVljN/kQzr8z+HgSLlpGP8On2JZF94Yaxxh1maDMoTtjBEyIz3Q0q9lZEi8nQ4D6LMHZg5Icru+AStoo2Zdg==;EndpointSuffix=core.windows.net'  # Replace with your Azure connection string
        container_name = 'backgroundaudiofiles'  # Replace with your container name
        blob_name = 'RelaxBackgroundAudio.mp3'  # Blob name for the background audio

        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Fetch and store the background audio in memory
        background_audio_buffer = BytesIO()
        background_audio_stream = blob_client.download_blob()

        background_audio_stream.readinto(background_audio_buffer)
        background_audio_buffer.seek(0)  # Reset buffer position to the start

        # Load the background audio for processing
        background = AudioSegment.from_file(background_audio_buffer, format="mp3")
        background = background - 20  # Reduces volume by 20 dB

        # Overlay background on sound1
        combined = sound1.overlay(background)
        
        # Export 'combined' to a byte stream
        combined_byte_stream = BytesIO()
        combined.export(combined_byte_stream, format="mp3")

        # Reset buffer position to the start of the stream
        combined_byte_stream.seek(0)

        # Read the byte stream and return it in the response
        return Response(combined_byte_stream.read(), mimetype='audio/mpeg')


    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

def chunk_script(script, chunk_length=1000):
    
    #Divide the script into smaller parts. Each part should be small enough for Azure TTS to handle.
    
    chunks = []
    while script:
        chunk = script[:chunk_length]
        script = script[chunk_length:]
        chunks.append(chunk)
    return chunks

#if __name__ == '__main__':
    # Run the app



    #except Exception as e:
    #    return jsonify({"error": str(e)}), 500
