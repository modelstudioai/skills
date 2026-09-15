# application [use cases](use-cases.md)

百炼平台支持多种主流企业级通信与协作场景的 AI 助手快速集成，包括网站嵌入、微信公众号、企业微信、钉钉等渠道。所有方案均基于统一的大模型应用（智能体）和可复用的知识库能力，通过 AppFlow 低代码连接流实现模型服务与业务入口的解耦对接，开发者只需关注模型配置、知识注入与渠道适配，无需自行维护推理服务或消息协议。

## 支持的模型/功能

- **核心模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）或 `千问-Plus`（文档 2、3、5 中一致采用），该模型在效果、速度与成本间取得平衡，适用于通用客服问答场景；也可按需切换为 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及但未在其他文档中出现，需注意兼容性）。
- **核心功能**：
  - 基于 RAG 的私域知识增强问答（所有 5 篇文档均强调此能力）
  - 多渠道消息接入与响应（Web 悬浮窗、微信公众号被动/主动回复、企业微信自建应用、钉钉机器人 HTTP 模式）
  - 可视化 Prompt 配置与角色设定（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）
  - 知识库全生命周期管理（上传、切分、向量化、引用策略配置）

> **注意**：文档 1 明确推荐 `Qwen3.5-Plus`，而文档 2、3、5 均使用 `千问-Plus`。二者为不同版本模型，实际调用时需确认控制台可用模型列表及 API 兼容性，避免因模型名不一致导致部署失败。建议以 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 中的 `Qwen3.5-Plus` 为准进行初始验证。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源依据 |
|----------|--------|------|----------|
| **认证凭证** | `API Key` | 百炼平台调用凭证，需在 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建并保管 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| | `App ID` | 百炼应用唯一标识，在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面获取 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| **知识库配置** | `调用方式` | 控制知识检索触发逻辑，如 `必定调用`（强制检索）、`按需调用`（条件触发） | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| | `相似度阈值` | 过滤低相关性召回片段，默认值影响精度与噪声比 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **模型推理** | `Temperature` | 控制输出随机性，值越高越发散 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `Max Tokens` | 限制生成长度，影响回答详略程度 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |

## 使用方式

1. **创建大模型应用**：在百炼控制台 → 应用管理 → 创建智能体应用，选择模型（如 `Qwen3.5-Plus`），配置 Prompt，发布应用。
2. **准备私有知识**（可选但推荐）：
   - 上传文件至 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) 或 [文件中心](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)
   - 在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 创建标准版知识库，关联上传文件
   - 在应用配置中启用知识库，设置调用方式（如 `必定调用`）
3. **选择渠道并配置连接流**：
   - **网站嵌入**：使用 AppFlow 创建 AI 助手 → Web 页面集成 → 获取悬浮挂件脚本 → 插入 HTML
   - **微信公众号**：使用 AppFlow 微信模板 → 授权公众号 → 配置百炼凭证 → 发布连接流（注意区分认证/未认证公众号模板）
   - **企业微信/钉钉**：使用对应模板 → 配置企业微信/钉钉凭证（企业 ID/AgentId/Secret 或 Client ID/Secret）→ 配置百炼凭证 → 获取 WebhookUrl → 在企业微信/钉钉后台完成 API 接收或机器人 HTTP 地址配置
4. **验证与日志**：通过渠道端发起对话测试；如需分析，可在 AppFlow 连接流中添加 SLS 日志节点记录对话上下文。

## 限制和注意事项

- **免费额度**：新用户可使用 [新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md) 覆盖初期调用消耗，额度耗尽后按 token 计费；AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费。
- **知识文件限制**：
  - 云端知识库：单文档最大 100MB 或 1000 页，图片单张 ≤20MB，最多 200 个文件；文件默认存储于新加坡区域（文档 2）。
  - 本地 RAG 应用：不建议上传 >100MB 文件，受限于 Embedding API 限流（文档 4）。
- **渠道特异性限制**：
  - 微信公众号未认证时仅支持被动回复，响应超时为 5 秒，需优化 Prompt 或选用 `qwen-turbo` 保时效（文档 3）。
  - 钉钉机器人**必须**配置为 HTTP 模式，Stream 模式不兼容 AppFlow（文档 5）。
  - 企业微信配置 API 接收时，若域名主体校验失败，需配置自有备案域名或使用 AppFlow 内网代理（文档 2）。
- **调试要点**：
  - 出现 `request error` 或无响应时，优先检查 `API Key` 状态、`App ID` 正确性、以及智能体与 API Key 是否在同一业务空间（文档 1）。
  - 企业微信报错“可信 IP 属于第三方服务商”，需通过 ECS 或托管实例做请求转发，并将代理 IP 加入企业微信可信 IP 列表（文档 2）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


