# application [use cases](use-cases.md)

百炼平台支持多种主流渠道的 AI 助手快速集成，覆盖网站、企业微信、微信公众号、钉钉等私域触点，以及本地化 RAG 应用部署。所有方案均基于统一的大模型应用（App）和知识库能力，通过 AppFlow 低代码连接流实现渠道适配，无需自行维护推理服务或向量检索基础设施。核心逻辑为：**百炼提供模型与知识能力 → AppFlow 实现渠道协议桥接 → 前端/消息平台完成用户交互**。

## 支持的模型/功能

- **基础模型**：默认推荐 `Qwen3.5-Plus`（文档 1 中明确指定），亦支持 `qwen-max`、`qwen-turbo` 等通义千问系列商业模型 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。文档 5 进一步说明三者差异：`qwen-max` 性能最优，`qwen-turbo` 速度最快、成本最低，`qwen-plus` 在效果、速度、成本间均衡。
- **RAG 能力**：所有渠道方案均依赖百炼知识库（Knowledge Base）实现私有知识增强。知识库支持 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.md`, `.pptx`, `.png`, `.jpg` 等格式，单文件上限 100MB 或 1000 页 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **本地化扩展**：文档 5 提供了完整本地 RAG 方案，支持在本地执行文档切分与[向量嵌入](../concepts/embedding.md)（可选 ModelScope 模型如 `iic/nlp_gte_sentence-embedding_chinese-large`），仅将生成环节委托给百炼 API，适用于对数据主权或切分策略有强定制需求的场景 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1、2、3、4 均使用 `千问-Plus`（或 `Qwen3.5-Plus`）作为示例模型，但文档 5 的“优化回复效果”章节明确列出 `qwen-plus` 为可选项之一，且定义其为“效果、速度、成本均衡”的模型。此处无实质矛盾，`Qwen3.5-Plus` 是 `qwen-plus` 的具体版本号，二者指向同一模型族。

## 关键参数

- **身份凭证**：
  - `App ID`：百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取。
  - `API Key`：用于调用百炼 API 的密钥，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)页面创建。
- **知识库配置**：
  - `调用方式`：关键开关，如 `必定调用`（强制检索）、`按需调用`（模型自主判断）。
  - `相似度阈值`：控制召回片段质量，值越高筛选越严格（文档 2、5 均提及）。
  - `召回片段数`：决定送入大模型的上下文片段数量（文档 5 明确说明）。
- **模型参数**（本地 RAG 场景专属）：
  - `温度（temperature）`：控制输出随机性。
  - `最大回复长度（max_tokens）`：限制生成 token 数量。
  - `携带上下文轮数`：控制历史对话记忆深度（文档 5）。

## 使用方式

1. **创建百炼应用**：在百炼控制台选择“智能体应用”，配置模型（如 `Qwen3.5-Plus`）与 Prompt（例如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`），发布应用 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
2. **配置知识库**（可选但推荐）：上传私有文档（如产品手册），创建知识库，并在应用配置中启用“必定调用”。
3. **选择渠道并创建连接流**：
   - **网站**：通过 AppFlow 创建“AI助手”，配置 Web 集成，获取悬浮挂件脚本并嵌入 HTML。
   - **企业微信/微信公众号/钉钉**：使用 AppFlow 预置模板（如“企业微信自建应用大模型自动回复”），授权对应平台账号，填入百炼 `App ID` 和 `API Key`，获取 `WebhookUrl`。
4. **渠道侧配置**：
   - **网站**：粘贴脚本至 `<head>` 或 `<body>` 底部。
   - **企业微信**：在应用后台配置“API 接收消息”，填入 `WebhookUrl`、`Token`、`EncodingAESKey` 及可信 IP。
   - **微信公众号**：在后台开启“服务器配置”，填入 `WebhookUrl`；认证号需额外配置自定义菜单接口。
   - **钉钉**：在应用后台配置机器人 HTTP 模式，填入 `WebhookUrl`。
5. **验证与日志**：在对应渠道发起对话测试；如需分析，可在 AppFlow 连接流中添加 SLS 日志节点记录对话 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

> **注意**：文档 3 指出，未认证的微信公众号受 5 秒响应限制，若百炼应用响应超时将导致失败；此时应选用 `qwen-turbo` 模型或优化 Prompt（如添加“请总是给出简短的回答”）以提速。

## 限制和注意事项

- **免费额度**：新用户免费额度可覆盖教程消耗，额度用尽后按 token 计费；AppFlow、函数计算 FC、ADB-PG 等依赖云产品单独计费 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **文件处理限制**：云端知识库单文件上限 100MB 或 1000 页；本地 RAG 方案因受限于 Embedding API 限流，亦不建议传入 >100MB 文件（文档 5）。
- **渠道特异性限制**：
  - 微信公众号未认证时，仅支持被动回复（5秒超时），且无法同时启用自定义菜单（文档 3）。
  - 钉钉机器人必须配置为 **HTTP 模式**，Stream 模式不被 AppFlow 支持（文档 4）。
  - 企业微信要求可信 IP 与域名主体一致，若无自有备案域名，需通过 AppFlow 的 Nginx 代理或 ECS 实例转发解决（文档 2）。
- **调试要点**：常见 `request error` 或 `Failed to stream content` 多因 `API Key`、`App ID`、业务空间标识（`AgentKey`）三者不匹配或失效导致，需逐一核验 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


