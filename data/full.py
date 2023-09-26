from transformers import RobertaForSequenceClassification, AutoTokenizer
import torch
from text_preprocessing import process_text

def change_format_to(list_input):
    formatted_list = [[f"{value:.3f}" for value in sublist] for sublist in list_input]
    return formatted_list

def find_position_of_biggest_value(lst):
    if not lst:
        return None

    max_value = lst[0]
    max_position = 0

    for i in range(1, len(lst)):
        if lst[i] > max_value:
            max_value = lst[i]
            max_position = i

    return max_position

def map_position_to_label(position):
    label_mapping = {
        0: "Other",
        1: "Disgust",
        2: "Enjoyment",
        3: "Anger",
        4: "Surprise",
        5: "Sadness",
        6: "Fear"
    }

    return label_mapping.get(position, "Unknown")

def find_biggest_value_label(lst):
    position = find_position_of_biggest_value(lst)
    if position is not None:
        label = map_position_to_label(position)
        return label
    else:
        return "List is empty"

# Load the model and tokenizer
model_2 = RobertaForSequenceClassification.from_pretrained("save_weight_balance")
tokenizer = AutoTokenizer.from_pretrained("wonrax/phobert-base-vietnamese-sentiment", use_fast=False)

# Process the input text
def process_and_predict(text):
    processed_text = process_text(text)
    inputs = tokenizer(processed_text, padding=True, truncation=True, return_tensors='pt')
    outputs = model_2(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predictions = predictions.cpu().detach().numpy()
    output_list = change_format_to(predictions)
    result_label = find_biggest_value_label(output_list[0])
    return result_label

# Function to ask for user feedback
def ask_user_feedback(predicted_label):
    while True:
        user_feedback = input("Was the prediction accurate? (True/False): ")
        if user_feedback.lower() == "true":
            return True
        elif user_feedback.lower() == "false":
            return False
        else:
            print("Invalid input. Please enter True or False.")

emotion_labels = {
    0: "Other",
    1: "Disgust",
    2: "Enjoyment",
    3: "Anger",
    4: "Surprise",
    5: "Sadness",
    6: "Fear"
}

# Function to ask for user feedback and handle False cases
def ask_user_feedback(predicted_label):
    while True:
        user_feedback = input("Was the prediction accurate? (True/False): ")
        if user_feedback.lower() == "true":
            return True, None
        elif user_feedback.lower() == "false":
            correct_label = input("Enter the correct label number (0-6) " +
                                  "0: Other, 1: Disgust, 2: Enjoyment, 3: Anger, 4: Surprise, 5: Sadness, 6: Fear: ")
            try:
                correct_label = int(correct_label)
                selected_label = emotion_labels.get(correct_label)
                if selected_label is not None:
                    return False, selected_label
                else:
                    print("Invalid label number. Please enter a number from 0 to 6.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print("Invalid input. Please enter True or False.")

# Save user feedback to a txt file
def save_feedback_to_file(feedback, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(feedback + "\n")
# User interaction loop
feedback_file = "feedback.txt"

while True:
    user_input = input("Enter a sentence (or 'exit' to quit): ")
    
    if user_input.lower() == "exit":
        print("Exiting the program.")
        break
    
    predicted_label = process_and_predict(user_input)
    print("Emotion of sentence is:", predicted_label)
    
    is_correct, correct_label = ask_user_feedback(predicted_label)
    print("User feedback:", "Correct" if is_correct else "Incorrect")
    
    if is_correct:
        feedback = f"{user_input}, {predicted_label}"
        save_feedback_to_file(feedback, feedback_file)
        print("Feedback saved to", feedback_file)
    elif correct_label:
        feedback = f"{user_input}, {correct_label}"
        save_feedback_to_file(feedback, feedback_file)
        print("Feedback saved to", feedback_file)