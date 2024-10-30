from openai import OpenAI
# import ollama

client = OpenAI(
    api_key='sk-4ab55d5516414bdb97a6a53b823f0dde',  # 这里可以替换为 os.getenv("DASHSCOPE_API_KEY") 如果使用环境变量
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def openai_response(model,messages):
    chat_response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    reply = chat_response.choices[0].message.content
    return reply

# def ollama_response(model,messages):
#     chat_response = ollama.chat(model=model, 
#                     messages=messages)
#     reply = chat_response['message']['content']
#     return reply

def call_LLM(model,messages):
    reply = openai_response(model, messages)

def generate_code(model,language,requirement,messages):
    generate_prompt = f"Please generate a {language} code that meets the following requirements: {requirement}"
    messages.append({"role": "user", "content": generate_prompt})
    reply = openai_response(model, messages)
    return reply

def fix_code(model,language,code,error,messages):
    fix_prompt = f"Please fix the following {language} code: {code}, and code get the error: {error}, Respond with the fixed code and explain the error."
    messages.append({"role": "user", "content": fix_prompt})
    reply = openai_response(model, messages)
    return reply

def explain_code(model,language, code,messages):
    explain_prompt = f"Please read the following {language} code: {code}, explain the code for beginners, give a alternative solution, and give some improvement advice."
    messages.append({"role": "user", "content": explain_prompt})
    reply = openai_response(model, messages)
    return reply

if __name__ == "__main__":
    reply = generate_code("qwen-plus", 
                        "python",
                        "create a function to find a max from list",
                        [{"role": "system", "content": "you are a code assistant"}])

    print(reply)