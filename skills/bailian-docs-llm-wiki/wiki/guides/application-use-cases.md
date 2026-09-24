# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业通讯与内容平台的 AI 助手集成，覆盖企业微信、钉钉、微信公众号及网站等高频触点。所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + 私有知识库 + 低代码连接流（AppFlow）实现开箱即用的智能问答能力，适用于客服应答、内部知识查询、销售辅助等典型场景。[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)、[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 和 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 分别代表了云端 SaaS 集成、前端嵌入式部署和本地化可控部署三类核心路径。

## 支持的模型/功能

- **基础模型**：默认推荐 `qwen-plus`（文档 1、3、4），兼顾效果、速度与成本；文档 2 明确指定 `Qwen3.5-Plus`（当前为最新稳定版），建议优先采用该版本以获得更优推理表现。
- **RAG 增强**：所有方案均支持知识库配置，支持 `.pdf`, `.docx`, `.txt`, `.md`, `.xlsx`, `.csv`, `.png`, `.jpg` 等格式（单文件 ≤100 MB）；知识库可选用标准向量存储或集中式 `ADB-PG`。
- **高级功能**：
  - 钉钉机器人支持卡片消息、引用文档展示及 DeepSeek 思考过程渲染（需定制模板）；
  - 微信公众号区分认证/未认证账号，认证号支持客户消息接口（无 5 秒限制），未认证号仅支持被动回复（严格 5 秒超时）；
  - 网站嵌入支持悬浮挂件、预置问题、拖拽图标等前端定制；
  > **注意**：文档 1 中“模型选择千问-Plus”与文档 2 中“Qwen3.5-Plus”存在命名不一致。根据百炼控制台最新模型列表，`Qwen3.5-Plus` 是当前正式名称，`千问-Plus` 为旧称，实际指向同一模型。开发者应以控制台显示名称为准。

## 关键参数

| 参数 | 说明 | 取值建议 | 来源依据 |
|------|------|----------|----------|
| `temperature` | 控制生成随机性 | 0.1–0.5（客服场景建议偏低） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| `max_tokens` | 最大输出长度 | 512–2048（平衡详略与成本） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| `top_k`（召回片段数） | 检索返回的上下文段数 | 3–5（过高易引入噪声） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| `similarity_threshold` | 相似度过滤阈值 | 0.3–0.7（默认 0.5，调高可提升精准度） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| `AgentKey`（业务空间标识） | 用于 API Key 与智能体鉴权匹配 | 必须与百炼应用所在业务空间一致 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |

## 使用方式

1. **创建百炼应用**：进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择「智能体应用」，配置 Prompt（如 `你叫小助，帮助解答产品选购、使用问题`），发布应用。
2. **准备知识库（可选但推荐）**：
   - 上传文件至「数据连接」或「文件」页签；
   - 在「知识库」页签创建知识库，关联文件；
   - 在应用配置中启用知识库，设置调用方式（如「必定调用」）并发布。
3. **配置连接流/集成**：
   - **企业微信/钉钉/公众号**：使用 AppFlow 预置模板（如 `企业微信自建应用大模型自动回复`），配置企业凭证（CorpID/AgentID/Secret 或 AppID）与百炼 API Key + 应用 ID，获取 Webhook URL 并完成平台侧回调配置（含 [Token](../concepts/token.md)、EncodingAESKey、可信 IP）；
   - **网站嵌入**：在 AppFlow「模型服务AI助手」中创建助手，导入百炼应用，配置 Web 页面集成（含悬浮挂件脚本），将脚本插入 HTML `<head>` 或 `<body>` 底部；
   - **本地部署**：解压 `local_rag.zip`，安装依赖，配置环境变量 `BAI_LIAN_API_KEY`，运行 `uvicorn main:app --port 7866` 启动 Gradio 服务。
4. **验证与日志**：在目标平台发起对话测试；如需分析，可在 AppFlow 连接流中追加「SLS日志云服务」步骤记录原始请求与响应。

## 限制和注意事项

- **免费额度**：新用户免费额度可覆盖入门级使用（文档 1、2、3、4 均明确提及），但 AppFlow、函数计算 FC、ADB-PG 等依赖组件按各自产品计费（文档 2 特别注明）。
- **平台限制**：
  - 微信公众号未认证时，被动回复严格限时 5 秒，超时即失败；必须完成认证才能解除限制（文档 3）；
  - 钉钉机器人**必须配置为 HTTP 模式**，Stream 模式不兼容 AppFlow（文档 4 强调）；
  - 企业微信要求配置可信域名/IP，若使用非备案域名，需通过 AppFlow 内网代理或计算巢 Nginx 实例中转（文档 1）。
- **知识处理**：
  - 文档解析耗时 1–6 分钟，大文件（>100 MB）可能失败或超时（文档 1、2、3、4 均提示）；
  - 本地 RAG 方案明确限制单文件不宜超过 100 MB（文档 5）；
  > **注意**：文档 1 与文档 2 对「密钥管理」路径描述不一致：文档 1 写为 `[API Key](https://bailian.console.aliyun.com/?tab=app#/api-key)`，文档 2 写为 `[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)`。二者实际为同一页面，`/api-key` 是正确路径，`密钥管理` 仅为 UI 标签文字，不影响操作。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


