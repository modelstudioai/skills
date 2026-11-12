# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业级通信与内容平台的 AI 助手集成，覆盖网站、企业微信、钉钉、微信公众号等典型私域触点。所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 无代码连接流 + 可选本地/云端知识库实现快速部署。核心逻辑为：用户请求 → 平台路由至 AppFlow 连接流 → 调用百炼 API（含可选知识检索）→ 返回结构化或流式响应。

## 支持的模型/功能

- **基础模型**：默认推荐 `qwen-plus`（即文档中所述“千问-Plus”），兼顾效果、速度与成本；亦支持 `qwen-max`（高精度）、`qwen3.5-flash`（低延迟）、`qwen3.5-plus`（文档 1 中明确指定）等商业模型。> **注意**：文档 1 明确要求模型选择 `Qwen3.5-Plus`，而文档 2、3、4 均写为“千问-Plus”，二者是否等价需以控制台实际模型列表为准；若存在差异，应以 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 中的 `Qwen3.5-Plus` 为准。
- **核心功能**：
  - 7×24 智能问答（文本输入/输出）
  - 私有知识注入（RAG）：支持 PDF/DOCX/TXT/Excel 等格式上传、自动解析、向量化与检索
  - 多端 UI 集成：网站悬浮窗、企业微信应用、钉钉机器人、微信公众号客服消息
  - 流式响应与卡片消息（钉钉/企业微信支持富媒体卡片）

## 关键参数

| 参数 | 说明 | 来源示例 |
|------|------|----------|
| `AppId` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| `API Key` | 百炼调用凭证，用于 AppFlow 或自定义后端鉴权，需在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| `WebhookUrl` | AppFlow 连接流对外暴露的 HTTP 回调地址，需配置到企业微信/钉钉/公众号后台 | [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) |
| `AgentKey` / `业务空间标识` | 用于校验百炼 API Key 与智能体所属业务空间一致性，避免跨空间鉴权失败 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `qwen-plus`）、配置 Prompt（如 `你叫小助...`）→ 发布。
2. **准备知识库（可选但推荐）**：
   - 云端方式：上传文件至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) → 创建知识库 → 在应用配置中启用“必定调用”。
   - 本地方式：使用 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 提供的 `local_rag` 工具链，支持自定义切分、嵌入模型与向量存储。
3. **配置目标平台连接流**：
   - **网站**：AppFlow → 模型服务AI助手 → Web 页面集成 → 获取悬浮挂件脚本并嵌入 HTML。
   - **企业微信/钉钉/公众号**：AppFlow → 使用对应预置模板（如“企业微信自建应用大模型自动回复”）→ 授权平台凭证（企业 ID/AgentId/Secret 或 AppID）→ 绑定百炼 API Key 与 AppId → 获取 WebhookUrl。
4. **平台侧配置**：
   - 企业微信：配置 API 接收消息（填 WebhookUrl/[Token](../concepts/token.md)/EncodingAESKey）+ 企业可信 IP。
   - 钉钉：配置机器人 HTTP 模式接收地址（必须为 HTTP，非 Stream）。
   - 微信公众号：根据认证状态选择不同模板，完成服务器配置（需备案域名或白名单 IP）。

## 限制和注意事项

- **免费额度**：新用户可使用 [新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md) 覆盖初期调用，额度耗尽后按 token 计费；AppFlow、FC、ADB-PG 等依赖云产品单独计费。
- **知识库限制**：
  - 单文档最大 100MB 或 1000 页（文档 2）；不建议上传 >100MB 文件（文档 5）。
  - 向量存储类型选择：`ADB-PG` 适用于多应用集中管理；默认存储为百炼托管。
- **平台特异性限制**：
  - 微信公众号未认证时，仅支持被动回复（5 秒超时限制），需在 Prompt 中强调“简短回答”或选用 `qwen3.5-flash` 加速（文档 4）。
  - 钉钉机器人必须使用 **HTTP 模式**，Stream 模式不兼容（文档 3）。
  - 企业微信可信 IP 冲突：单个 IP 仅能绑定一个企业，多企业需通过 ECS/Nginx 代理转发（文档 2）。
- **调试要点**：
  - 出现 `request error` 或 `Failed to stream content`：优先检查 `AppId`、`API Key`、`AgentKey` 三者是否同属一个业务空间（文档 1）。
  - 公众号无响应：确认工作流模板与认证状态匹配，并检查 AppFlow 运行日志（文档 4）。
  - 企业微信“域名主体校验未通过”：需配置自有备案二级域名或使用 AppFlow Nginx 代理（文档 2）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


