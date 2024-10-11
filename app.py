from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_community.llms import Ollama
import re
import json
import os
app = Flask(__name__)
llm = Ollama(model='llama2')
prompt_file_name = 'yaml_prompt.txt'
prompt_file_path = os.path.join('prompts',prompt_file_name)
@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')  # get video_id from query parameters
    print(video_id)
    try:
        # Retrieve the available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Fetch the transcript (assuming the first available transcript is in English)
        transcript = transcript_list.find_transcript(['en'])
        # Check if transcript is available
        if not transcript:
            return jsonify({'error': 'No English transcript available for this video.'}), 404
        
        # Concatenate all text lines into a single string
        transcript_text = ''
        for line in transcript.fetch():
            transcript_text += line['text'] + ' '
        
        words = transcript_text.split()
        first_x_words = words[:200]
        transcript_text = ' '.join(first_x_words)

        # Prepare prompt for Ollama
        with open(prompt_file_path,'r') as file:
            prompt = file.read()
        prompt += '\n{' + transcript_text + '}'
        print(prompt)

        # Call Ollama to generate quizzes
        response = llm.invoke(prompt)
        print(response)

        # regex pattern to extract from the yaml
        pattern = re.compile(r"""
        -\s*question:\s* # Match the start of a question entry
            (?:header:)?\s*['"]?([^"]+)['"]?\s* # Optionally match 'header:' and capture the question text
            choices_list:\s*\[([^\]]+)\]\s* # Match 'choices_list:' and capture the list of choices
            correct_answer:\s*(\d+) # Match 'correct_answer:' and capture the answer number
        """, re.VERBOSE)

        # Find all matches
        matches = pattern.findall(response)
        # Prepare list to store parsed questions
        questions_list = []

        # Iterate through matches and create dictionaries
        for match in matches:
            question = {
                'question': match[0].strip(),
                'options': [option.strip("\"\' ") for option in match[1].split(',')],
                'answer': match[2].strip(),
            }
            questions_list.append(question)

        # Convert list to JSON format
        json_data = json.dumps(questions_list, indent=2)
        print(questions_list)
        return json_data

    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video.'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
