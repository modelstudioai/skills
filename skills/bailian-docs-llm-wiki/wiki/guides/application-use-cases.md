# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景，所有方案均基于统一的 RAG（检索增强生成）架构，通过百炼大模型应用 + AppFlow 低代码连接流实现。核心流程一致：创建百炼智能体应用 → 配置私有知识库 → 使用 AppFlow 关联目标渠道 → 发布并验证。开发者可复用同一套知识库和提示词策略，降低多端维护成本。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定），该模型在效果、速度与成本间取得平衡，适用于客服问答类任务；其他可用模型包括 `qwen-max`、`qwen-plus`、`qwen3.5-flash`（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)），其中 `qwen3.5-flash` 更适合对响应延迟敏感的场景（如未认证公众号的 5 秒限制）。
- **核心能力**：所有用例均默认启用 RAG，支持上传 `.pdf`、`.docx`、`.txt`、`.xlsx` 等格式文档（文档 2 和文档 3 均列出完整支持列表），通过百炼知识库实现私域知识注入；同时支持自定义 Prompt 引导角色与回复风格（如“请总是给出简短的回答”）。
- **扩展能力**：支持对话日志记录至 SLS（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 和 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) 均提供详细配置步骤）；钉钉场景额外支持卡片消息与思考过程展示（文档 4）。

> **注意**：文档 1 明确要求模型选择 `Qwen3.5-Plus`，而文档 2、3、4 均仅写为“千问-Plus”。经核对百炼控制台当前模型列表，“千问-Plus”实为 `Qwen3.5-Plus` 的旧称，属同一模型。此为命名不一致，非功能差异，建议统一采用 `Qwen3.5-Plus` 作为标准标识。

## 关键参数

| 参数 | 说明 | 取值建议 | 来源依据 |
|--------|------|-----------|----------|
| **调用方式** | 知识库在推理时的触发策略 | `必定调用`（确保私域问题必查知识） | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| **相似度阈值** | 过滤低相关性检索片段 | 默认 0（不过滤），可调高至 0.6~0.8 提升精准度 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **召回片段数** | 每次检索返回给模型的文本段数量 | 3~5（平衡信息量与噪声） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **温度（temperature）** | 控制生成随机性 | 0.1~0.3（客服场景需确定性回复） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |

## 使用方式

1. **创建百炼应用**：进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择**智能体应用**，配置模型（`Qwen3.5-Plus`）、Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）并发布。
2. **配置知识库**：上传文档至 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) 或 [文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)，在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面创建标准版知识库，并在应用配置中启用 `必定调用`。
3. **创建渠道连接流**：
   - **网站**：在 AppFlow 创建 **模型服务AI助手**，导入百炼应用凭证，配置 Web 页面集成（悬浮挂件脚本）。
   - **微信公众号/企业微信/钉钉**：使用对应 [AppFlow 模板](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/fastTemplate/)，完成渠道凭证（AppID/AgentId/Client ID 等）与百炼 API Key 的授权，填写应用 ID 后发布。
4. **渠道侧配置**：按各平台要求完成回调地址（WebhookUrl）、[Token](../concepts/token.md)、可信 IP/域名等配置（如企业微信需配置 [可信IP](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)，钉钉需启用 `Card.Streaming.Write` 权限）。

## 限制和注意事项

- **免费额度**：新用户可使用 [新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md) 覆盖初期调用，额度耗尽后按 token 计费；AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费。
- **认证依赖**：微信公众号未认证时，被动回复受 5 秒超时限制，必须选用专用模板并考虑模型响应速度（文档 3 明确指出可切换为 `qwen3.5-flash` 或优化 Prompt 缩短回复）。
- **安全校验**：企业微信/微信公众号配置 Webhook 时可能因域名主体校验失败而报错，需通过 AppFlow [域名管理](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/domain/manage) 添加二级域名或配置 Nginx 代理（文档 2 详述解决方案）。
- **调试要点**：若出现 `request error` 或无响应，优先检查三项是否匹配且有效：① 百炼 API Key 状态；② 百炼应用 ID；③ AppFlow 连接流中配置的凭证与业务空间（AgentKey）是否同属一个百炼业务空间（文档 1 的“常见问题”章节明确列出此排查项）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


