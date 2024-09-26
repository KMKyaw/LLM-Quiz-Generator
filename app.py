from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_community.llms import Ollama
import re
import json
app = Flask(__name__)
llm = Ollama(model="llama2")
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
        first_500_words = words[:50]
        transcript_text = ' '.join(first_500_words)
        # Prepare prompt for Ollama
        prompt = '''
        Make multiple choice quizzes with 4 choices. Examples as below. [Important] DO NOT SAY ANYTHING ELSE! FOLLOW THE FORMAT BELOW. DO NOT PUT A, B, C, D in CHOICES!
        PUT THE QUESTION BETWEEN //start and //end. 
        //start

        QUESTION(Which company has partnered with Amazon to develop new smart home devices?)
        CHOICES(Apple, Google, Microsoft, Samsung)
        ANSWER(Apple)

        QUESTION(Which company has good burgers?)
        CHOICES(BurgerKing, Macdonald, KFC, JolieBee)
        ANSWER(BurgerKing)
        
        QUESTION(Which country has the nothern lights)
        CHOICES(Netherland, Thailand, North Korea, Burma)
        ANSWER(Netherland)
        
        //end
        Now, try to generate the quiz on the given transcript below. 
        '''
        prompt += transcript_text
        print(prompt)
        # Call Ollama to generate quizzes
        response = llm.invoke(prompt)

        # Regular expression patterns to extract questions, choices, and answers
        pattern_question = r"QUESTION\((.*?)\)"
        pattern_choices = r"CHOICES\((.*?)\)"
        pattern_answer = r"ANSWER\((.*?)\)"

        # Find all matches
        matches = re.findall(pattern_question + r"\n" + pattern_choices + r"\n" + pattern_answer, response, re.DOTALL)

        # Prepare list to store parsed questions
        questions_list = []

        # Iterate through matches and create dictionaries
        for match in matches:
            question = {
                'question': match[0].strip(),
                'options': [option.strip() for option in match[1].split(',')],
                'answer': match[2].strip(),
            }
            questions_list.append(question)

        # Convert list to JSON format
        json_data = json.dumps(questions_list, indent=2)
        return json_data

    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video.'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)