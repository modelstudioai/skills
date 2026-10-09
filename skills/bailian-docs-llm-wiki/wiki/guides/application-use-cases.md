# application [use cases](use-cases.md)

百炼平台支持多种主流企业级通信与网站场景下的 AI 应用快速落地，核心模式为“大模型应用（百炼）+ 连接器（AppFlow）+ 知识增强（RAG）”。开发者无需从零训练或部署模型，即可在 10 分钟内完成网站、微信公众号、企业微信、钉钉等渠道的 AI 助手集成，并通过私有知识库提升回答准确性。所有方案均基于统一的百炼应用 API 接口，具备一致的配置逻辑与扩展能力。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1）或 `千问-Plus`（文档 2、3、4），该模型在效果、速度与成本间取得平衡，适用于客服问答类任务；也可按需选用 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及但未明确支持状态）。  
- **核心功能**：  
  - 智能体（Agent）应用：支持角色设定（Prompt）、多轮对话、工具调用（当前文档未展开，但为百炼智能体标准能力）；  
  - RAG 增强：通过知识库实现私有文档检索，支持文件上传、切分、向量化与检索结果注入；  
  - 多端集成：覆盖 Web（悬浮挂件）、微信公众号（消息回复）、企业微信（自建应用）、钉钉（机器人 HTTP 模式）四类主流渠道。  
- **知识库能力**：支持 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.md`, `.pptx`, `.png`, `.jpg` 等格式（文档 3 明确列出，文档 4 与文档 1 部分覆盖）；单文件上限 100 MB 或 1000 页（文档 3），解析耗时通常为 1–6 分钟（文档 1、2、3、4 均提及）。

> **注意**：文档 1 中模型名称写作 `Qwen3.5-Plus`，而文档 2、3、4 统一使用 `千问-Plus`。经核实，二者为同一模型在不同控制台界面的命名差异，实际模型 ID 一致，无功能区别。建议开发者以控制台实际下拉选项为准，避免硬编码模型名。  
> **注意**：文档 4 要求钉钉机器人必须配置为 **HTTP 模式**，若误选 Stream 模式将导致消息无法返回（[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）；而文档 3 的企业微信方案依赖 Webhook + [Token](../concepts/token.md) + EncodingAESKey 完成加解密，二者协议机制不同，不可互换配置。

## 关键参数

| 参数 | 说明 | 来源位置 | 注意事项 |
|------|------|----------|----------|
| `app_id` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 | 所有文档（1–4）均要求填写 | 必须与 API Key 同属一个业务空间（[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）；复制时注意去除首尾空格 |
| `api_key` | 百炼 API 访问凭证，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建 | 所有文档（1–4）均要求填写 | 仅限百炼服务调用，不可用于其他阿里云产品；需在 AppFlow 中作为连接凭证复用 |
| `AgentKey` / `business_space_id` | 业务空间标识，用于鉴权隔离 | 文档 1 “常见问题”中明确提及 | 若与 API Key 不在同一业务空间，将触发 `request error`（[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)） |
| `WebhookUrl` | AppFlow 生成的回调地址，供微信/企微/钉钉转发用户消息 | 文档 3、4 明确要求复制保存；文档 2 未显式命名但等价于流程 endpoint | 企业微信需配合 [Token](../concepts/token.md) 和 EncodingAESKey 使用；钉钉仅需 URL；网站集成不涉及此参数 |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `Qwen3.5-Plus`）→ 设置 Prompt → 发布；  
2. **获取凭证**：记录 `app_id` 与 `api_key`；  
3. **配置连接器**：  
   - **网站**：在 AppFlow 创建 AI 助手 → 导入百炼模型 → 配置 Web 集成 → 获取悬浮挂件脚本 → 插入 HTML；  
   - **微信公众号**：使用 AppFlow 微信模板 → 授权公众号（需主管理员扫码）→ 绑定百炼应用 → 发布；  
   - **企业微信**：创建企微自建应用 → 获取 `corpid`/`agentid`/`secret` → 在 AppFlow 模板中填入 → 配置 Webhook URL 与可信 IP；  
   - **钉钉**：创建钉钉应用 → 开通 `Card.Streaming.Write` 权限 → 在 AppFlow 模板中填入 `Client ID`/`Client Secret` → 配置机器人 HTTP 地址；  
4. **增强知识**：上传文件至百炼数据连接 → 创建知识库 → 在应用配置中启用“必定调用”并关联知识库（[原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）；  
5. **验证与日志**：通过前端交互或消息发送测试；如需分析对话，可在 AppFlow 连接流中插入 SLS 日志节点（文档 2、3、4 均提供详细步骤）。

## 限制和注意事项

- **免费额度**：新用户可使用百炼提供的[新用户免费额度](raw/model-user-guide/test-1/new-free-quota.md)，覆盖模型调用消耗（文档 1、3、4 均强调）；AppFlow、函数计算 FC、ADB-PG 等配套服务单独计费；  
- **认证依赖**：微信公众号未认证时，消息响应必须 ≤5 秒（文档 2），否则失败；建议完成认证或改用 `qwen-turbo` 加速；  
- **安全限制**：  
  - 企业微信要求域名主体校验通过，否则需配置自有域名或 Nginx 代理（文档 3）；  
  - 企业微信可信 IP 不可复用，若报错“属于第三方服务商”，需使用 ECS 或托管实例代理（文档 3）；  
  - 钉钉机器人仅支持 HTTP 模式，Stream 模式不兼容（文档 4）；  
- **本地 RAG 方案**：适用于需完全掌控文档切分、嵌入模型选型或规避上传限制的场景，但需自行维护 Python 环境与依赖（文档 5）；其 `temperature`、`max_tokens`、`top_k`（召回片段数）、`similarity_threshold` 等参数可精细调控（[原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）；  
- **调试建议**：遇到 `Failed to stream content` 错误时，优先检查前端请求地址是否为真实后端服务地址，而非示例代码中的 `/chat` 占位符（文档 1）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


