
import requests
from pydub import AudioSegment


CHUNK_SIZE = 1024
# url = "https://api.elevenlabs.io/v1/text-to-speech/777yuCuW9suIZEWPrrI7"

# This is the path to Fiona's voice
url = "https://api.elevenlabs.io/v1/text-to-speech/7L2F0M8ojXkZ6StuH3Zr/stream?optimize_streaming_latency=4"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "0c52b0aafc66e364c2338723afba2a22" #Fiona's API key
  # "xi-api-key": "4e70d3c60c3478c19d8017048d7273f6" #John's API key
}

script = """Find a comfortable and quiet place to sit or lie down.<break time="1.0s" />
Close your eyes and take a deep breath in.<break time="1.0s" />
Now, exhale slowly.<break time="1.0s" />
Feel the air moving in and out of your lungs.<break time="1.0s" />
With each breath, imagine releasing self-doubt and worry.<break time="1.0s" />
Inhale peace and confidence.<break time="1.0s" />
Exhale doubt and fear.<break time="3.0s" />

Picture yourself at the end of a path, just graduated and ready for the next step.<break time="1.0s" />
Acknowledge your achievement in completing grad school.<break time="1.0s" />
Feel the pride and satisfaction in your accomplishment.<break time="1.0s" />
As you inhale, draw in the energy of that success.<break time="1.0s" />
Exhale any lingering doubts about your future.<break time="3.0s" />

Now, envision the path ahead, shrouded in mist.<break time="1.0s" />
This is the unknown future, full of possibilities.<break time="1.0s" />
As you take your next breath, step forward into the mist.<break time="1.0s" />
Feel the mist as a cool, reassuring presence.<break time="1.0s" />
It represents change, growth, and new opportunities.<break time="1.0s" />
With each step, feel more assured, more confident.<break time="3.0s" />

Imagine supportive hands on your back, gently pushing you forward.<break time="1.0s" />
These are the hands of your friends, family, and mentors.<break time="1.0s" />
Feel their love and support with you always.<break time="1.0s" />
Allow this feeling of support to fill you with confidence.<break time="1.0s" />
You are not alone on this journey.<break time="1.0s" />
Your path is yours, but you are surrounded by love and encouragement.<break time="3.0s" />

With each breath, feel more grounded and centered.<break time="1.0s" />
You have the tools and skills you need to succeed.<break time="1.0s" />
Your education and experiences have prepared you well.<break time="1.0s" />
Trust in yourself and in the journey ahead.<break time="1.0s" />
You are capable of navigating any challenge that comes your way.<break time="1.0s" />
Embrace the unknown with confidence and hope.<break time="3.0s" />

Now, take three deep breaths, slowly and deeply.<break time="1.0s" />
With each breath, feel more present and aware.<break time="1.0s" />
Begin to wiggle your fingers and toes.<break time="1.0s" />
When you are ready, open your eyes.<break time="1.0s" />
Carry this feeling of assurance and support with you as you move forward in your day.<break time="3.0s" />"""


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

response = requests.post(url, json=data, headers=headers)
with open('Fiona_output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)

sound1 = AudioSegment.from_file("Fiona_output.mp3")
background = AudioSegment.from_file("RelaxBG.mp3")
background = background - 20  # Reduces volume by 20 dB

# Overlay background on sound1
combined = sound1.overlay(background)

combined.export("Fiona_output_with_bg.mp3", format='mp3')






