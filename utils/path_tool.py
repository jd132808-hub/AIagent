"""
为整个项目提供统一的绝对路径
"""
import os
from email.contentmanager import maintype

from dashscope.acli.extensions import current
from sympy.core.evalf import get_abs


def get_project_root() -> str:
    """
    获取工程所在的根目录
    :return: 字符串目录
    """

    #当前文件的绝对路径
    current_file = os.path.abspath(__file__)
    #上一层目录
    current_dir = os.path.dirname(current_file)
    #根目录
    project_root = os.path.dirname(current_dir)

    return project_root


def get_abs_path(relative_path: str) -> str:
    """
    传递相对路径，得到绝对路径
    :param relative_path: 相对
    :return: 绝对
    """

    project_root = get_project_root()
    return os.path.join(project_root, relative_path)


if __name__ == '__main__':
    print(get_abs_path("config/config.txt"))





















