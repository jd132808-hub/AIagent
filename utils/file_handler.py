import os.path
import hashlib
from importlib.metadata import files
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from utils.logger_handler import logger

def get_file_md5_hex(filepath: str) -> str:
    """获取文件的md5值"""
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件不存在: {filepath}")
        return None

    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]不是文件: {filepath}")
        return None

    md5_obj = hashlib.md5()

    chunk_size = 4096  # 每次读取的块大小
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)

                md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"[md5计算]读取文件出错: {filepath}, 错误信息: {str(e)}")
        return None

def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    """返回指定目录下的所有文件，过滤掉不允许的文件类型"""
    files = []

    if not os.path.isdir(path):
        logger.error(f"[文件列表]指定路径不是目录: {path}")
        return allowed_types

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))

    return tuple(files)



def pdf_loader(file_path: str, passwd = None) -> list[Document]:
    """加载pdf文件"""
    return PyPDFLoader(file_path, password=passwd).load()


def txt_loader(filepath: str) -> list[Document]:
    """加载txt文件"""
    return TextLoader(filepath,encoding="utf-8").load()





