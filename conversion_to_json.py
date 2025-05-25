import openai
import json
import os

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get('OPEN_AI_KEY')

def generate_specifications(text_description):
    prompt = f"""
        You receive the content of a complete construction document and you need to extract and summarize all structural parameters - such as material types, thicknesses, usage classifications, and compliance standards - from that document into clean JSON.
        Reply in JSON format only No further comments!
        The content of the document is:
        {text_description}
    """

    response = openai.chat.completions.create(
        model="gpt-4",  
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    content = response.choices[0].message.content.strip()
    try:
        result_json = json.loads(content)
    except json.JSONDecodeError:
        return None

    return result_json

if __name__ == "__main__":
    f = open("construction specification.txt", 'r', encoding='utf-8')
    description = f.readlines()
    result = generate_specifications(description)
    if result:
        with open("results/specifications.json", "w") as f:
            json.dump(result, f, indent=2)
        print("✅ specifications.json created")
