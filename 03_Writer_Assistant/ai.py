from openai import OpenAI

#基本身份设定
standards = """
you are a best writer assistant.
you follow 3 key standards that make your writing clear, concise, and engaging.
Clarity means Simple Language, Logical Structure, Focus.
Conciseness means Brevity, Directness, Efficiency.
Engagement means Vivid Language, Active Voice, Varied Sentence Structure.
you can write in english and chinese.
"""

client = OpenAI(
    api_key='sk-4ab55d5516414bdb97a6a53b823f0dde',  # 这里可以替换为 os.getenv("DASHSCOPE_API_KEY") 如果使用环境变量
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

class WriterAssistant:
    def __init__(self,model='qwen-plus'):#初始化千问模型
        self.messages = [{"role": "system", "content": standards}]#系统身份认定，prompt添加
        #模型api接口
        self.client = OpenAI(
            api_key='sk-4ab55d5516414bdb97a6a53b823f0dde',  # 这里可以替换为 os.getenv("DASHSCOPE_API_KEY") 如果使用环境变量
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        
        self.model = model #模型选择
        self.reply = None #模型回复

    def set_model(self,model): #封装模型设计函数
        self.model = model

    def clear_messages(self): #清空模型记忆，初始化
        self.messages = [{"role": "system", "content": standards}]

    def openai_response(self): #模型回答函数
        chat_response = self.client.chat.completions.create(
            model=self.model, #封装模型设计函数
            messages=self.messages #prompt接入
        )
        self.reply = chat_response.choices[0].message.content #模型回答

    # def ollama_response(self):
    #     chat_response = ollama.chat(
    #         model=self.model, 
    #         messages=self.messages
    #     )
    #     self.reply = chat_response['message']['content']


    def call_LLM(self):
        self.openai_response()


    def improve_write(self,text):#功能代码1
        self.clear_messages()
        prompt = f"Please improve the following text: {text}, output should in chinese and english."
        self.messages.append({"role": "user", "content": prompt})
        self.call_LLM()

    def fix_grammar(self,text):#功能代码2
        self.clear_messages()
        prompt = f"Please fix the grammar in the following text: {text}, output should include correct text and explain the error. output should in chinese and english."
        self.messages.append({"role": "user", "content": prompt})
        self.call_LLM()

    def new_article(self,text):#功能代码3
        self.clear_messages()
        prompt = f"Please write a new article based on the following topic: {text}, output should in chinese and english."
        self.messages.append({"role": "user", "content": prompt})
        self.call_LLM()

    def get_reply(self):#返回函数
        return self.reply

if __name__ == "__main__":
    gpt = WriterAssistant()
    gpt.new_article("life and journey")
    reply = gpt.get_reply()
    print(reply)