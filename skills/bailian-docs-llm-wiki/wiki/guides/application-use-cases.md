# application [[use-cases|use cases]]

百炼平台提供多端集成与本地部署方案，支持开发者快速将大模型问答能力接入 Web、企微、公众号、钉钉及本地业务系统。基于 [[智能体应用]] 与 [[AppFlow]] 服务，可通过零代码/低代码方式实现 [[RAG]] 增强、多轮对话及私有 [[知识库]] 挂载。

## 支持的模型/功能
- **基础模型**：默认推荐通义千问商业版系列（`qwen-plus`、`qwen-max`、`qwen-turbo`）。可根据业务对推理精度、延迟与 Token 成本的权衡进行选型。
- **核心能力**：多端消息网关接入（Webhook/HTTP）、[[知识库]] 检索增强、多轮上下文记忆、对话日志持久化至 SLS、卡片交互与推理过程透传。
- **集成载体**：支持网页悬浮脚本注入、第三方 IM 平台应用模板编排，以及基于 Python/Gradio 的本地化独立服务部署（数据不出域）。

## 关键参数
- **应用凭证**：百炼 `API Key` 与 `App ID`；第三方平台凭证（如企微 `CorpID`/`AgentId`/`Secret`、公众号 `AppID`/`AppSecret`、钉钉 `ClientID`/`ClientSecret`）。
- **模型推理参数**：`temperature`（控制生成随机性）、`max_tokens`（限制最大输出长度）、`top_p`（核采样策略）。
- **RAG 检索参数**：`top_k`/`召回片段数`（控制参考文本数量）、`similarity_threshold`（相似度阈值，设为 0 表示不剔除低相似度片段）、`embedding_model`（向量嵌入模型）、`chunk_strategy`（文档切分策略）。
- **对话控制参数**：`history_turns`（携带历史对话轮数，设为 1 时不参考上下文）。

## 使用方式
- **Web 页面集成**：在 [[AppFlow]] 控制台配置 Web 页面集成方案，生成悬浮挂件部署脚本。直接将该脚本粘贴至业务站点 HTML 的 `<body>` 末尾即可生效。详见：[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- **企微/钉钉/公众号集成**：使用 [[AppFlow]] 预置连接流模板，分别配置平台凭证与百炼应用 ID。在目标 IM 后台将消息接收地址绑定为生成的 `WebhookUrl`，并配置可信 IP/域名白名单。详见：[10分钟在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat-in-10-minutes.md)
- **本地化 RAG 部署**：适用于对向量库驻留或 Embedding 模型有强管控要求的场景。解压示例工程后安装依赖，配置百炼 `API Key` 环境变量，通过 `uvicorn main:app --port 7866` 启动服务。支持临时文件上传与本地目录持久化知识库构建。详见：[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)

## 限制和注意事项
- **公众号未认证超时限制**：未完成微信认证的订阅号响应窗口仅为 5 秒，超时平台将丢弃请求。需精简系统 Prompt 或切换至低延迟模型（如 `qwen-turbo`）。
- **钉钉消息模式限制**：当前仅支持 `HTTP` 消息接收模式，若配置为 `Stream` 模式将导致消息无法返回。
- **文件解析与限流**：单文档建议控制在 100 MB 以内。知识库上传后的解析、分块与向量化索引构建通常耗时 1~6 分钟，期间新建查询可能无法命中最新文档。
- **网络与鉴权拦截**：第三方 IM 平台对回调地址的域名备案主体及服务器出口 IP 有严格校验，需按控制台指引配置可信 IP 白名单或使用 Nginx 反向代理。

> **注意**：文档 1 中示例模型标注为 `Qwen3.5-Plus`，而文档 2、3、4 及本地部署指南均标注为 `千问-Plus`（`qwen-plus`）。模型版本命名与控制台可用性可能随迭代调整，实际创建 [[智能体应用]] 时请以百炼控制台模型下拉列表为准。建议在 [[应用评测]] 阶段结合业务 QPS 预算进行压测验证。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [10分钟在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)

