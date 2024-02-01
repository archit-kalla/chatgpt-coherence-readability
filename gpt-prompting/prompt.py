"""
Running this script will call the ChatGPT API on all prompts in the file `prompts.txt`,
storing the results in `results.csv`.
"""

import openai
from ratelimit import limits, sleep_and_retry

OUTPUT_FILE = "results.md"
INPUT_FILE = "prompts.txt"
NUM_ITERS = 3


openai.api_key = open('key.txt').read().strip()

@sleep_and_retry
@limits(calls=3, period=66)
def prompt(prompt_string: str):
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt_string}
        ]
    )

    return result['choices'][0]['message']['content']


if __name__ == "__main__":
    input_prompts = open(INPUT_FILE).read().splitlines()
    output_file = open(OUTPUT_FILE, 'a')

    for prompt_text in input_prompts:
        print(f"P: {prompt_text}")
        for i in range(NUM_ITERS):
            print(f"Iteration {i}")
            result = prompt(prompt_text)
            print(f"Result: \n{result}")
            output_file.write(f"### {prompt_text}\n{result}\n")

    output_file.close()
