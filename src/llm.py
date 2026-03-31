import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def chat(prompt: str, system: str = "") -> str:
    if PROVIDER == "groq":
        return _groq_chat(prompt, system)
    
    else:
        return _ollama_chat(prompt, system)

def _ollama_chat(prompt: str, system: str) -> str:
    import ollama
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = ollama.chat(model=OLLAMA_MODEL, messages=messages)
    return response["message"]["content"].strip()

def _groq_chat(prompt: str, system: str) -> str:
    from groq import Groq
    client = Groq(api_key = os.getenv("GROQ_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(model=GROQ_MODEL, messages=messages)
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    response = chat(
        prompt = "Say LLM connected! and nothing else.",
        system = "You are a helpful assistant."

    )
    print(f"Response: {response}")

