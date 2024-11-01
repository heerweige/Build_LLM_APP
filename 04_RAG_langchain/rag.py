from langchain_openai import ChatOpenAI,OpenAIEmbeddings
#model=dashscope.TextEmbedding.Models.text_embedding_v1
import dashscope
from dashscope import TextEmbedding

from langchain_community.document_loaders import PyPDFLoader,TextLoader #读取pdf和text文本格式
from langchain.text_splitter import RecursiveCharacterTextSplitter #分词系统
from langchain_community.vectorstores.utils import filter_complex_metadata #分词工具
from langchain_community.vectorstores import Chroma #词向量库
from langchain_core.prompts import ChatPromptTemplate #prompt工具
from langchain.schema.runnable import RunnablePassthrough #
from langchain.schema.output_parser import StrOutputParser

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

class ChatDoc:

    def __init__(self):
        self.model = ChatOpenAI(model_name="qwen-plus",#可以根据参数列表更换模型名称。如"qwen-2.5""
                                temperature=0,
                                api_key='sk-7ad9d51e442b42c585b01c817272107a',  # 确保 API 密钥是字符串，换成大家自己的api
                                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
                                )
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        # self.embeddings = TextEmbedding.call(model=dashscope.TextEmbedding.Models.text_embedding_v1,
        #                                      input = ''
        #                                      #model=TextEmbedding.Models.text_embedding_v1,
        #                                      )
        
        #self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        system_prompt = (
            '''
            You are an assistant for question-answering tasks. 
            Use the following pieces of retrieved context to answer the question. 
            If you don't know the answer, say that you don't know.
            context: {context}'''
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{question}"),
            ]
        )

    def ingest(self, file_path: str):
        print(f"Processing file: {file_path}")  # 添加调试信息
        # 判断文件类型
        if file_path.endswith('.pdf'):
            docs = PyPDFLoader(file_path=file_path).load()
        elif file_path.endswith('.txt'):
            docs = TextLoader(file_path=file_path, encoding='utf-8').load()
        else:
            raise ValueError("Unsupported file type")

        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)
        # 将文档内容传递给嵌入
        input_text = format_docs(chunks)  # 将 chunks 转换为文本格式
        self.embeddings = TextEmbedding.call(model=dashscope.TextEmbedding.Models.text_embedding_v1,
                                         input=input_text)  # 使用文档内容作为输入
    
        vector_store = Chroma.from_documents(documents=chunks, embedding=self.embeddings)
        self.retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={
        "k": 6,
        "fetch_k": 20,
        "include_metadata": True
            }
        )

        self.chain = ({"context": self.retriever| format_docs, "question": RunnablePassthrough()}
                      | self.prompt
                      | self.model
                      | StrOutputParser())


    def ask(self, query: str):
        if not self.chain:
            return "please add document first"
        response = self.chain.invoke(query)
        return response
    
    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None


# if __name__ == "__main__":
#     chat = ChatDoc()
#     chat.ingest("test.text")

#     print(chat.ask("What is critical thinking?"))