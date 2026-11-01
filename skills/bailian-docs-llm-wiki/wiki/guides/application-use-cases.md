# application [use cases](use-cases.md)

百炼平台支持多种主流企业级通信与协作场景下的 AI 助手快速集成，包括网站嵌入、微信公众号、企业微信、钉钉等渠道。所有方案均基于统一的百炼大模型应用底座，通过 AppFlow 低代码连接流实现模型能力与业务入口的解耦对接，开发者可复用同一套知识库、Prompt 和模型配置，仅需按渠道适配前端交互与认证协议。核心流程均为：创建百炼智能体应用 → 配置私有知识（可选）→ 在 AppFlow 中创建对应渠道的连接流 → 完成渠道侧认证与 Webhook 配置。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1）、`千问-Plus`（文档 2、4、5），该模型在效果、速度与成本间取得平衡；也可选用 `qwen-max`（高精度）、`qwen3.5-flash`（高吞吐）或 `qwen-turbo`（低延迟）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **RAG 增强**：所有场景均支持通过百炼知识库实现[检索增强生成](../concepts/rag.md)，支持 PDF/DOCX/TXT/CSV 等格式上传，索引类型默认为向量检索，可选 ADB-PG 集中存储 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **本地 RAG 变体**：若需完全控制文档切分、嵌入模型及向量存储，可采用本地部署方案，支持自定义切分策略、更换 ModelScope 嵌入模型（如 `iic/nlp_gte_sentence-embedding_chinese-large`）及调整召回参数 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 明确指定模型为 `Qwen3.5-Plus`，而文档 2、4、5 统一使用 `千问-Plus`。二者为不同版本模型，实际效果与计费策略存在差异，建议以百炼控制台当前可用模型列表为准，避免硬编码模型名。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `App ID` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取，用于连接流调用目标应用 | 所有文档共用 |
| `API Key` | 百炼服务调用凭证，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建，需与 App ID 同属一个业务空间 | 所有文档共用 |
| `WebhookUrl` | AppFlow 连接流生成的回调地址，需填入各渠道后台（如企业微信 API 接收消息、钉钉机器人 HTTP 地址） | 文档 2、4、5 |
| `AgentKey`（业务空间标识） | 用于校验 API Key 与智能体归属同一业务空间，排查 `request error` 时必查项 | [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |

## 使用方式

1. **创建百炼智能体应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `Qwen3.5-Plus`）→ 配置 Prompt（如角色设定）→ 发布。
2. **配置知识库（可选）**：上传文档至数据连接 → 创建知识库 → 在应用配置中启用“必定调用”并关联知识库。
3. **创建渠道连接流**：
   - 网站：AppFlow → 模型服务 AI 助手 → 创建 AI 助手 → Web 页面集成 → 获取悬浮挂件脚本并嵌入 HTML。
   - 微信公众号/企业微信/钉钉：AppFlow → 使用预置模板（如 `tl-qiyeweixinself0813shzoa`）→ 配置渠道凭证（AppID/Secret 或 Client ID/Secret）→ 配置百炼凭证（API Key + App ID）→ 发布后获取 WebhookUrl。
4. **渠道侧配置**：将 WebhookUrl 及配套 [Token](../concepts/token.md)/EncodingAESKey（企业微信）、可信 IP（企业微信/钉钉）填入对应平台后台。

## 限制和注意事项

- **免费额度覆盖范围**：新用户免费额度可覆盖网站、微信公众号、企业微信、钉钉四类场景的模型调用消耗，但 AppFlow、函数计算 FC、ADB-PG 等依赖云产品单独计费 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **认证与权限要求**：
  - 企业微信/钉钉需主管理员账号授权，且钉钉应用需提前申请 `Card.Streaming.Write` 权限；
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证以启用客服接口 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
- **安全与合规**：
  - 企业微信/钉钉要求可信 IP 白名单，若使用 AppFlow 默认出口 IP 报错“第三方服务商”，需启用内网代理（ECS/Nginx）并配置自有 IP；
  - 微信公众号配置服务器 URL 时若报“严重安全风险”，需改用服务商授权模式重新创建连接流。
- **调试要点**：出现 `Failed to stream content` 或无响应时，优先检查 `App ID`、`API Key`、`AgentKey` 三者是否同空间，以及 WebhookUrl 是否被正确填入渠道后台。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


