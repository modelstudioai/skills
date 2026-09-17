# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流渠道的 AI 助手快速集成，覆盖网站、企业微信、微信公众号、钉钉等私域触点，以及本地化部署的 RAG 应用场景。所有方案均基于统一的大模型应用（智能体）与知识库能力，通过 AppFlow 低代码连接流或本地 SDK 实现模型调用与业务系统解耦，适用于客服问答、产品咨询、内部知识助手等典型业务需求。

## 支持的模型/功能

- **核心模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）或 `千问-Plus`（文档 2、3、4 中一致采用），该模型在效果、速度与成本间取得平衡，适用于通用问答与 RAG 场景；也可按需选用 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **关键功能**：
  - 智能体（Agent）编排：支持多步骤任务分解、工具调用（如知识库检索、函数计算）；
  - RAG 增强：通过知识库实现私有文档问答，支持文件上传、切片策略配置、相似度阈值与权重调整 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；
  - 多端集成：提供 Web 悬浮挂件、企业微信自建应用、微信公众号消息回复、钉钉机器人卡片等开箱即用模板；
  - 本地化 RAG：支持知识库在本地构建与管理，嵌入模型可选云端 API 或本地部署（如 GTE-Chinese-Large）[原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 明确推荐 `Qwen3.5-Plus`，而文档 2、3、4 统一使用 `千问-Plus`。二者为同一模型的不同命名方式（`千问-Plus` 是控制台显示名，`Qwen3.5-Plus` 是模型 ID），无功能差异，属命名一致性问题，非实质矛盾。

## 关键参数

| 参数 | 说明 | 取值建议 | 来源 |
|------|------|----------|------|
| `applicationId` | 百炼应用唯一标识 | 在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面复制，**不可含前后空格** | 文档 1、2、3、4 |
| `apiKey` | 百炼 API 访问凭证 | 在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建，需确保与应用在同一业务空间 | 文档 1、2、3、4 |
| `AgentKey`（业务空间标识） | 鉴权必需，用于校验 apiKey 与智能体归属关系 | 必须与应用所在业务空间一致，否则报 `request error` | [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| `knowledgeBaseId` | 知识库唯一标识 | 创建知识库后生成，需在应用配置中显式引用并设为 `必定调用` | 文档 1、2、3、4 |
| `retrieval.top_k` / `召回片段数` | RAG 检索返回的最相关文本段数量 | 默认 3–5；增大可提升信息覆盖，但可能引入噪声 | 文档 5 |
| `retrieval.similarity_threshold` / `相似度阈值` | 过滤低相关性检索结果的阈值 | 范围 0–1；设为 0 表示不过滤；建议 0.3–0.6 | 文档 5 |

## 使用方式

1. **创建大模型应用**：  
   进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择 `Qwen3.5-Plus` 或 `千问-Plus` → 配置 Prompt（如 `你叫小助，帮助解答产品选购问题`）→ 发布。

2. **配置知识库（可选但推荐）**：  
   - 上传文件：支持 `.pdf`, `.docx`, `.txt`, `.xlsx` 等格式（单文件 ≤100MB）；  
   - 创建知识库：在知识库页面选择“标准版”，关联已上传文件；  
   - 引用知识：在应用配置中启用知识库开关，设置调用方式为 `必定调用`。

3. **集成至目标渠道**：  
   - **网站**：通过 AppFlow 创建 AI 助手 → 获取悬浮挂件脚本 → 插入 HTML `<head>` 或 `<body>`；  
   - **企业微信/微信公众号/钉钉**：使用对应 AppFlow 模板 → 授权第三方平台（微信/钉钉）→ 配置百炼凭证与应用 ID → 获取 Webhook URL → 在第三方平台后台完成回调地址与可信 IP 配置；  
   - **本地 RAG**：下载 `local_rag.zip` → 安装依赖（Python 3.9–3.12）→ 配置 `BAI_LIAN_API_KEY` 环境变量 → 启动 `uvicorn main:app --port 7866` → 通过 Gradio 界面或 API 调用。

## 限制和注意事项

- **免费额度**：新用户可享百炼免费额度，覆盖模型调用消耗；AppFlow、函数计算（FC）、ADB-PG 等依赖服务单独计费 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **认证要求**：  
  - 微信公众号未认证时，仅支持被动回复（5 秒超时限制），建议完成认证以启用客户消息接口；  
  - 企业微信/钉钉需确保应用已获取对应权限（如企业微信的 `接收消息`、钉钉的 `Card.Streaming.Write`）。
- **安全与合规**：  
  - 企业微信/钉钉配置时需添加 AppFlow 提供的 IP 白名单至可信 IP 列表，否则触发安全拦截；  
  - 微信公众号配置服务器地址时若报“严重安全风险”，需通过服务商授权或 Nginx 代理解决 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
- **调试要点**：  
  - 出现 `Failed to stream content` 或 `request error`，优先检查 `apiKey` 状态、`applicationId` 是否正确、`AgentKey`（业务空间）是否匹配；  
  - 本地 RAG 创建大知识库时，受限于 Embedding API 限流，避免单次上传 >100 MB 文件。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


