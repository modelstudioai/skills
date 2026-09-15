# application [use cases](use-cases.md)

百炼平台支持多种主流渠道的 AI 应用快速落地，涵盖网站、企业微信、微信公众号、钉钉等私域触点，以及本地化部署的 RAG 场景。所有方案均基于统一的大模型应用（智能体）能力，通过 AppFlow 实现零代码连接与编排，适用于客户支持、知识问答、智能导购等典型业务场景。核心流程高度一致：创建百炼应用 → 配置模型与知识 → 通过 AppFlow 关联渠道 → 集成上线。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）或 `千问-Plus`（文档 2、3、4 中统一表述），该模型在效果、速度与成本间取得平衡，适用于通用问答、客服响应等任务；也可按需选用 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及）。
- **RAG 增强**：所有渠道方案均支持通过百炼知识库接入私有文档（PDF/DOCX/TXT 等），实现领域知识精准问答；文档 5 还提供**本地知识库构建路径**，支持自定义切分、嵌入模型（如 GTE-Chinese-Large）及向量存储，适用于对数据主权或切分策略有强要求的场景 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **交互能力**：支持 Web 悬浮窗、企业微信/公众号/钉钉群内对话、卡片消息（钉钉）、流式响应等多形态输出；钉钉方案额外支持展示引用来源和 DeepSeek 思考过程 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。

> **注意**：文档 1 中模型名称为 `Qwen3.5-Plus`，而文档 2、3、4 统一写作 `千问-Plus`。二者实为同一模型（Qwen3.5-Plus 是其新版命名），开发者应以控制台实际可选模型列表为准，避免硬编码模型 ID。

## 关键参数

- **身份凭证**：必需 `应用ID`（来自百炼应用管理页）与 `API Key`（来自百炼密钥管理页），用于 AppFlow 调用百炼 API；各渠道还需对应平台凭证（如企业微信的 `CorpID/AgentID/Secret`、钉钉的 `Client ID/Secret`、公众号的 `AppID`）。
- **知识库配置**：
  - `调用方式`：关键选项，如 `必定调用`（强制检索）或 `按需调用`（模型自主判断）；
  - `相似度阈值` 与 `召回片段数`：直接影响检索质量，需根据文档语义密度调优；
  - `文件处理方式`：`全文引用`、`切片检索` 或 `自定义处理`（文档 2 中明确说明）。
- **模型推理参数**（文档 5 明确列出）：
  - `温度（temperature）`：控制生成随机性；
  - `最大回复长度（max_tokens）`：限制输出 token 数；
  - `携带上下文轮数`：决定历史对话记忆深度；
  - `召回片段数` 与 `相似度阈值`：同属 RAG 检索层参数。

## 使用方式

1. **创建大模型应用**：在百炼控制台 → 应用管理 → 创建**智能体应用**，选择模型、配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题`），发布应用。
2. **配置知识库（可选但推荐）**：上传私有文档 → 创建知识库 → 在应用配置中关联知识库并设置调用策略。
3. **选择渠道并集成**：
   - **网站**：在 AppFlow 创建 AI 助手 → 关联百炼应用 → 生成悬浮挂件脚本 → 嵌入 HTML（文档 1）；
   - **企业微信/公众号/钉钉**：在 AppFlow 使用对应模板 → 授权平台账号 → 配置百炼凭证 → 获取 Webhook URL → 在平台后台完成回调地址与可信 IP/域名配置（文档 2、3、4）；
   - **本地 RAG**：下载 `local_rag.zip` → 配置 Python 环境与 API Key → 运行 `uvicorn main:app` 启动 Web UI（文档 5）。
4. **验证与日志**：所有方案均支持通过 AppFlow 添加 SLS 日志节点记录对话 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

## 限制和注意事项

- **免费额度**：新用户可享百炼免费额度，覆盖教程消耗；额度用尽后按 token 计费；AppFlow、FC、ADB-PG 等依赖服务单独计费（文档 1、2、4 均强调）。
- **渠道限制**：
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证（文档 3）；
  - 钉钉机器人**必须使用 HTTP 模式**，Stream 模式不兼容（文档 4 明确警告）；
  - 企业微信配置需解决“域名主体校验”与“可信 IP”问题，常需通过 AppFlow Nginx 代理或自有 ECS 转发（文档 2 详细说明）。
- **文件与性能**：
  - 百炼知识库单文件上限 100MB 或 1000 页，大文件解析需 1–6 分钟（文档 2、3、4）；
  - 本地 RAG 方案受限于 Embedding API 限流，不建议上传 >100MB 文件（文档 5）；
  - 公众号未认证场景下，若百炼响应超时，可改用 `qwen-turbo` 模型或精简 Prompt（文档 3 建议）。
- **调试要点**：常见 `request error` 或无响应问题，优先检查 API Key 状态、应用 ID 准确性、业务空间标识（AgentKey）一致性，以及渠道平台的 Webhook URL、Token、EncodingAESKey 配置（文档 1、3）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


