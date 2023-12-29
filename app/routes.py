from flask import Blueprint, request, jsonify
import openai  # Assuming you're using the OpenAI Python client

main = Blueprint('main', __name__)

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
            max_tokens=150
        )
        script = response.choices[0].text.strip()

        # TODO: Integrate with a text-to-speech service like Descript

        return jsonify({"script": script})
    except Exception as e:
        return jsonify({"error": str(e)})
