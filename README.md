# 智扫通机器人智能客服

基于 Streamlit、LangChain Agent 和 RAG 的扫地机器人智能客服项目，使用 DeepSeek 对话模型、Ollama 本地嵌入模型与 Chroma 向量数据库。

## 版本

- [原始版本 v1.0-original](https://github.com/jd132808-hub/AIagent/tree/v1.0-original)：保留首次上传的完整代码与知识库资料。
- [新版 v1.1.0](https://github.com/jd132808-hub/AIagent/tree/v1.1.0)：优化 Streamlit 界面，支持快捷提问、对话导出、失败重试和逐字显示回答，修复 Python 新版本的导入兼容问题。

`main` 分支用于当前版本；历史版本通过上述标签查看和下载。

## 功能

- 通过 Streamlit 聊天界面咨询选购、使用、维护和故障排除问题。
- 检索 `data/` 中的知识库资料，生成参考资料摘要。
- 通过 Agent 工具读取使用记录并生成报告。
- 天气、位置、用户 ID 和月份工具目前使用演示数据或随机返回值。

## 项目结构

```text
app.py          Streamlit 入口
agent/          Agent、工具和中间件
config/         模型、知识库和提示词配置
data/           知识库资料及外部记录数据
model/          对话模型与嵌入模型工厂
prompts/        客服、检索摘要和报告提示词
rag/            文档入库、向量检索与摘要服务
utils/          路径、配置、文件和日志工具
```

## 本地运行

建议使用 Python 3.11 或更新版本。使用依赖清单安装项目所需的软件包（该清单不是精确版本锁文件）：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

安装并启动 Ollama，下载配置中使用的嵌入模型：

```powershell
ollama pull qwen3-embedding:4b
```

在运行项目的终端设置 DeepSeek API 密钥。当前代码使用 `ChatOpenAI`，因此读取 `OPENAI_API_KEY` 环境变量：

```powershell
$env:OPENAI_API_KEY = "你的 DeepSeek API 密钥"
```

请勿将真实密钥提交到仓库。代码目前不会自动加载 `.env` 文件。

在项目根目录依次执行知识库入库和启动界面：

```powershell
python -m rag.vector_store
python -m streamlit run app.py
```

首次入库需要 Ollama 服务可用。`rag.vector_store` 的直接运行入口还会执行一次示例检索。DeepSeek API 访问需要有效密钥和网络连接。

## 配置与本地数据

- `config/rag.yml`：对话模型与嵌入模型名称。
- `config/chroma.yml`：知识库路径、分块参数和向量库配置。
- `config/prompts.yml`：提示词文件路径。
- `config/agent.yml`：外部记录文件路径。

仓库包含源码、配置、提示词、知识库资料和外部记录文件。日志、IDE 配置、Python 缓存、密钥及生成的 Chroma 数据库和入库指纹通过 `.gitignore` 排除；克隆后需重新构建向量索引。
