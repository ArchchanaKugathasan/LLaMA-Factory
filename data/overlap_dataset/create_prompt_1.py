import pandas as pd
import json

def read_data(filename):
    # Read the dataset
    return pd.read_csv(filename, delimiter='\t', usecols=['src', 'mt', 'ref', 'score'])

# def construct_json_with_history(filename):
    # df = read_data(filename)
    # json_list = []

    # # Pre-defined instructions
    # instructions = [
    #     "Evaluate machine translation quality for English-Chinese sentences, step by step.",
    #     "Analyze the source, machine translation, and reference translation. List where the machine translation is bad or wrong.",
    #     "Give a score between 0 and 100 to indicate the quality of the MT. Note: 0 is the worst, 100 is perfect.",
    #     "Provide an exact number for the score, not a range."
    # ]

def construct_json(filename):
    df = read_data(filename)
    json_list = []

    # Add your custom instruction text here
    instruction = "You are going to evaluate machine translation quality for Sinhala-English sentences. You will achieve this step by step."
    output_text = ""
    for i, row in df.iterrows():
        # # Construct the instruction
        # instruction = f"{instruction_template}\ , \n Original sentence: {row['original']}\n translation: {row['translation']}"


        #output_text = f"The predicted DA score is : {row['mean']}"
        #output_text = f"The predicted DA score is : {row['mean']:.2f} , Original:{row['original']} , Translation:{row['translation']}"

        # Construct the JSON object
        json_dict = {
            "instruction": instruction,
            "input": "",
            "output": output_text
        }
        
        # Append to the list
        json_list.append(json_dict)

    return json.dumps(json_list, ensure_ascii=False, indent=2)



json_output = construct_json('wmt22_dataset/si-en_overlaps.tsv')
with open('wmt22_dataset/json_created/prompt1/ensi_prmpt1.json', 'w', encoding='utf-8') as f:
    f.write(json_output)
