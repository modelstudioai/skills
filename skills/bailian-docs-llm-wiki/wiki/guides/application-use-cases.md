# application [use cases](use-cases.md)

百炼平台支持多种主流企业级通信与网站场景下的 AI 应用快速落地，核心模式为“大模型应用（百炼）+ 连接器（AppFlow）+ 知识增强（RAG）”。开发者无需从零开发后端服务或训练模型，即可在 10 分钟内完成网站、微信公众号、企业微信、钉钉等渠道的 AI 助手集成，并通过私有知识库提升回答准确性。所有方案均基于统一的百炼应用 API 和 AppFlow 低代码编排能力构建。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）或 `千问-Plus`（文档 2、3、4 中一致采用），该模型在效果、速度与成本间取得平衡，适用于客服问答类任务。  
- **可选模型**：`qwen-max`（高精度）、`qwen-turbo`（低延迟）、`qwen-flash`（文档 1 提及）等，具体能力差异见 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 的模型选型说明。  
- **核心功能**：  
  - 智能体（Agent）应用：支持 Prompt 角色设定（如“你叫小助…”）、多轮对话、工具调用（隐式）；  
  - RAG 增强：通过知识库实现私域问答，支持文件上传、向量索引、检索调用方式配置（如“必定调用”）；  
  - 多端集成：提供 Web 悬浮挂件、微信公众号消息流、企业微信/钉钉机器人 HTTP Webhook 接入能力。

> **注意**：文档 1 使用 `Qwen3.5-Plus`，而文档 2–4 统一使用 `千问-Plus`。二者为不同版本模型，实际部署时应以控制台当前可用模型列表为准，避免硬编码模型名。建议优先参考 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) 中对 `千问-Plus` 的能力描述进行选型。

## 关键参数

| 参数 | 说明 | 来源位置 | 注意事项 |
|--------|------|-----------|----------|
| `app_id` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 | 所有文档（1–4）均要求填写 | 必须与 API Key 同属一个业务空间，否则鉴权失败（见 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 常见问题） |
| `api_key` | 百炼 API 访问凭证，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建 | 所有文档（1–4）均要求配置 | 需在 AppFlow 中作为“连接凭证”复用，不可明文写入前端代码 |
| `knowledge_base_id` | 知识库 ID，用于在应用配置中启用 RAG | 文档 1、2、3、4 的“引用知识”步骤 | 调用方式支持 `必定调用` / `按需调用`，影响推理延迟与准确性权衡 |
| `WebhookUrl` | AppFlow 生成的 HTTP 回调地址，供微信/企微/钉钉转发用户消息 | 文档 2、3、4 的连接流发布后生成 | 企业微信需额外配置可信 IP 和域名主体校验（见 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)） |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `Qwen3.5-Plus` 或 `千问-Plus`）→ 配置 Prompt → 发布。  
2. **获取凭证**：记录 `app_id` 和 `api_key`；若对接微信/企微/钉钉，还需分别获取对应平台的凭证（如微信 `AppID`、企微 `AgentId/Secret`、钉钉 `Client ID/Secret`）。  
3. **配置 AppFlow 连接流**：  
   - 选择预置模板（如“微信公众号连接流”、“企业微信自建应用大模型自动回复”）；  
   - 在“账户授权”页添加百炼和目标平台（微信/企微/钉钉）的凭证；  
   - 在“执行动作”页填入 `app_id`；  
   - 发布后复制 `WebhookUrl`（微信/企微/钉钉必需）或获取悬浮挂件脚本（网站必需）。  
4. **平台侧配置**：  
   - **网站**：将悬浮挂件脚本插入 HTML `<head>` 或 `<body>` 底部；  
   - **微信公众号**：在公众号后台开启服务器配置，填入 `WebhookUrl`、Token、EncodingAESKey；  
   - **企业微信**：在应用详情页配置“API接收消息”，填入 `WebhookUrl`、Token、EncodingAESKey，并配置可信 IP；  
   - **钉钉**：在应用开发页添加机器人能力，设置消息接收模式为 **HTTP 模式**（非 Stream 模式），填入 `WebhookUrl`。  
5. **启用知识库（可选但推荐）**：上传文档 → 创建知识库 → 在百炼应用中绑定并设为“必定调用” → 重新发布应用。

## 限制和注意事项

- **免费额度**：新用户可使用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md) 提供的免费额度覆盖初期调用，超限后按 token 计费；AppFlow、FC、ADB-PG 等依赖服务单独计费。  
- **文件限制**：知识库上传单文件 ≤ 100 MB 或 1000 页，支持格式包括 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.md`, `.png`, `.jpg` 等（见文档 3、5）；本地 RAG 方案同样限制单文件 ≤ 100 MB（见 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。  
- **响应时效性**：  
  - 微信未认证公众号受 5 秒响应限制，超时即失败；建议完成认证或选用 `qwen-turbo` 加速（文档 2 常见问题）；  
  - 企业微信/钉钉无此硬性限制，但模型响应过慢仍影响用户体验。  
- **安全与合规**：  
  - 企业微信要求可信 IP 与域名主体校验，需通过 AppFlow 内网代理或自有 Nginx 解决（见文档 3）；  
  - 钉钉机器人必须使用 HTTP 模式，Stream 模式不兼容（文档 4 强调）；  
  - 前端不得暴露 `api_key`，所有百炼调用必须经 AppFlow 或后端服务中转。  
- **调试建议**：  
  - 出现 `request error` 或 `Failed to stream content` 时，优先检查 `app_id`、`api_key`、业务空间一致性（文档 1 常见问题）；  
  - 微信/企微/钉钉无响应时，查看 AppFlow 运行日志定位失败步骤（文档 2、3、4 均提供日志排查指引）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


