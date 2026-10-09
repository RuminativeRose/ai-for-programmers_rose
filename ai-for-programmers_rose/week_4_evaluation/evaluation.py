from openai import OpenAI
from langsmith.evaluation import evaluate as ls_evaluate

import json

import os, sys, logging

logger = logging.Logger(__name__)
logger.addHandler(logging.NullHandler())

# Initialize the OpenAI client
client = OpenAI()

# Dataset name in LangSmith (already uploaded)
dataset_name = "news_dataset_class"

# System prompt for extraction
SYSTEM_PROMPT = """Extract information from the news into a dictionary. 
The dictionary keys are company_name, date_of_transaction, amount, product_service, location. 
Make sure the output is in proper JSON with double quotes around the keys and values. 
For all dates, use the following format: mm-dd-yyyy."""

def make_call_to_llm(input):
    # Extract the input content from the dataset item
    user_content = input["news"] if isinstance(input, dict) else input
    
    # Create the message array for the API call
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content}
    ]
    
    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages,
        temperature=0
    )
    logger.info("Made call with query %s",user_content)
    # Extract the output from the response
    output = response.choices[0].message.content
    logger.info("Got output %s",output)
    return {"output": output}

# llm_result is the result of the make_call_to_llm call
# It contains the model's response that we'll compare against the expected output
def perform_eval(llm_result, dataset_item):
    try:
        # Parse the model's output
        llm_output = json.loads(llm_result.outputs['output'])
        
        # Parse the expected output
        expected_output = json.loads(dataset_item.outputs['output'])
        
        # Extract score from response
        # For a simpler implementation, let's manually calculate the score
        total_keys = len(expected_output)
        correct_keys = sum(1 for key in expected_output if key in llm_output and llm_output[key] == expected_output[key])
        score = correct_keys / total_keys if total_keys > 0 else 0
        logging.info("Got score %f for llm output %s",score,llm_output)
        logging.info('Expected output from dataset was %s',expected_output)
        return {"score": score}
    except json.JSONDecodeError:
        # Handle the case where JSON parsing fails
        logging.error('Failed to parse JSON for either llm or expected output; using 0 for score',exc_info=True)
        return {"score": 0.0}

# Evaluate the target task
# TODO: Implement the evaluate function to run the evaluation
# See https://docs.smith.langchain.com/evaluation for reference and examples
# This should evaluate make_call_to_llm against the dataset_name using perform_eval
# and create an experiment with the prefix "news_extraction_homework"
def evaluate():
    results = ls_evaluate(
    make_call_to_llm,
    data=dataset_name,
    evaluators=[perform_eval],
    experiment_prefix="news_extraction_homework"
    )
    logging.info("Made call to Langsmith evaluator with results %s",str(results))
    print(results)
    
    
if __name__ == "__main__":
    logging.basicConfig(filename="news_evaluation.log",level=logging.INFO)
    sys.exit(evaluate())