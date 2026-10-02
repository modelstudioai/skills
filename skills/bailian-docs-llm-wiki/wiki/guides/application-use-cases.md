# application [use cases](use-cases.md)

阿里云百炼平台支持将大模型能力快速集成到主流企业通讯与业务平台中，实现开箱即用的 AI 助手、智能客服或机器人。所有方案均基于统一的 RAG 应用架构，通过百炼应用提供推理服务，由 AppFlow 或本地代码桥接外部渠道，无需从零开发后端逻辑。核心流程一致：创建百炼智能体应用 → 配置知识库（可选）→ 通过连接流/SDK/前端脚本对接目标平台。

## 支持的模型/功能

- **基础模型**：所有用例均支持 `qwen-plus`（文档 1、3、4 明确指定）、`qwen-turbo`（文档 3 提及用于提速）、`qwen-max`（文档 5 列为可选）及 `qwen3.5-plus`（文档 2 指定）。`qwen-plus` 是多数场景的默认推荐，兼顾效果、速度与成本。
- **RAG 能力**：全部用例均支持知识库增强，文件格式覆盖 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.md`, `.pptx`, `.png`, `.jpg` 等（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)、[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)、[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 均明确列出）。
- **部署形态**：
  - **云端托管**：企业微信、微信公众号、钉钉、网站等场景均通过百炼应用 + AppFlow 连接流实现零代码集成。
  - **本地部署**：支持完全本地运行的 RAG 应用，检索环节在本地执行，生成环节调用百炼 API（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

> **注意**：文档 1 与文档 2 在模型选择上存在不一致。文档 1 明确要求使用 `千问-Plus`，而文档 2 指定 `Qwen3.5-Plus`。实际开发中应以控制台当前可用模型列表为准，`qwen-plus` 为稳定通用选项；`Qwen3.5-Plus` 属于新版本模型，需确认其已在目标地域和业务空间中发布。

## 关键参数

- **应用 ID 与 API Key**：所有云端集成方案（企业微信、公众号、钉钉、网站）均需在百炼控制台获取应用 ID 和 API Key，并在 AppFlow 中配置凭证（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)、[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。
- **知识库配置参数**：
  - **调用方式**：`必定调用`（文档 2、3、4）、`按需调用`（文档 1 提及“知识”区域可设置）。
  - **相似度阈值**：文档 1、5 明确提及，用于过滤低相关性召回片段。
  - **召回片段数**：文档 5 明确列为可调参数，影响信息输入量。
- **本地 RAG 参数**（仅文档 5）：
  - **模型参数**：温度（`temperature`）、最大回复长度（`max_tokens`）、上下文轮数（`history_rounds`）。
  - **RAG 参数**：召回片段数、相似度阈值、嵌入模型选择（支持云端 API 或本地 ModelScope 模型）。

## 使用方式

- **云端集成（推荐）**：
  1. 在百炼控制台创建智能体应用，配置 Prompt 并发布。
  2. 在对应平台（企业微信/公众号/钉钉）创建应用并获取凭证（如 AgentId/Secret、AppID、Client ID/Secret）。
  3. 在 AppFlow 控制台使用预置模板创建连接流，关联平台凭证与百炼应用 ID/API Key。
  4. 将连接流生成的 Webhook URL 或悬浮挂件脚本配置到目标平台（如企业微信的 API 接收消息、网站 HTML 的 `<script>` 标签）。
- **本地部署（高级）**：
  - 下载 `local_rag.zip`，安装依赖（Python 3.9–3.12），配置百炼 API Key 环境变量。
  - 上传知识文件（临时或持久化创建知识库）。
  - 启动服务（`uvicorn main:app --port 7866`），通过 Gradio 界面交互或调用自动生成的 API（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

## 限制和注意事项

- **平台认证要求**：
  - 微信公众号：未认证订阅号仅支持被动回复（5 秒超时限制），已认证方可使用客户消息接口（[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）。
  - 企业微信/钉钉：需确保账号具备开发者权限（文档 1、4 明确提示）。
- **安全与网络**：
  - 企业微信要求配置可信 IP 白名单，若使用第三方代理（如 AppFlow 默认域名），需通过 Nginx 代理或计算巢实例解决（文档 1）。
  - 微信公众号服务器配置 URL 若报“严重安全风险”，需采用服务商授权模式重配（文档 3）。
- **文件与性能**：
  - 单文件上传上限为 100 MB（文档 1、5），超大文件建议分拆或使用本地 RAG 方案。
  - 本地 RAG 创建知识库时，受 Embedding API 限流影响，大文件可能耗时较长（文档 5）。
- **调试与日志**：
  - 所有 AppFlow 连接流均支持添加 SLS 日志节点记录对话（文档 1、3、4 共同提及）。
  - 常见错误（如 `request error`、`Failed to stream content`）多源于 API Key 失效、应用 ID 错误或跨业务空间鉴权失败（文档 2、3）。

> **注意**：文档 4 中关于钉钉机器人的“消息接收模式”强调必须选择 **HTTP 模式**，而文档 2、3、1 均未对各自平台的接收模式做此限定。此为钉钉平台特有约束，开发者在配置钉钉机器人时须严格遵守，否则无法返回消息。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


