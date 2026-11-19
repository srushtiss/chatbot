import os
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken

class Chatbot:
    def __init__(self,api_key,url,model="gemini-3.1-flash-lite",temperature=0.7,max_tokens=100,token_budget=1000,system_prompt="You are a helpful assistant."):
        self.client=OpenAI(api_key=api_key,base_url=url)
        self.model=model
        self.temperature=temperature
        self.max_tokens=max_tokens
        self.token_budget=token_budget
        self.messages=[{"role":"system","content":system_prompt}]
        self.encoding=self._get_encoding()

    def _get_encoding(self):
        """Get the appropriate tokenizer for the model"""
        try:
            return tiktoken.encoding_for_model(self.model)
        except KeyError:
            print(f"Warning: Tokenizer for model '{self.model}' not found")
            return tiktoken.get_encoding("cl100k_base")

    def _count_tokens(self,text):
        return len(self.encoding.encode(text))

    def _total_tokens_used(self):
        try:
            return sum(self._count_tokens(msg["content"]) for msg in self.messages)
        except Exception as e:
            print(f"[token count error]: {e}")
            return 0


    def _enforce_token_budget(self):
        try:
            while self._total_tokens_used()>self.token_budget:
                if len(self.messages)<=2: #keep system prompt and atleast 1 msg
                    break;
                self.messages.pop(1)
        except Exception as e:
            print(f"[token budget error]: {e}")

    def chat(self,user_input):
       self.messages.append({"role":"user","content":user_input})

       response=self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

       reply=response.choices[0].message.content
       self.messages.append({"role":"assistant","content":reply})

       self._enforce_token_budget()
       return reply

load_dotenv() #reads the .env file and sets the variables

api_key=os.getenv("GOOGLE_API_KEY")
url=os.getenv("GEMINI_BASE_URL")

if not api_key:
    raise ValueError("No API key found. Set api key")

bot=Chatbot(api_key=api_key,url=url)


while True:
    user_input=input("You: ")
    if user_input.strip().lower() in {"exit","quit"}:
        break
    answer=bot.chat(user_input)
    print("Assistant:",answer)