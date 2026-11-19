import os
from openai import OpenAI

api_key=os.getenv("GOOGLE_API_KEY")

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

client=OpenAI(
    api_key=api_key,
    base_url=GEMINI_BASE_URL
)



SYSTEM_PROMPT="You are a fed up and sassy assistenat who hates answering questions."
messages=[ { "role":"system", "content" : SYSTEM_PROMPT }]


def chat(user_input):

    messages.append({"role":"user","content":user_input})

    response=client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=messages,
        temperature=0.7,
        max_tokens=100
    )

    reply=response.choices[0].message.content
    messages.append({"role":"assistant","content":reply})


    return reply

while(True):
    user_input=input("You: ")
    if user_input.strip().lower() in {"exit","quit"}:
        break
    answer=chat("Hello, how are you?")
    print("Assistant:",answer)