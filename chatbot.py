import os
from openai import OpenAI
import tiktoken

api_key=os.getenv("GOOGLE_API_KEY")
url=os.getenv("GEMINI_BASE_URL")

client=OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT="You are a fed up and sassy assistenat who hates answering questions."
MODEL="gemini-3.1-flash-lite"
TOKEN_BUDGET=1000 #Maximum tokens to keep in conversation

#Initialize conversation
messages=[ { "role":"system", "content" : SYSTEM_PROMPT }]

def get_encoding(model):
    """Get the appropriate tokenizer for the model"""

    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        print(f"Warning: Tokenizer for model '{model}' not found")
        return tiktoken.get_encoding("cl100k_base")
ENCODING=get_encoding(MODEL)

def count_tokens(text):
    return len(ENCODING.encode(text))

def total_count_tokens(messages):
    try:
        return sum(count_tokens(msg["content"]) for msg in messages)
    except Exception as e:
        print(f"[token count error]: {e}")
        return 0

def enforce_token_budget(messages,budget=TOKEN_BUDGET):
    try:
        while total_count_tokens(messages)>budget:
            if len(messages)<=2: #keep system prompt and atleast 1 msg
                break;
            messages.pop(1)
    except Exception as e:
        print(f"[token budget error]: {e}")

def chat(user_input):

    messages.append({"role":"user","content":user_input})

    response=client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=100
    )

    reply=response.choices[0].message.content
    messages.append({"role":"assistant","content":reply})

    print(total_count_tokens(messages))
    enforce_token_budget(messages)
    print(total_count_tokens(messages))
    

    return reply

while(True):
    user_input=input("You: ")
    if user_input.strip().lower() in {"exit","quit"}:
        break
    answer=chat("Hello, how are you?")
    print("Assistant:",answer)