import os
import sys
import subprocess
import ast

# Load the original QuestionProcessor.py content
question_processor_path = "QuestionProcessor.py"
with open(question_processor_path, "r", encoding="utf-8") as file:
    content = file.read()

# Extract the responses dictionary
responses_start = content.find("responses = {")
responses_end = content.find("}\n", responses_start) + 1
responses_code = content[responses_start:responses_end]
responses = ast.literal_eval(responses_code[11:])  # Safely evaluate the dictionary part

# Prompt the user to update the responses dictionary
for key in list(responses.keys()):
    new_response = input(f"Enter your response for '{key}': ")
    responses[key] = new_response

# Prompt for additional questions
more_questions = input("Do you have more questions to add to the responses dictionary? (yes/no): ")
if more_questions.lower() == 'yes':
    while True:
        key = input("Enter the new question: ")
        value = input(f"Enter the response for '{key}': ")
        responses[key] = value
        more_questions = input("Do you have more questions to add to the responses dictionary? (yes/no): ")
        if more_questions.lower() != 'yes':
            break

# Convert the updated responses dictionary back to a string
responses_str = "responses = {\n"
for key, value in responses.items():
    responses_str += f"    '{key}': '{value}',\n"
responses_str += "}\n"

# Replace the old responses dictionary in the original content
new_content = content[:responses_start] + responses_str + content[responses_end:]

# Write the updated content back to QuestionProcessor.py
with open(question_processor_path, "w", encoding="utf-8") as file:
    file.write(new_content)

print("Updated responses dictionary in QuestionProcessor.py successfully.")

# Run the QuestionProcessor.py script
subprocess.run([sys.executable, question_processor_path])
