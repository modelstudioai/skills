# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景。所有方案均基于统一的百炼大模型应用与 RAG 知识增强能力，通过 AppFlow 低代码连接流实现模型服务与业务渠道的解耦对接，开发者可复用同一套知识库和提示词配置，大幅降低多端部署成本。

## 支持的模型/功能

- **核心模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指出其“能力均衡，推理效果、成本和速度介于千问Max和千问Flash之间”），亦支持 `qwen-max`、`qwen-plus`、`qwen3.5-flash` 等商业模型（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
- **关键能力**：
  - 智能体（Agent）应用：支持多步推理、[工具调用](../concepts/tool-calling.md)（如知识库检索）；
  - RAG 增强：通过知识库引用实现私域问答，支持“必定调用”等调用策略；
  - 多模态文件解析：支持 PDF、DOCX、TXT、XLSX、PPTX、PNG/JPG 等格式（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；
  - 自定义 Prompt：可在应用配置中设置角色指令（如“你叫小助，可以帮助用户解答产品选购、使用等方面的问题”）。

> **注意**：文档 1 和文档 2–5 在模型名称表述上存在不一致——文档 1 使用 `Qwen3.5-Plus`（带版本号），而文档 2、3、5 统一使用 `千问-Plus`。实际控制台中二者指向同一模型，但开发者应以控制台当前显示名称为准，避免硬编码。

## 关键参数

| 参数 | 说明 | 取值建议 | 来源依据 |
|------|------|----------|----------|
| `temperature` | 控制生成随机性 | 0.1–0.6（客服场景建议偏低） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| `max_tokens` | 最大输出 token 数 | 512–2048（平衡详略与延迟） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| `top_p` | 核采样阈值 | 0.9–1.0（默认） | 文档未显式说明，但为百炼通用参数 |
| `retrieval_top_k` | RAG 召回片段数 | 3–5（兼顾精度与噪声） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| `similarity_threshold` | 相似度过滤阈值 | 0.3–0.7（0 表示不过滤） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |

## 使用方式

1. **创建百炼应用**：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中创建智能体应用，选择模型并配置 Prompt；
2. **获取凭证**：从[API Key](https://bailian.console.aliyun.com/?tab=app#/api-key)页获取 API Key，从应用详情页复制 Application ID；
3. **配置知识库（可选但推荐）**：
   - 上传文件至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)；
   - 在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页创建并关联；
   - 在应用配置中启用“文档”模块并选择知识库，调用方式设为“必定调用”；
4. **对接渠道**：
   - **网站**：通过 AppFlow 创建 AI 助手 → 获取悬浮挂件脚本 → 插入 HTML；
   - **微信公众号/企业微信/钉钉**：使用对应 AppFlow 模板 → 配置渠道凭证（AppID/AgentID/Client ID + Secret）→ 配置百炼凭证 → 发布后获取 Webhook URL → 在渠道后台完成回调地址配置；
5. **验证与日志**：可通过渠道内直接对话测试；如需分析，可在 AppFlow 连接流中添加 SLS 日志节点（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）。

## 限制和注意事项

- **免费额度**：新用户免费额度可覆盖入门教程消耗，但超出后按 token 计费；AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）；
- **认证要求**：
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证（见 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)）；
  - 企业微信需配置可信 IP 或通过 Nginx 代理解决主体校验问题（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；
- **安全限制**：
  - 企业微信/钉钉要求 Webhook 地址必须为备案域名或经代理转发（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；
  - 钉钉机器人必须使用 HTTP 模式（非 Stream 模式），否则无法返回消息（见 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）；
- **调试要点**：
  - 出现 `request error` 或 `Failed to stream content` 时，优先检查 API Key 状态、应用 ID 是否匹配、业务空间标识（`AgentKey`）是否一致（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）；
  - 企业微信报错“以下IP属于第三方服务商”，需通过 ECS 或托管实例配置可信 IP（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


