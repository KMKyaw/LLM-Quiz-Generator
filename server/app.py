from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_community.llms import Ollama
import re
import json
import os

app = Flask(__name__)
small_llm = Ollama(model='llama3.2:1b')
large_llm = Ollama(model='llama3')

prompt_file_name = 'original.txt'
prompt_file_path = os.path.join('prompts', prompt_file_name)

@app.route('/transcript', methods=['GET'])
def generate():
    video_id = request.args.get('video_id')  # get video_id from query parameters
    print(video_id)
    try:
        # Retrieve the available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Fetch the transcript (assuming the first available transcript is in English)
        transcript = transcript_list.find_transcript(['en']).fetch()
        
        # Combine transcript into text
        transcript_text = " ".join([entry['text'] for entry in transcript])
        
        if len(transcript_text.split()) > 200:  # Threshold for summarization
            transcript_text = summarize_transcript(transcript_text)
            print(f"Transcript summarized to: {transcript_text}")

        response = generate_quiz_from_transcript(transcript_text)

        # Extract questions from the response
        quiz_response = extract_questions_from_response(response)

        return jsonify(json.loads(quiz_response))  # Return as JSON

    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video.'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)})

def summarize_transcript(transcript):
    print("Summarizing transcript...")
    summary_prompt = f"Summarize the following text:\n{transcript}\nSummary:"
    summary = ''

    for chunk in small_llm.stream(summary_prompt):
        print(chunk, end='', flush=True)
        summary += chunk

    return summary.strip()

def generate_quiz_from_transcript(transcript):
    """Generate quiz using the main LLM with the provided transcript."""
    with open(prompt_file_path, 'r') as file:
        prompt = file.read()

    prompt += '{\n' + transcript + '\n}'
    print(f"Generated prompt:\n{prompt}")

    response = ''
    for chunk in large_llm.stream(prompt):  # Use large_llm here
        print(chunk, end='', flush=True)
        response += chunk

    return response

def extract_questions_from_response(response):
    """Extract questions, options, and answers from YAML response."""
    pattern = re.compile(r"""
        -\s*question:\s*  # Match start of a question entry
        (?:header:)?\s*['"]?([^"]+)['"]?\s*  # Capture question text
        choices_list:\s*\[([^\]]+)\]\s*  # Capture list of choices
        correct_answer:\s*(\d+)  # Capture correct answer index
    """, re.VERBOSE)

    matches = pattern.findall(response)
    questions_list = []

    for match in matches:
        question = {
            'question': match[0].strip(),
            'options': [option.strip("\"\' ") for option in match[1].split(',')],
            'answer': match[2].strip(),
        }
        questions_list.append(question)

    return json.dumps(questions_list, indent=2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

