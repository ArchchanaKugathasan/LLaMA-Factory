import pandas as pd
import json
# JSON Format
# [
#   {
#     "instruction": "user instruction (required)",
#     "input": "user input (optional)",
#     "output": "model response (required)",
#     "history": [
#       ["user instruction in the first round (optional)", "model response in the first round (optional)"],
#       ["user instruction in the second round (optional)", "model response in the second round (optional)"]
#     ]
#   }
# ]

def read_data(filename):
    # Adjust the delimiter to the one used in your TSV (tab-separated file usually uses '\t')
    return pd.read_csv(filename, delimiter='\t', usecols=['index', 'original', 'translation', 'mean'])

def construct_json(filename):
    df = read_data(filename)
    json_list = []

    # Add your custom instruction text here
    instruction_template = "We need to Evaluate the machine translation output, with scores ranging from 0 to 100. Scores of 0-30 indicate that the translation is mostly unintelligible, either completely inaccurate or containing only some keywords. Scores of 31-50 suggest partial intelligibility, with some keywords present but numerous grammatical errors. A score between 51-70 means the translation is generally clear, with most keywords included and only minor grammatical errors. Scores of 71-90 indicate the translation is clear and intelligible, with all keywords present and only minor non-grammatical issues. Finally, scores of 91-100 reflect a perfect or near-perfect translation, accurately conveying the source meaning without errors. The evaluation criteria focus on two main aspects: Adequacy (how much information is conveyed) and Fluency (how grammatically correct the translation is).Score the following translation with respect to the given instructions. "
    
    for i, row in df.iterrows():
        # Construct the instruction
        instruction = f"{instruction_template}\ \n Original sentence: {row['original']}\n translation: {row['translation']}"

        output_text = f"The predicted DA score is : {row['mean']}"
        # Construct the JSON object
        json_dict = {
            "instruction": instruction,
            "input": "",
            "output": output_text
        }
        
        # Append to the list
        json_list.append(json_dict)

    return json.dumps(json_list, ensure_ascii=False, indent=2)

# Save the JSON output to a file
json_output = construct_json('train.enta.df.short.tsv')
with open('DA_data.json', 'w', encoding='utf-8') as f:
    f.write(json_output)
