# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景，所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 低代码连接流实现。核心流程一致：创建百炼智能体应用 → 配置私有知识库 → 通过 AppFlow 关联目标渠道 → 完成渠道侧认证与 Webhook 配置。开发者可复用同一套知识库和提示词策略，实现跨渠道能力对齐。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指出其“能力均衡，推理效果、成本和速度介于千问Max和千问Flash之间”），也支持 `qwen-max`、`qwen3.5-flash` 等商业模型（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
- **核心功能**：
  - 智能体（Agent）应用：支持角色设定、多轮对话、工具调用（当前各渠道案例均以问答型智能体为主）。
  - RAG 增强：通过百炼知识库模块接入私有文档（PDF/DOCX/TXT 等），支持“必定调用”等知识引用方式（[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。
  - 多端嵌入：提供 Web 悬浮挂件、企业微信自建应用、微信公众号消息接口、钉钉机器人 HTTP 模式四种标准化集成路径。

> **注意**：文档 2（企业微信）、文档 3（微信公众号）、文档 4（钉钉）均要求使用 AppFlow 预置模板创建连接流，但文档 1（网站）未提及模板，而是引导用户手动配置 AI 助手 Web 集成。三者底层能力一致，但配置入口和自动化程度存在差异，建议优先采用模板化路径以降低出错率。

## 关键参数

| 参数 | 说明 | 来源示例 |
|------|------|----------|
| `AppId`（百炼应用 ID） | 百炼控制台「应用管理」页面获取，用于标识调用的目标智能体应用 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| `API Key` | 百炼控制台「密钥管理」创建，用于鉴权调用 API | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| `WebhookUrl` | AppFlow 连接流发布后生成，需填入企业微信/钉钉/公众号后台作为回调地址 | [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) |
| `AgentKey`（业务空间标识） | 仅企业微信场景需校验，确保智能体与 API Key 在同一业务空间（见文档 1 常见问题） | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |

## 使用方式

1. **创建百炼智能体应用**  
   进入百炼控制台 → 应用管理 → 创建「智能体应用」→ 选择模型（如 `Qwen3.5-Plus`）→ 设置 Prompt（例如 `"你叫小助，可以帮助用户解答产品选购、使用等方面的问题。"`）→ 发布。

2. **配置知识库（可选但推荐）**  
   - 上传文件：通过「数据连接」或「文件」页签导入文档（支持 PDF/DOCX/TXT 等，单文件 ≤100MB）；  
   - 创建知识库：进入「知识库」页面 → 创建标准版 → 关联已上传文件；  
   - 引用知识：返回应用配置页 → 开启「知识库」开关 → 添加知识库 → 设置调用方式为「必定调用」→ 再次发布。

3. **通过 AppFlow 关联渠道**  
   - **网站**：AppFlow 控制台 → 模型服务 AI 助手 → 创建 AI 助手 → 导入百炼模型 → Web 页面集成 → 获取悬浮挂件脚本 → 插入 HTML。  
   - **企业微信/微信公众号/钉钉**：使用对应 AppFlow 预置模板（如 `tl-qiyeweixinself0813shzoa`）→ 授权渠道凭证（企业 ID/AgentId/Secret 或 AppID）→ 配置百炼凭证（API Key）→ 填写百炼 `AppId` → 发布并获取 `WebhookUrl`。  
   - **渠道侧配置**：将 `WebhookUrl` 及配套 Token/EncodingAESKey/IP 白名单填入对应平台后台（企业微信需配置可信 IP；公众号需完成认证以避免 5 秒超时限制；钉钉必须选 HTTP 模式）。

## 限制和注意事项

- **免费额度**：新用户可享百炼免费额度，覆盖教程内模型调用消耗；额度用尽后按 token 计费（[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)）。AppFlow、函数计算 FC、ADB-PG 向量存储等组件单独计费。
- **文件限制**：百炼知识库单文档最大 100MB 或 1000 页，图片单张 ≤20MB，最多上传 200 个文件（见文档 2）；本地 RAG 应用不建议传入 >100MB 文件（见文档 5）。
- **认证依赖**：微信公众号未认证时仅支持被动回复（5 秒限制），强烈建议完成认证（见文档 3 常见问题）；企业微信需配置可信 IP，若使用第三方服务器可能触发安全拦截（见文档 2 常见问题）。
- **模型响应时效**：钉钉机器人要求 HTTP 模式，若选用 `qwen-max` 等高延迟模型可能导致超时，可改用 `qwen3.5-flash` 平衡速度与效果（见文档 5）。
- **调试要点**：出现 `request error` 或无响应时，优先检查三项：API Key 状态、`AppId` 正确性、业务空间标识（`AgentKey`）一致性（见文档 1 常见问题）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


