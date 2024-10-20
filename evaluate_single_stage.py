import csv
import time
import re
import json
import os
from langchain_community.llms import Ollama

# Initialize the model
llm = Ollama(model='llama3')

# File paths
input_csv_path = 'transcriptions.csv'  # Adjust this to your input CSV path
output_csv_path = 'single_stage_output.csv'
prompt_file_name = 'original.txt'
prompt_file_path = os.path.join('prompts', prompt_file_name)

def generate_quiz_from_transcript(transcript):
    """Generate quiz using Ollama with the provided transcript."""
    with open(prompt_file_path, 'r') as file:
        prompt = file.read()
    
    prompt += '{\n' + transcript + '\n}'
    print(f"Generated prompt:\n{prompt}")

    # Call Ollama API to generate the quiz
    response = ''
    for chunk in llm.stream(prompt):
        print(chunk, end='', flush=True)
        response += chunk

    return response

def extract_questions_from_response(response):
    """Extract questions, options, and answers from Ollama's YAML response."""
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

def process_csv(input_csv, output_csv):
    """Process the input CSV, generate quizzes, and save results to output CSV."""
    with open(input_csv, 'r') as input_file, open(output_csv, 'w', newline='') as output_file:
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames + ['generation_time', 'quiz_response']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in reader:
            transcript = row['transcription']
            print(f"Processing yt_id: {row['yt_id']}")

            # Measure time taken for quiz generation
            start_time = time.time()
            try:
                response = generate_quiz_from_transcript(transcript)
                generation_time = time.time() - start_time

                # Extract questions from the response
                quiz_response = response
                # quiz_response = extract_questions_from_response(response)
            except Exception as e:
                quiz_response = f"Error: {str(e)}"
                generation_time = 'N/A'

            # Write result to output CSV
            row['generation_time'] = f"{generation_time:.2f} seconds" if generation_time != 'N/A' else 'N/A'
            row['quiz_response'] = quiz_response
            writer.writerow(row)

if __name__ == '__main__':
    try:
        print(f"Starting quiz generation from {input_csv_path}...")
        process_csv(input_csv_path, output_csv_path)
        print(f"Quiz generation completed. Results saved to {output_csv_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")

