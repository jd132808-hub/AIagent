from langchain_core.documents import Document
from utils.path_tool import get_abs_path
import os
from utils.file_handler import pdf_loader, txt_loader,listdir_with_allowed_type,get_file_md5_hex
from langchain_chroma import Chroma
from utils.config_handler import chroma_conf
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.logger_handler import logger

class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_conf["persist_directory"],
        )


        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(
            search_kwargs={
                "k": chroma_conf["k"],
            }
        )

    def load_document(self):
        """
        从数据文件夹内部读取数据文件，转为向量存入
        :return:
        """

        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                # 创建文件
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False

            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()    #移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
                    if line == md5_for_check:
                        return True  #md5值已存在，说明文件未修改过

                return False  #md5值不存在，说明文件已修改过或是新文件


        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        def get_file_documents(read_path: str):
            """
            根据文件路径获取文件内容
            :param read_path:
            :return:
            """
            if read_path.endswith("txt"):
                return txt_loader(read_path)

            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []

        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            allowed_types=tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已存在知识库中，跳过加载")
                continue

            try:
                documents: list[Document] = get_file_documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}文件内容为空，跳过加载")
                    continue

                split_documents: list[Document] = self.spliter.split_documents(documents)

                if not split_documents:
                    logger.warning(f"[加载知识库]{path}文件内容分割后为空，跳过加载")
                    continue

                #将内容存入向量库
                self.vector_store.add_documents(split_documents)


                #记录md5值，避免重复
                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库]{path}文件内容已成功加载到知识库中")

            except Exception as e:
                # exc_info=True参数会在日志中打印异常的堆栈信息，方便调试
                logger.error(f"[加载知识库]{path}文件内容加载失败，错误信息: {str(e)}",exc_info=True)
                continue


if __name__ == '__main__':
    vs = VectorStoreService()


    vs.load_document()

    retriever = vs.get_retriever()

    res = retriever.invoke("迷路")

    for r in res:
        print(r.page_content)
        print("*"*20)





















