# application [use cases](use-cases.md)

阿里云百炼平台支持将大模型能力快速集成至多种主流业务触点，包括网站、企业微信、微信公众号、钉钉等渠道，构建7×24小时响应的AI助手。所有方案均基于统一的RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼应用作为核心推理引擎，结合AppFlow低代码连接器完成渠道对接，开发者只需关注模型选型、知识配置与参数调优，无需编写后端逻辑。[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)是其中最典型的入门场景。

## 支持的模型/功能

- **基础模型**：默认支持通义千问系列商业模型（如 `qwen-plus`、`qwen-max`、`qwen3.5-flash`），可通过应用配置页的“规划”区域直接选择；新版智能体应用支持 `AUTO` 智能模式，由平台自动平衡效果与成本。
- **RAG增强**：所有渠道均支持关联知识库实现私域问答。知识库类型包括文档搜索（标准版）、结构化数据（xlsx/csv）和非结构化数据（pdf/docx/txt等），支持自定义切分策略与相似度阈值控制。
- **多模态扩展**：钉钉场景支持卡片消息格式，可配置展示引用文档来源或DeepSeek深度思考过程；企业微信与钉钉均支持内网代理模式以满足可信IP要求。

> **注意**：文档2（企业微信）与文档3（微信公众号）均要求使用“旧版智能体”，而文档1（网站）明确说明“当前默认创建新版智能体应用（Agent 2.0）”。实际开发中应以百炼控制台最新UI为准，新版Agent已全面兼容RAG与Web集成能力，旧版入口仅作兼容保留。[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)中关于新版Agent的说明具有时效优先级。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | `temperature` | 控制输出随机性，范围0~2，推荐值0.1~0.7 | 应用配置页 > 规划 > 高级设置 |
| | `max_tokens` | 限制单次回复最大token数 | 同上 |
| | `history_rounds` | 携带历史对话轮数（设为0表示无上下文） | 同上 |
| **RAG层** | `top_k` | 召回片段数（默认3） | 应用配置页 > 知识库 > 检索策略 |
| | `similarity_threshold` | 相似度阈值（0~1，0表示不过滤） | 同上 |
| | `retrieval_mode` | 调用方式：`ALWAYS`（必定调用）、`ON_DEMAND`（按需触发） | 同上 |
| **渠道层** | `WebhookUrl` | AppFlow生成的HTTP回调地址，用于企业微信/钉钉/公众号 | AppFlow连接流发布后获取 |
| | `AgentKey` | 百炼业务空间ID，必须与API Key所属空间一致 | AppFlow AI助手 > 参数配置 |

## 使用方式

1. **创建百炼应用**：在[应用管理](https://bailian.console.aliyun.com/flow-agent/app-center)创建智能体应用，配置模型、提示词（如`你叫小助，可以帮助用户解答产品选购、使用等方面的问题`）并发布；
2. **准备知识库**（可选但推荐）：上传文档至[知识库](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list)，创建并发布[知识检索服务](https://bailian.console.aliyun.com/cn-beijing/rag/retrieval/list)，在应用配置中关联；
3. **配置渠道连接器**：
   - **网站**：在AppFlow创建AI助手 → 导入百炼模型 → Web页面集成 → 复制悬浮挂件脚本嵌入HTML；
   - **企业微信/公众号/钉钉**：在AppFlow使用对应模板创建连接流 → 分别配置渠道凭证（企业ID/AgentId/Secret或AppID）和百炼API Key → 填写应用ID → 发布获取WebhookUrl；
4. **渠道侧配置**：
   - 企业微信：在应用后台配置API接收消息（填入WebhookUrl、[Token](../concepts/token.md)、EncodingAESKey）及可信IP；
   - 微信公众号：完成服务器配置（需认证）或被动回复（未认证）；
   - 钉钉：在开放平台机器人配置中启用HTTP模式并填入WebhookUrl；
5. **验证与日志**：通过渠道发起对话测试；排查问题时查阅[AppFlow执行日志](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/manage)。[在企业微信中集成一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)详细说明了域名主体校验与可信IP配置的绕过方案。

## 限制和注意事项

- **费用**：AppFlow连接器本身免费，但底层资源（百炼模型调用、知识库实例、函数计算FC部署示例站）按各自产品计费；新用户免费额度覆盖初期体验，详见[新用户免费额度](../../model-user-guide/test-1/new-free-quota.md)。
- **文件限制**：知识库上传单文件≤100MB（文档）或≤20MB（图片），单次最多200个文件；本地RAG应用建议单文件≤100MB以避免Embedding超时。
- **安全约束**：
  - 企业微信/钉钉要求Webhook主机名必须为备案域名或通过内网代理（ECS/Nginx）转发；
  - API Key与百炼应用必须位于同一业务空间，否则鉴权失败；
  - 微信公众号未认证时仅支持5秒内被动回复，超时即丢弃。
- **调试要点**：
  - 出现 `request error` 或 `Failed to stream content`：优先检查API Key状态、应用ID拼写（含空格）、AgentKey空间一致性；
  - 企业微信报错“以下IP属于第三方服务商”：必须使用自有ECS或托管实例作为代理，并将代理IP加入企业可信IP列表；
  - 钉钉机器人无响应：确认消息接收模式为**HTTP模式**（非Stream模式）。

> **注意**：文档4（钉钉）提到“授予应用发送卡片消息权限”需开通 `Card.Streaming.Write` 和 `Card.Instance.Write`，但文档2（企业微信）与文档3（公众号）未提及类似权限配置。该差异源于各平台API能力设计不同，钉钉卡片需显式授权，而企业微信/公众号通过Webhook自动获得消息收发权限，开发者无需额外操作。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


