from venv import logger

from utils.config_handler import prompts_conf
from utils.path_tool import get_abs_path


def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompts]在yaml配置文件中缺少main_prompt_path键")
        raise e

    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompts]读取系统提示词文件失败: {system_prompt_path}, 错误信息: {str(e)}")
        raise e


def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml配置文件中缺少rag_summarize_path键")
        raise e

    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]读取系统提示词文件失败: {rag_prompt_path}, 错误信息: {str(e)}")
        raise e


def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompts]在yaml配置文件中缺少report_prompt_path键")
        raise e

    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompts]读取系统提示词文件失败: {report_prompt_path}, 错误信息: {str(e)}")
        raise e



if __name__ == '__main__':
    print(load_report_prompts())





















