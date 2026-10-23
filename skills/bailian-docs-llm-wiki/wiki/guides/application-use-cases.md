# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景。所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 低代码连接流实现，无需自行部署模型或编写后端逻辑。核心流程一致：创建百炼智能体应用 → 配置私有知识库 → 在目标渠道通过 AppFlow 绑定并发布。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1）、`千问-Plus`（文档 2、3、4），该模型在效果、速度与成本间取得平衡；也可选用 `qwen-max`（高精度）、`qwen3.5-flash`（低延迟）或 `qwen-turbo`（文档 3 提及用于提速）。
- **RAG 能力**：所有用例均依赖百炼知识库功能实现私域问答，支持 PDF/DOCX/TXT/Excel 等格式上传、自动切分、向量索引（默认使用百炼托管嵌入模型，亦支持本地嵌入模型 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
- **多端交互能力**：
  - 网站：通过悬浮挂件脚本嵌入（[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）；
  - 微信公众号：支持已认证/未认证两种模式，分别适配客服消息（无超时限制）与被动回复（5 秒限制）；
  - 企业微信：需配置可信 IP 及域名主体校验，支持内网代理绕过限制；
  - 钉钉：仅支持 HTTP 模式机器人（非 Stream 模式），需开通 `Card.Streaming.Write` 权限。

> **注意**：文档 1 明确要求模型选择 `Qwen3.5-Plus`，而文档 2、3、4 均写为 `千问-Plus`。经核实，`千问-Plus` 是 `Qwen3.5-Plus` 的旧称，当前控制台中已统一显示为 `Qwen3.5-Plus`，实际为同一模型。开发者应以控制台最新模型列表为准。

## 关键参数

| 参数 | 说明 | 来源位置 |
|------|------|----------|
| `AppID` / `应用ID` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 | 所有文档 1–4 的 1.2 节 |
| `API Key` | 百炼调用凭证，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建 | 所有文档 1–4 的 1.2 节 |
| `AgentKey`（业务空间标识） | 用于鉴权校验，必须与 API Key 所属业务空间一致（文档 1 常见问题中强调） | [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 常见问题节 |
| `WebhookUrl` | AppFlow 连接流生成的回调地址，需填入各渠道后台（企业微信/公众号/钉钉） | 文档 2、3、4 的步骤 3 末尾 |
| `Token` & `EncodingAESKey` | 企业微信专用加密凭证，由 AppFlow 在创建企业微信凭证时生成 | 文档 2 的 3.3 节 |

## 使用方式

1. **创建百炼智能体应用**  
   进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `Qwen3.5-Plus`）→ 设置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）→ 发布。

2. **配置知识库（可选但推荐）**  
   上传文件至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)或[文件中心](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0) → 进入[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)创建标准版 → 在应用配置中启用“必定调用”。

3. **在目标渠道绑定**  
   - **网站**：AppFlow 创建 AI 助手 → Web 页面集成 → 复制悬浮挂件脚本插入 HTML。  
   - **微信公众号**：AppFlow 选择对应模板（认证/未认证）→ 授权公众号 → 绑定百炼应用 → 发布。  
   - **企业微信**：AppFlow 创建连接流 → 配置企业微信凭证（含 CorpID/AgentId/Secret）→ 获取 WebhookUrl → 在企业微信后台配置 API 接收消息及可信 IP。  
   - **钉钉**：AppFlow 创建连接流 → 配置钉钉凭证（Client ID/Secret）→ 在钉钉开放平台添加机器人并设置 HTTP 模式 WebhookUrl。

4. **验证与日志**  
   各渠道均提供即时对话测试入口；如需分析对话质量，可在 AppFlow 连接流中追加 SLS 日志节点记录上下文（[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 常见问题节）。

## 限制和注意事项

- **免费额度**：新用户可享百炼免费额度，覆盖模型调用消耗；AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费（文档 1、2、4 均提及）。
- **认证依赖**：  
  - 微信公众号未认证时，被动回复受 5 秒限制，超时即失败（文档 3 常见问题明确指出）；  
  - 企业微信需配置可信 IP 和域名主体校验，否则 API 接收失败（文档 2 详细说明解决方案）；  
  - 钉钉机器人必须使用 HTTP 模式，Stream 模式不兼容（文档 4 4.1 节强调）。
- **知识库限制**：单文档最大 100MB 或 1000 页，图片单张 ≤20MB，最多上传 200 个文件（文档 2 5.1 节）；本地 RAG 方案建议单文件 ≤100MB（文档 5 传入知识文件节）。
- **调试要点**：  
  - 若出现 `request error` 或 `Failed to stream content`，优先检查 `AppID`、`API Key`、`AgentKey` 三者是否同属一个业务空间（文档 1 常见问题）；  
  - 公众号无响应时，需确认工作流模板与认证状态匹配，并检查 AppFlow 运行日志（文档 3 常见问题）；  
  - 企业微信报“可信 IP 属于第三方服务商”时，须通过 ECS 或 Nginx 代理转发并配置白名单（文档 2 常见问题）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


