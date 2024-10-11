import re
from pprint import pprint

# List of sample responses for testing
handled_test_responses = [
    '''
    questions_list:
        - question: 
            header: "Which company has partnered with Amazon to develop new smart home devices?"
            choices_list: ["Google", "Microsoft", "Samsung", "Apple"]
            correct_answer: 4

        - question:
            header: "What is the capital of England?"
            choices_list: ["Paris", "London", "Prague", "Berlin"]
            correct_answer: 2
    '''
    ,
    '''
    questions_list:
        - question: "What is the largest planet in our solar system?" 
            choices_list: ["Earth", "Mars", "Jupiter", "Saturn"]
            correct_answer: 3

        - question: "Who wrote 'To Kill a Mockingbird'?"
            choices_list: ["Harper Lee", "Mark Twain", "Ernest Hemingway", "F. Scott Fitzgerald"]
            correct_answer: 1
    '''
]

# Refined regex pattern to extract from the yaml
pattern = re.compile(r'''
    -\s*question:\s* 
    (?:header:)?\s*"?([^"]+)"?\s* 
    choices_list:\s*\[([^\]]+)\]\s*
    correct_answer:\s*(\d+)
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