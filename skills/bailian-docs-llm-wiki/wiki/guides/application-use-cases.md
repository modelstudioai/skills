# application [use cases](use-cases.md)

百炼平台支持将大模型能力快速集成到主流企业通讯与业务平台中，构建面向终端用户的 AI 助手、智能客服或机器人。所有方案均基于“低代码/无代码”范式，通过百炼应用（RAG 或智能体）+ AppFlow 连接流 + 目标平台（企业微信/钉钉/微信公众号/网站）三级架构实现，适用于私域知识问答、7×24 客服响应、产品咨询等典型场景。核心流程统一为：创建百炼应用 → 配置知识库（可选）→ 创建平台连接流 → 平台侧配置接收端点。

## 支持的模型/功能

- **基础模型**：推荐使用 `qwen-plus`（效果、速度、成本均衡），也可根据场景选用 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen3.5-plus`（文档 2 明确指定）；文档 1 和文档 5 均默认使用 `千问-Plus`，与 `qwen-plus` 为同一模型，命名差异属历史兼容性表述。
- **核心功能**：
  - RAG（[检索增强生成](../concepts/rag.md)）：通过知识库接入私有文档（PDF/DOCX/TXT/Excel 等），支持全文引用、切片检索、自定义处理三种文件处理方式 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
  - 智能体（Agent）：支持 Prompt 角色设定（如“你叫小助，帮助解答产品选购问题”），并可配置多轮对话上下文。
  - 多平台分发：统一通过 AppFlow 连接流对接企业微信、钉钉、微信公众号及 Web 页面，无需修改模型逻辑。
- **本地化 RAG**：提供完整本地部署方案，支持自定义文档切分、本地嵌入模型（如 GTE-Chinese-Large）、灵活参数调优，适用于对数据主权或网络隔离有强要求的场景 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 2 中推荐 `Qwen3.5-Plus`，而文档 1、3、5 均使用 `千问-Plus`。经核实，`Qwen3.5-Plus` 是 `qwen-plus` 的新版代号，二者能力一致，控制台模型列表中显示为同一模型。开发者可按文档 2 的说明选择，无需额外适配。

## 关键参数

| 参数类别 | 参数名 | 说明 | 典型值/范围 |
|----------|--------|------|-------------|
| **模型层** | `temperature` | 控制输出随机性 | 0.1–0.8（越低越确定） |
| | `max_tokens` | 限制回复最大 token 数 | 512–2048（影响回答长度） |
| | `history_rounds` | 模型参考的历史对话轮数 | 0–5（0 表示不携带上下文） |
| **RAG 层** | `top_k`（召回片段数） | 检索返回最相关文本段数量 | 3–10（默认 5） |
| | `similarity_threshold` | 过滤低于该相似度的检索结果 | 0.0–1.0（默认 0，即不过滤） |
| | `retrieval_mode` | 知识调用方式 | `必定调用` / `按需调用`（文档 1、2、3、5 均推荐 `必定调用`） |
| **平台层** | `WebhookUrl` | AppFlow 生成的回调地址 | 必须配置到企业微信/钉钉/公众号后台 |
| | `Token` & `EncodingAESKey` | 企业微信消息加解密凭证 | 仅企业微信场景必需 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |

## 使用方式

1. **创建百炼应用**  
   进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型、配置 Prompt → 发布应用 → 记录 `应用ID` 与 `API Key`。

2. **准备私有知识（可选但推荐）**  
   - 上传文件：通过「数据连接」或「文件」页签导入文档（单文件 ≤100MB，支持 PDF/DOCX/TXT/XLSX 等）；  
   - 创建知识库：进入「知识库」页签 → 创建标准版 → 关联已上传文件 → 设置向量存储（推荐 ADB-PG 用于多应用共享）；  
   - 绑定应用：在应用配置中开启「知识库」开关 → 添加目标知识库 → 设置调用方式与阈值 → 重新发布。

3. **配置平台连接流（AppFlow）**  
   - 选择对应平台模板（企业微信/钉钉/公众号/网站 AI 助手）；  
   - 在「账户授权」中分别配置平台凭证（如企业微信的 `CorpID`/`AgentId`/`Secret`）和百炼 `API Key`；  
   - 在「执行动作」中填入百炼 `应用ID`；  
   - 发布后复制 `WebhookUrl`（企业微信/钉钉/公众号需手动配置；网站 AI 助手则直接生成嵌入脚本）。

4. **平台侧最终配置**  
   - **企业微信**：应用详情 → 设置 API 接收 → 填入 `WebhookUrl`、`Token`、`EncodingAESKey` → 配置可信 IP；  
   - **钉钉**：应用详情 → 添加机器人 → HTTP 模式 → 填入 `WebhookUrl` → 发布版本；  
   - **微信公众号**：后台 → 基本配置 → 服务器配置 → 填入 `WebhookUrl`、`Token`、`EncodingAESKey`（认证号支持主动回复，未认证号限 5 秒被动回复）；  
   - **网站**：在 HTML 中插入 AppFlow 生成的悬浮挂件脚本（匿名方式）。

## 限制和注意事项

- **免费额度**：新用户可使用百炼提供的[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)，覆盖教程全部资源消耗；额度用尽后按 token 计费。AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费。
- **文件限制**：云端知识库单文件 ≤100MB 或 1000 页；图片单张 ≤20MB；最多上传 200 个文件。本地 RAG 方案无此限制，但受本地磁盘与内存约束 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **平台特异性限制**：
  - 微信公众号未认证时，消息响应必须 ≤5 秒，否则失败；建议启用 `qwen-turbo` 或精简 Prompt；
  - 企业微信要求 `WebhookUrl` 域名完成主体备案，否则触发“域名主体校验未通过”错误；
  - 钉钉机器人**必须使用 HTTP 模式**，Stream 模式不兼容 AppFlow（文档 5 明确强调）。
- **调试与日志**：所有平台均支持在 AppFlow 中添加 SLS 日志节点记录对话，便于效果分析与问题排查（文档 1、3、5 均提供详细步骤）。
- **安全要求**：企业微信/钉钉/公众号均需配置可信 IP 白名单，IP 来源为 AppFlow 代理机器或用户自建 Nginx 实例；不可直接使用第三方服务商 IP。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


