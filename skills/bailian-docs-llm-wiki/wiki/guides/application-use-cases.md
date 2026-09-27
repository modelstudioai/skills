# application [use cases](use-cases.md)

百炼平台支持将大模型能力快速集成到主流企业通讯与业务场景中，实现开箱即用的 RAG 应用。核心路径统一为：创建智能体应用 → 配置知识库（可选）→ 通过 AppFlow 连接目标渠道（企业微信、钉钉、微信公众号、网站等）→ 部署验证。所有方案均支持零代码配置，且新用户免费额度可覆盖入门级使用 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

## 支持的模型/功能

- **基础模型**：默认推荐 `qwen-plus`（效果、速度、成本均衡），亦支持 `qwen-max`（高精度）、`qwen-turbo`（低延迟）、`qwen3.5-plus`（文档 5 明确指定，[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。
- **核心功能**：
  - 智能体（Agent）应用：支持角色设定（Prompt）、多轮对话、工具调用（隐式）。
  - RAG 增强：通过知识库注入私域知识，支持 `.pdf`, `.docx`, `.txt`, `.md`, `.xlsx` 等格式（单文件 ≤100MB）。
  - 多端集成：原生支持企业微信、钉钉、微信公众号（订阅号/服务号）、Web 网站四种渠道。
  - 本地化 RAG：提供完整本地部署方案，支持自定义切分、嵌入模型（如 GTE-Chinese-Large）及向量存储 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 和文档 3 均指定 `千问-Plus`，而文档 5 明确要求 `Qwen3.5-Plus`；当前控制台实际可用模型以 `qwen-plus` 为准，`Qwen3.5-Plus` 尚未在标准模型列表中公开，建议优先使用 `qwen-plus` 并关注控制台最新模型更新。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置性 |
|----------|--------|------|----------|
| **模型层** | 温度（temperature） | 控制输出随机性，值域 0~2，生产环境建议设为 0.1~0.5 | ✅（仅本地 RAG 方案支持，见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)） |
| | 最大回复长度（max_tokens） | 限制生成 token 数量 | ✅（同上） |
| **RAG 层** | 召回片段数（top_k） | 检索返回给 LLM 的最相关文本段数量 | ✅（同上） |
| | 相似度阈值（similarity_threshold） | 过滤低于该阈值的检索结果 | ✅（同上） |
| | 文档处理方式 | 全文引用 / 切片检索 / 自定义处理（百炼控制台应用配置页） | ✅（云上 RAG） |
| **集成层** | Webhook URL | AppFlow 生成的回调地址，需填入各平台后台 | ⚠️（由 AppFlow 自动生成，不可修改） |
| | [Token](../concepts/token.md) & EncodingAESKey | 企业微信消息加解密密钥，由 AppFlow 生成 | ⚠️（同上） |

## 使用方式

1. **创建智能体应用**  
   进入百炼控制台「应用管理」→「创建应用」→ 选择「智能体应用」→ 设置模型（如 `qwen-plus`）和 Prompt（如 `"你叫小助，帮助解答产品问题。"`）→ 发布。

2. **配置知识库（可选）**  
   - 上传文件：至「数据连接」或「文件」页签（支持 200 个文件，单文件 ≤100MB）；  
   - 创建知识库：在「知识库」页签选择「标准版」→ 关联已上传文件；  
   - 绑定应用：在应用配置页开启「知识库」开关 → 添加知识库 → 设为「必定调用」。

3. **连接目标渠道（AppFlow）**  
   - 选择预置模板（如「企业微信自建应用大模型自动回复」）；  
   - 配置双端凭证：企业微信/钉钉/公众号的 `CorpID/AgentID/AppID + Secret`，以及百炼的 `API Key + 应用 ID`；  
   - 发布连接流，获取 `WebhookUrl` 或 `悬浮挂件脚本`。

4. **平台侧配置**  
   - **企业微信/钉钉/公众号**：在各自开发者后台填写 `WebhookUrl`、`Token`、`EncodingAESKey` 及可信 IP；  
   - **网站**：将 AppFlow 生成的悬浮挂件 JS 脚本插入 HTML `<head>` 或 `<body>` 底部。

## 限制和注意事项

- **免费额度**：新用户免费额度可覆盖全部入门场景，但额度耗尽后按 token 计费；AppFlow、FC、ADB-PG 等依赖服务单独计费 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **认证依赖**：微信公众号未认证时，仅支持被动回复（5 秒超时限制），必须完成认证才能启用客服接口 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
- **可信 IP 冲突**：企业微信要求每个可信 IP 仅归属单一企业；若复用阿里云 ECS IP，需通过 AppFlow「内网代理」配置专属实例并添加其 IP 到白名单。
- **文件解析延迟**：上传文档后需等待 1~6 分钟完成解析，期间知识库不可用。
- **本地 RAG 限制**：`local_rag` 示例应用要求 Python 3.9~3.12，且大文件（>100MB）可能导致创建失败；嵌入模型 API 有调用限流 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **调试建议**：遇到无响应时，优先检查 AppFlow 执行日志、API Key 状态、应用 ID 是否跨业务空间、以及各平台的可信域名/IP 配置。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)


