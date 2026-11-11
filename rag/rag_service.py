
"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料传入模型，生成回答，并返回给用户。
"""
from langchain_core.documents import Document

from langchain_core.output_parsers import StrOutputParser

from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model


def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt


class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()  #向量存储
        self.retriever = self.vector_store.get_retriever()  #向量检索器
        self.prompt_text = load_rag_prompts()  #提示词文本
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)  #提示词模板
        self.model = chat_model  #模型
        self.chain = self._init_chain()  #链式调用


    def _init_chain(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain


    def retrieve_docs(self, query: str) -> list[Document]:   #得到检索文档
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:

        context_docs = self.retrieve_docs(query)  #检索文档

        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"\n[参考资料{counter}]:\n{doc.page_content}\n参考元数据: {doc.metadata}\n"

        return self.chain.invoke(
            {
                "input": query,      #用户提问
                "context": context,  #参考资料
            }
        )


if __name__ == '__main__':
    rag = RagSummarizeService()

    print(rag.rag_summarize("小户型适合哪些扫地机器人"))





















