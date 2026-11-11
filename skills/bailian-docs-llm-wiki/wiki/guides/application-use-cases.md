# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景。所有方案均基于统一的百炼大模型应用与 RAG 知识增强能力，通过 AppFlow 低代码连接流实现模型服务与渠道消息系统的对接，无需自行开发后端逻辑。核心流程均为：创建百炼智能体应用 → 配置渠道凭证与 Webhook → 关联知识库 → 发布上线。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1）、`千问-Plus`（文档 2、3、5），该模型在效果、速度与成本间取得平衡；也可选用 `qwen-max`（高精度）、`qwen3.5-flash`（低延迟）或 `qwen-turbo`（文档 3 提及用于提速）。
- **RAG 增强**：所有渠道均支持通过百炼知识库实现私有知识注入，支持 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.md`, `.pptx`, `.png`, `.jpg` 等格式（文档 2 明确列出，文档 4 补充说明本地 RAG 支持相同格式）。
- **本地 RAG 变体**：除云端托管方案外，还提供 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)，支持本地文档切分、自定义嵌入模型（如 `iic/nlp_gte_sentence-embedding_chinese-large`）及灵活参数调优。

> **注意**：文档 1 中称模型为“Qwen3.5-Plus”，而文档 2、3、5 统一使用“千问-Plus”表述。经核实，二者为同一模型（Qwen3.5-Plus 即千问 Qwen3.5 系列中的 Plus 版本），属命名差异，非功能矛盾。

## 关键参数

- **Prompt 工程**：所有方案均支持在百炼应用配置中设置系统 Prompt，用于角色定义与行为约束（如 `"你叫小助，可以帮助用户解答产品选购、使用等方面的问题。"`）。文档 3 进一步建议添加 `"请总是给出简短的回答，不要讲太多。"` 以适配微信公众号 5 秒响应限制。
- **知识库调用方式**：在应用配置中可设为“必定调用”（强制检索）、“按需调用”或“不调用”（文档 1、2、3、5 均提及）。
- **RAG 检索参数**（仅本地 RAG 方案）：支持调整召回片段数、相似度阈值、切分策略及嵌入模型（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
- **生成参数**（仅本地 RAG 方案）：支持温度（temperature）、最大回复长度（max_tokens）、上下文轮数（history rounds）等（同上）。

## 使用方式

1. **创建百炼智能体应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `Qwen3.5-Plus`）→ 配置 Prompt → 发布。
2. **获取凭证**：在应用管理页复制 **应用 ID**；在密钥管理页创建并保存 **API Key**。
3. **配置渠道连接流**：
   - **网站**：使用 AppFlow 创建 AI 助手 → 导入百炼模型 → 配置 Web 页面集成 → 获取悬浮挂件脚本 → 插入 HTML（[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。
   - **微信公众号**：使用 AppFlow 模板 → 授权公众号（需主管理员扫码）→ 关联百炼应用 → 发布（区分认证/未认证公众号模板）。
   - **企业微信**：使用 AppFlow 模板 → 配置企业微信凭证（企业 ID / AgentId / Secret）→ 获取 WebhookUrl 与 Token → 在企业微信后台配置 API 接收消息及可信 IP。
   - **钉钉**：使用 AppFlow 模板 → 配置钉钉凭证（Client ID / Client Secret）→ 在钉钉开放平台配置机器人 HTTP 模式接收地址 → 发布应用版本。
4. **接入私有知识**：上传文件至百炼数据连接 → 创建知识库 → 在目标应用中引用该知识库 → 重新发布应用。

## 限制和注意事项

- **免费额度与计费**：新用户可享百炼免费额度（覆盖教程消耗），额度用尽后按 token 计费；AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费（文档 1、2、5 均强调）。
- **渠道响应时限**：
  - 微信公众号未认证时，被动回复必须在 **5 秒内完成**，超时将失败；建议认证后使用客服接口，或优化 Prompt/模型（如选 `qwen-turbo`）提速（文档 3）。
  - 企业微信与钉钉无此硬性限制，但需确保 Webhook 端点稳定性。
- **安全与权限**：
  - 企业微信要求配置**可信 IP 白名单**，若使用第三方代理（如 AppFlow 默认域名），需通过 Nginx 代理或计算巢实例解决（文档 2）。
  - 钉钉机器人**必须使用 HTTP 模式**，Stream 模式不兼容 AppFlow（文档 5 强调）。
- **调试与日志**：所有 AppFlow 连接流均支持添加 SLS 日志节点记录对话（文档 2、3、5 共同提供详细步骤），便于问题排查与效果分析。
- **模型与知识一致性**：知识库更新后，必须**重新发布**百炼应用才能生效（文档 1、2、3、5 均明确要求）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


