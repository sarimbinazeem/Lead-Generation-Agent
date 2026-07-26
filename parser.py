"""
Purpose -> Extracts the business type and locations from user prompt

OpenAI will extract the info
"""

import os
import sys
import json #to handle json response

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
sys.stdout.reconfigure(encoding = "utf-8")

client = OpenAI(
    api_key=os.getenv("DO_API_KEY"),
    base_url=os.getenv("DO_BASE_URL"),
)

def parse_prompt(prompt):
    """
    It takes user prompt 

    this function extracts the business type and lcoations from the prompt
    
    """

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        temperature=0,
        response_format={"type": "json_object"},        
        messages=[
            {
                "role":"system",
                "content":(
                    "You are an AI Agent that extracts lead information only\n"
                    "Return only the JSON Foramt response in the following format: \n"
                    '{'
                    '"business_type":"...",'
                    '"location":"..."'
                    '}'
                    
                ),

            },
            {
                "role":"user",
                "content":prompt,
            },
        ]

    )

    result = json.loads(response.choices[0].message.content)

    return (
        result.get("business_type",""),
        result.get("location",""),
    )