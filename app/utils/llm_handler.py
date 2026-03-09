import os
import boto3
import streamlit as st
import json

from prompts.llm_output_generation import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

MODEL_ID = "arn:aws:bedrock:us-east-1:811839032244:inference-profile/global.amazon.nova-2-lite-v1:0"

bedrock = boto3.client(service_name="bedrock-runtime", region_name=os.environ.get("AWS_REGION_NAME"), aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"), aws_secret_access_key=os.environ.get("AWS_ACCESS_SECRET_KEY"))

def generate_answer(query, chunks):
    context = ""
    for chunk in chunks:
        context += f"[Source: {chunk['source']}]\n{chunk['text']}\n\n"


    prompt = USER_PROMPT_TEMPLATE.format(context=context, query=query, language=st.session_state.user_language_preference)

    body = {
        "system": [{"text": SYSTEM_PROMPT.format(language=st.session_state.user_language_preference)}],
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 512,
            "temperature": 0.3
        }
    }

    response = bedrock.invoke_model(
        modelId="global.amazon.nova-2-lite-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())

    return result["output"]["message"]["content"][0]["text"]