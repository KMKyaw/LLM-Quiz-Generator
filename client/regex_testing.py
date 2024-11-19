import re
from pprint import pprint

# List of sample responses for testing
handled_test_responses = [
    '''
    questions_list:
        - question: 
            header: "expected format"
            choices_list: ["text", "text", "text", "text"]
            correct_answer: 4

        - question:
            header: "expected format"
            choices_list: ["text", "text", "text", "text"]
            correct_answer: 2
    '''
    ,
    '''
    handled_formats:
        - question: 
            header: missing quotes 
            choices_list: ["text", "text", "text", "text"]
            correct_answer: 3

        - question: "missing header" 
            choices_list: ["text", "text", "text", "text"]
            correct_answer: 3

        - question: missing header and quotes
            choices_list: ["text", "text", "text", "text"]
            correct_answer: 1
        
        - question:
            header: "missing quotes in list, done in post-processing, not in regex"
            choices_list: [text, text, text, text]
            correct_answer: 4
    '''
]

# Refined regex pattern to extract from the yaml
pattern = re.compile(r'''
    -\s*question:\s*               # Match the start of a question entry
    (?:header:)?\s*['"]?([^"]+)['"]?\s*  # Optionally match 'header:' and capture the question text
    choices_list:\s*\[([^\]]+)\]\s* # Match 'choices_list:' and capture the list of choices
    correct_answer:\s*(\d+)        # Match 'correct_answer:' and capture the answer number
''', re.VERBOSE)

# Prepare list to store parsed questions lists
all_questions_lists = []

# Iterate through each response
for response in handled_test_responses:
    # Find all matches
    matches = pattern.findall(response)
    
    # Prepare list to store questions for the current response
    questions_list = []
    
    # Iterate through matches and create dictionaries
    for match in matches:
        question = {
            'question': match[0].strip(),
            'choices_list': [choice.strip("\'\" ") for choice in match[1].split(',')],
            'correct_answer': int(match[2].strip())
        }
        questions_list.append(question)
    
    # Add the current questions list to the all questions lists
    all_questions_lists.append(questions_list)

# Print the extracted questions lists
pprint(all_questions_lists)