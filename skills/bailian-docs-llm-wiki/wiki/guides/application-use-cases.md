# application [use cases](use-cases.md)

百炼平台提供多种典型应用场景的接入方案，帮助开发者在数分钟内为网站、微信公众号、企业微信、钉钉以及本地部署的 RAG 应用接入大模型能力。所有方案都基于「百炼智能体应用 + AppFlow 连接流 + 知识库（可选）」的统一架构，按 token 计费，新用户有免费额度覆盖初期投入。

## 支持的接入渠道

| 渠道 | 说明 | 是否需要编码 | 核心依赖 |
| --- | --- | --- | --- |
| 网站 | 通过 AppFlow 的 Web 页面集成，在网站 HTML 中嵌入几行脚本 | 仅粘贴脚本 | AppFlow AI 助手 Web 集成 |
| 微信公众号（订阅号） | 通过 AppFlow 模板将公众号消息转发到百炼 RAG 应用 | 无 | 公众号认证状态决定使用不同模板 |
| 企业微信 | 自建企业微信应用 + AppFlow 连接流 + Webhook 配置 | 无 | 企业 ID、AgentId、Secret |
| 钉钉 | 自建钉钉应用 + AppFlow 连接流 + 机器人配置 | 无 | Client ID、Client Secret |
| 本地 RAG | 本地 Python 服务 + 通义千问 API + Gradio 界面 | 需要 Python 环境 | LlamaIndex、百炼 Embedding API |

各渠道的详细接入步骤请参考：[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)、[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)、[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)、[在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)、[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

## 通用接入流程

所有渠道都遵循以下步骤，差异仅在第二步的「平台侧配置」：

1. **创建百炼智能体应用**：在百炼控制台 → 应用管理 → 创建智能体应用，选择模型并配置 Prompt，发布后获得**应用 ID**。
2. **获取 API Key**：在百炼控制台 → 密钥管理 中创建 API Key。
3. **创建 AppFlow 连接流**：使用对应渠道的 AppFlow 预置模板，分别配置「平台侧凭证」（如微信 AppID、企业微信 AgentId/Secret、钉钉 Client ID/Secret）和「百炼凭证」（API Key + 应用 ID），完成后发布连接流并获得 **WebhookUrl**（网站集成除外）。
4. **平台侧配置**：把 WebhookUrl 填入对应平台的机器人/消息接收配置中。
5. **（可选）配置知识库**：让 AI 能回答私域问题，具体见下文「知识库配置」。

## 各渠道关键差异

### 网站

- 不走 Webhook，而是通过 AppFlow 的 **Web 页面集成** → 复制「悬浮挂件部署脚本」，粘贴到网站 HTML 文件中即可。
- 支持自定义字体、背景、头像、预置问题等可视化样式。
- 也可用函数计算 FC 一键部署示例网站快速体验。

### 微信公众号

- **已认证**公众号使用「客户消息」接口，支持长回复；**未认证**公众号只能走「被动回复」，响应时间被微信限制为 5 秒。
- 开启服务器配置后，原有**自定义菜单会被关闭**。未认证订阅号无法通过接口恢复自定义菜单；已认证服务号/订阅号需通过微信菜单接口重新配置。

### 企业微信

- 需要在企业微信开发者中心创建「企业内部应用」，获取 **企业 ID、AgentId、Secret**。
- AppFlow 连接流发布后会生成 Token 和 EncodingAESKey，需填入企业微信「API 接收消息」页面。
- 必须配置**企业可信 IP**，否则通讯录、身份校验等接口会被限制。
- 若遇到「域名主体校验未通过」，需要通过 AppFlow 域名管理添加二级域名（需在阿里云备案），或使用 Nginx/ECS 代理转发。

### 钉钉

- 需要在钉钉开放平台创建应用并获取 **Client ID、Client Secret**。
- 必须为应用授予 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限（发送卡片消息）。
- 机器人消息接收模式**只能选 HTTP 模式**，选 Stream 模式会导致无法返回消息。
- 应用需「创建版本并发布」后，其他组织成员才能使用。
- 如需在回答中展示引用文档或 DeepSeek 深度思考过程，需使用特定的钉钉卡片模板和 AppFlow 工作流模板。

### 本地 RAG

- 通过 Python 脚本搭建本地检索 + 云端生成的 RAG 应用，不依赖 AppFlow。
- Python 版本要求 3.8 ~ 3.12，默认使用百炼 Embedding API；也可切换为本地 Embedding 模型（如 GTE-large）。
- 支持临时上传文件（pdf/docx/txt/xlsx/csv）和持久化知识库两种方式。
- 通过 Gradio 界面交互，也可通过 Gradio 自动生成的 API 集成到业务系统。

## 支持的模型

所有方案默认推荐 **千问-Plus（Qwen-Plus）**，效果、速度、成本均衡。其他可选模型：

- **Qwen-Max**：效果最优，速度较慢、成本较高，适合复杂推理。
- **Qwen-Turbo**：速度最快、成本最低，适合对响应延迟敏感但准确度要求不高的场景。

> **注意**：网站集成文档中推荐的模型已更新为 **Qwen3.5-Plus**，而微信公众号、企业微信、钉钉三篇文档仍写作「千问-Plus」。实际选择时以百炼控制台当前可用模型列表为准，两者在能力定位上等价。

## 关键参数

### 模型参数

| 参数 | 说明 |
| --- | --- |
| 温度 | 越高生成越随机；客服场景建议偏低 |
| 最大回复长度 | 控制最多 token 数，详细描述调高、简短回答调低 |
| 携带上下文轮数 | 设为 1 时模型不参考历史对话 |

### RAG 参数

| 参数 | 说明 |
| --- | --- |
| 召回片段数 | 越大参考信息越多，但可能引入噪音 |
| 相似度阈值 | 过滤相似度低于该值的片段；设为 0 表示不过滤 |

本地 RAG 还支持调整文档切分策略和更换嵌入模型。

## 知识库配置

无论哪种接入渠道，让 AI 回答私域问题的关键都是给百炼应用**挂载知识库**：

1. **上传文档**：在百炼控制台 → 数据连接 / 文件页签上传 pdf、docx、txt、xlsx、csv 等文件，单文档最大 100MB 或 1000 页。
2. **创建知识库**：在知识库页面创建标准版，勾选上一步上传的文档。向量存储可选默认或 **ADB-PG**（集中管理多个应用的向量数据时推荐）。
3. **应用引用知识库**：在应用的「知识库 / 文档」配置中添加目标知识库，调用方式建议选「**必定调用**」，验证效果后点击「发布」。

> **注意**：本地 RAG 同时支持「临时文件」和「持久化知识库」两种知识源，若两者同时使用，应用会优先参考临时文件。

## 限制与注意事项

- **新用户免费额度**可覆盖所有教程场景的资源消耗，超出后按 token 计费。
- **微信公众号未认证**：被动回复 5 秒超时限制会导致长回答失败，建议完成认证，或在 Prompt 中要求模型「给出简短回答」并改用 Qwen-Turbo。
- **企业微信域名主体校验**：Webhook 域名必须与企业主体备案一致，否则需配置二级域名或 Nginx 代理。
- **企业微信可信 IP**：一个可信 IP 只能用于一个企业，多企业共用会被识别为服务商。建议使用自有 ECS 或托管实例转发请求。
- **钉钉机器人**：消息接收模式必须选 HTTP 模式；应用必须发布版本后其他成员才能使用。
- **本地 RAG 文件体积**：受 Embedding API 限流影响，不建议上传超过 100MB 的单文件。
- **文档解析时间**：上传大文档后，百炼通常需要 1~6 分钟解析，请耐心等待。

## 应用评测与优化

正式上线前建议组织业务人员参与**人工评测**，验证回答是否符合预期。效果不佳时的优化方向：

- **优化提示词**：明确角色、回复风格、边界（参考 [prompt](prompt.md) engineering 最佳实践）。
- **完善知识库**：补充缺失文档、调整切分策略。
- **调整参数**：温度、召回片段数、相似度阈值等。
- **本地 RAG**：可尝试更换嵌入模型（如从云端 API 切换到 GTE-large 本地模型）对比召回效果。

如需记录对话日志用于分析，可在 AppFlow 连接流中追加 SLS 日志云服务节点，将用户输入、模型输出写入指定的 Project / Logstore。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)






