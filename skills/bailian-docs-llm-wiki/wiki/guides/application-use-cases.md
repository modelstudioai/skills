# application [use cases](use-cases.md)

百炼平台支持将大模型能力快速集成到主流企业协作与客户触点渠道中，实现开箱即用的 RAG（[检索增强生成](../concepts/rag.md)）型 AI 助手。典型场景包括在企业微信、钉钉、微信公众号和网站嵌入智能客服，以及构建完全本地化部署的 RAG 应用。所有方案均基于统一的百炼应用模型服务与知识库能力，通过 AppFlow 低代码连接流或轻量级 SDK 实现渠道适配，无需自行维护推理服务。

## 支持的模型/功能

- **核心模型**：支持 `qwen-plus`（文档 1、3、4 默认推荐）、`qwen3.5-plus`（文档 2 明确指定）、`qwen-max` 和 `qwen3.5-flash`（文档 5 列出可选模型），模型选择需兼顾效果、延迟与成本。
- **RAG 能力**：所有集成场景均依赖百炼知识库（Knowledge Base）实现私域知识增强，支持 `.pdf`, `.docx`, `.txt`, `.md`, `.xlsx` 等 15+ 格式，单文件上限 100MB [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **本地 RAG 模式**：文档 5 提供完整本地部署方案，支持自定义文档切分、本地或云端 embedding 模型（如 `iic/nlp_gte_sentence-embedding_chinese-large`）、灵活的向量存储与 Gradio 交互界面，适用于对数据主权和定制性要求高的场景 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 与文档 2 在模型推荐上存在差异——文档 1 明确使用 `千问-Plus`，而文档 2 推荐 `Qwen3.5-Plus`。实际部署时应以百炼控制台当前可用模型列表为准，`qwen-plus` 是稳定版通用名称，`qwen3.5-plus` 为其具体迭代版本，二者在 API 层兼容。

## 关键参数

- **身份凭证**：所有外部渠道集成均需 `App ID`（百炼应用唯一标识）与 `API Key`（用于 AppFlow 或前端 SDK 鉴权），二者必须属于同一业务空间，否则触发鉴权失败 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **知识库配置**：
  - `调用方式`：推荐设为“必定调用”以确保私域问题必经检索；
  - `相似度阈值`：默认 0（不剔除），生产环境建议设为 0.3–0.6 以过滤低相关片段；
  - `召回片段数`：通常设为 3–5，平衡信息量与噪声。
- **本地 RAG 参数**（文档 5）：支持细粒度调控，包括温度（`temperature`）、最大输出长度（`max_tokens`）、上下文轮数（`history_rounds`）、召回数（`top_k`）及相似度阈值（`similarity_threshold`）。

## 使用方式

- **SaaS 渠道集成（企业微信/钉钉/公众号/网站）**：  
  统一路径为：① 在百炼创建智能体应用并发布 → ② 在对应渠道（如企业微信开发者中心）创建应用并获取凭证（CorpID/AgentID/Secret 或 AppID）→ ③ 在 AppFlow 中选用预置模板（如“企业微信自建应用大模型自动回复”）→ ④ 配置双向凭证（渠道凭证 + 百炼 API Key）与应用 ID → ⑤ 发布连接流并配置渠道端 Webhook 或消息接收地址。

- **网站嵌入**：  
  采用悬浮挂件模式，仅需在 HTML `<head>` 或 `<body>` 底部插入一段由 AppFlow 生成的 JS 脚本，无需修改后端逻辑。

- **本地 RAG 部署**（文档 5）：  
  下载 `local_rag.zip` → `pip install -r requirements.txt` → 配置百炼 API Key 环境变量 → `uvicorn main:app --port 7866` 启动服务 → 访问 `http://127.0.0.1:7866` 进行交互或 API 调用。

## 限制和注意事项

- **渠道限制**：
  - 微信公众号未认证时，仅支持被动回复（5 秒超时限制），必须完成认证才能启用主动客服能力；
  - 钉钉机器人必须配置为 **HTTP 模式**，Stream 模式不被 AppFlow 支持；
  - 企业微信需配置可信 IP 白名单，若使用第三方代理（如 Nginx），必须将代理服务器公网 IP 加入白名单，否则接口调用失败。

- **知识库与文件限制**：
  - 云端知识库文件解析耗时 1–6 分钟，大文件（>50MB）易超时；
  - 单次上传最多 200 个文件，总大小无明确上限但受解析稳定性影响；
  - 本地 RAG 方案明确提示“不建议传入超过 100 MB 的文件”，因 embedding API 存在限流 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

- **调试与可观测性**：  
  所有 AppFlow 连接流均支持添加 SLS 日志节点，可将对话请求、响应、上下文等结构化写入日志服务，用于效果分析与问题排查。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


